import { day, shadow } from "../theme/tokens";

/**
 * Floating confirmation toast (README: 6s toast offering 撤销).
 * Ink background, gold undo link. Sits above the tab bar.
 */
export function Toast({
  message,
  undo,
  onUndo,
}: {
  message: string;
  undo?: () => void;
  onUndo: () => void;
}) {
  return (
    <div
      style={{
        position: "absolute",
        left: 20,
        right: 20,
        bottom: 96,
        zIndex: 70,
        background: day.ink,
        color: "#fff",
        borderRadius: 22,
        padding: "14px 18px",
        boxShadow: shadow.toast,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 12,
        fontSize: 14,
        fontWeight: 700,
        animation: "lsFadeIn .2s ease-out",
      }}
    >
      <span>✓ {message}</span>
      {undo && (
        <button
          onClick={() => {
            undo();
            onUndo();
          }}
          style={{ color: day.gold, fontSize: 14, fontWeight: 800 }}
        >
          撤销
        </button>
      )}
    </div>
  );
}
