import React, { useState, useEffect, useRef, useContext, createContext } from 'react';

// Chat Context for managing multiple chat rooms
const ChatContext = createContext();

export const useChat = () => useContext(ChatContext);

/**
 * Chat Manager - Handles WebSocket connections to Django Channels
 */
class ChatManager {
  constructor(user, token) {
    this.user = user;
    this.token = token;
    this.connections = new Map();
    this.wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';
  }

  /**
   * Connect to a chat room
   */
  connect(roomId, onMessage, onError, onOpen) {
    if (this.connections.has(roomId)) {
      return this.connections.get(roomId);
    }

    const ws = new WebSocket(
      `${this.wsUrl}/ws/chat/${roomId}/?token=${this.token}`
    );

    ws.onopen = () => {
      console.log(`Connected to room ${roomId}`);
      onOpen?.();
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage?.(data);
    };

    ws.onerror = (error) => {
      console.error(`WebSocket error in room ${roomId}:`, error);
      onError?.(error);
    };

    ws.onclose = () => {
      console.log(`Disconnected from room ${roomId}`);
      this.connections.delete(roomId);
    };

    this.connections.set(roomId, ws);
    return ws;
  }

  /**
   * Send a message to a room
   */
  send(roomId, message) {
    const ws = this.connections.get(roomId);
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(
        JSON.stringify({
          type: 'message',
          message,
        })
      );
    } else {
      console.warn(`WebSocket for room ${roomId} is not open`);
    }
  }

  /**
   * Disconnect from a room
   */
  disconnect(roomId) {
    const ws = this.connections.get(roomId);
    if (ws) {
      ws.close();
      this.connections.delete(roomId);
    }
  }

  /**
   * Disconnect from all rooms
   */
  disconnectAll() {
    for (const ws of this.connections.values()) {
      ws.close();
    }
    this.connections.clear();
  }
}

/**
 * Chat Provider - Manages chat connections
 */
export const ChatProvider = ({ user, token, children }) => {
  const [chatManager] = useState(() => new ChatManager(user, token));

  useEffect(() => {
    return () => {
      chatManager.disconnectAll();
    };
  }, [chatManager]);

  return (
    <ChatContext.Provider value={{ chatManager }}>
      {children}
    </ChatContext.Provider>
  );
};

/**
 * Chat Room Component
 */
export const ChatRoom = ({ roomId, roomName }) => {
  const { chatManager } = useChat();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Connect to room on mount
  useEffect(() => {
    if (!roomId || !chatManager) return;

    chatManager.connect(
      roomId,
      (data) => {
        if (data.type === 'message') {
          setMessages((prev) => [...prev, data]);
        } else if (data.type === 'history') {
          setMessages(data.messages);
        }
      },
      (err) => {
        setError('Failed to connect to chat room');
      },
      () => {
        setConnected(true);
        setError(null);
      }
    );

    return () => {
      chatManager.disconnect(roomId);
      setConnected(false);
    };
  }, [roomId, chatManager]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    chatManager.send(roomId, input);
    setInput('');
  };

  return (
    <div className="chat-room">
      <div className="chat-header">
        <h2>{roomName}</h2>
        <span className={`status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? '🟢 Connected' : '🔴 Disconnected'}
        </span>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="messages">
        {messages.length === 0 ? (
          <p className="empty">No messages yet. Start the conversation!</p>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className="message">
              <strong>{msg.sender_name}:</strong>
              <p>{msg.message}</p>
              <small>{new Date(msg.timestamp).toLocaleTimeString()}</small>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="input-form">
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={!connected}
        />
        <button type="submit" disabled={!connected || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

/**
 * Chat Rooms List Component
 */
export const ChatRoomsList = ({ rooms, onSelectRoom }) => {
  return (
    <div className="chat-list">
      <h3>Chat Rooms</h3>
      {rooms.length === 0 ? (
        <p>No chat rooms available</p>
      ) : (
        <ul>
          {rooms.map((room) => (
            <li key={room.id}>
              <button onClick={() => onSelectRoom(room)}>
                {room.name}
                {room.unread_count > 0 && (
                  <span className="unread-badge">{room.unread_count}</span>
                )}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

/**
 * Full Chat Component with room list
 */
export const Chat = ({ user, token, apiClient }) => {
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRooms();
  }, []);

  const fetchRooms = async () => {
    try {
      const response = await apiClient.get('/chat/rooms/');
      setRooms(response.data.results || response.data);
      if (response.data.length > 0) {
        setSelectedRoom(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching chat rooms:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading chat rooms...</div>;

  return (
    <ChatProvider user={user} token={token}>
      <div className="chat-container">
        <ChatRoomsList rooms={rooms} onSelectRoom={setSelectedRoom} />
        {selectedRoom ? (
          <ChatRoom roomId={selectedRoom.id} roomName={selectedRoom.name} />
        ) : (
          <div className="no-room">Select a chat room to start messaging</div>
        )}
      </div>
    </ChatProvider>
  );
};

export default Chat;
