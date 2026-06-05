import { useEffect, useRef } from "react"
import type { Message } from "../types/chat"
import { MessageBubble } from "./MessageBubble"

interface Props {
  messages: Message[]
  isLoading: boolean
}

export function ChatWindow({ messages, isLoading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div style={{
      flex: 1,
      overflowY: "auto",
      padding: "16px",
      display: "flex",
      flexDirection: "column"
    }}>
      {messages.length === 0 && (
        <p style={{ color: "#666", textAlign: "center" }}>
          No messages yet. Say hello!
        </p>
      )}
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}
      {isLoading && (
        <p style={{ color: "#666" }}>Message received...</p>
      )}
      <div ref={bottomRef} />
    </div>
  )
}