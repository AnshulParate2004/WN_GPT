import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";
import { Building2, BedDouble, Package } from "lucide-react";

export default function HospitalPage() {
  const [status, setStatus] = useState<any>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    api.getHospitalStatus().then(setStatus).catch(() => setError(true));
  }, []);

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-heading font-semibold text-foreground mb-1">Facility View</h1>
      <p className="text-sm text-muted-foreground mb-8">Real-time bed and inventory status</p>

      {error && (
        <div className="card-elegant p-4 text-sm text-muted-foreground mb-6">
          Unable to connect to backend. Showing placeholder layout.
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="card-elegant p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="h-9 w-9 rounded-md bg-emerald-soft flex items-center justify-center">
              <BedDouble className="h-4 w-4 text-primary" />
            </div>
            <span className="text-xs text-muted-foreground uppercase tracking-wider font-medium">Beds Available</span>
          </div>
          <span className="text-2xl font-heading font-semibold text-foreground">
            {status?.beds_available ?? "—"}
          </span>
          <span className="text-sm text-muted-foreground ml-1">/ {status?.beds_total ?? "—"}</span>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.08 }} className="card-elegant p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="h-9 w-9 rounded-md bg-emerald-soft flex items-center justify-center">
              <Package className="h-4 w-4 text-primary" />
            </div>
            <span className="text-xs text-muted-foreground uppercase tracking-wider font-medium">Inventory Items</span>
          </div>
          <span className="text-2xl font-heading font-semibold text-foreground">
            {status?.inventory_count ?? "—"}
          </span>
        </motion.div>
      </div>

      {status?.departments && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="card-elegant p-5">
          <div className="flex items-center gap-2 mb-4">
            <Building2 className="h-4 w-4 text-primary" />
            <h3 className="text-sm font-medium text-foreground">Departments</h3>
          </div>
          <div className="space-y-3">
            {status.departments.map((dept: any, i: number) => (
              <div key={i} className="flex justify-between text-sm">
                <span className="text-foreground">{dept.name}</span>
                <span className="text-muted-foreground">{dept.beds_available}/{dept.beds_total} beds</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
