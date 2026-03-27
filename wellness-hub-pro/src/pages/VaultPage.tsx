import { useState, useRef } from "react";
import { api } from "@/lib/api";
import { Upload, FileText, CheckCircle2, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";

export default function VaultPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [result, setResult] = useState<any>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const upload = async () => {
    if (!file) return;
    setStatus("uploading");
    try {
      const res = await api.uploadDocument(file);
      setResult(res);
      setStatus("success");
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Medical Vault</h1>
      <p className="text-sm text-muted-foreground mb-8">Upload medical documents for AI-powered analysis</p>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-elegant p-8 text-center"
      >
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          onChange={(e) => {
            setFile(e.target.files?.[0] || null);
            setStatus("idle");
            setResult(null);
          }}
        />
        <div
          onClick={() => inputRef.current?.click()}
          className="cursor-pointer border border-dashed border-border rounded-lg p-10 hover:border-primary/40 transition-colors"
        >
          <Upload className="h-8 w-8 text-muted-foreground mx-auto mb-3" />
          <p className="text-sm text-foreground font-medium">
            {file ? file.name : "Click to select a file"}
          </p>
          <p className="text-xs text-muted-foreground mt-1">PDF, images, or medical documents</p>
        </div>

        {file && status === "idle" && (
          <button
            onClick={upload}
            className="mt-6 px-6 py-2 rounded-md bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity"
          >
            Upload & Analyze
          </button>
        )}

        {status === "uploading" && (
          <p className="mt-6 text-sm text-muted-foreground animate-pulse">Uploading & analyzing...</p>
        )}
        {status === "success" && (
          <div className="mt-6 flex items-center justify-center gap-2 text-primary">
            <CheckCircle2 className="h-4 w-4" />
            <span className="text-sm font-medium">Analysis complete</span>
          </div>
        )}
        {status === "error" && (
          <div className="mt-6 flex items-center justify-center gap-2 text-destructive">
            <AlertCircle className="h-4 w-4" />
            <span className="text-sm">Upload failed. Ensure backend is running.</span>
          </div>
        )}
      </motion.div>

      {result && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card-elegant p-5 mt-6"
        >
          <div className="flex items-center gap-2 mb-3">
            <FileText className="h-4 w-4 text-primary" />
            <h3 className="text-sm font-medium text-foreground">Analysis Result</h3>
          </div>
          <pre className="text-xs text-muted-foreground whitespace-pre-wrap overflow-auto max-h-60">
            {JSON.stringify(result, null, 2)}
          </pre>
        </motion.div>
      )}
    </div>
  );
}
