import { day, font, night, radius } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";
import { TabBar } from "../../components/TabBar";
import { useApp } from "../../state/store";

/**
 * B3 今天 · 夜间 — auto night theme (21:00–06:00). Baby is asleep at night;
 * night wakes don't trigger predictions. 醒了 opens the C3 二选一 sheet.
 */
export function TodayNight({ now }: { now: number }) {
  void now;
  const app = useApp();
  return (
    <div
      style={{
        fontFamily: font.family,
        height: "100%",
        boxSizing: "border-box",
        background: night.pageBg,
        color: night.ink,
        display: "flex",
        flexDirection: "column",
        padding: "62px 20px 0",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <button onClick={() => app.openOverlay("babySwitcher")} style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ width: 40, height: 40, borderRadius: 20, background: night.gold, color: night.onGoldText, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, fontWeight: 800 }}>
            {app.baby.initial}
          </span>
          <div style={{ lineHeight: 1.1, textAlign: "left" }}>
            <div style={{ fontSize: 17, fontWeight: 800, color: night.ink }}>{app.baby.name}</div>
            <div style={{ fontSize: 13, color: night.muted, fontWeight: 700 }}>7 个月 · 夜间</div>
          </div>
        </button>
        <button onClick={() => app.openOverlay("settings")} style={{ width: 40, height: 40, borderRadius: 20, background: night.controlFill, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, color: night.muted }}>
          ⚙
        </button>
      </div>

      {/* Night status card */}
      <div style={{ marginTop: 22, background: night.card, border: night.cardBorder, borderRadius: radius.pageCard, padding: "22px 22px 20px" }}>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 14, fontWeight: 800, color: night.muted, letterSpacing: ".04em" }}>正在睡 · NIGHT</div>
            <div style={{ marginTop: 2, fontSize: 46, fontWeight: 800, lineHeight: 1.05, letterSpacing: "-.02em", whiteSpace: "nowrap" }}>7h 05m</div>
            <div style={{ marginTop: 4, fontSize: 15, fontWeight: 700, color: night.periwinkle }}>19:42 睡着 · 夜醒 1 次</div>
          </div>
          <div style={{ flex: "none", paddingTop: 6 }}>
            <Mascot size="md" state="night" />
          </div>
        </div>
        <div style={{ marginTop: 14, padding: 16, borderRadius: radius.innerCard, background: "rgba(255,255,255,.05)" }}>
          <div style={{ fontSize: 13, fontWeight: 800, color: night.gold }}>仍在夜间 · STILL NIGHT</div>
          <div style={{ marginTop: 4, fontSize: 14, fontWeight: 600, color: night.periwinkle, lineHeight: 1.5 }}>
            晨醒记录后再算第一觉；夜里不推小觉提醒。
          </div>
        </div>
      </div>

      {/* Actions */}
      <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
        <button onClick={() => app.openOverlay("nightWake")} style={{ flex: 1, height: 64, borderRadius: radius.pageCard, background: night.gold, color: night.onGoldText, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 19, fontWeight: 800 }}>
          醒了
        </button>
        <button onClick={app.openSheet} style={{ height: 64, padding: "0 22px", borderRadius: radius.pageCard, background: night.controlFill, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, fontWeight: 800, color: night.periwinkle }}>
          补记
        </button>
      </div>
      <div style={{ marginTop: 12, fontSize: 12, fontWeight: 700, color: night.muted, textAlign: "center" }}>
        按「醒了」后弹出 C3：夜醒 / 起床了 二选一
      </div>

      {/* Timeline */}
      <div style={{ marginTop: 22, display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <div style={{ fontSize: 15, fontWeight: 800 }}>今夜</div>
        <div style={{ fontSize: 13, fontWeight: 700, color: night.muted }}>‹ 昨天</div>
      </div>
      <div style={{ marginTop: 10, position: "relative", height: 56, borderRadius: 28, background: "rgba(255,255,255,.06)", overflow: "hidden" }}>
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: "11%", background: night.periwinkleLight, borderRadius: "28px 0 0 28px" }} />
        <div style={{ position: "absolute", left: "82%", top: 0, bottom: 0, right: 0, background: night.periwinkleLight, borderRadius: "0 28px 28px 0" }} />
        <div style={{ position: "absolute", left: "90%", top: 0, bottom: 0, width: 3, background: night.gold }} />
      </div>
      <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 8, fontSize: 15, fontWeight: 700, color: night.periwinkle }}>
        <NightRow dot={night.gold} time="02:31" text="夜醒 16 分钟" tag="聊天" />
        <NightRow dot={night.periwinkleLight} time="19:42" text="夜觉开始" />
        <NightRow dot={day.periwinkle} time="12:40" text="第二觉 1h 25m" />
      </div>

      <div style={{ marginTop: "auto" }}>
        <TabBar active="today" onChange={app.setTab} dark />
      </div>
    </div>
  );
}

function NightRow({ dot, time, text, tag }: { dot: string; time: string; text: string; tag?: string }) {
  return (
    <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
      <span style={{ width: 12, height: 12, borderRadius: 6, background: dot, display: "block", flex: "none" }} />
      <span style={{ width: 48, color: night.muted, flex: "none" }}>{time}</span>
      <span style={{ flex: 1 }}>{text}</span>
      {tag && <span style={{ fontSize: 12, color: night.gold, flex: "none" }}>{tag}</span>}
    </div>
  );
}
