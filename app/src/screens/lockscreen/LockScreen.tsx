import { day } from "../../theme/tokens";
import { useApp } from "../../state/store";

/**
 * G1 锁屏提醒 — a standard iOS notification. The reminder means "start getting
 * ready", not a must-sleep moment. Fires at window start − lead time; suppressed
 * during quiet hours, while a sleep is in progress, or during safety pause.
 * Uses the system font, not Baloo.
 */
export function LockScreen({ onDismiss }: { onDismiss: () => void }) {
  const app = useApp();
  const asleep = () => {
    app.markAsleep();
    onDismiss();
  };
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 65,
        boxSizing: "border-box",
        background: "linear-gradient(180deg,#1B2743 0%,#2B3A66 100%)",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        padding: "96px 16px 0",
        fontFamily: "-apple-system, system-ui, 'Noto Sans SC', sans-serif",
        animation: "lsFadeIn .2s ease-out",
      }}
    >
      <div style={{ textAlign: "center", fontSize: 22, fontWeight: 600, letterSpacing: ".02em", opacity: 0.9 }}>9月25日 星期四</div>
      <div style={{ textAlign: "center", fontSize: 88, fontWeight: 700, letterSpacing: "-.03em", lineHeight: 1, marginTop: 4 }}>12:45</div>

      <div style={{ marginTop: 60, background: "rgba(255,255,255,.16)", borderRadius: 24, padding: "14px 16px", display: "flex", gap: 12, alignItems: "flex-start", backdropFilter: "blur(20px)" }}>
        {/* App icon tile with lamp */}
        <div style={{ flex: "none", width: 38, height: 38, borderRadius: 9, background: day.navy, display: "flex", alignItems: "flex-end", justifyContent: "center", paddingBottom: 6 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ width: 22, height: 12, borderRadius: "12px 12px 3px 3px", background: day.gold }} />
            <div style={{ width: 8, height: 8, borderRadius: "0 0 3px 3px", background: day.lampStem }} />
          </div>
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 15, fontWeight: 600 }}>
            <span>知眠</span>
            <span style={{ fontSize: 13, opacity: 0.6 }}>现在</span>
          </div>
          <div style={{ marginTop: 2, fontSize: 15, lineHeight: 1.4, fontWeight: 400 }}>
            小满的第二觉可能在 13:15–13:55，可以开始准备了。已经睡了的话点「睡着了」。
          </div>
        </div>
      </div>

      <div style={{ marginTop: 10, display: "flex", gap: 10 }}>
        <button onClick={asleep} style={notifBtn}>睡着了</button>
        <button onClick={onDismiss} style={notifBtn}>推迟 15 分</button>
      </div>

      <button onClick={onDismiss} style={{ marginTop: "auto", marginBottom: 60, textAlign: "center", fontSize: 13, opacity: 0.6, color: "#fff", width: "100%" }}>
        — 长按可关闭今天的提醒 —
      </button>
    </div>
  );
}

const notifBtn = {
  flex: 1,
  height: 44,
  borderRadius: 22,
  background: "rgba(255,255,255,.16)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 15,
  fontWeight: 600,
  color: "#fff",
} as const;
