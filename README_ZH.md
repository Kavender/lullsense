<!-- Language: [English](README.md) · **中文** -->

[English](README.md) · **中文**

<p align="center">
  <img src="assets/lullsense-logo.png" alt="LullSense (知眠)" width="200">
</p>

# LullSense（知眠）

> **一个开源的婴幼儿睡眠顾问 Agent Skill：不只告诉你“这个月龄通常怎样”，更想帮你看懂“这个孩子最近发生了什么”。**

[![CI](https://github.com/Kavender/lullsense/actions/workflows/ci.yml/badge.svg)](https://github.com/Kavender/lullsense/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Scope](https://img.shields.io/badge/适用月龄-4–36%20个月-brightgreen)
![Safety](https://img.shields.io/badge/安全优先-绝不做诊断-orange)
![Status](https://img.shields.io/badge/状态-public%20alpha-brightgreen)

**给那些凌晨 3 点、拿不准宝宝为什么醒、要不要调作息的时刻，多一个随时能聊、尽量靠谱的帮手。**

LullSense（知眠）是一个开源、基于证据的 baby / toddler sleep consultant，以 **Agent Skill** 的形式运行。

没有睡眠记录也可以直接聊。你可以只告诉它：“最近每天 5 点醒”“午睡突然变短了”“daycare 的午睡时间固定，改不了怎么办”。它会先理解孩子现在的情况、家庭里哪些事情不能改，再一起判断可能发生了什么，以及下一步最值得试什么。

如果你有最近几天或几周的睡眠记录，LullSense 还能进一步参考**这个孩子自己的历史规律（personal baseline）**，看看最近到底哪里变了，而不是只拿一张通用月龄表来套。

> **数据会让判断更有把握，但没有数据也不妨碍开始。**

LullSense 是教育和支持工具，**不是医疗器械，也不会替代儿科医生**。它不做诊断；遇到需要优先关注的健康或安全信号时，会先停下作息和睡眠训练建议，再提醒家长寻求合适的医疗帮助。对于研究证据、专业共识和产品经验法则，它也会尽量把边界说清楚。

> **先说清楚现在的形态：** LullSense 的长期目标是让更多普通家庭也能方便使用，但当前 public alpha 仍然是一个偏开发者的 Agent Skill。第一批用户更适合是熟悉 AI agent / Claude Code / MCP 的家长、开发者和 builder。降低使用门槛、最终走到手机和更自然的家庭入口，是后续要解决的问题，而不是假装现在已经做到了。

---

## 为什么做这个项目

带娃以后很容易遇到这种时刻：

宝宝突然开始早醒、夜里频繁醒、小睡乱掉，或者本来好好的作息突然不工作了。你打开搜索，能看到很多“这个月龄应该睡多久”“wake window 应该是多少”的答案，但真正难回答的问题往往是：

**为什么是这几天突然变了？**

**是需要调整作息，还是先别动？**

**daycare 午睡时间固定、工作和接送时间也不能改，那现实里到底还能调什么？**

权威的安全睡眠指南、睡眠时长共识和发育研究其实都是公开的，但它们分散在不同论文和指南里，也不会直接告诉你“你家这个孩子今晚怎么办”。

另一方面，专业睡眠顾问很有价值，但不一定每个家庭都负担得起，也不可能凌晨 3 点随时在线。

LullSense 就是从这个缺口开始的。

我们想做的不是另一个“几点该睡”的计算器，而是把公开证据、孩子自己的近期变化，以及家庭真实的限制放在一起，尽量像一个好的睡眠顾问那样思考：

**先理解发生了什么，再给一个现实里做得到的下一步。**

---

## 它大概怎么聊

### 没有睡眠记录，也可以开始

> **家长：** 我家 8 个月宝宝最近突然每天 5 点醒，是不是哪里不对？
>
> **LullSense：** 连着这么早醒确实很累。先不急着把它归成某个“睡眠倒退期”——我更想先看看最近到底变了什么。她这几天大概几点入睡、白天睡几觉？5 点早醒是突然出现的，还是慢慢提前的？有了这些信息，我们可以先排两个更可能的方向，再挑一个最小的调整试几天。

### 有近期数据，就看孩子自己的变化

> **家长：** 帮我看看过去两周睡得怎么样？
>
> **LullSense：** 整体其实挺稳：夜间总睡眠、小睡和入睡时间都没有明显变化。比较值得注意的是最近几天早晨在持续提前，大约比她自己的前一段基线早了 40 分钟。我们可以先围绕这个变化看，而不是把整套作息都推翻。

### 现实限制不能改，就别给“理想答案”

> **家长：** 她 15 个月，daycare 只有中午一次午睡，我完全改不了，但最近总感觉很累。
>
> **LullSense：** 那午睡时间就是一个固定条件，我们就不再建议你“把午睡提前”。真正能动的可能是 bedtime、早晨怎么处理，以及周末要不要补偿。可以先从最小的一步开始，比如把 bedtime 稍微提前几天，再看早醒和入睡有没有一起改善。

### 问下一觉，也只给范围

> **家长：** 她 7 点醒，下一觉大概几点？
>
> **LullSense：** 如果目前只有月龄信息，我会先给一个比较宽的参考区间，而不是一个“必须睡”的时间点；如果有她自己最近几天的记录，就可以把范围收窄到更贴近她自己的节律。犯困信号始终比钟表更重要。

LullSense 给的是**信号、假设和下一步怎么验证**，不是诊断，也不是一次把一大篇分析倒给家长。

---

## LullSense 能做什么

- **直接对话（默认方式）**  
  不要求 tracker。家长对最近几天的描述本身就是信息，可以从早醒、夜醒、小睡、入睡困难、nap transition、daycare 作息等问题直接开始。

- **结合近期睡眠记录分析**  
  支持手写记录、通用 CSV / JSON，以及 Huckleberry 官方导出的 CSV。分析时不只看月龄平均值，而是先建立孩子自己的 baseline，再找最近有没有明显偏移。

- **识别近期睡眠模式变化**  
  当前分析引擎可以检测 early waking、night waking、short nap、split night、total sleep drop、schedule drift、high variability、nap transition 等信号。它们是观察信号，不是医学诊断。

- **回顾最近一段时间“哪里变了”**  
  当家长问“最近这两周睡得怎么样”，会先说哪些部分仍然稳定，再挑真正值得关注的变化，避免把每个小波动都变成警报。

- **给下一次 nap / bedtime 一个合理范围**  
  没有个人数据时参考月龄常见节律；有近期记录时参考孩子自己的 pattern。wake window 会明确标为产品 heuristic，而不是临床标准。

- **把现实约束放进建议里**  
  daycare 午睡、接送时间、家长工作安排、room sharing 等限制会先进入推理。不可改变的条件不会被包装成“你应该做到但没有做到”的理想方案。

- **记住少量真正长期有用的信息**  
  可以在本地保存孩子的生日、长期约束和正在尝试的小实验，避免每次重新解释。**原始睡眠日志不会写入本地存储。**

---

## 我们比较在意的几条原则

| 原则 | 实际意味着什么 |
|---|---|
| **安全优先** | 如果家长描述里出现需要优先就医的信号，会先停下普通睡眠优化，不在健康风险上继续调 wake window 或做 sleep training。 |
| **不做诊断** | 可以讨论可能影响睡眠的因素，但不会根据睡眠表现判断“孩子得了某种病”。 |
| **不装作什么都知道** | 有研究依据的内容给出处；只是产品经验法则的，就明确说是 heuristic。文献没有精确阈值时，不自己造一个。 |
| **先看这个孩子** | 月龄规范是参考，不是说明书。有个人历史数据时，优先看孩子自己的 baseline 和变化。 |
| **先看现实能不能做到** | daycare、工作、接送、家庭偏好都属于计划的一部分，不是给完建议以后再处理的“例外”。 |
| **尽量一次只改一件事** | 比起同时重做整套作息，更倾向于提出一个小调整、观察几天，再决定要不要继续。 |
| **数据可选** | 没有 tracker 也能开始；有持续数据时，个体化判断会更有价值。 |

---

## 适用范围

当前 public alpha 的主要支持范围是：

- **4–36 个月：** 睡眠习惯、作息、入睡、夜醒、小睡等非医疗问题。
- **4 个月以下：** 不提供 sleep training 或结构化作息优化，只提供安全睡眠相关信息和必要的安全提醒。

这不是为了暗示“4 个月以后所有睡眠问题都适合自己处理”。如果对话中出现需要医疗评估的情况，安全规则优先于睡眠建议。

---

## 安装

### 安装 Agent Skill

安装到当前项目：

```bash
npx skills add Kavender/lullsense
```

或者全局安装：

```bash
npx skills add Kavender/lullsense -g
```

查看 Skills CLI 的其他选项：

```bash
npx skills add --help
```

项目级安装会放到项目的 agent skills 目录；全局安装使用共享的 `~/.agents/skills/lullsense/`，再链接到对应 agent 的 skill 目录。以 Claude Code 为例，会链接到 `~/.claude/skills/lullsense/`。

安装以后，直接用自然语言问宝宝睡眠问题即可。

### 可选：安装分析引擎

如果想使用结构化日志分析、longitudinal review 和 prediction，可以再安装 Python engine：

```bash
pip install "git+https://github.com/Kavender/lullsense.git"
```

安装后提供：

```bash
lullsense-analyze
lullsense-experiment
```

目前 alpha 阶段尚未发布到 PyPI，因此暂时使用 GitHub source install。

如果已经 clone 了仓库：

```bash
git clone https://github.com/Kavender/lullsense.git
cd lullsense
pip install .
```

> **当前状态：public alpha。** 核心流程已经实现并有 CI / eval 覆盖；安全内容以权威来源为基础，并做了来源校验，但**还没有完成独立的儿科睡眠 / 临床专家审阅**。来源核验不等于临床审阅，后者会作为 stable release 前的重要步骤。

---

## 数据和隐私

LullSense 自己没有云端后台。

本地只会保存少量跨会话有用的状态，例如：

- 孩子的生日 / 月龄信息
- 长期有效的家庭约束
- 当前正在尝试的 sleep experiment

**原始睡眠记录不会被写入 LullSense 的本地状态。**

第一次保存信息时会明确告诉用户；记忆可以随时关闭，也可以查看或删除已经保存的状态。

需要特别说明的是：**LullSense 运行在你选择的 AI agent / 模型里面。**  
因此，你在对话里输入的内容、主动提供的睡眠日志，以及连接工具返回的数据，仍可能由你所使用的 AI 模型提供方按照它自己的隐私政策处理。

更完整的数据说明见 [`DATA_HANDLING.md`](DATA_HANDLING.md)。

---

## 知识和证据是怎么组织的

LullSense 不把“论文里写的”“专业机构建议的”和“睡眠顾问常用的经验”混成一件事。

当前知识库分成四层：

| 层级 | 主要内容 | 怎么使用 |
|---|---|---|
| **A · Safety** | 安全睡眠、需要就医的风险信号、低月龄安全边界 | 只接受指南、专业共识或系统综述等较高等级来源；安全规则优先级最高。 |
| **B · Development** | 睡眠时长、发育变化、nap transition、正常差异 | 用来提供背景和参考范围，不直接拿群体平均值给单个孩子定作息。 |
| **C · Behavioral** | bedtime、night waking、settling、sleep-training approaches | 尽量基于系统综述 / 临床睡眠文献，同时尊重家庭对不同方法的偏好。 |
| **D · Practice** | 一个好的 sleep consultant 怎么问问题、怎么处理现实约束、怎么复盘 | 这部分属于实践方法，不冒充医学证据；经验规则会明确标注。 |

目前知识库包含 **56 条 claims、34 个 sources**，并通过 `scripts/validate_knowledge.py` 做 schema、来源和安全规则校验。

---

## 安全边界

LullSense 的安全设计不是在每句话后面加一句“请咨询医生”，而是尽量把边界放在真正需要的地方：

- **不诊断、不治疗、不替代儿科医生。**
- 出现明确风险信号时，**暂停普通睡眠建议**，先提醒家长寻求合适的医疗帮助。
- 安全结论只能来自预先核验的权威来源，不能临时搜到一篇网页就当依据。
- wake window、schedule threshold、signal severity 等如果属于产品 heuristic，会明确这样标注。
- 对家长已经明确提到的疾病或状况，可以做一般性的教育说明，但不会反推“你家孩子就是这个问题”。

---

## 工作原理

LullSense 分成两部分：

1. **Sleep consultant**：负责对话、理解家庭情境、形成假设、给出一个现实可行的小调整。
2. **Sleep observer / analysis engine**：在有日志时，把记录标准化，建立个人 baseline，提取特征并识别近期变化。

大致流程：

```text
家长的问题 / 睡眠记录
        │
        ▼
安全边界 → 月龄 → 真正想解决的问题 → 家庭约束
        │
        ├── 没有数据 ──> 基于对话 + 证据进行推理
        │
        └── 有数据 ────> 标准化 → personal baseline → signals
                                      │
                                      ▼
                              排出最可能的解释
                                      │
                                      ▼
                              一个最小、可验证的调整
                                      │
                                      ▼
                                  观察结果
```

仓库里的实现大致是：

```text
skills/lullsense/SKILL.md
   │
   ├─ references/*.md        15 份按需加载的参考资料
   ├─ knowledge/*.yaml      带版本的 claims / sources / heuristics
   │
   └─ baby_sleep/           可选的纯 Python 分析引擎
        ├─ contract/        统一睡眠数据结构与 provenance
        ├─ ingest/          manual / CSV / JSON / Huckleberry export
        ├─ analyze/         特征提取 + personal baseline
        ├─ detect/          baseline-relative signal detectors
        ├─ review/          最近睡眠变化回顾
        ├─ predict/         下一次 nap / bedtime 范围预测
        └─ store/           profile / constraints / experiments
```

分析引擎和知识校验是 deterministic、可检查的；咨询部分由 LLM 驱动，但它使用的 reasoning framework、证据来源和 eval 标准都放在仓库里公开。

LullSense 的核心不依赖某一个 sleep tracker 或模型提供商。CSV、JSON、MCP 或未来其他数据源，都应该只是可替换的 adapter。

---

## 仓库结构

| 路径 | 内容 |
|---|---|
| `skills/lullsense/` | Agent Skill 本体：`SKILL.md`、references、knowledge |
| `baby_sleep/` | 可选 Python analysis engine |
| `scripts/` | knowledge validator 和 CLI 入口 |
| `evals/` | detector / review eval、consultant rubric、安全测试场景 |
| `examples/` | 合成睡眠数据示例 |
| `tests/` | 自动化测试；push / PR 时由 GitHub Actions CI 执行 |
| `assets/` | Logo 与品牌素材 |

---

## 一起把它做得更好

LullSense 现在最需要的不是更多“完美功能”，而是真实使用反馈。

如果你是家长，或者正在做 AI agent / parenting tech / health-tech 相关项目，都很欢迎试试看：

- 哪些回答真的帮到了你？
- 哪些地方听起来还是很像 AI？
- 哪些建议不符合真实家庭生活？
- 数据接入哪里最麻烦？
- 哪些场景它根本没有理解对？

**What works, what doesn’t，都欢迎直接告诉我们。**

Issue、PR 和讨论都欢迎。贡献代码需要 **DCO sign-off**（`git commit -s`），详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

请不要提交真实儿童的睡眠记录、姓名或其他敏感家庭信息；测试和示例一律使用 synthetic data。

---

## License

**Apache-2.0**

见 [`LICENSE`](LICENSE) 和 [`NOTICE`](NOTICE)。

LullSense 不复制商业睡眠产品或私人顾问的专有内容；公开实践资料只做归纳，并尽可能保留来源与证据边界。
