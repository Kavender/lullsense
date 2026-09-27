import { day, font } from "../../theme/tokens";
import { useApp } from "../../state/store";

/**
 * C4 多宝宝切换 — popover from the baby name. Each baby has its own log,
 * prediction and memory. Naming a baby in chat routes directly, no switch needed.
 */
export function BabySwitcher({ now, onClose }: { now: number; onClose: () => void }) {
  const app = useApp();
  return (
    <div style={{ position: "absolute", inset: 0, zIndex: 65 }}>
      <div onClick={onClose} style={{ position: "absolute", inset: 0, background: "rgba(11,18,38,.5)", animation: "lsFadeIn .2s ease-out" }} />
      <div style={{ position: "relative", padding: "62px 20px 0", fontFamily: font.family }}>
        {/* Faded anchor (the tapped name) */}
        <div style={{ display: "flex", alignItems: "center", gap: 10, opacity: 0.4, color: "#fff" }}>
          <span style={{ width: 40, height: 40, borderRadius: 20, background: day.periwinkle, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, fontWeight: 800 }}>
            {app.baby.initial}
          </span>
          <div style={{ fontSize: 17, fontWeight: 800 }}>{app.baby.name} ▴</div>
        </div>

        <div style={{ marginTop: 12, background: "#FFF9EE", borderRadius: 28, padding: 8, boxShadow: "0 20px 50px rgba(0,0,0,.35)", width: 300 }}>
          {app.babies.map((b) => {
            const selected = b.id === app.selectedBabyId;
            return (
              <button
                key={b.id}
                onClick={() => app.selectBaby(b.id)}
                style={{
                  width: "100%",
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  padding: "12px 14px",
                  borderRadius: 20,
                  background: selected ? day.periTintStrong : "transparent",
                  textAlign: "left",
                }}
              >
                <span style={{ width: 40, height: 40, borderRadius: 20, background: b.id === "b1" ? day.navy : day.gold, color: b.id === "b1" ? "#fff" : day.ink, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, fontWeight: 800 }}>
                  {b.initial}
                </span>
                <div style={{ flex: 1, lineHeight: 1.15 }}>
                  <div style={{ fontSize: 16, fontWeight: 800, color: day.ink }}>{b.name}</div>
                  <div style={{ fontSize: 12, fontWeight: 700, color: day.periwinkle }}>{app.babyStatusLabel(b.id, now)}</div>
                </div>
                {selected && <span style={{ color: day.navy, fontWeight: 800 }}>✓</span>}
              </button>
            );
          })}
          <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 14px", borderRadius: 20, color: day.navy }}>
            <span style={{ width: 40, height: 40, borderRadius: 20, border: "2px dashed #B9C7E6", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18, fontWeight: 800, boxSizing: "border-box" }}>+</span>
            <div style={{ fontSize: 15, fontWeight: 800 }}>添加宝宝</div>
          </div>
        </div>

        <div style={{ marginTop: 14, fontSize: 12, fontWeight: 600, color: "rgba(255,255,255,.75)", lineHeight: 1.5, width: 300 }}>
          聊知眠里说"安安刚睡了"会直接记到安安，不用先切换；没指名时按当前选中的宝宝。
        </div>
      </div>
    </div>
  );
}
