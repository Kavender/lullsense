# 知眠 LullSense — iOS app prototype (React/Vite)

A faithful, interactive rebuild of the LullSense iOS design handoff, built as a
web prototype (React + Vite + TypeScript). It doubles as a precise spec for a
later SwiftUI port.

> **Source of truth:** the design handoff (`知眠 App 全套.dc.html` + its README).
> Design tokens, copy and layout here are transcribed from that handoff; the
> HTML original is a reference, not shipped code.

## What's built (Gate 1 — core flow)

- **Onboarding** — A1 欢迎 · A2 宝宝资料 · A3 当前困扰 (with a working preterm
  toggle and multi-select concern chips).
- **今天 (B1/B2)** — status card with a **live** elapsed timer, prediction
  sub-card, 昨晚 ring card, 24-hour timeline, event list. `睡着了`/`醒了` toggle
  the awake ↔ napping states and write to the log; a 6-second toast offers 撤销.
- **聊知眠 (D1)** — header with remembered facts, plan strip, chat bubbles
  (including the "记好了" logged card), suggestion chips, and a working composer
  that echoes and logs from natural language.
- **补记 (C1)** — bottom sheet with a segmented 小觉/夜觉/夜醒 control and the
  "大约" fuzzy-time toggle; saving writes a new event to today's timeline.
- **Shared** — design tokens (day + night themes), the iPhone device frame, the
  「小灯」 mascot placeholder, and the two-item tab bar.

A small out-of-frame demo bar toggles the day/night theme and restarts
onboarding.

## Not yet built

B3–B5 (night / first-day / safety-pause), C2–C4, D2–D4, E1–E3 settings & memory,
F1 subscription, G1 lock-screen, H1–H3 review. Tokens and components are in place
to add them quickly.

## Run

```bash
cd app
npm install
npm run dev      # http://localhost:5173
npm run build    # typecheck + production build
```

## Layout

```
src/
  theme/tokens.ts      design tokens (day + night)
  theme/global.css     canvas + keyframes
  state/store.ts       app state types + context + helpers
  App.tsx              provider, live clock, actions, router
  components/          IOSFrame · Mascot · TabBar · Toast
  screens/
    onboarding/        Welcome (A1) · BabyProfile (A2) · Concerns (A3)
    today/Today.tsx    B1/B2
    chat/Chat.tsx      D1
    record/RecordSheet.tsx  C1
```

The mascot 「小灯」 and app icon are geometric placeholders, per the handoff —
the illustrator's final asset replaces them at the same sizes/positions.
