import { useState, type ReactNode } from "react";
import { day, font, radius } from "../../theme/tokens";

/**
 * A2 宝宝资料 (step 1/2) — only asks for the three things that change current
 * support: name, birthday/age, corrected-age toggle, timezone (README A2).
 */
export function BabyProfile({ onNext, onSkip }: { onNext: () => void; onSkip: () => void }) {
  const [preterm, setPreterm] = useState(false);

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
        padding: "70px 22px 0",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 14, fontWeight: 700, color: day.periwinkle }}>
        <span>1 / 2</span>
        <button onClick={onSkip} style={{ fontSize: 14, fontWeight: 700, color: day.periwinkle }}>
          先聊聊，稍后再填 ›
        </button>
      </div>
      <div style={{ marginTop: 22, fontSize: 28, fontWeight: 800, lineHeight: 1.25 }}>先认识一下宝宝</div>
      <div style={{ marginTop: 6, fontSize: 14, fontWeight: 600, color: day.periwinkle, lineHeight: 1.5 }}>
        只问会改变当前支持的三件事。托班、觉数、偏好等用到时再补。
      </div>

      <div style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 12 }}>
        <Field label="怎么叫 TA">
          <div style={{ marginTop: 4, fontSize: 20, fontWeight: 800 }}>小满</div>
        </Field>

        <Field
          label="生日 或 大致月龄"
          trailing={<span style={{ fontSize: 12, fontWeight: 800, color: day.navy }}>改成填月龄</span>}
        >
          <div style={{ marginTop: 4, fontSize: 20, fontWeight: 800 }}>
            2026 年 2 月 18 日 <span style={{ fontSize: 14, color: day.periwinkle }}>· 7 个月 1 周</span>
          </div>
        </Field>

        <div
          style={{
            background: day.card,
            borderRadius: radius.innerCard,
            padding: "16px 18px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <div style={{ fontSize: 15, fontWeight: 800 }}>早产，按矫正月龄</div>
            <div style={{ marginTop: 2, fontSize: 13, fontWeight: 600, color: day.periwinkle }}>
              37 周前出生的宝宝建议打开
            </div>
          </div>
          <Switch on={preterm} onToggle={() => setPreterm((v) => !v)} />
        </div>

        <Field label="时区">
          <div style={{ marginTop: 4, display: "flex", justifyContent: "space-between", fontSize: 17, fontWeight: 800 }}>
            <span>America/Los_Angeles</span>
            <span style={{ color: day.periwinkle, fontSize: 13, fontWeight: 700 }}>跟随手机 ✓</span>
          </div>
        </Field>
      </div>

      <div
        style={{
          marginTop: 18,
          padding: "14px 16px",
          borderRadius: 18,
          background: day.goldTint,
          fontSize: 13,
          fontWeight: 600,
          color: day.goldTintText,
          lineHeight: 1.5,
        }}
      >
        0–4 个月：可以记录、回看和安全睡眠支持，暂不开放预测与作息优化。
      </div>

      <div style={{ marginTop: "auto", paddingBottom: 40 }}>
        <button
          onClick={onNext}
          style={{
            width: "100%",
            height: 60,
            borderRadius: 30,
            background: day.navy,
            color: "#fff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 18,
            fontWeight: 800,
          }}
        >
          下一步
        </button>
      </div>
    </div>
  );
}

function Field({
  label,
  trailing,
  children,
}: {
  label: string;
  trailing?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div style={{ background: day.card, borderRadius: radius.innerCard, padding: "16px 18px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <div style={{ fontSize: 12, fontWeight: 800, color: day.periwinkle, letterSpacing: ".06em" }}>{label}</div>
        {trailing}
      </div>
      {children}
    </div>
  );
}

function Switch({ on, onToggle }: { on: boolean; onToggle: () => void }) {
  return (
    <button
      onClick={onToggle}
      style={{
        width: 52,
        height: 32,
        borderRadius: 16,
        background: on ? day.navy : "#DCE2F0",
        position: "relative",
        transition: "background .15s ease",
      }}
      aria-pressed={on}
    >
      <span
        style={{
          position: "absolute",
          left: on ? 23 : 3,
          top: 3,
          width: 26,
          height: 26,
          borderRadius: 13,
          background: "#fff",
          display: "block",
          transition: "left .15s ease",
          boxShadow: "0 1px 3px rgba(0,0,0,.2)",
        }}
      />
    </button>
  );
}
