import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import DashboardLayout from "@/components/DashboardLayout";
import ChatPage from "@/pages/ChatPage";
import DashboardPage from "@/pages/DashboardPage";
import VaultPage from "@/pages/VaultPage";
import SymptomsPage from "@/pages/SymptomsPage";
import NutritionPage from "@/pages/NutritionPage";
import FitnessPage from "@/pages/FitnessPage";
import MentalHealthPage from "@/pages/MentalHealthPage";
import HealthRecordsPage from "@/pages/HealthRecordsPage";
import HospitalPage from "@/pages/HospitalPage";
import NotFound from "@/pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route element={<DashboardLayout children={undefined} />}>
          </Route>
          <Route path="/" element={<DashboardLayout><ChatPage /></DashboardLayout>} />
          <Route path="/dashboard" element={<DashboardLayout><DashboardPage /></DashboardLayout>} />
          <Route path="/vault" element={<DashboardLayout><VaultPage /></DashboardLayout>} />
          <Route path="/symptoms" element={<DashboardLayout><SymptomsPage /></DashboardLayout>} />
          <Route path="/nutrition" element={<DashboardLayout><NutritionPage /></DashboardLayout>} />
          <Route path="/fitness" element={<DashboardLayout><FitnessPage /></DashboardLayout>} />
          <Route path="/mental-health" element={<DashboardLayout><MentalHealthPage /></DashboardLayout>} />
          <Route path="/health-records" element={<DashboardLayout><HealthRecordsPage /></DashboardLayout>} />
          <Route path="/hospital" element={<DashboardLayout><HospitalPage /></DashboardLayout>} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
