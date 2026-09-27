import { day, font, radius, shadow } from "../../theme/tokens";
import { Mascot } from "../../components/Mascot";
import { TabBar } from "../../components/TabBar";
import { useApp } from "../../state/store";

/**
 * B4 今天 · 数据不足 (first day) — falls back to a wider age-range estimate and
 * says so; does not claim personalization. No reminder set by default.
 */
export function TodayFirstDay() {
  const app = useApp();
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
      }}
    >
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <button onClick={() => app.openOverlay("babySwitcher")} style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={avatar}>{app.baby.initial}</span>
          <div style={{ lineHeight: 1.1, textAlign: "left" }}>
            <div style={{ fontSize: 17, fontWeight: 800, color: day.ink }}>{app.baby.name}</div>
            <div style={{ fontSize: 13, color: day.periwinkle, fontWeight: 700 }}>{app.baby.age} · 第 1 天</div>
          </div>
        </button>
        <button onClick={() => app.openOverlay("settings")} style={gear}>⚙</button>
      </div>

      <div style={{ marginTop: 22, background: day.card, borderRadius: radius.pageCard, padding: "22px 22px 20px", boxShadow: shadow.card }}>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 14, fontWeight: 800, color: day.periwinkle, letterSpacing: ".04em" }}>已醒 · AWAKE</div>
            <div style={{ marginTop: 2, fontSize: 46, fontWeight: 800, lineHeight: 1.05, letterSpacing: "-.02em" }}>0h 35m</div>
            <div style={{ marginTop: 4, fontSize: 15, fontWeight: 700, color: day.periwinkle }}>15:10 醒 · 这是今天第一条记录</div>
          </div>
          <div style={{ flex: "none", paddingTop: 6 }}>
            <Mascot size="md" state="day" />
          </div>
        </div>
        <div style={{ marginTop: 14, padding: 16, borderRadius: radius.innerCard, background: day.periTint, border: "1.5px dashed #B9C7E6" }}>
          <div style={{ fontSize: 13, fontWeight: 800, color: day.navy }}>下一觉 · 年龄段估计</div>
          <div style={{ marginTop: 2, fontSize: 28, fontWeight: 800, letterSpacing: "-.02em", color: day.periwinkle }}>17:15 – 18:15</div>
          <div style={{ marginTop: 4, fontSize: 13, fontWeight: 600, color: "#4A5570", lineHeight: 1.5 }}>
            还没有小满自己的记录，这是 7 个月宝宝的常见范围，比较宽。记几天后会换成她自己的。<b>暂未设提醒</b>，需要的话可以手动开。
          </div>
          <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
            <span style={chip}>开 16:45 提醒</span>
            <span style={chip}>这是最后一觉</span>
          </div>
        </div>
      </div>

      <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
        <button onClick={app.markAsleep} style={{ flex: 1, height: 64, borderRadius: radius.pageCard, background: day.navy, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 19, fontWeight: 800, boxShadow: shadow.primaryButton }}>
          睡着了
        </button>
        <button onClick={app.openSheet} style={secondary}>补记</button>
      </div>

      <div style={{ marginTop: 22, display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <div style={{ fontSize: 15, fontWeight: 800 }}>今天 · 9月25日</div>
      </div>
      <div style={{ marginTop: 10, position: "relative", height: 56, borderRadius: 28, background: "rgba(255,255,255,.7)", overflow: "hidden" }}>
        <div style={{ position: "absolute", left: "63%", top: 0, bottom: 0, width: 3, background: day.gold }} />
      </div>
      <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 8, fontSize: 15, fontWeight: 700 }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span style={{ width: 12, height: 12, borderRadius: 6, background: day.gold, display: "block", flex: "none" }} />
          <span style={{ width: 48, color: day.periwinkle, flex: "none" }}>15:10</span>
          <span style={{ flex: 1 }}>醒来 · 之前的觉没记，没关系</span>
        </div>
      </div>

      <div style={{ marginTop: 16, background: day.card, borderRadius: radius.innerCard, padding: "16px 18px", display: "flex", gap: 14, alignItems: "center" }}>
        <div style={{ flex: "none" }}>
          <Mascot size="sm" state="day" />
        </div>
        <div style={{ fontSize: 14, fontWeight: 600, lineHeight: 1.5 }}>
          想补上午的觉？说一句"上午九点多睡的，十点醒"就行，模糊时间我不会替你编精确。
        </div>
      </div>

      <div style={{ marginTop: "auto" }}>
        <TabBar active="today" onChange={app.setTab} />
      </div>
    </div>
  );
}

const avatar = {
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
} as const;

const gear = {
  width: 40,
  height: 40,
  borderRadius: 20,
  background: "rgba(255,255,255,.7)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: 14,
  color: day.periwinkle,
} as const;

const chip = { padding: "8px 14px", borderRadius: 16, background: "#fff", fontSize: 13, fontWeight: 800, color: day.navy } as const;

const secondary = {
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
} as const;
