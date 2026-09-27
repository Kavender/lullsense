import { useState } from "react";
import { day, font, radius } from "../../theme/tokens";
import { Group, Label, Row, Switch } from "./Settings";

/**
 * E3 数据控制 — two independent switches; delete shows the full scope with real
 * counts before confirming. Mirrors the DATA_HANDLING wording (on-device vs
 * server vs sent-to-model). Never says "整个 App 免费" or "零留存".
 */
export function DataControl({ onBack }: { onBack: () => void }) {
  const [saveLog, setSaveLog] = useState(true);
  const [chatMemory, setChatMemory] = useState(true);

  return (
    <div style={{ ...screen, animation: "lsFadeIn .2s ease-out" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <button onClick={onBack} style={{ fontSize: 15, fontWeight: 800, color: day.navy }}>‹ 设置</button>
        <span style={{ fontSize: 17, fontWeight: 800 }}>数据控制</span>
        <span style={{ width: 40 }} />
      </div>

      <div style={{ marginTop: 14, background: "#fff", borderRadius: radius.innerCard, padding: "14px 18px", fontSize: 13, fontWeight: 600, color: "#4A5570", lineHeight: 1.5 }}>
        <b style={{ color: day.ink }}>在你手机上：</b>睡眠记录、时间轴、预测、提醒、宝宝资料、聊天记忆。纳入 iCloud 备份（你自己的云）。
        <br />
        <b style={{ color: day.ink }}>在我们服务器上：</b>只有 Apple 账号 ID、用量计数、订阅状态。
        <br />
        <b style={{ color: day.ink }}>发给 AI 模型的：</b>聊天与自然语言记录的本轮相关内容，不用于训练。
      </div>

      <Label>开关</Label>
      <Group>
        <Row
          left={
            <span>
              <div style={{ fontSize: 15, fontWeight: 800 }}>记录保存</div>
              <div style={{ fontSize: 12, fontWeight: 600, color: day.periwinkle }}>关闭后按钮仍可计时，但不写入历史</div>
            </span>
          }
          right={<Switch on={saveLog} onToggle={() => setSaveLog((v) => !v)} />}
        />
        <Row
          last
          left={
            <span>
              <div style={{ fontSize: 15, fontWeight: 800 }}>聊天长期记忆</div>
              <div style={{ fontSize: 12, fontWeight: 600, color: day.periwinkle }}>关闭期间的对话不会进入“知眠记得什么”</div>
            </span>
          }
          right={<Switch on={chatMemory} onToggle={() => setChatMemory((v) => !v)} />}
        />
      </Group>

      <Label>导出与删除</Label>
      <Group>
        <Row left="导出小满的记录（JSON）" right={<span style={{ color: day.periwinkle }}>分享 ›</span>} />
        <Row last left={<span style={{ color: day.destructive }}>删除小满的全部数据</span>} />
      </Group>

      <div style={{ marginTop: 12, marginBottom: 22, background: day.ink, color: "#fff", borderRadius: 28, padding: "16px 20px", boxShadow: "0 14px 40px rgba(34,51,92,.35)" }}>
        <div style={{ fontSize: 17, fontWeight: 800 }}>删除会覆盖这些：</div>
        <div style={{ marginTop: 6, fontSize: 13, fontWeight: 600, color: "#DCE2F0", lineHeight: 1.5 }}>
          · 手机上 128 条睡眠记录与修订历史
          <br />· 预测缓存与 1 个待发提醒
          <br />· 聊天记忆里的 6 条事实与 1 个进行中计划
          <br />· 服务端临时日志（若有）
          <br />iCloud 备份中的旧副本需你在 iOS 设置里另行处理。
        </div>
        <div style={{ marginTop: 12, display: "flex", gap: 10 }}>
          <span style={{ flex: 1, height: 48, borderRadius: 24, background: "rgba(255,255,255,.12)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, fontWeight: 800 }}>先导出</span>
          <span style={{ flex: 1, height: 48, borderRadius: 24, background: day.destructiveSoft, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, fontWeight: 800 }}>确认删除</span>
        </div>
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
