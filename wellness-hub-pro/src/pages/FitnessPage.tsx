import { useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function FitnessPage() {
  const [form, setForm] = useState({ activity: "", duration_minutes: "", intensity: "moderate", calories_burned: "", notes: "" });
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.logFitness({ ...form, duration_minutes: Number(form.duration_minutes), calories_burned: Number(form.calories_burned) });
      toast.success("Activity logged successfully");
      setForm({ activity: "", duration_minutes: "", intensity: "moderate", calories_burned: "", notes: "" });
    } catch {
      toast.error("Failed to log activity.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Fitness Log</h1>
      <p className="text-sm text-muted-foreground mb-8">Track workouts for the FitGuide engine</p>

      <motion.form initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} onSubmit={submit} className="card-elegant p-6 space-y-5">
        <Field label="Activity">
          <input value={form.activity} onChange={(e) => setForm({ ...form, activity: e.target.value })} placeholder="e.g., Running, Yoga" required className="form-input" />
        </Field>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Duration (min)">
            <input type="number" value={form.duration_minutes} onChange={(e) => setForm({ ...form, duration_minutes: e.target.value })} placeholder="min" className="form-input" />
          </Field>
          <Field label="Calories Burned">
            <input type="number" value={form.calories_burned} onChange={(e) => setForm({ ...form, calories_burned: e.target.value })} placeholder="kcal" className="form-input" />
          </Field>
        </div>
        <Field label="Intensity">
          <select value={form.intensity} onChange={(e) => setForm({ ...form, intensity: e.target.value })} className="form-input">
            <option value="low">Low</option>
            <option value="moderate">Moderate</option>
            <option value="high">High</option>
          </select>
        </Field>
        <Field label="Notes">
          <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} rows={2} className="form-input resize-none" placeholder="Optional notes..." />
        </Field>
        <button type="submit" disabled={loading} className="w-full py-2.5 rounded-md bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40">
          {loading ? "Logging..." : "Log Activity"}
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
