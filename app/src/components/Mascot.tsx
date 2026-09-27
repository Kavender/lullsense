/**
 * 「小灯」 — the faceless mushroom night-lamp mascot.
 *
 * PLACEHOLDER ONLY. Per the handoff, this is a geometric CSS placeholder; the
 * illustrator's final asset will replace it at the same sizes/positions. It
 * appears only on the status card corner and as the chat avatar — never on
 * buttons, empty states, badges, or notifications (other than the app icon).
 *
 * States: day (bright) · night (dimmed) · thinking (1.4s pulse) ·
 * nap (on the navy in-progress card) · amber (safety pause) · offline (grey).
 */
import { day, night } from "../theme/tokens";

export type MascotSize = "lg" | "md" | "sm";
export type MascotState = "day" | "night" | "thinking" | "nap" | "amber" | "offline";

type Preset = {
  cap: [number, number];
  capR: string;
  stem: [number, number];
  stemR: string;
  stemTop: number;
  base: [number, number] | null;
  baseTop: number;
};

const PRESETS: Record<MascotSize, Preset> = {
  // A1 welcome — large hero lamp
  lg: {
    cap: [132, 72],
    capR: "72px 72px 14px 14px",
    stem: [46, 60],
    stemR: "0 0 18px 18px",
    stemTop: -2,
    base: [84, 10],
    baseTop: 6,
  },
  // Status card corner (B-screens)
  md: {
    cap: [76, 42],
    capR: "42px 42px 8px 8px",
    stem: [26, 34],
    stemR: "0 0 10px 10px",
    stemTop: -2,
    base: [48, 7],
    baseTop: 4,
  },
  // Chat header avatar / A3 info card
  sm: {
    cap: [44, 24],
    capR: "24px 24px 5px 5px",
    stem: [16, 18],
    stemR: "0 0 6px 6px",
    stemTop: -1,
    base: null,
    baseTop: 0,
  },
};

function skin(state: MascotState) {
  switch (state) {
    case "night":
      return { cap: night.lampCap, stem: night.lampStem, base: "rgba(255,255,255,.18)", shadow: "none" };
    case "nap":
      // On the navy in-progress card: dimmed gold cap, indigo stem
      return { cap: "#E3B85F", stem: "#41599A", base: "rgba(255,255,255,.18)", shadow: "none", capOpacity: 0.8 };
    case "amber":
      return { cap: day.amber, stem: day.lampStem, base: day.lampBase, shadow: "none" };
    case "offline":
      return { cap: "#E3D6BC", stem: day.lampStem, base: day.lampBase, shadow: "none" };
    case "day":
    case "thinking":
    default:
      return { cap: day.lampCap, stem: day.lampStem, base: day.lampBase, shadow: "0 10px 24px rgba(243,179,74,.3)" };
  }
}

export function Mascot({
  size = "md",
  state = "day",
}: {
  size?: MascotSize;
  state?: MascotState;
}) {
  const p = PRESETS[size];
  const s = skin(state);
  const animation =
    state === "thinking"
      ? "lsPulse 1.4s ease-in-out infinite"
      : state === "night"
        ? "lsBreathe 4s ease-in-out infinite"
        : undefined;

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", animation }}>
      <div
        style={{
          width: p.cap[0],
          height: p.cap[1],
          borderRadius: p.capR,
          background: s.cap,
          boxShadow: s.shadow,
          opacity: "capOpacity" in s ? (s.capOpacity as number) : 1,
        }}
      />
      <div
        style={{
          width: p.stem[0],
          height: p.stem[1],
          borderRadius: p.stemR,
          background: s.stem,
          marginTop: p.stemTop,
        }}
      />
      {p.base && (
        <div
          style={{
            width: p.base[0],
            height: p.base[1],
            borderRadius: p.base[1] / 2,
            background: s.base,
            marginTop: p.baseTop,
          }}
        />
      )}
    </div>
  );
}
