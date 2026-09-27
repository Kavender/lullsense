# 知眠 LullSense — iOS app prototype (React/Vite)

A faithful, interactive rebuild of the LullSense iOS design handoff, built as a
web prototype (React + Vite + TypeScript). It doubles as a precise spec for a
later SwiftUI port.

> **Source of truth:** the design handoff (`知眠 App 全套.dc.html` + its README).
> Design tokens, copy and layout here are transcribed from that handoff; the
> HTML original is a reference, not shipped code.

## What's built (full screen set, A–H)

- **Onboarding (A1–A3)** — 欢迎 · 宝宝资料 (working preterm toggle) · 当前困扰
  (multi-select concern chips).
- **今天 (B1–B5)** — B1 已醒 / B2 小觉进行中 with a **live** elapsed timer,
  prediction sub-card, 昨晚 ring card, timeline; `睡着了`/`醒了` toggle the states,
  write to the log, and fire a 6-second 撤销 toast. Plus B3 夜间 (night theme),
  B4 数据不足 (age-range fallback) and B5 安全暂停 (amber), selected by state.
- **记录 (C1–C4)** — C1 补记 sheet (segmented + 大约 fuzzy toggle, saves to the
  timeline), C2 编辑记录, C3 夜间「醒了」二选一 sheet, C4 多宝宝切换 popover
  (actually switches the active baby).
- **聊知眠 (D1–D4)** — D1 白天 with a working composer that logs from natural
  language; D2 夜间, D3 安全暂停 (routes to care), D4 断网 (offline fallback),
  selected by theme / pause / network state.
- **回看 (H1–H3)** — 昨晚 (ring + night bar), 小觉 (7-day distribution), 两周
  (night-duration bars + normal band, wake-time strip, nap totals) via a working
  segmented control.
- **记忆与设置 (E1–E3)** — E1 知眠记得什么, E2 设置, E3 数据控制 (with live toggles
  and the delete-scope card).
- **F1 深度咨询 gate** and **G1 锁屏提醒**.
- **Shared** — design tokens (day + night), iPhone device frame, 「小灯」 mascot
  placeholder (6 states), tab bar, toast.

### Navigation

Real in-app navigation: onboarding → tabs (今天 / 聊知眠); gear → 设置 → 数据控制;
回看 links → 回看; chat header → 知眠记得什么; baby name → 多宝宝切换; B3 醒了 →
夜间二选一 sheet. An out-of-frame **demo bar** flips the day/night theme, the
safety-pause / offline / first-day flags (which select screen variants), and
opens the screens without an in-flow entry yet (锁屏, 订阅, 编辑记录).

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
  App.tsx              provider, live clock, actions, router, overlay host
  components/          IOSFrame · Mascot · TabBar · Toast
  screens/
    onboarding/        Welcome (A1) · BabyProfile (A2) · Concerns (A3)
    today/             Today (B1/B2) · TodayNight (B3) · TodayFirstDay (B4) · TodayPaused (B5)
    chat/              Chat (D1) · ChatNight (D2) · ChatPaused (D3) · ChatOffline (D4)
    record/            RecordSheet (C1) · EditRecord (C2) · NightWakeSheet (C3) · BabySwitcher (C4)
    review/Review.tsx  H1 / H2 / H3
    memory/Memory.tsx  E1
    settings/          Settings (E2) · DataControl (E3)
    subscription/      Subscription (F1)
    lockscreen/        LockScreen (G1)
```

The mascot 「小灯」 and app icon are geometric placeholders, per the handoff —
the illustrator's final asset replaces them at the same sizes/positions.
