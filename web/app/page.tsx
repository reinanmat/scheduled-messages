"use client"

import { useState, useEffect } from "react"
import { Plus, Calendar, Clock, Send, Filter } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

interface ScheduledMessage {
  id: string
  content: string
  scheduledTime: Date
  sent: boolean
  createdAt: Date
}

export default function ScheduledMessagesApp() {
  const [messages, setMessages] = useState<ScheduledMessage[]>([])
  const [newMessage, setNewMessage] = useState({
    content: "",
    scheduledDate: "",
    scheduledTime: "",
  })
  const [filter, setFilter] = useState<"all" | "sent" | "pending">("all")
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await fetch("http://localhost:8000/messages");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setMessages(data.map((msg: any) => {
        const scheduledTime = new Date(msg.scheduled_time);
        let createdAtString = msg.created_at;
        // If createdAt string doesn't have timezone info, assume UTC and append 'Z'
        if (typeof createdAtString === 'string' && !createdAtString.endsWith('Z') && !createdAtString.includes('+') && !createdAtString.includes('-')) {
          createdAtString += 'Z';
        }
        const createdAt = new Date(createdAtString);
        return {
          ...msg,
          scheduledTime: isNaN(scheduledTime.getTime()) ? new Date() : scheduledTime,
          createdAt: isNaN(createdAt.getTime()) ? new Date() : createdAt,
        };
      }));
    } catch (error) {
      console.error("Erro ao buscar mensagens:", error);
    }
  };

  const handleAddMessage = async () => {
    if (!newMessage.content || !newMessage.scheduledDate || !newMessage.scheduledTime) {
      return
    }

    const scheduledDateTime = new Date(`${newMessage.scheduledDate}T${newMessage.scheduledTime}`)

    try {
      const response = await fetch("http://localhost:8000/schedule", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: newMessage.content,
          scheduled_time: scheduledDateTime.toISOString(),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setNewMessage({ content: "", scheduledDate: "", scheduledTime: "" });
      setIsDialogOpen(false);
      fetchMessages();
    } catch (error) {
      console.error("Erro ao adicionar mensagem:", error);
    }
  }

  const filteredMessages = messages.filter((msg) => {
    if (filter === "sent") return msg.sent
    if (filter === "pending") return !msg.sent
    return true
  })

  const sortedMessages = filteredMessages.sort(
    (a, b) => new Date(a.scheduledTime).getTime() - new Date(b.scheduledTime).getTime(),
  )

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    }).format(date)
  }

  const isOverdue = (date: Date, sent: boolean) => {
    return !sent && new Date() > date
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Mensagens Agendadas</h1>
          <p className="text-gray-600">Gerencie suas mensagens programadas de forma simples e eficiente</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{messages.length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Enviadas</CardTitle>
              <Send className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{messages.filter((m) => m.sent).length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pendentes</CardTitle>
              <Clock className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{messages.filter((m) => !m.sent).length}</div>
            </CardContent>
          </Card>
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-blue-600 hover:bg-blue-700">
                <Plus className="h-4 w-4 mr-2" />
                Nova Mensagem
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Agendar Nova Mensagem</DialogTitle>
                <DialogDescription>Crie uma nova mensagem agendada</DialogDescription>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="content">Conteúdo da Mensagem</Label>
                  <Textarea
                    id="content"
                    placeholder="Digite sua mensagem..."
                    value={newMessage.content}
                    onChange={(e) => setNewMessage((prev) => ({ ...prev, content: e.target.value }))}
                    className="mt-1"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="date">Data</Label>
                    <Input
                      id="date"
                      type="date"
                      value={newMessage.scheduledDate}
                      onChange={(e) => setNewMessage((prev) => ({ ...prev, scheduledDate: e.target.value }))}
                      className="mt-1"
                    />
                  </div>
                  <div>
                    <Label htmlFor="time">Horário</Label>
                    <Input
                      id="time"
                      type="time"
                      value={newMessage.scheduledTime}
                      onChange={(e) => setNewMessage((prev) => ({ ...prev, scheduledTime: e.target.value }))}
                      className="mt-1"
                    />
                  </div>
                </div>
                <Button onClick={handleAddMessage} className="w-full">
                  Agendar Mensagem
                </Button>
              </div>
            </DialogContent>
          </Dialog>

          <Select value={filter} onValueChange={(value: "all" | "sent" | "pending") => setFilter(value)}>
            <SelectTrigger className="w-full sm:w-48">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas as mensagens</SelectItem>
              <SelectItem value="pending">Pendentes</SelectItem>
              <SelectItem value="sent">Enviadas</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Messages List */}
        <div className="space-y-4">
          {sortedMessages.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Calendar className="h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhuma mensagem encontrada</h3>
                <p className="text-gray-500 text-center">
                  {filter === "all"
                    ? "Comece criando sua primeira mensagem agendada"
                    : `Não há mensagens ${filter === "sent" ? "enviadas" : "pendentes"}`}
                </p>
              </CardContent>
            </Card>
          ) : (
            sortedMessages.map((message) => (
              <Card key={message.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg mb-2">{message.content}</CardTitle>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          <span>Agendada para: {formatDate(message.scheduledTime)}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          <span>Criada em: {formatDate(message.createdAt)}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {isOverdue(message.scheduledDate, message.sent) && <Badge variant="destructive">Atrasada</Badge>}
                      <Badge
                        variant={message.sent ? "default" : "secondary"}
                        className={message.sent ? "bg-green-600" : "bg-orange-500"}
                      >
                        {message.sent ? "Enviada" : "Pendente"}
                      </Badge>
                      
                    </div>
                  </div>
                </CardHeader>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
