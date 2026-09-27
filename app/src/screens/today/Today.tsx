import type { CSSProperties } from "react";
import { day, font, radius, shadow } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";
import { TabBar } from "../../components/TabBar";
import { fmtElapsed, useApp, type SleepEvent } from "../../state/store";
import { TodayNight } from "./TodayNight";
import { TodayFirstDay } from "./TodayFirstDay";
import { TodayPaused } from "./TodayPaused";

/**
 * B 今天 — the home tab. Dispatches to the right state:
 * B5 安全暂停 (paused) · B3 夜间 (night theme) · B4 数据不足 (first day) ·
 * else the live day screen (B1 已醒 ↔ B2 小觉进行中).
 */
export function Today({ now }: { now: number }) {
  const app = useApp();
  if (app.optimizationPaused) return <TodayPaused />;
  if (app.theme === "night") return <TodayNight now={now} />;
  if (app.firstDay) return <TodayFirstDay />;
  return <TodayDay now={now} />;
}

function TodayDay({ now }: { now: number }) {
  const app = useApp();
  const napping = app.statusKind === "napping";
  const elapsed = fmtElapsed(app.statusSince, now);

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
        padding: "62px 20px 0",
        overflow: "hidden",
      }}
    >
      <Header
        baby={app.baby}
        onGear={() => app.openOverlay("settings")}
        onName={() => app.openOverlay("babySwitcher")}
      />

      {napping ? <NapCard elapsed={elapsed} napIndex={app.napIndex} /> : <AwakeCard elapsed={elapsed} />}

      <ActionRow napping={napping} onAsleep={app.markAsleep} onAwake={app.markAwake} onBackfill={app.openSheet} />

      {!napping && <NightRingCard onReview={() => app.openOverlay("review")} />}

      <TimelineHeader />
      <TimelineBar napping={napping} />
      <EventList events={app.log} />

      <div style={{ marginTop: "auto" }}>
        <TabBar active="today" onChange={app.setTab} />
      </div>
    </div>
  );
}

function Header({
  baby,
  onGear,
  onName,
}: {
  baby: { initial: string; name: string; ageLabel: string };
  onGear: () => void;
  onName: () => void;
}) {
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
      <button onClick={onName} style={{ display: "flex", alignItems: "center", gap: 10, textAlign: "left" }}>
        <span
          style={{
            width: 40,
            height: 40,
            borderRadius: 20,
            background: day.navy,
            color: "#fff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 16,
            fontWeight: 800,
          }}
        >
          {baby.initial}
        </span>
        <div style={{ lineHeight: 1.1 }}>
          <div style={{ fontSize: 17, fontWeight: 800, color: day.ink }}>
            {baby.name} <span style={{ fontSize: 12, color: day.periwinkle }}>▾</span>
          </div>
          <div style={{ fontSize: 13, color: day.periwinkle, fontWeight: 700 }}>{baby.ageLabel}</div>
        </div>
      </button>
      <button
        onClick={onGear}
        style={{
          width: 40,
          height: 40,
          borderRadius: 20,
          background: "rgba(255,255,255,.7)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 14,
          color: day.periwinkle,
        }}
      >
        ⚙
      </button>
    </div>
  );
}

function AwakeCard({ elapsed }: { elapsed: string }) {
  return (
    <div
      style={{
        marginTop: 22,
        background: day.card,
        borderRadius: radius.pageCard,
        padding: "22px 22px 20px",
        boxShadow: shadow.card,
      }}
    >
      <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: 14, fontWeight: 800, color: day.periwinkle, letterSpacing: ".04em" }}>已醒 · AWAKE</div>
          <div style={{ marginTop: 2, fontSize: 46, fontWeight: 800, lineHeight: 1.05, letterSpacing: "-.02em", whiteSpace: "nowrap" }}>
            {elapsed}
          </div>
          <div style={{ marginTop: 4, fontSize: 15, fontWeight: 700, color: day.periwinkle }}>
            10:15 起床 · 夜觉 11h 23m · 醒 2 次
          </div>
        </div>
        <div style={{ flex: "none", paddingTop: 6 }}>
          <Mascot size="md" state="day" />
        </div>
      </div>
      <PredictionCard />
    </div>
  );
}

function PredictionCard() {
  return (
    <div style={{ marginTop: 14, padding: 16, borderRadius: radius.innerCard, background: day.goldTint }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <div style={{ fontSize: 13, fontWeight: 800, color: day.goldText }}>第二觉 SECOND NAP</div>
        <div style={{ fontSize: 12, fontWeight: 800, color: day.goldText }}>依据 ›</div>
      </div>
      <div style={{ marginTop: 2, fontSize: 28, fontWeight: 800, letterSpacing: "-.02em" }}>13:15 – 13:55</div>
      <div style={{ marginTop: 4, fontSize: 13, fontWeight: 600, color: day.goldTintText, lineHeight: 1.5 }}>
        按最近同类时段估的清醒时长，宝宝困意优先 · <b>12:45 提醒</b> 已设，可改
      </div>
    </div>
  );
}

function NapCard({ elapsed, napIndex }: { elapsed: string; napIndex: number }) {
  return (
    <div
      style={{
        marginTop: 22,
        background: day.navy,
        color: "#fff",
        borderRadius: radius.pageCard,
        padding: "22px 22px 20px",
        boxShadow: shadow.navyCard,
      }}
    >
      <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: 14, fontWeight: 800, color: day.periwinklePale, letterSpacing: ".04em" }}>
            正在睡 · NAP {napIndex}
          </div>
          <div style={{ marginTop: 2, fontSize: 46, fontWeight: 800, lineHeight: 1.05, letterSpacing: "-.02em", whiteSpace: "nowrap" }}>
            {elapsed}
          </div>
          <div style={{ marginTop: 4, fontSize: 15, fontWeight: 700, color: day.periwinklePale }}>
            刚刚睡着 · 醒来记录后再算今晚入睡窗口
          </div>
        </div>
        <div style={{ flex: "none", paddingTop: 6 }}>
          <Mascot size="md" state="nap" />
        </div>
      </div>
      <div
        style={{
          marginTop: 14,
          padding: "14px 16px",
          borderRadius: radius.innerCard,
          background: "rgba(255,255,255,.1)",
          fontSize: 13,
          fontWeight: 600,
          color: "#DCE2F0",
          lineHeight: 1.5,
        }}
      >
        12:45 的准备提醒已取消。醒来记录后再算今晚入睡窗口。
      </div>
    </div>
  );
}

function ActionRow({
  napping,
  onAsleep,
  onAwake,
  onBackfill,
}: {
  napping: boolean;
  onAsleep: () => void;
  onAwake: () => void;
  onBackfill: () => void;
}) {
  return (
    <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
      {napping ? (
        <>
          <button
            onClick={onAwake}
            style={{
              flex: 1,
              height: 64,
              borderRadius: radius.pageCard,
              background: day.gold,
              color: day.ink,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 19,
              fontWeight: 800,
              boxShadow: shadow.goldButton,
            }}
          >
            醒了
          </button>
          <button style={secondaryPill}>改开始时间</button>
        </>
      ) : (
        <>
          <button
            onClick={onAsleep}
            style={{
              flex: 1,
              height: 64,
              borderRadius: radius.pageCard,
              background: day.navy,
              color: "#fff",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 19,
              fontWeight: 800,
              boxShadow: shadow.primaryButton,
            }}
          >
            睡着了
          </button>
          <button onClick={onBackfill} style={secondaryPill}>
            补记
          </button>
        </>
      )}
    </div>
  );
}

const secondaryPill: CSSProperties = {
  height: 64,
  padding: "0 22px",
  borderRadius: radius.pageCard,
  background: day.card,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 16,
  fontWeight: 800,
  color: day.navy,
};

function NightRingCard({ onReview }: { onReview: () => void }) {
  return (
    <div
      style={{
        marginTop: 14,
        background: day.card,
        borderRadius: 28,
        padding: "16px 18px",
        boxShadow: shadow.cardLighter,
        display: "flex",
        gap: 16,
        alignItems: "center",
      }}
    >
      <div
        style={{
          flex: "none",
          width: 104,
          height: 104,
          borderRadius: 52,
          background: "conic-gradient(#E8EEF9 0 200deg,#FFC862 200deg 260deg,#E8EEF9 260deg 360deg)",
          position: "relative",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: 52,
            background: "conic-gradient(#2B4A8A 0 235deg,transparent 235deg 360deg)",
            WebkitMask: "radial-gradient(circle,transparent 42px,#000 43px)",
            mask: "radial-gradient(circle,transparent 42px,#000 43px)",
          }}
        />
        <div
          style={{
            width: 78,
            height: 78,
            borderRadius: 39,
            background: "#fff",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
          }}
        >
          <div style={{ fontSize: 19, fontWeight: 800, lineHeight: 1, whiteSpace: "nowrap" }}>11h 23m</div>
          <div style={{ fontSize: 10, fontWeight: 700, color: day.periwinkle, marginTop: 2 }}>昨晚夜觉</div>
        </div>
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <span style={{ fontSize: 12, fontWeight: 800, color: day.periwinkle, letterSpacing: ".06em" }}>昨晚 · 9月24日</span>
          <button onClick={onReview} style={{ fontSize: 12, fontWeight: 800, color: day.navy }}>回看 ›</button>
        </div>
        <div style={{ marginTop: 4, fontSize: 16, fontWeight: 800, lineHeight: 1.3 }}>在她的常态区间偏上</div>
        <div style={{ marginTop: 4, fontSize: 12, fontWeight: 600, color: "#4A5570", lineHeight: 1.5 }}>
          <span style={{ display: "inline-block", width: 9, height: 9, borderRadius: 5, background: day.gold, verticalAlign: -1, marginRight: 4 }} />
          金色段 = 最近 14 晚常态 10h 20m – 11h 50m
          <br />
          醒 2 次 · 都自己接回去了
        </div>
      </div>
    </div>
  );
}

function TimelineHeader() {
  return (
    <div style={{ marginTop: 18, display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
      <div style={{ fontSize: 15, fontWeight: 800 }}>今天 · 9月25日</div>
      <div style={{ fontSize: 13, fontWeight: 700, color: day.periwinkle }}>‹ 昨天</div>
    </div>
  );
}

function TimelineBar({ napping }: { napping: boolean }) {
  return (
    <div
      style={{
        marginTop: 10,
        position: "relative",
        height: 56,
        borderRadius: 28,
        background: "rgba(255,255,255,.7)",
        overflow: "hidden",
      }}
    >
      {/* night sleep block */}
      <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: "43%", background: day.periwinkle, borderRadius: "28px 0 0 28px" }} />
      {napping ? (
        <div
          style={{
            position: "absolute",
            left: "55.5%",
            top: 0,
            bottom: 0,
            width: "3%",
            background: day.navy,
            borderRadius: 12,
            animation: "lsPulse 2s ease-in-out infinite",
          }}
        />
      ) : (
        <>
          <div style={{ position: "absolute", left: "10%", top: 0, bottom: 0, width: 3, background: day.gold }} />
          <div style={{ position: "absolute", left: "21%", top: 0, bottom: 0, width: 3, background: day.gold }} />
          <div style={{ position: "absolute", left: "47%", top: 0, bottom: 0, width: 2, background: day.ink }} />
        </>
      )}
    </div>
  );
}

function dotColor(e: SleepEvent): string {
  if (e.inProgress) return day.navy;
  switch (e.kind) {
    case "morningWake":
      return day.gold;
    case "nap":
      return day.periwinkleLight;
    default:
      return day.periwinkle;
  }
}

function sourceTag(source: SleepEvent["source"]): { text: string; color: string } | null {
  switch (source) {
    case "button":
      return { text: "按钮", color: day.periwinkle };
    case "chat":
      return { text: "聊天", color: day.goldText };
    case "backfill":
      return { text: "补记", color: day.periwinkle };
    case "notification":
      return { text: "提醒", color: day.periwinkle };
    default:
      return null;
  }
}

function EventList({ events }: { events: SleepEvent[] }) {
  return (
    <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 8, fontSize: 15, fontWeight: 700, overflow: "hidden" }}>
      {events.map((e) => {
        const tag = sourceTag(e.source);
        return (
          <div key={e.id} style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <span style={{ width: 12, height: 12, borderRadius: 6, background: dotColor(e), display: "block", flex: "none" }} />
            <span style={{ width: 48, color: day.periwinkle, flex: "none" }}>{e.time}</span>
            <span style={{ flex: 1, minWidth: 0, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {e.label}
              {e.detail ? ` · ${e.detail}` : ""}
            </span>
            {tag && <span style={{ fontSize: 12, color: tag.color, flex: "none" }}>{tag.text}</span>}
          </div>
        );
      })}
    </div>
  );
}
