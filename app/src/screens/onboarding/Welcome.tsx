import { day, font } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";

/**
 * A1 欢迎 — value prop, privacy sentence, Sign in with Apple.
 * Copy is final (README A1).
 */
export function Welcome({ onNext, onSkip }: { onNext: () => void; onSkip: () => void }) {
  void onSkip;
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
        padding: "120px 28px 0",
        textAlign: "center",
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        <Mascot size="lg" state="day" />
      </div>
      <img
        src="/lullsense-logo.png"
        alt="LullSense 知眠"
        style={{ width: 150, margin: "36px auto 0", display: "block" }}
      />
      <div style={{ marginTop: 14, fontSize: 22, fontWeight: 800, lineHeight: 1.35 }}>
        说中文也说英文、记得你宝宝和家庭情况的睡眠助手
      </div>
      <div style={{ marginTop: 12, fontSize: 14, fontWeight: 600, color: day.periwinkle, lineHeight: 1.6 }}>
        按钮记录、预测和提醒完全在你的手机上，不联网也能用。聊天与自然语言记录会把本轮相关内容发送给 AI 模型处理（不用于训练）。
      </div>
      <div style={{ marginTop: "auto", paddingBottom: 40, display: "flex", flexDirection: "column", gap: 12 }}>
        <button
          onClick={onNext}
          style={{
            height: 56,
            borderRadius: 28,
            background: "#000",
            color: "#fff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 8,
            fontSize: 17,
            fontWeight: 700,
            fontFamily: "-apple-system, system-ui",
          }}
        >
           Sign in with Apple
        </button>
        <div style={{ fontSize: 12, color: day.periwinkle, fontWeight: 600, lineHeight: 1.5 }}>
          账号只用于用量与订阅状态。睡眠记录与聊天内容留在你的设备，不进入我们的数据库。
          <br />
          <span style={{ textDecoration: "underline" }}>隐私政策</span> ·{" "}
          <span style={{ textDecoration: "underline" }}>非医疗建议</span>
        </div>
      </div>
    </div>
  );
}
