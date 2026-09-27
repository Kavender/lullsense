import { useState } from "react";
import { day, font, radius } from "../../theme/tokens";

type Seg = "nap" | "night" | "nightWake";
const SEGMENTS: { key: Seg; label: string }[] = [
  { key: "nap", label: "小觉" },
  { key: "night", label: "夜觉" },
  { key: "nightWake", label: "夜醒" },
];

/**
 * C1 补记 (sheet) — backfill a sleep. Segmented 小觉/夜觉/夜醒, 睡着/醒来 times,
 * optional note. "大约" preserves start-time fuzziness (stored as a range).
 * All entry points write to the same log (README: Interactions).
 */
export function RecordSheet({
  onCancel,
  onSave,
}: {
  onCancel: () => void;
  onSave: (entry: { kind: Seg; start: string; end: string }) => void;
}) {
  const [seg, setSeg] = useState<Seg>("nap");
  const [fuzzy, setFuzzy] = useState(true);
  const start = "09:10";
  const end = "10:00";

  return (
    <div style={{ position: "absolute", inset: 0, zIndex: 65, display: "flex", flexDirection: "column", justifyContent: "flex-end" }}>
      {/* Backdrop */}
      <div
        onClick={onCancel}
        style={{ position: "absolute", inset: 0, background: "rgba(11,18,38,.55)", animation: "lsFadeIn .2s ease-out" }}
      />
      {/* Sheet */}
      <div
        style={{
          position: "relative",
          background: "#FFF9EE",
          borderRadius: `${radius.sheetTop}px ${radius.sheetTop}px 0 0`,
          padding: "12px 22px 34px",
          fontFamily: font.family,
          color: day.ink,
          animation: "lsSheetUp .28s cubic-bezier(.2,.8,.2,1)",
        }}
      >
        <div style={{ width: 40, height: 5, borderRadius: 3, background: "#D9D0BF", margin: "0 auto" }} />

        <div style={{ marginTop: 18, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <button onClick={onCancel} style={{ fontSize: 15, fontWeight: 800, color: day.periwinkle }}>
            取消
          </button>
          <span style={{ fontSize: 20, fontWeight: 800 }}>补记一觉</span>
          <button onClick={() => onSave({ kind: seg, start, end })} style={{ fontSize: 15, fontWeight: 800, color: day.navy }}>
            保存
          </button>
        </div>

        {/* Segmented control */}
        <div style={{ marginTop: 20, display: "flex", background: "#fff", borderRadius: 20, padding: 4 }}>
          {SEGMENTS.map((s) => {
            const active = s.key === seg;
            return (
              <button
                key={s.key}
                onClick={() => setSeg(s.key)}
                style={{
                  flex: 1,
                  padding: "12px 0",
                  borderRadius: 16,
                  background: active ? day.navy : "transparent",
                  color: active ? "#fff" : day.periwinkle,
                  textAlign: "center",
                  fontSize: 15,
                  fontWeight: 800,
                }}
              >
                {s.label}
              </button>
            );
          })}
        </div>

        <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 10 }}>
          {/* 睡着 */}
          <div style={{ background: "#fff", borderRadius: radius.innerCard, padding: "16px 18px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 800, color: day.periwinkle, letterSpacing: ".06em" }}>睡着</div>
              <div style={{ marginTop: 2, fontSize: 24, fontWeight: 800 }}>{start}</div>
            </div>
            <div style={{ display: "flex", gap: 6 }}>
              <span style={{ padding: "8px 12px", borderRadius: 14, background: day.periTint, fontSize: 13, fontWeight: 800, color: day.navy }}>
                今天
              </span>
              <button
                onClick={() => setFuzzy((v) => !v)}
                style={{
                  padding: "8px 12px",
                  borderRadius: 14,
                  background: fuzzy ? day.goldTint : "#F1F1F1",
                  fontSize: 13,
                  fontWeight: 800,
                  color: fuzzy ? day.goldText : day.periwinkle,
                }}
              >
                大约
              </button>
            </div>
          </div>

          {/* 醒来 */}
          {seg !== "nightWake" && (
            <div style={{ background: "#fff", borderRadius: radius.innerCard, padding: "16px 18px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ fontSize: 12, fontWeight: 800, color: day.periwinkle, letterSpacing: ".06em" }}>醒来</div>
                <div style={{ marginTop: 2, fontSize: 24, fontWeight: 800 }}>{end}</div>
              </div>
              <div style={{ fontSize: 15, fontWeight: 800, color: day.periwinkle }}>50 分钟</div>
            </div>
          )}

          {/* 备注 */}
          <div style={{ background: "#fff", borderRadius: radius.innerCard, padding: "14px 18px", fontSize: 15, fontWeight: 600, color: day.periwinkle }}>
            备注（可选）· 比如"在车上睡的"
          </div>
        </div>

        <div style={{ marginTop: 12, fontSize: 13, fontWeight: 600, color: day.periwinkle, lineHeight: 1.5 }}>
          "大约"会保留开始时间的模糊性，预测时按范围处理，不会伪造精度。保存后可随时改、可撤销。
        </div>

        <button
          onClick={() => onSave({ kind: seg, start, end })}
          style={{
            marginTop: 16,
            width: "100%",
            height: 60,
            borderRadius: 30,
            background: day.navy,
            color: "#fff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 18,
            fontWeight: 800,
          }}
        >
          保存到今天
        </button>
      </div>
    </div>
  );
}
