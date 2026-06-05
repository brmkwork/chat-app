import { useState } from "react"

interface Props {
  onSend: (content: string) => void
  disabled: boolean
}

export function MessageInput({ onSend, disabled }: Props) {
  const [text, setText] = useState("")

  function handleSend() {
    if (!text.trim() || disabled) return
    onSend(text)
    setText("")
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div style={{
      display: "flex",
      gap: "8px",
      padding: "16px",
      borderTop: "1px solid #333"
    }}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder="Type a message..."
        rows={1}
        style={{
          flex: 1,
          padding: "10px",
          borderRadius: "8px",
          border: "1px solid #333",
          background: "#1a1a1a",
          color: "white",
          resize: "none",
          fontSize: "14px"
        }}
      />
      <button
        onClick={handleSend}
        disabled={disabled}
        style={{
          background: "#6c63ff",
          color: "white",
          border: "none",
          borderRadius: "8px",
          padding: "10px 20px",
          cursor: disabled ? "not-allowed" : "pointer",
          opacity: disabled ? 0.5 : 1
        }}
      >
        Send
      </button>
    </div>
  )
}