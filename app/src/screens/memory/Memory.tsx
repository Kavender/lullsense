import type { ReactNode } from "react";
import { day, font, radius } from "../../theme/tokens";

/**
 * E1 知眠记得什么 — canonical facts + source + confirmed date; most-recent
 * confirmation wins. Shows what won't be remembered. Pushed from the chat header.
 */
export function Memory({ onBack }: { onBack: () => void }) {
  return (
    <div style={{ ...screen, animation: "lsFadeIn .2s ease-out" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <button onClick={onBack} style={{ fontSize: 15, fontWeight: 800, color: day.navy }}>‹ 聊知眠</button>
        <span style={{ fontSize: 17, fontWeight: 800 }}>知眠记得什么</span>
        <span style={{ width: 52 }} />
      </div>
      <div style={{ marginTop: 16, fontSize: 13, fontWeight: 600, color: day.periwinkle, lineHeight: 1.5 }}>
        这些是知眠在回答时会用到的事实。点任意一条纠正或删除；被你改过的以最新确认为准，旧摘要不会再复活。
      </div>

      <Label>家庭与作息</Label>
      <div style={{ marginTop: 8, background: "#fff", borderRadius: radius.innerCard, padding: "4px 18px" }}>
        <Fact title="托班中午 12:30 安排小觉" meta="你改过 · 9月20日 确认（原“中午”）" metaGold last={false} />
        <Fact title="和父母同房睡" meta="来自聊天 · 9月2日" last={false} />
        <Fact title="不做睡训" meta="首次设置 · 9月1日" last={false} />
        <Fact title="外婆周三、周五白天带" meta="来自聊天 · 9月14日" last />
      </div>

      <Label>正在尝试</Label>
      <div style={{ marginTop: 8, background: "#fff", borderRadius: radius.innerCard, padding: "14px 18px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 15, fontWeight: 800 }}>
          <span>第一觉提前到 8:45</span>
          <span style={{ color: day.goldText }}>第 3/5 天</span>
        </div>
        <div style={{ marginTop: 3, fontSize: 12, fontWeight: 700, color: day.periwinkle }}>
          你接受于 9月23日 · 复盘 9月27日 · <span style={{ color: day.navy }}>暂停</span> · <span style={{ color: day.navy }}>结束</span>
        </div>
      </div>

      <Label>不会记住</Label>
      <div style={{ marginTop: 8, background: "rgba(255,255,255,.6)", borderRadius: radius.innerCard, padding: "14px 18px", fontSize: 13, fontWeight: 600, color: "#4A5570", lineHeight: 1.5 }}>
        未被你接受的建议 · 安全暂停期间提到的症状 · 关闭记忆时段内的对话
      </div>

      <div style={{ marginTop: "auto", paddingBottom: 22, display: "flex", flexDirection: "column", gap: 8 }}>
        <button style={{ height: 52, borderRadius: 26, background: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, fontWeight: 800, color: day.navy }}>
          添加一条知眠应该知道的
        </button>
        <button style={{ height: 52, borderRadius: 26, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, fontWeight: 800, color: day.destructive }}>
          忘掉小满的全部信息
        </button>
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

function Label({ children }: { children: ReactNode }) {
  return <div style={{ marginTop: 18, fontSize: 12, fontWeight: 800, color: day.periwinkle, letterSpacing: ".08em" }}>{children}</div>;
}

function Fact({ title, meta, metaGold = false, last }: { title: string; meta: string; metaGold?: boolean; last: boolean }) {
  return (
    <div style={{ padding: "14px 0", borderBottom: last ? "none" : `1px solid ${day.periTint}` }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 15, fontWeight: 800 }}>
        <span>{title}</span>
        <span style={{ color: day.periwinkle }}>›</span>
      </div>
      <div style={{ marginTop: 3, fontSize: 12, fontWeight: 700, color: metaGold ? day.goldText : day.periwinkle }}>{meta}</div>
    </div>
  );
}
