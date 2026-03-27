import { useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function NutritionPage() {
  const [form, setForm] = useState({ meal_type: "breakfast", description: "", calories: "", protein: "", carbs: "", fat: "" });
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.logNutrition({ ...form, calories: Number(form.calories), protein: Number(form.protein), carbs: Number(form.carbs), fat: Number(form.fat) });
      toast.success("Meal logged successfully");
      setForm({ meal_type: "breakfast", description: "", calories: "", protein: "", carbs: "", fat: "" });
    } catch {
      toast.error("Failed to log meal.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Nutrition Log</h1>
      <p className="text-sm text-muted-foreground mb-8">Track meals and macros for the NutriSense engine</p>

      <motion.form
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        onSubmit={submit}
        className="card-elegant p-6 space-y-5"
      >
        <Field label="Meal Type">
          <select value={form.meal_type} onChange={(e) => setForm({ ...form, meal_type: e.target.value })} className="form-input">
            <option value="breakfast">Breakfast</option>
            <option value="lunch">Lunch</option>
            <option value="dinner">Dinner</option>
            <option value="snack">Snack</option>
          </select>
        </Field>
        <Field label="Description">
          <input value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="e.g., Grilled chicken salad" required className="form-input" />
        </Field>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Calories">
            <input type="number" value={form.calories} onChange={(e) => setForm({ ...form, calories: e.target.value })} placeholder="kcal" className="form-input" />
          </Field>
          <Field label="Protein (g)">
            <input type="number" value={form.protein} onChange={(e) => setForm({ ...form, protein: e.target.value })} placeholder="g" className="form-input" />
          </Field>
          <Field label="Carbs (g)">
            <input type="number" value={form.carbs} onChange={(e) => setForm({ ...form, carbs: e.target.value })} placeholder="g" className="form-input" />
          </Field>
          <Field label="Fat (g)">
            <input type="number" value={form.fat} onChange={(e) => setForm({ ...form, fat: e.target.value })} placeholder="g" className="form-input" />
          </Field>
        </div>
        <button type="submit" disabled={loading} className="w-full py-2.5 rounded-md bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40">
          {loading ? "Logging..." : "Log Meal"}
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
