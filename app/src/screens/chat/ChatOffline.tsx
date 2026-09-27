import { day, font } from "../../theme/tokens";
import { TabBar } from "../../components/TabBar";
import { useApp } from "../../state/store";

/**
 * D4 聊知眠 · 断网 — chat + natural-language logging are unavailable; button
 * logging, timeline, prediction and reminders keep working. Grey mascot.
 */
export function ChatOffline() {
  const app = useApp();
  return (
    <div
      style={{
        fontFamily: font.family,
        height: "100%",
        boxSizing: "border-box",
        background: day.pageBg,
        color: day.ink,
        display: "flex",
        flexDirection: "column",
        padding: "62px 18px 0",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ width: 48, display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ width: 44, height: 24, borderRadius: "24px 24px 5px 5px", background: "#E3D6BC" }} />
          <div style={{ width: 16, height: 18, borderRadius: "0 0 6px 6px", background: day.lampStem, marginTop: -1 }} />
        </div>
        <div style={{ lineHeight: 1.15 }}>
          <div style={{ fontSize: 20, fontWeight: 800 }}>知眠</div>
          <div style={{ fontSize: 13, fontWeight: 700, color: day.periwinkle }}>离线 · 暂时联系不上</div>
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, minHeight: 0, overflowY: "auto", marginTop: 22, display: "flex", flexDirection: "column", gap: 12, fontSize: 15, lineHeight: 1.5, fontWeight: 600 }}>
        <div style={{ alignSelf: "flex-end", maxWidth: "80%", padding: "12px 16px", borderRadius: "22px 22px 6px 22px", background: day.navy, color: "#fff", opacity: 0.55 }}>
          刚睡着了
        </div>
        <div style={{ alignSelf: "flex-end", fontSize: 12, fontWeight: 700, color: day.destructive }}>未发送 · 需要联网 · 重试</div>
        <div style={{ alignSelf: "flex-start", maxWidth: "92%", padding: "14px 16px", borderRadius: "6px 22px 22px 22px", background: "#fff", border: "1.5px dashed #B9C7E6" }}>
          <div style={{ fontWeight: 800 }}>现在没网，这句话我还没收到。</div>
          <div style={{ marginTop: 6, color: "#4A5570" }}>
            按钮记录、时间轴、预测和提醒都在手机上，不受影响。要记"刚睡着了"的话，直接点下面这个就行：
          </div>
          <button
            onClick={app.markAsleep}
            style={{ marginTop: 12, width: "100%", height: 56, borderRadius: 28, background: day.navy, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17, fontWeight: 800 }}
          >
            睡着了 · 现在 13:22
          </button>
          <button onClick={app.openSheet} style={{ marginTop: 8, width: "100%", fontSize: 13, color: day.periwinkle, textAlign: "center", fontWeight: 700 }}>
            或 补记其他时间
          </button>
        </div>
      </div>

      {/* Composer (disabled) + tab bar */}
      <div style={{ paddingBottom: 14 }}>
        <div style={{ height: 58, borderRadius: 29, background: "#fff", opacity: 0.6, display: "flex", alignItems: "center", padding: "0 8px 0 20px", justifyContent: "space-between" }}>
          <span style={{ fontSize: 15, color: day.periwinkle, fontWeight: 700 }}>联网后可以继续聊</span>
          <span style={{ width: 42, height: 42, borderRadius: 21, background: "#E3D6BC", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800 }}>↑</span>
        </div>
        <div style={{ marginTop: 12 }}>
          <TabBar active="chat" onChange={app.setTab} />
        </div>
      </div>
    </div>
  );
}
