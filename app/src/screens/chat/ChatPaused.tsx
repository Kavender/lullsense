import { day, font } from "../../theme/tokens";
import { useApp } from "../../state/store";

/**
 * D3 聊知眠 · 安全暂停 — the safety classifier fired (fever + lethargy). The
 * assistant stops treating it as a sleep problem, routes to care, keeps logging,
 * and excludes the symptoms from long-term memory. Amber mascot.
 */
export function ChatPaused() {
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
        padding: "62px 18px 0",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ width: 48, display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ width: 44, height: 24, borderRadius: "24px 24px 5px 5px", background: day.amber }} />
          <div style={{ width: 16, height: 18, borderRadius: "0 0 6px 6px", background: day.lampStem, marginTop: -1 }} />
        </div>
        <div style={{ lineHeight: 1.15 }}>
          <div style={{ fontSize: 20, fontWeight: 800 }}>知眠</div>
          <div style={{ fontSize: 13, fontWeight: 700, color: day.amberText }}>睡眠优化已暂停 · 先照顾好她</div>
        </div>
      </div>

      <div style={{ marginTop: 14, padding: "14px 16px", borderRadius: 20, background: day.amberTint, fontSize: 13, fontWeight: 700, color: "#6B4A2A", lineHeight: 1.5 }}>
        暂停期间：首页不显示下一觉预测，准备提醒已取消，正在尝试的调整计划已搁置。确认情况稳定后可以在这里恢复。
      </div>

      {/* Messages */}
      <div style={{ flex: 1, minHeight: 0, overflowY: "auto", marginTop: 18, display: "flex", flexDirection: "column", gap: 12, fontSize: 15, lineHeight: 1.5, fontWeight: 600 }}>
        <div style={{ alignSelf: "flex-end", maxWidth: "82%", padding: "12px 16px", borderRadius: "22px 22px 6px 22px", background: day.navy, color: "#fff" }}>
          她今天特别蔫 睡了三小时还叫不太醒 额头有点烫 是不是并觉了
        </div>
        <div style={{ alignSelf: "flex-start", maxWidth: "92%", padding: "14px 16px", borderRadius: "6px 22px 22px 22px", background: "#fff", border: `1.5px solid ${day.amber}` }}>
          <div style={{ fontWeight: 800, color: day.amberText }}>这个先不当睡眠问题看。</div>
          <div style={{ marginTop: 6 }}>
            "叫不太醒"加上发热，对 7 个月的宝宝来说值得现在就联系儿科医生或护士热线，而不是等观察。我不能判断原因，也不会去猜。
          </div>
          <div style={{ marginTop: 10, display: "flex", flexDirection: "column", gap: 8 }}>
            <span style={{ padding: "12px 16px", borderRadius: 16, background: day.navy, color: "#fff", fontSize: 14, fontWeight: 800, textAlign: "center" }}>拨打儿科 / 护士热线</span>
            <span style={{ padding: "12px 16px", borderRadius: 16, background: day.amberTint, fontSize: 14, fontWeight: 800, textAlign: "center", color: "#6B4A2A" }}>现在需要注意什么</span>
          </div>
        </div>
        <div style={{ alignSelf: "flex-start", maxWidth: "92%", padding: "14px 16px", borderRadius: "6px 22px 22px 22px", background: "#fff" }}>
          记录我照常帮你记（刚才那觉 10:40–13:45 已记下），作息的事等她好了我们再聊。这段对话里的症状不会存进长期记忆。
        </div>
      </div>

      {/* Composer + tab bar */}
      <div style={{ paddingBottom: 14 }}>
        <div style={{ height: 58, borderRadius: 29, background: "#fff", display: "flex", alignItems: "center", padding: "0 8px 0 20px", justifyContent: "space-between" }}>
          <span style={{ fontSize: 15, color: day.periwinkle, fontWeight: 700 }}>跟知眠说…</span>
          <span style={{ width: 42, height: 42, borderRadius: 21, background: day.amber, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800 }}>↑</span>
        </div>
        {/* Amber-tinted tab bar (README D3) */}
        <div style={{ marginTop: 12, height: 64, borderRadius: 32, background: "#fff", display: "flex", alignItems: "center", justifyContent: "space-around", fontSize: 14, fontWeight: 800 }}>
          <button onClick={() => app.setTab("today")} style={{ display: "flex", alignItems: "center", gap: 8, color: day.periwinkle, padding: "10px 20px" }}>
            <span style={{ width: 16, height: 16, borderRadius: 8, border: `3px solid ${day.periwinkle}`, display: "block", boxSizing: "border-box" }} />
            今天
          </button>
          <div style={{ display: "flex", alignItems: "center", gap: 8, color: day.navy, background: day.amberTint, padding: "10px 20px", borderRadius: 22 }}>
            <span style={{ width: 16, height: 16, borderRadius: 8, background: day.amber, display: "block" }} />
            聊知眠
          </div>
        </div>
      </div>
    </div>
  );
}
