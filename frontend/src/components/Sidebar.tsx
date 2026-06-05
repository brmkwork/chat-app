import type { Conversation } from "../types/chat"

interface Props {
  conversations: Conversation[]
  selectedId: number | null
  onSelect: (id: number) => void
  onNewChat: () => void
  onDelete: (id: number) => void
}

export function Sidebar({ conversations, selectedId, onSelect, onNewChat, onDelete }: Props) {
  return (
    <div style={{
      width: "260px",
      background: "#1a1a1a",
      borderRight: "1px solid #333",
      display: "flex",
      flexDirection: "column",
      height: "100vh"
    }}>
      <div style={{
        padding: "16px",
        borderBottom: "1px solid #333",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
      }}>
        <h2 style={{ color: "white", margin: 0, fontSize: "16px" }}>Chats</h2>
        <button
          onClick={onNewChat}
          style={{
            background: "#6c63ff",
            color: "white",
            border: "none",
            borderRadius: "6px",
            padding: "6px 12px",
            cursor: "pointer",
            fontSize: "12px"
          }}
        >
          + New
        </button>
      </div>
      <div style={{ flex: 1, overflowY: "auto" }}>
        {conversations.length === 0 && (
          <p style={{ color: "#666", padding: "16px", fontSize: "14px" }}>
            No conversations yet
          </p>
        )}
        {conversations.map((conv) => (
          <div
            key={conv.id}
            onClick={() => onSelect(conv.id)}
            style={{
              padding: "12px 16px",
              cursor: "pointer",
              background: conv.id === selectedId ? "#6c63ff" : "transparent",
              color: "white",
              fontSize: "14px",
              borderBottom: "1px solid #222",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center"
            }}
          >
            <span>{conv.title}</span>
            <button
              onClick={(e) => {
                e.stopPropagation()
                onDelete(conv.id)
              }}
              style={{
                background: "transparent",
                border: "1px solid #555",
                color: "#ddd",
                borderRadius: "6px",
                padding: "4px 8px",
                cursor: "pointer",
                fontSize: "12px"
              }}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}