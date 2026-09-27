import { day, night, radius, shadow } from "../theme/tokens";

export type Tab = "today" | "chat";

/**
 * Bottom tab bar (2 items, pill style): 今天 · 聊知眠.
 * Active: navy text on a #DCEBFF pill with a filled gold dot.
 * Inactive: periwinkle text with a 3px-ring dot.
 * Night: gold text on rgba(240,195,106,.12).
 */
export function TabBar({
  active,
  onChange,
  dark = false,
}: {
  active: Tab;
  onChange: (t: Tab) => void;
  dark?: boolean;
}) {
  return (
    <div style={{ paddingBottom: 14 }}>
      <div
        style={{
          height: 64,
          borderRadius: radius.tabBar,
          background: dark ? night.controlFill : day.card,
          boxShadow: dark ? "none" : shadow.tabBar,
          border: dark ? night.cardBorder : undefined,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-around",
          fontSize: 14,
          fontWeight: 800,
        }}
      >
        <TabItem label="今天" active={active === "today"} dark={dark} onClick={() => onChange("today")} />
        <TabItem label="聊知眠" active={active === "chat"} dark={dark} onClick={() => onChange("chat")} />
      </div>
    </div>
  );
}

function TabItem({
  label,
  active,
  dark,
  onClick,
}: {
  label: string;
  active: boolean;
  dark: boolean;
  onClick: () => void;
}) {
  const activeText = dark ? night.gold : day.navy;
  const activeBg = dark ? "rgba(240,195,106,.12)" : day.periTintStrong;
  const inactiveText = dark ? night.muted : day.periwinkle;
  const dot = active ? (
    <span style={{ width: 16, height: 16, borderRadius: 8, background: dark ? night.gold : day.gold, display: "block" }} />
  ) : (
    <span
      style={{
        width: 16,
        height: 16,
        borderRadius: 8,
        border: `3px solid ${inactiveText}`,
        display: "block",
        boxSizing: "border-box",
      }}
    />
  );
  return (
    <button
      onClick={onClick}
      style={{
        display: "flex",
        alignItems: "center",
        gap: 8,
        color: active ? activeText : inactiveText,
        background: active ? activeBg : "transparent",
        padding: "10px 20px",
        borderRadius: 22,
        fontSize: 14,
        fontWeight: 800,
      }}
    >
      {dot}
      {label}
    </button>
  );
}
