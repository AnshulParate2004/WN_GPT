import { useState, useRef, useEffect } from "react";
import { api } from "@/lib/api";
import { Send } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    let assistantContent = "";
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    try {
      await api.chat(userMsg, (chunk) => {
        assistantContent += chunk;
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = { role: "assistant", content: assistantContent };
          return updated;
        });
      });
    } catch {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          content: "Sorry, I couldn't connect to the server. Please ensure the backend is running on localhost:8000.",
        };
        return updated;
      });
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-5rem)] max-w-3xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-heading font-semibold text-foreground">Agent Chat</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Interact with all 15 WellnessGPT agents — Triage, FitGuide, NutriSense, and more.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="h-16 w-16 rounded-full bg-emerald-soft flex items-center justify-center mb-4">
              <span className="text-primary text-2xl font-heading font-bold">W</span>
            </div>
            <h2 className="text-lg font-heading text-foreground">Welcome to WellnessGPT</h2>
            <p className="text-muted-foreground text-sm mt-2 max-w-sm">
              Ask me anything about your health — symptoms, nutrition, fitness, mental wellness, or medical records.
            </p>
          </div>
        )}
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] px-4 py-3 rounded-lg text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "card-elegant text-card-foreground"
                }`}
              >
                {msg.content || <span className="animate-pulse">●●●</span>}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={bottomRef} />
      </div>

      <div className="card-elegant p-2 flex items-center gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Type a message..."
          className="flex-1 bg-transparent px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground outline-none"
        />
        <button
          onClick={send}
          disabled={loading || !input.trim()}
          className="h-9 w-9 rounded-md bg-primary text-primary-foreground flex items-center justify-center disabled:opacity-40 transition-opacity"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
