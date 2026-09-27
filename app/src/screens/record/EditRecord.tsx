import { day, font, radius, shadow } from "../../theme/tokens";

/**
 * C2 编辑记录 — edit a logged sleep. Revisions keep the source; the change
 * recomputes downstream predictions/reminders and is undoable via the toast.
 */
export function EditRecord({ onBack }: { onBack: () => void }) {
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 55,
        fontFamily: font.family,
        boxSizing: "border-box",
        background: day.pageBg,
        color: day.ink,
        display: "flex",
        flexDirection: "column",
        padding: "62px 20px 0",
        animation: "lsFadeIn .2s ease-out",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <button onClick={onBack} style={{ fontSize: 15, fontWeight: 800, color: day.navy }}>‹ 今天</button>
        <span style={{ fontSize: 17, fontWeight: 800 }}>第一觉</span>
        <button onClick={onBack} style={{ fontSize: 15, fontWeight: 800, color: day.navy }}>完成</button>
      </div>

      <div style={{ marginTop: 22, background: "#fff", borderRadius: radius.pageCard, padding: 22, boxShadow: shadow.card }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 800, color: day.periwinkle, letterSpacing: ".06em" }}>
          <span>9 月 25 日 · 小觉</span>
          <span style={{ color: day.goldText }}>来源：聊天</span>
        </div>
        <div style={{ marginTop: 14, display: "flex", gap: 10 }}>
          <div style={{ flex: 1, background: day.periTint, borderRadius: radius.tile, padding: "14px 16px" }}>
            <div style={{ fontSize: 12, fontWeight: 800, color: day.periwinkle }}>睡着</div>
            <div style={{ marginTop: 2, fontSize: 26, fontWeight: 800 }}>09:10</div>
            <div style={{ fontSize: 12, fontWeight: 700, color: day.goldText }}>大约</div>
          </div>
          <div style={{ flex: 1, background: day.periTint, borderRadius: radius.tile, padding: "14px 16px", outline: `2px solid ${day.navy}` }}>
            <div style={{ fontSize: 12, fontWeight: 800, color: day.navy }}>醒来 · 正在改</div>
            <div style={{ marginTop: 2, fontSize: 26, fontWeight: 800 }}>10:20</div>
            <div style={{ fontSize: 12, fontWeight: 700, color: day.periwinkle }}>原 10:00</div>
          </div>
        </div>
        <div
          style={{
            marginTop: 14,
            height: 120,
            borderRadius: radius.tile,
            background: "repeating-linear-gradient(0deg,#F4F6FB 0 1px,#fff 1px 24px)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            font: "600 11px ui-monospace, monospace",
            color: "#8A97BF",
            textAlign: "center",
          }}
        >
          iOS 时间选择器（滚轮）
        </div>
        <div style={{ marginTop: 14, fontSize: 13, fontWeight: 600, color: day.periwinkle, lineHeight: 1.5 }}>
          保存后第二觉预测与 12:45 提醒会重算；原记录保留在修订历史里。
        </div>
      </div>

      <div style={{ marginTop: 14, background: "#fff", borderRadius: radius.innerCard, padding: "6px 18px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", padding: "12px 0", borderBottom: `1px solid ${day.periTint}`, fontSize: 15, fontWeight: 700 }}>
          <span>修订历史</span>
          <span style={{ color: day.periwinkle }}>2 次 ›</span>
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", padding: "12px 0", fontSize: 15, fontWeight: 700, color: day.destructive }}>
          <span>删除这条记录</span>
        </div>
      </div>

      <div style={{ marginTop: "auto", paddingBottom: 22 }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: day.ink, color: "#fff", borderRadius: radius.innerCard, padding: "14px 18px", fontSize: 14, fontWeight: 700, boxShadow: shadow.toast }}>
          <span>
            <span style={{ color: day.gold }}>✓</span> 已改为 10:20 · 提醒已重算
          </span>
          <button onClick={onBack} style={{ color: day.gold, fontWeight: 800 }}>撤销</button>
        </div>
      </div>
    </div>
  );
}
