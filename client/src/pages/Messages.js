import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";

import api from "../services/api";
import { useAuth } from "../context/AuthContext";

import "./Messages.css";

function Messages() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [conversations, setConversations] = useState([]);
  const [thread, setThread] = useState([]);
  const [loadingConversations, setLoadingConversations] = useState(true);
  const [loadingThread, setLoadingThread] = useState(false);

  const [newMessage, setNewMessage] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  const bottomRef = useRef(null);

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }

    api
      .get("/conversations")
      .then((res) => setConversations(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoadingConversations(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!userId || !user) return;

    setLoadingThread(true);

    api
      .get(`/messages/${user.id}/${userId}`)
      .then((res) => setThread(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoadingThread(false));
  }, [userId, user]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [thread]);

  async function handleSend(e) {
    e.preventDefault();

    if (!newMessage.trim()) return;

    setError("");
    setSending(true);

    try {
      await api.post("/messages", {
        receiver_id: userId,
        message: newMessage.trim(),
      });

      setNewMessage("");

      const res = await api.get(`/messages/${user.id}/${userId}`);
      setThread(res.data);

      const convoRes = await api.get("/conversations");
      setConversations(convoRes.data);
    } catch (err) {
      setError(
        err.response?.data?.error || "Unable to send message."
      );
    } finally {
      setSending(false);
    }
  }

  const activeConversation = conversations.find(
    (c) => String(c.user_id) === String(userId)
  );

  return (
    <div className="messages-page">

      <aside className="conversations-sidebar">

        <h2>Messages</h2>

        {loadingConversations ? (
          <p className="empty-state">Loading conversations...</p>
        ) : conversations.length === 0 ? (
          <p className="empty-state">
            No conversations yet. Message a host from a property page to
            start one.
          </p>
        ) : (
          conversations.map((c) => (
            <div
              key={c.user_id}
              className={
                "conversation-preview" +
                (String(c.user_id) === String(userId) ? " active" : "")
              }
              onClick={() => navigate(`/messages/${c.user_id}`)}
            >
              <strong>{c.username}</strong>
              <p>{c.last_message}</p>
            </div>
          ))
        )}

      </aside>

      <main className="conversation-thread">

        {!userId ? (
          <p className="empty-state">
            Select a conversation to view messages.
          </p>
        ) : loadingThread ? (
          <p className="empty-state">Loading messages...</p>
        ) : (
          <>
            <h3 className="thread-header">
              {activeConversation?.username || "Conversation"}
            </h3>

            <div className="thread-messages">

              {thread.map((msg) => (
                <div
                  key={msg.id}
                  className={
                    "message-bubble" +
                    (msg.sender_id === user.id ? " sent" : " received")
                  }
                >
                  <p>{msg.message}</p>
                  <span>
                    {new Date(msg.sent_at).toLocaleString()}
                  </span>
                </div>
              ))}

              <div ref={bottomRef} />

            </div>

            {error && <p className="form-error">{error}</p>}

            <form className="send-message-form" onSubmit={handleSend}>
              <input
                type="text"
                placeholder="Type a message..."
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
              />

              <button type="submit" disabled={sending}>
                {sending ? "Sending..." : "Send"}
              </button>
            </form>
          </>
        )}

      </main>

    </div>
  );
}

export default Messages;
