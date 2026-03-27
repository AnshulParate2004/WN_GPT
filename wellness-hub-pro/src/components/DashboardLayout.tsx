import { ReactNode } from "react";
import { useLocation } from "react-router-dom";
import { NavLink } from "@/components/NavLink";
import { useTheme } from "@/hooks/useTheme";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";
import {
  MessageCircle,
  LayoutDashboard,
  FileText,
  Stethoscope,
  Apple,
  Dumbbell,
  Brain,
  Database,
  Building2,
  Sun,
  Moon,
  User,
} from "lucide-react";

const navItems = [
  { title: "Agent Chat", url: "/", icon: MessageCircle },
  { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
  { title: "Medical Vault", url: "/vault", icon: FileText },
  { title: "Symptom Log", url: "/symptoms", icon: Stethoscope },
  { title: "Nutrition Log", url: "/nutrition", icon: Apple },
  { title: "Fitness Log", url: "/fitness", icon: Dumbbell },
  { title: "Mental Health", url: "/mental-health", icon: Brain },
  { title: "Govt Sync", url: "/health-records", icon: Database },
  { title: "Facility View", url: "/hospital", icon: Building2 },
];

function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const location = useLocation();

  return (
    <Sidebar collapsible="icon" className="border-r border-border">
      <SidebarContent className="pt-6">
        <div className="px-4 mb-8">
          {!collapsed && (
            <h1 className="text-heading text-xl font-semibold tracking-tight text-foreground">
              Wellness<span className="text-primary">GPT</span>
            </h1>
          )}
          {collapsed && (
            <span className="text-primary font-bold text-lg flex justify-center">W</span>
          )}
        </div>
        <SidebarGroup>
          <SidebarGroupLabel className="text-muted-foreground text-[10px] uppercase tracking-[0.15em] font-medium">
            Navigation
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => (
                <SidebarMenuItem key={item.url}>
                  <SidebarMenuButton asChild>
                    <NavLink
                      to={item.url}
                      end={item.url === "/"}
                      className="flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium text-muted-foreground transition-colors hover:text-foreground hover:bg-secondary"
                      activeClassName="bg-emerald-soft text-primary"
                    >
                      <item.icon className="h-4 w-4 flex-shrink-0" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}

function TopBar() {
  const { dark, toggle } = useTheme();

  return (
    <header className="h-14 flex items-center justify-between border-b border-border px-4 bg-card">
      <SidebarTrigger className="text-muted-foreground hover:text-foreground" />
      <div className="flex items-center gap-4">
        <button
          onClick={toggle}
          className="h-8 w-8 rounded-full flex items-center justify-center border border-border text-muted-foreground hover:text-foreground transition-colors"
          aria-label="Toggle theme"
        >
          {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
            <User className="h-4 w-4 text-primary" />
          </div>
          <span className="text-sm font-medium text-foreground hidden sm:block">Patient P001</span>
        </div>
      </div>
    </header>
  );
}

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <AppSidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <TopBar />
          <main className="flex-1 overflow-auto p-4 md:p-6">{children}</main>
        </div>
      </div>
    </SidebarProvider>
  );
}
