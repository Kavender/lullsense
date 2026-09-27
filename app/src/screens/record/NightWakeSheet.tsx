import { font, night, radius } from "../../theme/tokens";
import { nowHHMM } from "../../state/store";

/**
 * C3 夜间「醒了」二选一 — pops up from B3's 醒了. 夜里醒了 records a night wake
 * and keeps the night sleep running; 起床了 ends it and starts the new day.
 */
export function NightWakeSheet({
  now,
  onCancel,
  onNightWake,
  onGetUp,
}: {
  now: number;
  onCancel: () => void;
  onNightWake: () => void;
  onGetUp: () => void;
}) {
  return (
    <div style={{ position: "absolute", inset: 0, zIndex: 65, display: "flex", flexDirection: "column", justifyContent: "flex-end" }}>
      <div onClick={onCancel} style={{ position: "absolute", inset: 0, background: "#070C1B", animation: "lsFadeIn .2s ease-out" }} />
      {/* Faded context behind the sheet */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, padding: "62px 20px 0", opacity: 0.35, color: night.ink, fontFamily: font.family }}>
        <div style={{ fontSize: 17, fontWeight: 800 }}>小满</div>
        <div style={{ marginTop: 80, fontSize: 46, fontWeight: 800 }}>7h 05m</div>
      </div>

      <div
        style={{
          position: "relative",
          background: night.sheet,
          borderRadius: `${radius.sheetTop}px ${radius.sheetTop}px 0 0`,
          padding: "12px 22px 40px",
          borderTop: "1px solid rgba(240,195,106,.2)",
          fontFamily: font.family,
          color: night.ink,
          animation: "lsSheetUp .28s cubic-bezier(.2,.8,.2,1)",
        }}
      >
        <div style={{ width: 40, height: 5, borderRadius: 3, background: "rgba(255,255,255,.2)", margin: "0 auto" }} />
        <div style={{ marginTop: 20, fontSize: 22, fontWeight: 800, textAlign: "center" }}>{nowHHMM(now)} · 她是？</div>
        <div style={{ marginTop: 18, display: "flex", flexDirection: "column", gap: 10 }}>
          <OptionRow title="夜里醒了" sub="记一次夜醒，夜觉继续计时，再睡着时按「睡着了」" onClick={onNightWake} />
          <OptionRow title="起床了" sub="结束夜觉，开始新的一天并计算第一觉" onClick={onGetUp} />
        </div>
        <div style={{ marginTop: 14, fontSize: 12, fontWeight: 700, color: night.muted, textAlign: "center" }}>
          06:00 后按「醒了」默认为起床，可改
        </div>
        <button onClick={onCancel} style={{ marginTop: 14, width: "100%", textAlign: "center", fontSize: 15, fontWeight: 800, color: night.muted }}>
          取消
        </button>
      </div>
    </div>
  );
}

function OptionRow({ title, sub, onClick }: { title: string; sub: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "18px 20px",
        borderRadius: 24,
        background: "rgba(255,255,255,.08)",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        textAlign: "left",
        gap: 12,
      }}
    >
      <div>
        <div style={{ fontSize: 18, fontWeight: 800, color: night.ink }}>{title}</div>
        <div style={{ marginTop: 2, fontSize: 13, fontWeight: 600, color: night.periwinkle }}>{sub}</div>
      </div>
      <span style={{ color: night.gold, fontSize: 20 }}>›</span>
    </button>
  );
}
