import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import { IOSFrame } from "./components/IOSFrame";
import {
  AppContext,
  nowHHMM,
  uid,
  useApp,
  type AppState,
  type AppStore,
  type ChatMessage,
  type SleepEvent,
  type Tab,
  type Theme,
} from "./state/store";
import { Welcome } from "./screens/onboarding/Welcome";
import { BabyProfile } from "./screens/onboarding/BabyProfile";
import { Concerns } from "./screens/onboarding/Concerns";
import { Today } from "./screens/today/Today";
import { Chat } from "./screens/chat/Chat";
import { RecordSheet } from "./screens/record/RecordSheet";
import { Toast } from "./components/Toast";
import { EditRecord } from "./screens/record/EditRecord";
import { NightWakeSheet } from "./screens/record/NightWakeSheet";
import { BabySwitcher } from "./screens/record/BabySwitcher";
import { Review } from "./screens/review/Review";
import { Memory } from "./screens/memory/Memory";
import { Settings } from "./screens/settings/Settings";
import { DataControl } from "./screens/settings/DataControl";
import { Subscription } from "./screens/subscription/Subscription";
import { LockScreen } from "./screens/lockscreen/LockScreen";

const SEED_LOG: SleepEvent[] = [
  { id: uid("ev"), kind: "morningWake", label: "晨醒 · 开始今天", time: "10:15", source: "button" },
  { id: uid("ev"), kind: "nightWake", label: "夜醒 12 分钟 · 喂奶", time: "05:10", source: "chat" },
];

const SEED_MESSAGES: ChatMessage[] = [
  { id: uid("m"), role: "user", text: "上午九点多睡的 十点醒 有点短" },
  {
    id: uid("m"),
    role: "assistant",
    text: "",
    logged: { title: "记好了 · 第一觉 约 09:10 – 10:00", detail: '开始时间保留"九点多"。' },
  },
  {
    id: uid("m"),
    role: "assistant",
    text: "50 分钟和她最近两周的第一觉差不多（中位 55 分），不算短。真正变了的是入睡：这三天 8:45–9:10 都能睡着，说明提前是撑得住的。Keep it two more days, then we review.",
  },
];

export function App() {
  // Anchor the awake timer so the initial render reads ~1h 12m like the design,
  // then ticks live. Lazy init so it's stable across renders.
  const [statusSince, setStatusSince] = useState<number>(() => Date.now() - 72 * 60000);
  const [now, setNow] = useState<number>(() => Date.now());

  const [phase, setPhase] = useState<AppState["phase"]>("onboarding");
  const [onboardingStep, setOnboardingStep] = useState<AppState["onboardingStep"]>(1);
  const [tab, setTab] = useState<Tab>("today");
  const [theme, setTheme] = useState<Theme>("day");
  const [statusKind, setStatusKind] = useState<AppState["statusKind"]>("awake");
  const [napIndex, setNapIndex] = useState(2);
  const [log, setLog] = useState<SleepEvent[]>(SEED_LOG);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [toast, setToast] = useState<AppState["toast"]>(null);
  const [messages, setMessages] = useState<ChatMessage[]>(SEED_MESSAGES);
  const [optimizationPaused, setOptimizationPaused] = useState(false);
  const [network, setNetwork] = useState<AppState["network"]>("online");
  const [firstDay, setFirstDay] = useState(false);
  const [selectedBabyId, setSelectedBabyId] = useState("b1");
  const [overlay, setOverlay] = useState<AppState["overlay"]>(null);

  const babies = useMemo<AppState["babies"]>(
    () => [
      { id: "b1", name: "小满", initial: "满", ageLabel: "7 个月 · 2 觉宝宝" },
      { id: "b2", name: "安安", initial: "安", ageLabel: "2 岁 3 个月 · 2 觉宝宝" },
    ],
    [],
  );
  const baby = babies.find((b) => b.id === selectedBabyId) ?? babies[0];

  // Live clock — one tick per second drives every elapsed display.
  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);

  // Auto-dismiss toast after 6s (README: 6s toast with 撤销).
  const toastTimer = useRef<number | null>(null);
  const showToast = useCallback((message: string, undo?: () => void) => {
    setToast({ message, undo });
    if (toastTimer.current) window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToast(null), 6000);
  }, []);

  const markAsleep = useCallback(() => {
    const prevLog = log;
    const prevSince = statusSince;
    const t = nowHHMM(Date.now());
    setStatusKind("napping");
    setStatusSince(Date.now());
    setLog((l) => [
      { id: uid("ev"), kind: "nap", label: `第${napIndex}觉 · 进行中`, time: t, source: "button", inProgress: true },
      ...l,
    ]);
    showToast("已记录 · 睡着了", () => {
      setStatusKind("awake");
      setStatusSince(prevSince);
      setLog(prevLog);
    });
  }, [log, statusSince, napIndex, showToast]);

  const markAwake = useCallback(() => {
    const prevLog = log;
    const prevSince = statusSince;
    const prevKind = statusKind;
    const endedMin = Math.max(1, Math.floor((Date.now() - statusSince) / 60000));
    setStatusKind("awake");
    setStatusSince(Date.now());
    setNapIndex((n) => n + 1);
    setLog((l) =>
      l.map((e) => (e.inProgress ? { ...e, inProgress: false, label: `第${napIndex}觉`, detail: `${endedMin} 分钟` } : e)),
    );
    showToast("已记录 · 醒了", () => {
      setStatusKind(prevKind);
      setStatusSince(prevSince);
      setNapIndex((n) => n - 1);
      setLog(prevLog);
    });
  }, [log, statusSince, statusKind, napIndex, showToast]);

  const saveBackfill = useCallback<AppStore["saveBackfill"]>(
    (entry) => {
      const label = entry.kind === "nap" ? "补记的小觉" : entry.kind === "night" ? "补记的夜觉" : "夜醒";
      setLog((l) => [
        { id: uid("ev"), kind: entry.kind, label, time: entry.start, detail: `– ${entry.end}`, source: "backfill" },
        ...l,
      ]);
      setSheetOpen(false);
      showToast("已保存到今天");
    },
    [showToast],
  );

  const sendMessage = useCallback<AppStore["sendMessage"]>((text) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    setMessages((m) => [...m, { id: uid("m"), role: "user", text: trimmed }]);
    // Canned assistant follow-up so the composer feels live.
    const looksLikeLog = /(睡|醒|觉|nap|sleep|woke)/i.test(trimmed);
    window.setTimeout(() => {
      setMessages((m) => [
        ...m,
        looksLikeLog
          ? {
              id: uid("m"),
              role: "assistant",
              text: "",
              logged: { title: "记好了 · 已加入今天", detail: "按发送时刻推算，可随时改。" },
            }
          : {
              id: uid("m"),
              role: "assistant",
              text: "我在。跟我说说当下的情况，我们一起看看下一步怎么安排。",
            },
      ]);
    }, 600);
  }, []);

  const logNightWake = useCallback(() => {
    const t = nowHHMM(Date.now());
    setLog((l) => [{ id: uid("ev"), kind: "nightWake", label: "夜醒", time: t, source: "button" }, ...l]);
    setOverlay(null);
    showToast("已记录 · 夜醒");
  }, [showToast]);

  const getUp = useCallback(() => {
    const t = nowHHMM(Date.now());
    setStatusKind("awake");
    setStatusSince(Date.now());
    setLog((l) => [{ id: uid("ev"), kind: "morningWake", label: "晨醒 · 开始今天", time: t, source: "button" }, ...l]);
    setOverlay(null);
    showToast("已记录 · 起床了");
  }, [showToast]);

  const store: AppStore = {
    phase,
    onboardingStep,
    tab,
    theme,
    baby,
    statusKind,
    statusSince,
    napIndex,
    log,
    sheetOpen,
    toast,
    messages,
    optimizationPaused,
    network,
    firstDay,
    babies,
    selectedBabyId,
    overlay,
    advanceOnboarding: () => setOnboardingStep((s) => (s < 3 ? ((s + 1) as 1 | 2 | 3) : s)),
    skipToApp: () => setPhase("app"),
    restartOnboarding: () => {
      setPhase("onboarding");
      setOnboardingStep(1);
    },
    setTab,
    setTheme,
    toggleTheme: () => setTheme((t) => (t === "day" ? "night" : "day")),
    markAsleep,
    markAwake,
    openSheet: () => setSheetOpen(true),
    closeSheet: () => setSheetOpen(false),
    saveBackfill,
    dismissToast: () => setToast(null),
    sendMessage,
    setPaused: setOptimizationPaused,
    setNetwork,
    setFirstDay,
    selectBaby: (id) => {
      setSelectedBabyId(id);
      setOverlay(null);
    },
    openOverlay: (o) => setOverlay(o),
    closeOverlay: () => setOverlay(null),
    logNightWake,
    getUp,
  };

  // Onboarding A3 -> enter app; A1/A2 -> advance step.
  const onboardingNext = () => {
    if (onboardingStep < 3) store.advanceOnboarding();
    else store.skipToApp();
  };

  // Some overlays force a dark status bar regardless of the day/night theme.
  const dark = theme === "night" || overlay === "lockScreen" || overlay === "nightWake";

  return (
    <AppContext.Provider value={store}>
      <div
        style={{
          minHeight: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 16,
          padding: "40px 0 56px",
        }}
      >
        <DemoBar />
        <div style={{ position: "relative" }}>
          <IOSFrame dark={dark}>
            {phase === "onboarding" ? (
              onboardingStep === 1 ? (
                <Welcome onNext={onboardingNext} onSkip={store.skipToApp} />
              ) : onboardingStep === 2 ? (
                <BabyProfile onNext={onboardingNext} onSkip={store.skipToApp} />
              ) : (
                <Concerns onNext={store.skipToApp} onSkip={store.skipToApp} />
              )
            ) : tab === "today" ? (
              <Today now={now} />
            ) : (
              <Chat now={now} />
            )}

            {sheetOpen && <RecordSheet onCancel={store.closeSheet} onSave={saveBackfill} />}
            <OverlayHost now={now} />
            {toast && <Toast message={toast.message} undo={toast.undo} onUndo={store.dismissToast} />}
          </IOSFrame>
        </div>
      </div>
    </AppContext.Provider>
  );
}

/** Renders whichever overlay (pushed screen / sheet / popover) is active. */
function OverlayHost({ now }: { now: number }) {
  const app = useApp();
  const close = app.closeOverlay;
  switch (app.overlay) {
    case "settings":
      return <Settings onBack={close} onOpen={app.openOverlay} />;
    case "dataControl":
      return <DataControl onBack={() => app.openOverlay("settings")} />;
    case "memory":
      return <Memory onBack={close} />;
    case "review":
      return <Review onBack={close} onConsult={() => app.openOverlay("subscription")} />;
    case "subscription":
      return <Subscription onClose={close} />;
    case "editRecord":
      return <EditRecord onBack={close} />;
    case "babySwitcher":
      return <BabySwitcher onClose={close} />;
    case "nightWake":
      return <NightWakeSheet now={now} onCancel={close} onNightWake={app.logNightWake} onGetUp={app.getUp} />;
    case "lockScreen":
      return <LockScreen onDismiss={close} />;
    default:
      return null;
  }
}

/**
 * Out-of-frame control strip for demoing the prototype (not a screen). Flips the
 * day/night theme + state flags (safety pause, offline, first-day) that select
 * screen variants, and opens the pushed screens that have no in-flow entry yet.
 */
function DemoBar() {
  const s = useApp();
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: 8,
        alignItems: "center",
        maxWidth: 620,
        fontFamily: "system-ui, sans-serif",
        fontSize: 13,
        color: "#4a4a4a",
      }}
    >
      <strong style={{ fontWeight: 700 }}>知眠 LullSense</strong>
      <button onClick={() => s.setTheme("day")} style={demoBtn(s.theme === "day")}>白天</button>
      <button onClick={() => s.setTheme("night")} style={demoBtn(s.theme === "night")}>夜间</button>
      <span style={{ opacity: 0.4 }}>|</span>
      <button onClick={() => s.setPaused(!s.optimizationPaused)} style={demoBtn(s.optimizationPaused)}>安全暂停</button>
      <button onClick={() => s.setNetwork(s.network === "offline" ? "online" : "offline")} style={demoBtn(s.network === "offline")}>断网</button>
      <button onClick={() => s.setFirstDay(!s.firstDay)} style={demoBtn(s.firstDay)}>数据不足</button>
      <span style={{ opacity: 0.4 }}>|</span>
      <button onClick={() => s.openOverlay("review")} style={demoBtn(false)}>回看</button>
      <button onClick={() => s.openOverlay("memory")} style={demoBtn(false)}>记忆</button>
      <button onClick={() => s.openOverlay("settings")} style={demoBtn(false)}>设置</button>
      <button onClick={() => s.openOverlay("subscription")} style={demoBtn(false)}>订阅</button>
      <button onClick={() => s.openOverlay("editRecord")} style={demoBtn(false)}>编辑记录</button>
      <button onClick={() => s.openOverlay("lockScreen")} style={demoBtn(false)}>锁屏</button>
      <span style={{ opacity: 0.4 }}>|</span>
      <button onClick={s.restartOnboarding} style={demoBtn(false)}>重新上手</button>
    </div>
  );
}

function demoBtn(active: boolean): CSSProperties {
  return {
    padding: "5px 12px",
    borderRadius: 999,
    fontSize: 13,
    fontWeight: 600,
    background: active ? "#2B4A8A" : "#fff",
    color: active ? "#fff" : "#4a4a4a",
    boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
  };
}
