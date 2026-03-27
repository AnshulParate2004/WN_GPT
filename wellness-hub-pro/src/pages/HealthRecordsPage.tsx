import { useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { Database, RefreshCw } from "lucide-react";

export default function HealthRecordsPage() {
  const [records, setRecords] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const fetch = async () => {
    setLoading(true);
    setError(false);
    try {
      const data = await api.fetchHealthRecords();
      setRecords(data);
    } catch {
      setError(true);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Government Health Sync</h1>
      <p className="text-sm text-muted-foreground mb-8">Pull records from ABDM/ABHA database</p>

      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="card-elegant p-8 text-center">
        <Database className="h-10 w-10 text-primary mx-auto mb-4" />
        <h2 className="text-lg font-heading text-foreground mb-2">ABDM Health Records</h2>
        <p className="text-sm text-muted-foreground mb-6">Sync your health history from the national database</p>
        <button
          onClick={fetch}
          disabled={loading}
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-md bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          {loading ? "Fetching..." : "Fetch Records"}
        </button>
        {error && <p className="mt-4 text-sm text-destructive">Failed to fetch. Ensure backend is running.</p>}
      </motion.div>

      {records && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="card-elegant p-5 mt-6">
          <h3 className="text-sm font-medium text-foreground mb-3">Retrieved Records</h3>
          <pre className="text-xs text-muted-foreground whitespace-pre-wrap overflow-auto max-h-60">
            {JSON.stringify(records, null, 2)}
          </pre>
        </motion.div>
      )}
    </div>
  );
}
