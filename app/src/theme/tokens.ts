/**
 * Design tokens for 知眠 LullSense — transcribed verbatim from the design
 * handoff README ("Design Tokens") and cross-checked against the inline styles
 * in `知眠 App 全套.dc.html`. Colors/type/radii/spacing are final (high fidelity).
 *
 * The mascot 「小灯」 and app icon are geometric placeholders pending the
 * illustrator's final asset (see components/Mascot.tsx).
 */

export const font = {
  family: `"Baloo 2", "Noto Sans SC", system-ui, sans-serif`,
  system: `-apple-system, system-ui, "Noto Sans SC", sans-serif`,
} as const;

/** Light / day theme. */
export const day = {
  navy: "#2B4A8A", // primary, buttons, active tab
  ink: "#22335C", // body text
  periwinkle: "#5C73A8", // secondary text, icons
  periwinkleLight: "#7FA7E8", // nap bars, secondary data
  periwinklePale: "#B9C7E6",
  gold: "#FFC862", // assistant speaking / reminder / logged-success / lamp
  goldText: "#B8862B", // gold text on light
  goldTint: "#FFF3DC", // gold tint bg
  goldTintText: "#6B5A3A", // body text on gold tint
  periTint: "#EEF2FB",
  periTintStrong: "#DCEBFF",
  pageBg: "linear-gradient(180deg,#DCEBFF 0%,#FFF6E6 100%)",
  card: "#FFFFFF",
  positive: "#3C9A5F",
  destructive: "#C0392B",
  destructiveSoft: "#E85D4A",
  // Safety pause (amber)
  amber: "#D98B3A",
  amberText: "#A8642A",
  amberTint: "#F7E3CF",
  amberPageBg: "#FBF3EA",
  lampCap: "radial-gradient(circle at 50% 30%,#FFE1A0,#FFC862 70%)",
  lampStem: "#F1E6D0",
  lampBase: "#E3D6BC",
} as const;

/** Night theme — auto 21:00–06:00 or system dark. */
export const night = {
  navy: "#2B4A8A",
  ink: "#F2EEE6", // text
  periwinkle: "#C9D2EA", // secondary
  muted: "#8A97BF",
  periwinkleLight: "#3A4C80", // night-sleep bars
  periwinklePale: "#B9C7E6",
  gold: "#F0C36A",
  onGoldText: "#1A1F33",
  pageBg: "linear-gradient(180deg,#0B1226 0%,#141F3D 100%)",
  sheet: "#141F3D",
  card: "rgba(255,255,255,.05)",
  cardBorder: "1px solid rgba(240,195,106,.22)",
  controlFill: "rgba(255,255,255,.08)",
  userBubble: "#2B3A66",
  lampCap: "radial-gradient(#F7DFA3,#D9A94E)",
  lampStem: "#2B3A66",
} as const;

export const radius = {
  pageCard: 32,
  innerCard: 22,
  tile: 20,
  listGroup: 22,
  chip: 18,
  tabBar: 32,
  sheetTop: 36,
} as const;

export const shadow = {
  card: "0 8px 30px rgba(43,74,138,.10)",
  cardLight: "0 4px 16px rgba(43,74,138,.08)",
  cardLighter: "0 4px 16px rgba(43,74,138,.06)",
  primaryButton: "0 6px 18px rgba(43,74,138,.25)",
  goldButton: "0 6px 18px rgba(243,179,74,.3)",
  navyCard: "0 12px 34px rgba(43,74,138,.28)",
  toast: "0 10px 30px rgba(34,51,92,.3)",
  tabBar: "0 6px 20px rgba(43,74,138,.10)",
} as const;

export const spacing = {
  screenPad: 20,
  chatPad: 18,
  topSafeInset: 62, // status-bar reserve
  sectionGap: 22,
  cardInner: 22,
} as const;

/** Canvas / device frame — designed at 402 × 874 (iPhone 15/16 Pro). */
export const frame = {
  width: 402,
  height: 874,
  bezelRadius: 48,
} as const;

export type Theme = "day" | "night";

export function palette(theme: Theme) {
  return theme === "night" ? night : day;
}
