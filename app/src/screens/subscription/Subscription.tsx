import { day, font, radius, shadow } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";

/**
 * F1 深度咨询 gate — appears inline in chat when the weekly free consult quota is
 * used and the request needs full history. Logging / prediction / reminders and
 * unlimited safety guidance stay free forever. Never says "整个 App 免费".
 */
export function Subscription({ onClose }: { onClose: () => void }) {
  return (
    <div style={{ ...screen, animation: "lsFadeIn .2s ease-out" }}>
      {/* Chat header (this appears inline in the chat) */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ width: 48, display: "flex", justifyContent: "center" }}>
          <Mascot size="sm" state="day" />
        </div>
        <div style={{ lineHeight: 1.15 }}>
          <div style={{ fontSize: 20, fontWeight: 800 }}>知眠</div>
          <div style={{ fontSize: 13, fontWeight: 700, color: day.periwinkle }}>记得小满 ›</div>
        </div>
      </div>

      <div style={{ marginTop: 22, display: "flex", flexDirection: "column", gap: 12, fontSize: 15, lineHeight: 1.5, fontWeight: 600 }}>
        <div style={{ alignSelf: "flex-end", maxWidth: "80%", padding: "12px 16px", borderRadius: "22px 22px 6px 22px", background: day.navy, color: "#fff" }}>
          最近两周怎么样 早醒有没有好一点
        </div>
        <div style={{ alignSelf: "flex-start", maxWidth: "92%", padding: "14px 16px", borderRadius: "6px 22px 22px 22px", background: "#fff", boxShadow: shadow.cardLight }}>
          这需要把两周的记录一起看。本周的免费咨询轮次用完了，这类完整历史的复盘属于深度咨询。
        </div>
      </div>

      <div style={{ marginTop: 16, background: "#fff", borderRadius: radius.pageCard, padding: 22, boxShadow: shadow.card }}>
        <div style={{ fontSize: 12, fontWeight: 800, color: day.goldText, letterSpacing: ".08em" }}>深度咨询</div>
        <div style={{ marginTop: 4, fontSize: 34, fontWeight: 800, letterSpacing: "-.02em" }}>
          $3.99<span style={{ fontSize: 15, color: day.periwinkle, fontWeight: 700 }}> / 月</span>
        </div>
        <div style={{ marginTop: 10, fontSize: 14, fontWeight: 600, color: "#4A5570", lineHeight: 1.6 }}>
          · 结合完整历史的分析与复盘
          <br />· "最近怎么样"、基线与变化解读
          <br />· 调整计划的建立、跟踪、复盘
          <br />
          <span style={{ color: day.periwinkle }}>配公平使用上限 · 随时取消</span>
        </div>
        <div style={{ marginTop: 14, padding: "14px 16px", borderRadius: 18, background: day.goldTint, fontSize: 13, fontWeight: 700, color: day.goldTintText, lineHeight: 1.55 }}>
          不订阅也一直有：按钮记录、时间轴、下一觉预测、提醒、多宝宝、导出、每周几轮咨询，以及<b>永远不限量的安全引导</b>。到期后所有记录、预测、提醒、已接受的计划都保留。
        </div>
        <div style={{ marginTop: 14, height: 58, borderRadius: 29, background: day.navy, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17, fontWeight: 800 }}>
          开始订阅 · App Store 内购
        </div>
        <button onClick={onClose} style={{ marginTop: 8, width: "100%", textAlign: "center", fontSize: 14, fontWeight: 800, color: day.navy }}>
          先不用，问个不用历史的问题
        </button>
      </div>

      <div style={{ marginTop: "auto", paddingBottom: 14, fontSize: 12, fontWeight: 600, color: day.periwinkle, textAlign: "center", lineHeight: 1.5 }}>
        内测家庭：终身折扣将在公开上架前兑现
      </div>
    </div>
  );
}

const screen = {
  position: "absolute" as const,
  inset: 0,
  zIndex: 55,
  fontFamily: font.family,
  boxSizing: "border-box" as const,
  background: day.pageBg,
  color: day.ink,
  display: "flex",
  flexDirection: "column" as const,
  padding: "62px 18px 0",
  overflowY: "auto" as const,
};
