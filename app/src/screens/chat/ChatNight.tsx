import { night, font } from "../../theme/tokens";
import { TabBar } from "../../components/TabBar";
import { useApp } from "../../state/store";

const SUGGESTIONS = ["几点该起床？", "要不要喂奶", "Is this normal?"];

/**
 * D2 聊知眠 · 夜间 — dimmed mascot, "只记，不推提醒". Records night wakes and
 * offers reassurance without pushing schedule changes.
 */
export function ChatNight() {
  const app = useApp();
  return (
    <div
      style={{
        fontFamily: font.family,
        height: "100%",
        boxSizing: "border-box",
        background: night.pageBg,
        color: night.ink,
        display: "flex",
        flexDirection: "column",
        padding: "62px 18px 0",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ width: 48, display: "flex", justifyContent: "center" }}>
          <TinyLamp glow />
        </div>
        <div style={{ lineHeight: 1.15 }}>
          <div style={{ fontSize: 20, fontWeight: 800 }}>知眠</div>
          <div style={{ fontSize: 13, fontWeight: 700, color: night.muted }}>夜间 · 只记，不推提醒</div>
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, minHeight: 0, overflowY: "auto", marginTop: 22, display: "flex", flexDirection: "column", gap: 12, fontSize: 15, lineHeight: 1.5, fontWeight: 600 }}>
        <div style={{ alignSelf: "center", fontSize: 12, color: night.muted }}>02:47</div>
        <div style={{ alignSelf: "flex-end", maxWidth: "80%", padding: "12px 16px", borderRadius: "22px 22px 6px 22px", background: night.userBubble }}>
          刚醒了 哭了一会 又睡回去了
        </div>

        <div style={{ alignSelf: "flex-start", display: "flex", gap: 10, maxWidth: "92%", alignItems: "flex-end" }}>
          <div style={{ flex: "none", marginBottom: 4 }}><TinyLamp glow small /></div>
          <div style={{ padding: "14px 16px", borderRadius: "6px 22px 22px 22px", background: "rgba(255,255,255,.06)", border: "1px solid rgba(240,195,106,.3)" }}>
            <div style={{ fontWeight: 800 }}>记好了 · 夜醒 02:31 – 02:47</div>
            <div style={{ marginTop: 6, color: night.periwinkle, fontSize: 14 }}>16 分钟，按发送时刻推算，可以改早。夜觉继续。</div>
            <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
              <span style={{ padding: "8px 16px", borderRadius: 16, background: "rgba(255,255,255,.1)", fontSize: 13, fontWeight: 800 }}>改一下</span>
              <span style={{ padding: "8px 16px", borderRadius: 16, background: "rgba(255,255,255,.06)", fontSize: 13, fontWeight: 800, color: night.muted }}>撤销</span>
            </div>
          </div>
        </div>

        <div style={{ alignSelf: "flex-start", display: "flex", gap: 10, maxWidth: "92%", alignItems: "flex-end" }}>
          <div style={{ flex: "none", marginBottom: 4 }}><TinyLamp glow small /></div>
          <div style={{ padding: "14px 16px", borderRadius: "6px 22px 22px 22px", background: "rgba(255,255,255,.06)", color: "#E6E4DC" }}>
            这周第三次 2 点半左右醒，次数没变，但她接觉更快了（16 分 vs 上周约 30 分）。
            <span style={{ color: night.periwinkle }}>现在不用做什么，先睡。</span>我在这儿，早上再一起看。
          </div>
        </div>

        <div style={{ alignSelf: "flex-end", maxWidth: "80%", padding: "12px 16px", borderRadius: "22px 22px 6px 22px", background: night.userBubble }}>
          好 早上见
        </div>
      </div>

      {/* Composer + tab bar */}
      <div style={{ paddingBottom: 14 }}>
        <div style={{ display: "flex", gap: 8, marginBottom: 12, overflow: "hidden" }}>
          {SUGGESTIONS.map((s) => (
            <span key={s} style={{ padding: "8px 14px", borderRadius: 16, border: "1px solid rgba(255,255,255,.14)", fontSize: 13, color: night.periwinkle, fontWeight: 700, whiteSpace: "nowrap" }}>
              {s}
            </span>
          ))}
        </div>
        <div style={{ height: 58, borderRadius: 29, background: "rgba(255,255,255,.08)", display: "flex", alignItems: "center", padding: "0 8px 0 20px", justifyContent: "space-between" }}>
          <span style={{ fontSize: 15, color: night.muted, fontWeight: 700 }}>跟知眠说…</span>
          <span style={{ width: 42, height: 42, borderRadius: 21, background: night.gold, display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, color: night.onGoldText }}>↑</span>
        </div>
        <div style={{ marginTop: 12 }}>
          <TabBar active="chat" onChange={app.setTab} dark />
        </div>
      </div>
    </div>
  );
}

/** Tiny lamp used as the night chat avatar (cap 22×12). */
function TinyLamp({ glow = false, small = false }: { glow?: boolean; small?: boolean }) {
  const w = small ? 22 : 44;
  const capH = small ? 12 : 24;
  return (
    <div style={{ width: w, display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div
        style={{
          width: w,
          height: capH,
          borderRadius: small ? "12px 12px 3px 3px" : "24px 24px 5px 5px",
          background: "radial-gradient(circle at 50% 30%,#F7DFA3,#D9A94E 70%)",
          boxShadow: glow ? "0 0 20px rgba(240,195,106,.3)" : "none",
          animation: "lsBreathe 4s ease-in-out infinite",
        }}
      />
      <div style={{ width: small ? 8 : 16, height: small ? 9 : 18, borderRadius: "0 0 3px 3px", background: "#2B3A66", marginTop: -1 }} />
    </div>
  );
}
