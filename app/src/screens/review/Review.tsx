import { useState } from "react";
import { day, font, radius, shadow } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";

type Seg = "night" | "nap" | "twoweek";

/**
 * H 回看 — pushed from 今天. Segmented 昨晚 / 小觉 / 两周. All insights/trends are
 * computed locally by rules against the baby's own 14-day medians; no AI call.
 * Only the parent's logged times are drawn — no sleep-staging, no scoring.
 */
export function Review({ onBack, onConsult }: { onBack: () => void; onConsult: () => void }) {
  const [seg, setSeg] = useState<Seg>("night");
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 55,
        fontFamily: font.family,
        boxSizing: "border-box",
        background: day.pageBg,
        color: day.ink,
        display: "flex",
        flexDirection: "column",
        padding: "62px 20px 0",
        overflowY: "auto",
        animation: "lsFadeIn .2s ease-out",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <button onClick={onBack} style={{ fontSize: 15, fontWeight: 800, color: day.navy }}>‹ 今天</button>
        <span style={{ fontSize: 17, fontWeight: 800 }}>回看</span>
        <span style={{ fontSize: 15, fontWeight: 800, color: day.periwinkle }}>小满 ▾</span>
      </div>

      <div style={{ marginTop: 20, display: "flex", background: "#fff", borderRadius: 20, padding: 4, fontSize: 15, fontWeight: 800 }}>
        {(["night", "nap", "twoweek"] as Seg[]).map((s) => {
          const label = s === "night" ? "昨晚" : s === "nap" ? "小觉" : "两周";
          const active = s === seg;
          return (
            <button
              key={s}
              onClick={() => setSeg(s)}
              style={{ flex: 1, padding: "12px 0", borderRadius: 16, textAlign: "center", background: active ? day.navy : "transparent", color: active ? "#fff" : day.periwinkle }}
            >
              {label}
            </button>
          );
        })}
      </div>

      <div style={{ paddingBottom: 24 }}>
        {seg === "night" && <LastNight onConsult={onConsult} />}
        {seg === "nap" && <Naps />}
        {seg === "twoweek" && <TwoWeeks onConsult={onConsult} />}
      </div>
    </div>
  );
}

/* ── H1 昨晚 ─────────────────────────────────────────────────────────────── */
function LastNight({ onConsult }: { onConsult: () => void }) {
  return (
    <>
      <div style={{ marginTop: 18, background: "#fff", borderRadius: radius.pageCard, padding: 22, boxShadow: shadow.card }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 13, fontWeight: 800, color: day.periwinkle }}>‹ 9月24日 晚</span>
          <span style={{ fontSize: 13, fontWeight: 800, color: day.periwinklePale }}>›</span>
        </div>
        <div style={{ marginTop: 14, display: "flex", gap: 18, alignItems: "center" }}>
          <div style={{ flex: "none", width: 132, height: 132, borderRadius: 66, background: "conic-gradient(#E8EEF9 0 200deg,#FFC862 200deg 260deg,#E8EEF9 260deg 360deg)", position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div style={{ position: "absolute", inset: 0, borderRadius: 66, background: "conic-gradient(#2B4A8A 0 235deg,transparent 235deg 360deg)", WebkitMask: "radial-gradient(circle,transparent 54px,#000 55px)", mask: "radial-gradient(circle,transparent 54px,#000 55px)" }} />
            <div style={{ width: 100, height: 100, borderRadius: 50, background: "#fff", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", position: "relative" }}>
              <div style={{ fontSize: 24, fontWeight: 800, lineHeight: 1, whiteSpace: "nowrap" }}>11h 23m</div>
              <div style={{ fontSize: 11, fontWeight: 700, color: day.periwinkle, marginTop: 2 }}>夜觉时长</div>
            </div>
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 18, fontWeight: 800, lineHeight: 1.25 }}>在她的常态区间偏上</div>
            <div style={{ marginTop: 6, fontSize: 12, fontWeight: 600, color: "#4A5570", lineHeight: 1.5 }}>
              <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: 5, background: day.gold, verticalAlign: -1, marginRight: 4 }} />
              常态 10h 20m – 11h 50m
              <br />
              最近 14 晚中位 10h 55m
            </div>
          </div>
        </div>
        <div style={{ marginTop: 18, position: "relative", height: 44, borderRadius: 22, background: day.periTint, overflow: "hidden" }}>
          <Seg2 left={0} width={47} radius="22px 0 0 22px" color={day.periwinkle} />
          <Seg2 left={47} width={2} color={day.gold} />
          <Seg2 left={49} width={17} color={day.periwinkle} />
          <Seg2 left={66} width={1.5} color={day.gold} />
          <div style={{ position: "absolute", left: "67.5%", top: 0, bottom: 0, right: 0, background: day.periwinkle, borderRadius: "0 22px 22px 0" }} />
        </div>
        <div style={{ marginTop: 8, display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 700, color: day.periwinkle }}>
          <span>19:42</span><span>02:31 · 16m</span><span>05:10 · 12m</span><span>10:15</span>
        </div>
        <div style={{ marginTop: 14, fontSize: 13, fontWeight: 600, color: "#4A5570", lineHeight: 1.5 }}>
          在床 14h 33m · 醒 2 次 · 接觉中位 14m。只有你记的时间，不猜深睡浅睡。
        </div>
      </div>

      <div style={{ marginTop: 14, background: "#fff", borderRadius: radius.innerCard, padding: "18px 20px", display: "flex", gap: 14, alignItems: "center", boxShadow: shadow.cardLighter }}>
        <div style={{ flex: "none" }}><Mascot size="sm" state="day" /></div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 16, fontWeight: 800 }}>入睡后第一段 6h 49m</div>
          <div style={{ marginTop: 2, fontSize: 13, fontWeight: 600, color: "#4A5570", lineHeight: 1.5 }}>比她最近两周中位（约 5h）长；这周第 2 次。</div>
        </div>
        <span style={{ color: day.periwinkle, fontWeight: 800 }}>›</span>
      </div>

      <button onClick={onConsult} style={{ marginTop: 14, width: "100%", padding: "14px 18px", borderRadius: radius.innerCard, background: "rgba(255,255,255,.6)", fontSize: 14, fontWeight: 700, color: day.navy, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span>问知眠：昨晚为什么睡得好</span>
        <span style={{ fontSize: 12, color: day.goldText }}>用 1 轮咨询</span>
      </button>
    </>
  );
}

/* ── H2 小觉 ─────────────────────────────────────────────────────────────── */
const NAP_ROWS = [
  { date: "9/25", segs: [{ l: 12, w: 9, c: day.periwinkleLight }, { l: 44, w: 14, c: day.periwinkleLight }], total: "2h 15m" },
  { date: "9/24", segs: [{ l: 14, w: 10, c: day.periwinkleLight }, { l: 46, w: 15, c: day.periwinkleLight }], total: "2h 30m" },
  { date: "9/23", segs: [{ l: 10, w: 11, c: day.periwinkleLight }, { l: 44, w: 17, c: day.periwinklePale }], total: "2h 50m" },
  { date: "9/22", segs: [{ l: 16, w: 8, c: day.periwinkleLight }, { l: 47, w: 12, c: day.periwinklePale }], total: "2h 00m" },
  { date: "9/21", segs: [{ l: 15, w: 10, c: day.periwinkleLight }, { l: 45, w: 16, c: day.periwinkleLight }], total: "2h 35m" },
  { date: "9/20", segs: [{ l: 18, w: 7, c: day.periwinkleLight }, { l: 40, w: 8, c: day.periwinkleLight }, { l: 66, w: 7, c: day.periwinkleLight }], total: "2h 10m" },
  { date: "9/19", segs: [{ l: 14, w: 10, c: day.periwinkleLight }, { l: 46, w: 15, c: day.periwinklePale }], total: "2h 30m" },
];

function Naps() {
  return (
    <>
      <div style={{ marginTop: 18, background: "#fff", borderRadius: radius.pageCard, padding: 22, boxShadow: shadow.card }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
          <div>
            <div style={{ fontSize: 15, fontWeight: 800 }}>最近 7 天 · 白天</div>
            <div style={{ fontSize: 13, fontWeight: 700, color: day.periwinkle }}>每天 2 觉 · 合计中位 2h 35m</div>
          </div>
          <div style={{ display: "flex", gap: 10, fontSize: 11, fontWeight: 700, color: day.periwinkle }}>
            <span><Dot c={day.periwinkleLight} sq /> 在家</span>
            <span><Dot c={day.periwinklePale} sq /> 托班</span>
          </div>
        </div>
        <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 9, fontSize: 12, fontWeight: 700, color: day.periwinkle }}>
          {NAP_ROWS.map((r) => (
            <div key={r.date} style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <span style={{ width: 28 }}>{r.date}</span>
              <div style={{ flex: 1, position: "relative", height: 22, borderRadius: 11, background: "#F4F6FB" }}>
                {r.segs.map((s, i) => (
                  <span key={i} style={{ position: "absolute", left: `${s.l}%`, width: `${s.w}%`, top: 0, bottom: 0, borderRadius: 11, background: s.c }} />
                ))}
              </div>
              <span style={{ width: 44, textAlign: "right", color: day.ink }}>{r.total}</span>
            </div>
          ))}
          <div style={{ display: "flex", gap: 10, alignItems: "center", fontSize: 11 }}>
            <span style={{ width: 28 }} />
            <div style={{ flex: 1, display: "flex", justifyContent: "space-between" }}>
              <span>07:00</span><span>10:00</span><span>13:00</span><span>16:00</span><span>19:00</span>
            </div>
            <span style={{ width: 44 }} />
          </div>
        </div>
      </div>

      <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 8 }}>
        <InsightRow c={day.positive} title="第一觉入睡从 09:30 前后移到 08:50 前后" sub='近 3 天 · "第一觉提前"计划第 3 天' />
        <InsightRow c={day.periwinkle} title="托班日第二觉比在家长 20–30 分" sub="周一、三、五 · 12:30 固定开始" />
        <InsightRow c={day.periwinklePale} title="9/20 出现第三觉" sub="那天早醒 05:20，属于补觉，不算并觉反复" />
      </div>
    </>
  );
}

/* ── H3 两周 ─────────────────────────────────────────────────────────────── */
const NIGHT_BARS = [60, 55, 64, 40, 62, 66, 56, 63, 68, 58, 66, 70, 64, 74];
const NIGHT_COLORS = NIGHT_BARS.map((_, i) =>
  i === 13 ? day.gold : i === 3 ? day.periwinklePale : i >= 10 ? day.navy : day.periwinkle,
);
const NAP_TOTAL_BARS = [52, 60, 48, 70, 55, 58, 44, 62, 50, 40, 56, 64, 58, 50];
const WAKE_DOTS = [
  { l: 5, c: day.periwinklePale },
  { l: 12, c: day.periwinkle },
  { l: 30, c: day.periwinkle },
  { l: 44, c: day.periwinkle },
  { l: 58, c: day.periwinkle },
  { l: 66, c: day.navy },
  { l: 70, c: day.gold },
];

function TwoWeeks({ onConsult }: { onConsult: () => void }) {
  return (
    <>
      <div style={{ marginTop: 16, background: "#fff", borderRadius: radius.pageCard, padding: "18px 22px", boxShadow: shadow.card }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <div style={{ fontSize: 14, fontWeight: 800 }}>夜觉时长 · 9月12日 – 25日</div>
          <div style={{ fontSize: 12, fontWeight: 700, color: day.periwinkle }}>中位 10h 55m</div>
        </div>
        <div style={{ marginTop: 10, position: "relative", height: 84 }}>
          <div style={{ position: "absolute", left: 0, right: 0, top: "14%", height: "30%", background: day.goldTint, borderRadius: 8 }} />
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "flex-end", gap: 5 }}>
            {NIGHT_BARS.map((h, i) => (
              <span key={i} style={{ flex: 1, height: `${h}%`, background: NIGHT_COLORS[i], borderRadius: 4 }} />
            ))}
          </div>
        </div>
        <div style={{ marginTop: 4, display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 700, color: day.periwinkle }}>
          <span>9/12</span>
          <span style={{ color: day.goldText }}>▲ 9/23 起"第一觉提前"</span>
          <span>昨晚</span>
        </div>

        <div style={{ marginTop: 14, display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <div style={{ fontSize: 14, fontWeight: 800 }}>起床时间</div>
          <div style={{ fontSize: 12, fontWeight: 700, color: day.periwinkle }}>近 4 天 06:30 前后</div>
        </div>
        <div style={{ marginTop: 8, position: "relative", height: 30, borderRadius: 15, background: day.periTint }}>
          <div style={{ position: "absolute", left: "8%", right: "8%", top: 11, height: 8, borderRadius: 4, background: day.goldTint }} />
          {WAKE_DOTS.map((d, i) => (
            <span key={i} style={{ position: "absolute", left: `${d.l}%`, top: 8, width: 14, height: 14, borderRadius: 7, background: d.c }} />
          ))}
        </div>
        <div style={{ marginTop: 3, display: "flex", justifyContent: "space-between", fontSize: 11, fontWeight: 700, color: day.periwinkle }}>
          <span>05:00</span><span>06:00</span><span>07:00</span><span>08:00</span>
        </div>

        <div style={{ marginTop: 14, display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <div style={{ fontSize: 14, fontWeight: 800 }}>白天小觉合计</div>
          <div style={{ fontSize: 12, fontWeight: 700, color: day.periwinkle }}>中位 2h 35m · 2 觉</div>
        </div>
        <div style={{ marginTop: 8, position: "relative", height: 56 }}>
          <div style={{ position: "absolute", left: 0, right: 0, top: "20%", height: "36%", background: day.goldTint, borderRadius: 6 }} />
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "flex-end", gap: 5 }}>
            {NAP_TOTAL_BARS.map((h, i) => (
              <span key={i} style={{ flex: 1, height: `${h}%`, background: day.periwinkleLight, borderRadius: 3 }} />
            ))}
          </div>
        </div>
        <div style={{ marginTop: 8, fontSize: 12, fontWeight: 600, color: day.periwinkle, lineHeight: 1.5 }}>
          金色带 = 她自己的常态区间（14 天中位 ±）。9/15 外出过夜已按你说的不计入。
        </div>
      </div>

      <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 6 }}>
        <InsightRow small c={day.positive} title="起床从 05:30 前后移到 06:30 左右" sub='近 4 天 · 与"第一觉提前"同步' />
        <InsightRow small c={day.periwinkle} title="夜醒每晚 1–2 次没变，接觉从约 30 分缩到 10–16 分" />
        <InsightRow small c={day.periwinkleLight} title="白天合计稳定在 2h–2h 50m，没有随早起变短" />
      </div>

      <button onClick={onConsult} style={{ marginTop: 10, width: "100%", padding: "12px 18px", borderRadius: 20, background: "rgba(255,255,255,.6)", fontSize: 14, fontWeight: 700, color: day.navy, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span>让知眠复盘这两周</span>
        <span style={{ fontSize: 12, color: day.goldText }}>深度咨询</span>
      </button>
    </>
  );
}

/* ── shared bits ─────────────────────────────────────────────────────────── */
function Seg2({ left, width, color, radius: r }: { left: number; width: number; color: string; radius?: string }) {
  return <div style={{ position: "absolute", left: `${left}%`, top: 0, bottom: 0, width: `${width}%`, background: color, borderRadius: r }} />;
}

function Dot({ c, sq = false }: { c: string; sq?: boolean }) {
  return <span style={{ display: "inline-block", width: 9, height: 9, borderRadius: sq ? 3 : 5, background: c, verticalAlign: -1, marginRight: 3 }} />;
}

function InsightRow({ c, title, sub, small = false }: { c: string; title: string; sub?: string; small?: boolean }) {
  return (
    <div style={{ background: "#fff", borderRadius: small ? 20 : radius.innerCard, padding: small ? "12px 16px" : "14px 18px", display: "flex", gap: 12, alignItems: "center" }}>
      <span style={{ width: 10, height: 10, borderRadius: 5, background: c, flex: "none" }} />
      <div style={{ flex: 1, fontSize: 14, fontWeight: 700, lineHeight: small ? 1.35 : 1.4 }}>
        {title}
        {sub && <div style={{ fontSize: 12, fontWeight: 600, color: day.periwinkle }}>{sub}</div>}
      </div>
      <span style={{ color: day.periwinkle }}>›</span>
    </div>
  );
}
