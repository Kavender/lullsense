import { day, font, radius } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";
import { useApp } from "../../state/store";

/**
 * B5 今天 · 安全暂停 — triggered by the assistant's safety classifier (D3).
 * Predictions and reminders are hidden; logging continues; the mascot is amber.
 */
export function TodayPaused() {
  const app = useApp();
  return (
    <div
      style={{
        fontFamily: font.family,
        height: "100%",
        boxSizing: "border-box",
        background: day.amberPageBg,
        color: day.ink,
        display: "flex",
        flexDirection: "column",
        padding: "62px 20px 0",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <button onClick={() => app.openOverlay("babySwitcher")} style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={avatar}>{app.baby.initial}</span>
          <div style={{ lineHeight: 1.1, textAlign: "left" }}>
            <div style={{ fontSize: 17, fontWeight: 800, color: day.ink }}>
              {app.baby.name} <span style={{ fontSize: 12, color: day.periwinkle }}>▾</span>
            </div>
            <div style={{ fontSize: 13, color: day.amberText, fontWeight: 700 }}>{app.baby.age} · 优化已暂停</div>
          </div>
        </button>
        <button onClick={() => app.openOverlay("settings")} style={gear}>⚙</button>
      </div>

      <div style={{ marginTop: 22, background: day.card, borderRadius: radius.pageCard, padding: "22px 22px 20px", boxShadow: "0 8px 30px rgba(43,74,138,.08)" }}>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 14, fontWeight: 800, color: day.periwinkle, letterSpacing: ".04em" }}>已醒 · AWAKE</div>
            <div style={{ marginTop: 2, fontSize: 46, fontWeight: 800, lineHeight: 1.05, letterSpacing: "-.02em" }}>1h 40m</div>
            <div style={{ marginTop: 4, fontSize: 15, fontWeight: 700, color: day.periwinkle }}>13:45 醒 · 第二觉 10:40–13:45</div>
          </div>
          <div style={{ flex: "none", paddingTop: 6 }}>
            <Mascot size="md" state="amber" />
          </div>
        </div>
        <div style={{ marginTop: 14, padding: 16, borderRadius: radius.innerCard, background: day.amberTint }}>
          <div style={{ fontSize: 13, fontWeight: 800, color: day.amberText }}>睡眠优化已暂停</div>
          <div style={{ marginTop: 4, fontSize: 14, fontWeight: 600, color: "#6B4A2A", lineHeight: 1.5 }}>
            先照顾好她。这期间不显示下一觉预测、不推提醒、调整计划搁置。情况稳定后在聊知眠里恢复。
          </div>
          <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
            <button onClick={() => app.setTab("chat")} style={{ padding: "8px 14px", borderRadius: 16, background: "#fff", fontSize: 13, fontWeight: 800, color: day.navy }}>
              去聊知眠
            </button>
            <button onClick={() => app.setPaused(false)} style={{ padding: "8px 14px", borderRadius: 16, background: "#fff", fontSize: 13, fontWeight: 800, color: day.amberText }}>
              恢复优化
            </button>
          </div>
        </div>
      </div>

      <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
        <button onClick={app.markAsleep} style={{ flex: 1, height: 64, borderRadius: radius.pageCard, background: day.navy, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 19, fontWeight: 800, boxShadow: "0 6px 18px rgba(43,74,138,.25)" }}>
          睡着了
        </button>
        <button onClick={app.openSheet} style={secondary}>补记</button>
      </div>

      <div style={{ marginTop: 22, display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <div style={{ fontSize: 15, fontWeight: 800 }}>今天 · 9月26日</div>
        <button onClick={() => app.openOverlay("review")} style={{ fontSize: 13, fontWeight: 700, color: day.periwinkle }}>回看 ›</button>
      </div>
      <div style={{ marginTop: 10, position: "relative", height: 56, borderRadius: 28, background: "rgba(255,255,255,.7)", overflow: "hidden" }}>
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: "29%", background: day.periwinkle, borderRadius: "28px 0 0 28px" }} />
        <div style={{ position: "absolute", left: "44%", top: 0, bottom: 0, width: "13%", background: day.periwinkleLight, borderRadius: 16 }} />
        <div style={{ position: "absolute", left: "64%", top: 0, bottom: 0, width: 2, background: day.ink }} />
      </div>
      <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 8, fontSize: 15, fontWeight: 700 }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span style={{ width: 12, height: 12, borderRadius: 6, background: day.periwinkleLight, display: "block", flex: "none" }} />
          <span style={{ width: 48, color: day.periwinkle, flex: "none" }}>10:40</span>
          <span style={{ flex: 1 }}>第二觉 3h 05m</span>
          <span style={{ fontSize: 12, color: day.goldText, flex: "none" }}>聊天</span>
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span style={{ width: 12, height: 12, borderRadius: 6, background: day.gold, display: "block", flex: "none" }} />
          <span style={{ width: 48, color: day.periwinkle, flex: "none" }}>07:05</span>
          <span style={{ flex: 1 }}>晨醒</span>
        </div>
      </div>

      {/* Amber-tinted tab bar (README B5) */}
      <div style={{ marginTop: "auto", paddingBottom: 14 }}>
        <div style={{ height: 64, borderRadius: radius.tabBar, background: "#fff", display: "flex", alignItems: "center", justifyContent: "space-around", fontSize: 14, fontWeight: 800 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, color: day.navy, background: day.amberTint, padding: "10px 20px", borderRadius: 22 }}>
            <span style={{ width: 16, height: 16, borderRadius: 8, background: day.amber, display: "block" }} />
            今天
          </div>
          <button onClick={() => app.setTab("chat")} style={{ display: "flex", alignItems: "center", gap: 8, color: day.periwinkle, padding: "10px 20px" }}>
            <span style={{ width: 16, height: 16, borderRadius: 8, border: `3px solid ${day.periwinkle}`, display: "block", boxSizing: "border-box" }} />
            聊知眠
          </button>
        </div>
      </div>
    </div>
  );
}

const avatar = {
  width: 40,
  height: 40,
  borderRadius: 20,
  background: day.navy,
  color: "#fff",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 16,
  fontWeight: 800,
} as const;

const gear = {
  width: 40,
  height: 40,
  borderRadius: 20,
  background: "rgba(255,255,255,.7)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 14,
  color: day.periwinkle,
} as const;

const secondary = {
  height: 64,
  padding: "0 22px",
  borderRadius: radius.pageCard,
  background: day.card,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 16,
  fontWeight: 800,
  color: day.navy,
} as const;
