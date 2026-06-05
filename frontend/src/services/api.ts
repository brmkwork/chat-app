import type { Conversation, Message, MessagePair } from "../types/chat"

const BASE_URL = "http://localhost:8000"

export async function getConversations(): Promise<Conversation[]> {
  const res = await fetch(`${BASE_URL}/conversations`)
  if (!res.ok) throw new Error("Failed to fetch conversations")
  return res.json()
}

export async function createConversation(title: string): Promise<Conversation> {
  const res = await fetch(`${BASE_URL}/conversations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  })
  if (!res.ok) throw new Error("Failed to create conversation")
  return res.json()
}

export async function getMessages(conversationId: number): Promise<Message[]> {
  const res = await fetch(`${BASE_URL}/conversations/${conversationId}/messages`)
  if (!res.ok) throw new Error("Failed to fetch messages")
  return res.json()
}

export async function sendMessage(conversationId: number, content: string): Promise<MessagePair> {
  const res = await fetch(`${BASE_URL}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ conversation_id: conversationId, content })
  })
  if (!res.ok) throw new Error("Failed to send message")
  return res.json()
}

export async function deleteConversation(conversationId: number): Promise<{ deleted: boolean; id?: number }> {
  const res = await fetch(`${BASE_URL}/conversations/${conversationId}`, {
    method: "DELETE",
  })
  if (!res.ok) throw new Error("Failed to delete conversation")
  return res.json()
}