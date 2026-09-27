import type { CSSProperties, ReactNode } from "react";
import { frame } from "../theme/tokens";

/**
 * iPhone 15/16 Pro device frame (402 × 874): bezel, Dynamic Island, status bar
 * and home indicator. Adapted from the handoff's `ios-frame.jsx` preview
 * scaffold (which is not part of the design), pared down to what the prototype
 * needs. Each screen supplies its own background and reserves the 62px top
 * inset for the status bar.
 */
export function IOSFrame({
  children,
  dark = false,
  time = "9:41",
}: {
  children: ReactNode;
  dark?: boolean;
  time?: string;
}) {
  return (
    <div
      style={{
        width: frame.width,
        height: frame.height,
        borderRadius: frame.bezelRadius,
        overflow: "hidden",
        position: "relative",
        background: dark ? "#000" : "#F2F2F7",
        boxShadow: "0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.12)",
        fontFamily: "-apple-system, system-ui, sans-serif",
        WebkitFontSmoothing: "antialiased",
      }}
    >
      {/* Dynamic Island */}
      <div
        style={{
          position: "absolute",
          top: 11,
          left: "50%",
          transform: "translateX(-50%)",
          width: 126,
          height: 37,
          borderRadius: 24,
          background: "#000",
          zIndex: 50,
        }}
      />
      {/* Status bar (absolute, overlays the screen's 62px top inset) */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, zIndex: 40 }}>
        <StatusBar dark={dark} time={time} />
      </div>
      {/* Screen content */}
      <div style={{ height: "100%", position: "relative", zIndex: 1 }}>{children}</div>
      {/* Home indicator */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          zIndex: 60,
          height: 34,
          display: "flex",
          justifyContent: "center",
          alignItems: "flex-end",
          paddingBottom: 8,
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            width: 139,
            height: 5,
            borderRadius: 100,
            background: dark ? "rgba(255,255,255,0.7)" : "rgba(0,0,0,0.25)",
          }}
        />
      </div>
    </div>
  );
}

function StatusBar({ dark, time }: { dark: boolean; time: string }) {
  const c = dark ? "#fff" : "#000";
  const iconStyle: CSSProperties = { display: "flex", alignItems: "center" };
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "21px 34px 19px",
        boxSizing: "border-box",
        width: "100%",
      }}
    >
      <span
        style={{
          fontFamily: '-apple-system, "SF Pro", system-ui',
          fontWeight: 590,
          fontSize: 17,
          lineHeight: "22px",
          color: c,
        }}
      >
        {time}
      </span>
      <div style={{ ...iconStyle, gap: 7 }}>
        {/* cellular */}
        <svg width="19" height="12" viewBox="0 0 19 12">
          <rect x="0" y="7.5" width="3.2" height="4.5" rx="0.7" fill={c} />
          <rect x="4.8" y="5" width="3.2" height="7" rx="0.7" fill={c} />
          <rect x="9.6" y="2.5" width="3.2" height="9.5" rx="0.7" fill={c} />
          <rect x="14.4" y="0" width="3.2" height="12" rx="0.7" fill={c} />
        </svg>
        {/* wifi */}
        <svg width="17" height="12" viewBox="0 0 17 12">
          <path
            d="M8.5 3.2C10.8 3.2 12.9 4.1 14.4 5.6L15.5 4.5C13.7 2.7 11.2 1.5 8.5 1.5C5.8 1.5 3.3 2.7 1.5 4.5L2.6 5.6C4.1 4.1 6.2 3.2 8.5 3.2Z"
            fill={c}
          />
          <path
            d="M8.5 6.8C9.9 6.8 11.1 7.3 12 8.2L13.1 7.1C11.8 5.9 10.2 5.1 8.5 5.1C6.8 5.1 5.2 5.9 3.9 7.1L5 8.2C5.9 7.3 7.1 6.8 8.5 6.8Z"
            fill={c}
          />
          <circle cx="8.5" cy="10.5" r="1.5" fill={c} />
        </svg>
        {/* battery */}
        <svg width="27" height="13" viewBox="0 0 27 13">
          <rect x="0.5" y="0.5" width="23" height="12" rx="3.5" stroke={c} strokeOpacity="0.35" fill="none" />
          <rect x="2" y="2" width="20" height="9" rx="2" fill={c} />
          <path d="M25 4.5V8.5C25.8 8.2 26.5 7.2 26.5 6.5C26.5 5.8 25.8 4.8 25 4.5Z" fill={c} fillOpacity="0.4" />
        </svg>
      </div>
    </div>
  );
}
