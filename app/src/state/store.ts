import { createContext, useContext } from "react";

export type Tab = "today" | "chat";
export type Theme = "day" | "night";
export type StatusKind = "awake" | "napping";
export type LogSource = "button" | "chat" | "backfill" | "notification";
export type Network = "online" | "offline";

/** Pushed full-screens, sheets and popovers layered over the current tab. */
export type Overlay =
  | "settings" // E2
  | "dataControl" // E3
  | "memory" // E1
  | "review" // H1–H3
  | "subscription" // F1
  | "editRecord" // C2
  | "babySwitcher" // C4
  | "nightWake" // C3
  | "lockScreen"; // G1

/** One entry in the on-device sleep log (README: State Management). */
export interface SleepEvent {
  id: string;
  kind: "nap" | "night" | "nightWake" | "morningWake";
  label: string; // display text, e.g. "第二觉 · 进行中"
  time: string; // "HH:MM"
  detail?: string; // e.g. "12 分钟 · 喂奶"
  source: LogSource;
  inProgress?: boolean;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
  /** Logged-card variant: assistant bubble with a ✓ badge + chips. */
  logged?: { title: string; detail: string };
}

export interface Baby {
  id: string;
  name: string;
  initial: string;
  ageLabel: string; // "7 个月 · 2 觉宝宝"
}

export interface AppState {
  phase: "onboarding" | "app";
  onboardingStep: 1 | 2 | 3;
  tab: Tab;
  theme: Theme;
  baby: Baby;
  statusKind: StatusKind;
  statusSince: number; // epoch ms — anchor for the live elapsed timer
  napIndex: number;
  log: SleepEvent[];
  sheetOpen: boolean;
  toast: { message: string; undo?: () => void } | null;
  messages: ChatMessage[];
  // Cross-screen flags that select variants (B1–B5, D1–D4, F1)
  optimizationPaused: boolean; // safety pause → B5 / D3
  network: Network; // offline → D4
  firstDay: boolean; // data-insufficient → B4
  babies: Baby[];
  selectedBabyId: string;
  overlay: Overlay | null;
}

export interface AppActions {
  advanceOnboarding: () => void;
  skipToApp: () => void;
  restartOnboarding: () => void;
  setTab: (t: Tab) => void;
  setTheme: (t: Theme) => void;
  toggleTheme: () => void;
  markAsleep: () => void;
  markAwake: () => void;
  openSheet: () => void;
  closeSheet: () => void;
  saveBackfill: (entry: { kind: "nap" | "night" | "nightWake"; start: string; end: string }) => void;
  dismissToast: () => void;
  sendMessage: (text: string) => void;
  // Variant flags (also driven by the demo bar)
  setPaused: (b: boolean) => void;
  setNetwork: (n: Network) => void;
  setFirstDay: (b: boolean) => void;
  selectBaby: (id: string) => void;
  // Overlay navigation
  openOverlay: (o: Overlay) => void;
  closeOverlay: () => void;
  logNightWake: () => void; // C3 → 夜里醒了
  getUp: () => void; // C3 → 起床了
}

export type AppStore = AppState & AppActions;

export const AppContext = createContext<AppStore | null>(null);

export function useApp(): AppStore {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within <AppProvider>");
  return ctx;
}

// ── helpers ──────────────────────────────────────────────────────────────

export function fmtElapsed(sinceMs: number, nowMs: number): string {
  const totalMin = Math.max(0, Math.floor((nowMs - sinceMs) / 60000));
  const h = Math.floor(totalMin / 60);
  const m = totalMin % 60;
  return `${h}h ${m}m`;
}

export function nowHHMM(ms: number): string {
  const d = new Date(ms);
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

let counter = 0;
export function uid(prefix = "id"): string {
  counter += 1;
  return `${prefix}-${counter}`;
}
