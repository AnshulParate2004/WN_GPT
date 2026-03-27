import { useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { toast } from "sonner";

const phq9Questions = [
  "Little interest or pleasure in doing things",
  "Feeling down, depressed, or hopeless",
  "Trouble falling or staying asleep",
  "Feeling tired or having little energy",
  "Poor appetite or overeating",
  "Feeling bad about yourself",
  "Trouble concentrating",
  "Moving or speaking slowly / being fidgety",
  "Thoughts of self-harm",
];

const gad7Questions = [
  "Feeling nervous, anxious, or on edge",
  "Not being able to stop worrying",
  "Worrying too much about different things",
  "Trouble relaxing",
  "Being so restless it's hard to sit still",
  "Becoming easily annoyed or irritable",
  "Feeling afraid something awful might happen",
];

const options = [
  { label: "Not at all", value: 0 },
  { label: "Several days", value: 1 },
  { label: "More than half", value: 2 },
  { label: "Nearly every day", value: 3 },
];

export default function MentalHealthPage() {
  const [phq9, setPhq9] = useState<number[]>(new Array(9).fill(0));
  const [gad7, setGad7] = useState<number[]>(new Array(7).fill(0));
  const [loading, setLoading] = useState(false);

  const phq9Total = phq9.reduce((a, b) => a + b, 0);
  const gad7Total = gad7.reduce((a, b) => a + b, 0);

  const submit = async () => {
    setLoading(true);
    try {
      await api.submitMentalHealth({ phq9_score: phq9Total, gad7_score: gad7Total, phq9_answers: phq9, gad7_answers: gad7 });
      toast.success("Screening submitted successfully");
    } catch {
      toast.error("Failed to submit. Check backend connection.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Mental Health Screening</h1>
      <p className="text-sm text-muted-foreground mb-8">PHQ-9 (Depression) & GAD-7 (Anxiety) assessment</p>

      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <Section title="PHQ-9 — Depression Screening" questions={phq9Questions} answers={phq9} setAnswers={setPhq9} total={phq9Total} />
        <Section title="GAD-7 — Anxiety Screening" questions={gad7Questions} answers={gad7} setAnswers={setGad7} total={gad7Total} />

        <div className="flex items-center justify-between card-elegant p-5 mt-6">
          <div>
            <span className="text-sm text-muted-foreground">Combined Score: </span>
            <span className="text-lg font-heading font-semibold text-foreground">{phq9Total + gad7Total}</span>
          </div>
          <button
            onClick={submit}
            disabled={loading}
            className="px-6 py-2.5 rounded-md bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
          >
            {loading ? "Submitting..." : "Submit Screening"}
          </button>
        </div>
      </motion.div>
    </div>
  );
}

function Section({ title, questions, answers, setAnswers, total }: {
  title: string; questions: string[]; answers: number[];
  setAnswers: (a: number[]) => void; total: number;
}) {
  return (
    <div className="card-elegant p-5 mb-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-foreground">{title}</h3>
        <span className="text-xs text-muted-foreground">Score: {total}</span>
      </div>
      <div className="space-y-4">
        {questions.map((q, i) => (
          <div key={i}>
            <p className="text-sm text-foreground mb-2">{i + 1}. {q}</p>
            <div className="flex gap-2 flex-wrap">
              {options.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  onClick={() => {
                    const updated = [...answers];
                    updated[i] = opt.value;
                    setAnswers(updated);
                  }}
                  className={`px-3 py-1 rounded-md text-xs font-medium border transition-colors ${
                    answers[i] === opt.value
                      ? "bg-primary text-primary-foreground border-primary"
                      : "border-border text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
