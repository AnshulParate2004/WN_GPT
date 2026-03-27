import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { CalendarDays, ClipboardList, Heart, Activity } from "lucide-react";

export default function DashboardPage() {
  const [profile, setProfile] = useState<any>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api.getProfile().then(setProfile).catch(() => setError(true));
  }, []);

  const cards = [
    { icon: CalendarDays, label: "Appointments", value: profile?.appointments?.length ?? "—" },
    { icon: ClipboardList, label: "Care Plans", value: profile?.care_plans?.length ?? "—" },
    { icon: Heart, label: "Conditions", value: profile?.conditions?.length ?? "—" },
    { icon: Activity, label: "Vitals Logged", value: profile?.vitals?.length ?? "—" },
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Medical Overview</h1>
      <p className="text-sm text-muted-foreground mb-8">Patient profile and care summary</p>

      {error && (
        <div className="card-elegant p-4 text-sm text-muted-foreground mb-6">
          Unable to connect to backend. Showing placeholder data.
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {cards.map((card, i) => (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="card-elegant p-5"
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="h-9 w-9 rounded-md bg-emerald-soft flex items-center justify-center">
                <card.icon className="h-4 w-4 text-primary" />
              </div>
              <span className="text-xs text-muted-foreground uppercase tracking-wider font-medium">{card.label}</span>
            </div>
            <span className="text-2xl font-heading font-semibold text-foreground">{card.value}</span>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card-elegant p-5">
          <h3 className="text-sm font-medium text-foreground mb-4">Recent Appointments</h3>
          {profile?.appointments?.length ? (
            <ul className="space-y-3">
              {profile.appointments.slice(0, 5).map((apt: any, i: number) => (
                <li key={i} className="flex justify-between text-sm">
                  <span className="text-foreground">{apt.title || apt.type || "Appointment"}</span>
                  <span className="text-muted-foreground">{apt.date || "—"}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-muted-foreground">No appointment data available.</p>
          )}
        </div>
        <div className="card-elegant p-5">
          <h3 className="text-sm font-medium text-foreground mb-4">Active Care Plans</h3>
          {profile?.care_plans?.length ? (
            <ul className="space-y-3">
              {profile.care_plans.slice(0, 5).map((plan: any, i: number) => (
                <li key={i} className="text-sm text-foreground">{plan.name || plan.title || "Care Plan"}</li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-muted-foreground">No care plan data available.</p>
          )}
        </div>
      </div>
    </div>
  );
}
