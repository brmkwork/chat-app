import type { Message } from "../types/chat";

interface Props {
  message: Message
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === "user"

  return (
    <div style={{
      display: "flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      marginBottom: "8px"
    }}>
      <div style={{
        background: isUser ? "#6c63ff" : "#2a2a2a",
        color: "white",
        padding: "10px 14px",
        borderRadius: "12px",
        maxWidth: "70%"
      }}>
        {message.content}
      </div>
    </div>
  )
}