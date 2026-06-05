import { useState, useEffect } from "react"
import type { Conversation, Message } from "./types/chat"
import * as api from "./services/api"
import { Sidebar } from "./components/Sidebar"
import { ChatWindow } from "./components/ChatWindow"
import { MessageInput } from "./components/MessageInput"

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    api.getConversations().then(setConversations).catch(console.error)
  }, [])

  useEffect(() => {
    if (selectedId === null) {
      setMessages([])
      return
    }
    api.getMessages(selectedId).then(setMessages).catch(console.error)
  }, [selectedId])

  async function handleNewChat() {
    const title = `Chat ${conversations.length + 1}`
    const newConv = await api.createConversation(title)
    setConversations((prev) => [newConv, ...prev])
    setSelectedId(newConv.id)
  }

  async function handleSend(content: string) {
    if (selectedId === null) return
    setIsLoading(true)
    try {
      const { user_message, assistant_message } = await api.sendMessage(selectedId, content)
      setMessages((prev) => [...prev, user_message, assistant_message])
    } catch (err) {
      console.error(err)
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
    <div style={{
      display: "flex",
      height: "100vh",
      background: "#0f0f0f",
      color: "white"
    }}>
      <Sidebar
        conversations={conversations}
        selectedId={selectedId}
        onSelect={setSelectedId}
        onNewChat={handleNewChat}
        onDelete={handleDeleteChat}
      />
      <div style={{
        flex: 1,
        display: "flex",
        flexDirection: "column"
      }}>
        {selectedId === null ? (
          <div style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#666"
          }}>
            Select a chat or create a new one
          </div>
        ) : (
          <>
            <ChatWindow messages={messages} isLoading={isLoading} />
            <MessageInput onSend={handleSend} disabled={isLoading} />
          </>
        )}
      </div>
    </div>
  )
}

export default App