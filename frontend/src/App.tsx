import { useState, useEffect, useRef } from "react"
import type { Conversation, Message } from "./types/chat"
import * as api from "./services/api"
import { Sidebar } from "./components/Sidebar"
import { ChatWindow } from "./components/ChatWindow"
import { MessageInput } from "./components/MessageInput"

const BACKEND_URL = "http://localhost:8000"

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadedFiles, setUploadedFiles] = useState<Record<number, string>>({})
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    api.getConversations().then(setConversations).catch(console.error)
  }, [])

  useEffect(() => {
    setUploadProgress(0)

    if (selectedId === null) {
      setMessages([])
      return
    }

    api.getMessages(selectedId).then(setMessages).catch(console.error)
    api.getConversationDocument(selectedId)
      .then((doc) => {
        if (doc?.filename) {
          setUploadedFiles((prev) => ({ ...prev, [selectedId]: doc.filename }))
        }
      })
      .catch(() => {
        // No document metadata for this conversation
      })
  }, [selectedId])

  async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file || selectedId === null) return

    setUploading(true)
    setUploadProgress(0)

    const formData = new FormData()
    formData.append("file", file)

    const xhr = new XMLHttpRequest()
    xhr.open("POST", `${BACKEND_URL}/conversations/${selectedId}/upload`)

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        setUploadProgress(Math.round((event.loaded / event.total) * 100))
      }
    }

    xhr.onload = () => {
      setUploading(false)
      if (xhr.status >= 200 && xhr.status < 300) {
        setUploadedFiles((prev) => ({ ...prev, [selectedId]: file.name }))
        alert("PDF uploaded successfully!")
      } else {
        console.error("Upload failed", xhr.responseText)
        alert("Failed to upload PDF")
      }
    }

    xhr.onerror = () => {
      setUploading(false)
      console.error("Upload error")
      alert("Failed to upload PDF")
    }

    xhr.send(formData)
  }

  async function handleNewChat() {
    const title = `Chat ${conversations.length + 1}`
    const newConv = await api.createConversation(title)
    setConversations((prev) => [newConv, ...prev])
    setSelectedId(newConv.id)
  }

  async function handleSend(content: string) {
    if (selectedId === null) return

    const userTempId = Date.now()
    const assistantTempId = userTempId + 1
    const userMessage: Message = {
      id: userTempId,
      conversation_id: selectedId,
      role: "user",
      content,
      created_at: new Date().toISOString()
    }
    const assistantMessage: Message = {
      id: assistantTempId,
      conversation_id: selectedId,
      role: "assistant",
      content: "Typing...",
      created_at: new Date().toISOString()
    }

    setMessages((prev) => [...prev, userMessage, assistantMessage])
    setIsLoading(true)

    try {
      const { assistant_message } = await api.sendMessage(selectedId, content)
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantTempId ? assistant_message : msg
        )
      )
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === selectedId ? { ...conv, title: content } : conv
        )
      )
    } catch (err) {
      console.error(err)
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantTempId
            ? { ...msg, content: "Failed to send. Please try again." }
            : msg
        )
      )
    } finally {
      setIsLoading(false)
    }
  }

  async function handleDeleteChat(conversationId: number) {
    try {
      const result = await api.deleteConversation(conversationId)
      if (result.deleted) {
        setConversations((prev) => prev.filter((conv) => conv.id !== conversationId))
        if (selectedId === conversationId) {
          setSelectedId(null)
          setMessages([])
        }
      }
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div style={{ display: "flex", height: "100vh", background: "#0f0f0f", color: "white" }}>
      <Sidebar
        conversations={conversations}
        selectedId={selectedId}
        onSelect={setSelectedId}
        onNewChat={handleNewChat}
        onDelete={handleDeleteChat}
      />
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        {selectedId === null ? (
          <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", color: "#666" }}>
            Select a chat or create a new one
          </div>
        ) : (
          <>
            <div style={{ padding: "8px 16px", borderBottom: "1px solid #333", display: "flex", alignItems: "center", gap: "12px", flexWrap: "wrap" }}>
              <input
                type="file"
                accept=".pdf"
                ref={fileInputRef}
                onChange={handleFileUpload}
                style={{ display: "none" }}
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
                style={{
                  background: "transparent",
                  border: "1px solid #6c63ff",
                  color: "#6c63ff",
                  borderRadius: "6px",
                  padding: "6px 12px",
                  cursor: uploading ? "not-allowed" : "pointer",
                  fontSize: "12px",
                  opacity: uploading ? 0.6 : 1
                }}
              >
                + Upload PDF
              </button>
              {selectedId !== null && uploadedFiles[selectedId] && (
                <span style={{ color: "#888", fontSize: "12px" }}>
                  📄 {uploadedFiles[selectedId]}
                </span>
              )}
            </div>
            {uploading && (
              <div style={{ padding: "0 16px 12px", width: "100%" }}>
                <div style={{ width: "100%", height: "8px", background: "#2a2a2a", borderRadius: "999px", overflow: "hidden" }}>
                  <div style={{ width: `${uploadProgress}%`, height: "100%", background: "#6c63ff", transition: "width 0.2s ease" }} />
                </div>
                <div style={{ marginTop: "6px", color: "#aaa", fontSize: "12px" }}>
                  Uploading PDF: {uploadProgress}%
                </div>
              </div>
            )}
            <ChatWindow messages={messages} isLoading={isLoading} />
            <MessageInput onSend={handleSend} disabled={isLoading} />
          </>
        )}
      </div>
    </div>
  )
}

export default App