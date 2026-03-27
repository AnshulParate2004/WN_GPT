import { useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function SymptomsPage() {
  const [form, setForm] = useState({ symptom: "", severity: "mild", duration: "", notes: "" });
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.logSymptoms(form);
      toast.success("Symptom logged successfully");
      setForm({ symptom: "", severity: "mild", duration: "", notes: "" });
    } catch {
      toast.error("Failed to log symptom. Check backend connection.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Symptom Logger</h1>
      <p className="text-sm text-muted-foreground mb-8">Record physical symptoms for your care team</p>

      <motion.form
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        onSubmit={submit}
        className="card-elegant p-6 space-y-5"
      >
        <Field label="Symptom">
          <input
            value={form.symptom}
            onChange={(e) => setForm({ ...form, symptom: e.target.value })}
            placeholder="e.g., headache, chest pain"
            required
            className="form-input"
          />
        </Field>
        <Field label="Severity">
          <select
            value={form.severity}
            onChange={(e) => setForm({ ...form, severity: e.target.value })}
            className="form-input"
          >
            <option value="mild">Mild</option>
            <option value="moderate">Moderate</option>
            <option value="severe">Severe</option>
          </select>
        </Field>
        <Field label="Duration">
          <input
            value={form.duration}
            onChange={(e) => setForm({ ...form, duration: e.target.value })}
            placeholder="e.g., 2 hours, 3 days"
            className="form-input"
          />
        </Field>
        <Field label="Additional Notes">
          <textarea
            value={form.notes}
            onChange={(e) => setForm({ ...form, notes: e.target.value })}
            rows={3}
            className="form-input resize-none"
            placeholder="Any additional context..."
          />
        </Field>
        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 rounded-md bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
        >
          {loading ? "Logging..." : "Log Symptom"}
        </button>
      </motion.form>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">{label}</label>
      {children}
    </div>
  );
}
