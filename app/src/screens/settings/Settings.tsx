import { useState, type ReactNode } from "react";
import { day, font, radius } from "../../theme/tokens";
import type { Overlay } from "../../state/store";

/**
 * E2 设置 — baby, reminders, language & appearance, data & account.
 * 数据控制 pushes E3; 订阅 opens the F1 subscription gate.
 */
export function Settings({ onBack, onOpen }: { onBack: () => void; onOpen: (o: Overlay) => void }) {
  const [reminder, setReminder] = useState(true);
  return (
    <div style={{ ...screen, animation: "lsFadeIn .2s ease-out" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <button onClick={onBack} style={{ fontSize: 15, fontWeight: 800, color: day.navy }}>‹ 今天</button>
        <span style={{ fontSize: 17, fontWeight: 800 }}>设置</span>
        <span style={{ width: 40 }} />
      </div>

      <Label>宝宝</Label>
      <Group>
        <Row
          last
          left={
            <span style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span style={{ width: 30, height: 30, borderRadius: 15, background: day.navy, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13 }}>满</span>
              小满 · 7 个月
            </span>
          }
          right={<span style={{ color: day.periwinkle }}>管理 / 添加 ›</span>}
        />
      </Group>

      <Label>提醒</Label>
      <Group>
        <Row left="下一觉准备提醒" right={<Switch on={reminder} onToggle={() => setReminder((v) => !v)} />} />
        <Row left="提前多久" right={<span style={{ color: day.periwinkle }}>30 分钟 ›</span>} />
        <Row last left="夜间静默" right={<span style={{ color: day.periwinkle }}>21:00 – 06:00 ›</span>} />
      </Group>

      <Label>语言与外观</Label>
      <Group>
        <Row left="界面语言" right={<span style={{ color: day.periwinkle }}>中文 ›</span>} />
        <Row left="知眠回复语言" right={<span style={{ color: day.periwinkle }}>跟随我的输入 ›</span>} />
        <Row last left="夜间外观" right={<span style={{ color: day.periwinkle }}>按时段自动 ›</span>} />
      </Group>

      <Label>数据与账号</Label>
      <Group>
        <Row left="数据控制" right={<span style={{ color: day.periwinkle }}>›</span>} onClick={() => onOpen("dataControl")} />
        <Row left="订阅" right={<span style={{ color: day.goldText }}>内测期间免费 ›</span>} onClick={() => onOpen("subscription")} />
        <Row last left="Apple 账号" right={<span style={{ color: day.periwinkle }}>已登录 ›</span>} />
      </Group>

      <div style={{ marginTop: 12, marginBottom: 22, fontSize: 12, fontWeight: 600, color: day.periwinkle, textAlign: "center", lineHeight: 1.5 }}>
        知眠 1.0 (内测) · 非医疗建议 · 隐私政策
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
  padding: "62px 20px 0",
  overflowY: "auto" as const,
};

export function Label({ children }: { children: ReactNode }) {
  return <div style={{ marginTop: 14, fontSize: 12, fontWeight: 800, color: day.periwinkle, letterSpacing: ".08em" }}>{children}</div>;
}

export function Group({ children }: { children: ReactNode }) {
  return <div style={{ marginTop: 8, background: "#fff", borderRadius: radius.innerCard, padding: "4px 18px" }}>{children}</div>;
}

export function Row({
  left,
  right,
  last = false,
  onClick,
}: {
  left: ReactNode;
  right?: ReactNode;
  last?: boolean;
  onClick?: () => void;
}) {
  return (
    <button
      onClick={onClick}
      disabled={!onClick}
      style={{
        width: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "12px 0",
        borderBottom: last ? "none" : `1px solid ${day.periTint}`,
        fontSize: 15,
        fontWeight: 800,
        color: day.ink,
        textAlign: "left",
        cursor: onClick ? "pointer" : "default",
      }}
    >
      <span>{left}</span>
      {right}
    </button>
  );
}

export function Switch({ on, onToggle }: { on: boolean; onToggle: () => void }) {
  return (
    <span
      onClick={(e) => {
        e.stopPropagation();
        onToggle();
      }}
      style={{ width: 52, height: 32, borderRadius: 16, background: on ? day.navy : "#DCE2F0", position: "relative", display: "inline-block", flex: "none" }}
    >
      <span style={{ position: "absolute", left: on ? 23 : 3, top: 3, width: 26, height: 26, borderRadius: 13, background: "#fff", display: "block", transition: "left .15s ease", boxShadow: "0 1px 3px rgba(0,0,0,.2)" }} />
    </span>
  );
}
