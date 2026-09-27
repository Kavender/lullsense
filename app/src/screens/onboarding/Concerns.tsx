import { useState } from "react";
import { day, font, radius } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";

const CHIPS = [
  "早醒 · 5 点前",
  "夜醒频繁",
  "小觉短",
  "入睡困难",
  "正在并觉",
  "托班 / 家庭作息冲突",
  "隔代意见不一致",
];
const CALM_CHIP = "还好，先记录看看";

/**
 * A3 当前困扰 (step 2/2, skippable) — multi-select entry point into chat.
 * "知眠会从这里开始聊，而不是让你先记七天。" (README A3)
 */
export function Concerns({ onNext, onSkip }: { onNext: () => void; onSkip: () => void }) {
  const [selected, setSelected] = useState<Set<string>>(new Set(["早醒 · 5 点前", "小觉短"]));
  const toggle = (c: string) =>
    setSelected((s) => {
      const n = new Set(s);
      n.has(c) ? n.delete(c) : n.add(c);
      return n;
    });

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
        <span>2 / 2</span>
        <button onClick={onSkip} style={{ fontSize: 14, fontWeight: 700, color: day.periwinkle }}>
          跳过 ›
        </button>
      </div>
      <div style={{ marginTop: 22, fontSize: 28, fontWeight: 800, lineHeight: 1.25 }}>最近最困扰你的是？</div>
      <div style={{ marginTop: 6, fontSize: 14, fontWeight: 600, color: day.periwinkle, lineHeight: 1.5 }}>
        选几个都行。知眠会从这里开始聊，而不是让你先记七天。
      </div>

      <div style={{ marginTop: 24, display: "flex", flexWrap: "wrap", gap: 10 }}>
        {CHIPS.map((c) => (
          <Chip key={c} label={c} selected={selected.has(c)} onClick={() => toggle(c)} />
        ))}
        <Chip label={CALM_CHIP} selected={selected.has(CALM_CHIP)} calm onClick={() => toggle(CALM_CHIP)} />
      </div>

      <div
        style={{
          marginTop: 28,
          background: day.card,
          borderRadius: radius.innerCard,
          padding: "16px 18px",
          display: "flex",
          gap: 14,
          alignItems: "center",
        }}
      >
        <div style={{ flex: "none" }}>
          <Mascot size="sm" state="day" />
        </div>
        <div style={{ fontSize: 14, fontWeight: 600, color: day.ink, lineHeight: 1.5 }}>
          知眠不睡训、也不推销任何方法；不愿睡训的家庭同样得到完整支持。
        </div>
      </div>

      <div style={{ marginTop: "auto", paddingBottom: 40, display: "flex", flexDirection: "column", gap: 10 }}>
        <button
          onClick={onNext}
          style={{
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
          和知眠聊聊这两件事
        </button>
        <button
          onClick={onNext}
          style={{
            height: 52,
            borderRadius: 26,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 16,
            fontWeight: 800,
            color: day.navy,
          }}
        >
          直接去「今天」记一觉
        </button>
      </div>
    </div>
  );
}

function Chip({
  label,
  selected,
  calm = false,
  onClick,
}: {
  label: string;
  selected: boolean;
  calm?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "14px 18px",
        borderRadius: radius.tile,
        background: selected ? day.navy : day.card,
        color: selected ? "#fff" : calm ? day.periwinkle : day.ink,
        fontSize: 16,
        fontWeight: 800,
      }}
    >
      {label}
    </button>
  );
}
