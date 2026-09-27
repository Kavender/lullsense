import { useEffect, useRef, useState } from "react";
import { day, font, shadow } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";
import { TabBar } from "../../components/TabBar";
import { useApp, type ChatMessage } from "../../state/store";

const SUGGESTIONS = ["那第二觉呢", "暂停计划"];

/**
 * D1 聊知眠 (白天) — chat with the assistant, which also logs sleep from natural
 * language. Header remembers family facts; optional plan strip; logged-card
 * bubbles; suggestion chips; composer that also records.
 */
export function Chat() {
  const app = useApp();
  const [draft, setDraft] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [app.messages.length]);

  const send = (text: string) => {
    app.sendMessage(text);
    setDraft("");
  };

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
        padding: "62px 18px 0",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 48, display: "flex", justifyContent: "center" }}>
            <Mascot size="sm" state="day" />
          </div>
          <div style={{ lineHeight: 1.15 }}>
            <div style={{ fontSize: 20, fontWeight: 800 }}>知眠</div>
            <div style={{ fontSize: 13, fontWeight: 700, color: day.periwinkle }}>记得小满 · 托班 12:30、同房、不睡训 ›</div>
          </div>
        </div>
        <button style={{ fontSize: 13, fontWeight: 800, color: day.periwinkle }}>新对话</button>
      </div>

      {/* Plan strip */}
      <div
        style={{
          marginTop: 14,
          padding: "12px 16px",
          borderRadius: 20,
          background: "rgba(255,255,255,.7)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 10,
          fontSize: 13,
          fontWeight: 700,
        }}
      >
        <div>
          <span style={{ color: day.goldText }}>正在尝试 · 第 3/5 天</span>
          <br />
          <span>第一觉提前到 8:45，看早醒是否缓解</span>
        </div>
        <div style={{ color: day.navy, whiteSpace: "nowrap" }}>复盘 ›</div>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        style={{
          flex: 1,
          minHeight: 0,
          overflowY: "auto",
          marginTop: 18,
          display: "flex",
          flexDirection: "column",
          gap: 12,
          fontSize: 15,
          lineHeight: 1.5,
          fontWeight: 600,
        }}
      >
        {app.messages.map((m) => (
          <Bubble key={m.id} message={m} />
        ))}
        <div style={{ alignSelf: "flex-start", display: "flex", gap: 8, flexWrap: "wrap" }}>
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => send(s)}
              style={{
                padding: "9px 16px",
                borderRadius: 18,
                background: day.card,
                border: `2px solid ${day.periTintStrong}`,
                fontSize: 13,
                fontWeight: 800,
                color: day.navy,
              }}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Composer + tab bar */}
      <div style={{ paddingBottom: 14 }}>
        <Composer draft={draft} setDraft={setDraft} onSend={() => send(draft)} />
        <div style={{ marginTop: 12 }}>
          <TabBar active="chat" onChange={app.setTab} />
        </div>
      </div>
    </div>
  );
}

function Bubble({ message }: { message: ChatMessage }) {
  if (message.role === "user") {
    return (
      <div
        style={{
          alignSelf: "flex-end",
          maxWidth: "80%",
          padding: "12px 16px",
          borderRadius: "22px 22px 6px 22px",
          background: day.navy,
          color: "#fff",
        }}
      >
        {message.text}
      </div>
    );
  }

  if (message.logged) {
    return (
      <div
        style={{
          alignSelf: "flex-start",
          maxWidth: "88%",
          padding: "14px 16px",
          borderRadius: "6px 22px 22px 22px",
          background: day.card,
          boxShadow: shadow.cardLight,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              width: 22,
              height: 22,
              borderRadius: 11,
              background: day.gold,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 12,
              fontWeight: 800,
            }}
          >
            ✓
          </span>
          <span style={{ fontWeight: 800 }}>{message.logged.title}</span>
        </div>
        <div style={{ marginTop: 6, color: day.periwinkle, fontSize: 14 }}>{message.logged.detail}</div>
        <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
          <span style={{ padding: "8px 16px", borderRadius: 16, background: day.periTintStrong, fontSize: 13, fontWeight: 800, color: day.navy }}>
            改一下
          </span>
          <span style={{ padding: "8px 16px", borderRadius: 16, background: "#F1F1F1", fontSize: 13, fontWeight: 800, color: day.periwinkle }}>
            撤销
          </span>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        alignSelf: "flex-start",
        maxWidth: "88%",
        padding: "14px 16px",
        borderRadius: "6px 22px 22px 22px",
        background: day.card,
        boxShadow: shadow.cardLight,
      }}
    >
      {message.text}
    </div>
  );
}

function Composer({
  draft,
  setDraft,
  onSend,
}: {
  draft: string;
  setDraft: (s: string) => void;
  onSend: () => void;
}) {
  return (
    <div
      style={{
        height: 58,
        borderRadius: 29,
        background: day.card,
        boxShadow: shadow.tabBar,
        display: "flex",
        alignItems: "center",
        padding: "0 8px 0 20px",
        justifyContent: "space-between",
        gap: 10,
      }}
    >
      <input
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") onSend();
        }}
        placeholder="跟知眠说，或直接记…"
        style={{
          flex: 1,
          minWidth: 0,
          border: "none",
          outline: "none",
          background: "transparent",
          fontSize: 15,
          fontWeight: 700,
          color: day.ink,
          fontFamily: font.family,
        }}
      />
      <button
        onClick={onSend}
        style={{
          width: 42,
          height: 42,
          borderRadius: 21,
          background: day.gold,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontWeight: 800,
          fontSize: 18,
          color: day.ink,
          flex: "none",
        }}
      >
        ↑
      </button>
    </div>
  );
}
