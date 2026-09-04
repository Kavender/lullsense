<!-- Language: [English](README.md) · **中文** -->

[English](README.md) · **中文**

<p align="center">
  <img src="assets/lullsense-logo.png" alt="LullSense (知眠)" width="200">
</p>

# LullSense（知眠）

> **一个开源的婴幼儿睡眠支持 Agent Skill：在专业支持暂时不在身边的时候，先帮家长理清发生了什么。**

[![CI](https://github.com/Kavender/lullsense/actions/workflows/ci.yml/badge.svg)](https://github.com/Kavender/lullsense/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Scope](https://img.shields.io/badge/适用月龄-4–36%20个月-brightgreen)
![Safety](https://img.shields.io/badge/安全优先-绝不做诊断-orange)
![Status](https://img.shields.io/badge/状态-public%20alpha-brightgreen)

**给那些凌晨 3 点、拿不准宝宝为什么醒、要不要调整作息的时刻，多一个温和、尽量基于证据的参考。**

LullSense（知眠）是一个开源、基于证据的婴幼儿睡眠**支持** Agent Skill。

没有睡眠记录也可以直接开始。你可以只告诉它：“最近每天 5 点醒”“午睡突然变短了”“daycare 的午睡固定，我改不了怎么办”。它会先理解最近发生了什么、家庭里哪些事情不能改，再一起判断下一步最值得尝试什么。

如果你有最近几天或几周的睡眠记录，LullSense 还能进一步参考**这个孩子自己的历史规律（personal baseline）**，帮助发现近期真正发生变化的地方，而不是只拿通用的月龄标准来套。

> **数据会让判断更有把握，但没有数据也不妨碍开始。**

LullSense 是教育和支持工具，**不是医疗器械，也不是用来替代儿科医生或专业睡眠顾问的。** 它不做诊断；遇到需要优先关注的健康或安全问题时，会先停下普通的作息优化，再提醒家长寻求合适的专业帮助。

我们更希望 LullSense 成为专业睡眠支持之外**随时可用的持续性辅助**：两次咨询之间、顾问暂时联系不上、或者家长只是想先整理一下最近到底发生了什么时，都能有一个随时可用、有明确边界的辅助工具。

让 LullSense 保持**免费、开源**同样重要：好的睡眠支持能不能够得着，不该只取决于预算、订阅，或者你恰好在哪个时区。这是我们想走到的方向——具体现在能覆盖到谁，见下面那段坦白的说明。

长期来看，我们不觉得好的睡眠支持应该是“人”和“AI”二选一。

**专业判断、家庭真实情境、持续睡眠观察，以及随时可获得的工具，可以彼此补位。**

> **先说清楚现在的形态：** LullSense 目前还是一个偏开发者的 public alpha。第一批用户更适合熟悉 AI agent / Claude Code / MCP 的家长、开发者和 builder。让普通家庭更容易使用，是后续要解决的问题，而不是假装现在已经做到了。

---

## 为什么做这个项目

带娃以后很容易遇到这种时刻：

宝宝突然开始早醒、夜里频繁醒、小睡乱掉，或者原本稳定的作息突然不工作了。

网上能找到很多“这个月龄应该睡多久”“wake window 应该是多少”的答案，但真正难回答的问题往往是：

**为什么偏偏是这几天突然变了？**

**现在应该调整，还是先观察几天？**

**daycare 午睡固定、工作和接送时间也不能改，那现实里到底还能动什么？**

专业的睡眠顾问在这些问题上很有价值。

好的顾问不会只看一张作息表，而是会理解孩子的状态、家庭的限制、家长已经尝试过什么，以及这个家庭对不同方法的接受程度，再一起判断下一步。

但睡眠问题并不只发生在咨询的那一个小时里。

很多疑问反而出现在两次沟通之间：

- 今晚突然早醒了，这个变化重要吗？
- 这个调整已经试了三天，要继续还是停？
- 最近好像睡得好一点，是真的有趋势，还是只是偶尔一天？
- 下一次和顾问沟通之前，怎么把这几天发生的事情整理清楚？

LullSense 最初就是从这里开始的。

**它不是为了替代专业睡眠顾问，而是希望补在专业支持之外的这些空档里。**

没人在线的时候，可以先帮家长把问题理清楚；  
有连续睡眠记录时，可以帮助整理近期真正发生的变化；  
正在执行一个方案时，也可以帮助记录和复盘，让下一次和专业人士沟通时更高效。

我们想借鉴专业睡眠咨询里好的思考方式：

**先理解这个孩子和这个家庭，再决定下一步，而不是直接套一张标准作息表。**

长期来看，我们希望 LullSense 能成为家长和专业人士都可以使用、也可以在其上继续搭建的开放工具，让专业经验、持续观察和 AI 辅助彼此配合，帮助更多宝宝和家庭睡得更好。

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

LullSense 给的是**信号、假设和下一步怎么验证**，不是诊断，也不会一次把一大篇分析倒给已经很累的家长。

---

## LullSense 能做什么

- **直接对话（默认方式）**  
  不要求 tracker。家长对最近几天的描述本身就是有用的信息，可以从早醒、夜醒、小睡、入睡困难、nap transition、daycare 作息等问题直接开始。

- **结合近期睡眠记录分析**  
  支持手写记录、通用 CSV / JSON，以及 Huckleberry 官方导出的 CSV。有数据时，不只看月龄平均值，而是先建立孩子自己的 baseline，再看最近有没有明显偏移。如果已经连接了某个数据源 / MCP，也可以在给出一行提示后**自动拉取近期睡眠**（vendor-neutral），不必手动导出。

- **识别近期睡眠模式变化**  
  当前分析引擎可以检测 early waking、night waking、short nap、split night、total sleep drop、schedule drift、high variability、nap transition 等信号。它们是观察信号，不是医学诊断。

- **回顾最近一段时间“哪里变了”**  
  当家长问“最近这两周睡得怎么样”，会先说哪些部分仍然稳定，再挑真正值得关注的变化，避免把每个小波动都变成警报。

- **给下一次 nap / bedtime 一个合理范围**  
  没有个人数据时参考月龄常见节律；有近期记录时参考孩子自己的 pattern。wake window 会明确标为产品 heuristic，而不是临床标准。

- **把现实约束放进建议里**  
  daycare 午睡、接送时间、家长工作安排、room sharing、siblings 等限制会先进入推理。不可改变的条件不会被包装成“你应该做到但没有做到”的理想方案。

- **记住少量真正长期有用的信息**  
  可以在本地保存孩子的生日、长期约束和正在尝试的小实验，避免每次重新解释。**原始睡眠日志不会写入本地状态存储。**

---

## 我们比较在意的几条原则

| 原则 | 实际意味着什么 |
|---|---|
| **安全优先** | 如果家长描述里出现需要优先处理的健康或安全问题，会先停下普通睡眠优化，再引导寻求合适的专业帮助。 |
| **不做诊断** | 可以讨论可能影响睡眠的因素，但不会根据睡眠表现判断“孩子得了某种病”。 |
| **不装作什么都知道** | 有研究依据的内容保留来源；只是产品经验法则的，就明确说是 heuristic。文献没有精确阈值时，不自己造一个。 |
| **先看这个孩子** | 月龄规范是参考，不是说明书。有个人历史数据时，优先看孩子自己的 baseline 和变化。 |
| **先看现实能不能做到** | daycare、工作、接送、家庭偏好都属于问题本身，不是给完建议以后再处理的“例外”。 |
| **尽量一次只改一件事** | 比起同时重做整套作息，更倾向于提出一个小调整、观察几天，再决定要不要继续。 |
| **数据可选，但很有价值** | 没有 tracker 也能开始；有持续睡眠历史时，更适合做真正的纵向、个体化分析。 |
| **和专业支持互补** | LullSense 想帮助的是专业服务周围的空档，而不是声称 AI 可以替代专业人士的经验、判断和人与人支持。 |

---

## 适用范围

当前 public alpha 的主要支持范围是：

- **4–36 个月：** 睡眠习惯、作息、入睡、夜醒、小睡、早醒等非医疗问题。
- **4 个月以下：** 不提供 sleep training 或结构化作息优化，只提供安全睡眠相关信息和必要的安全提醒。

这并不意味着“4 个月以后所有睡眠问题都适合自己处理”。如果对话中出现需要专业评估的情况，安全规则始终优先于睡眠建议。

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

项目级安装会放到项目对应的 agent skills 目录；全局安装使用共享的 `~/.agents/skills/lullsense/`，再链接到相应 agent 的 skill 目录。以 Claude Code 为例，会链接到 `~/.claude/skills/lullsense/`。

安装以后，直接用自然语言问宝宝睡眠问题即可。

### 可选：安装分析引擎

如果想使用结构化睡眠日志分析、longitudinal review 和 timing prediction，可以再安装 Python engine：

```bash
# public alpha：目前尚未发布到 PyPI
pip install "git+https://github.com/Kavender/lullsense.git"
```

安装后提供：

```bash
lullsense-analyze
lullsense-experiment
```

如果已经 clone 了仓库：

```bash
git clone https://github.com/Kavender/lullsense.git
cd lullsense
pip install .
```

> **当前状态：public alpha。** 核心流程已经实现，并有 CI / eval 覆盖。安全内容以权威来源为基础，并做了来源校验，但**还没有完成独立的儿科睡眠 / 临床专家审阅**。来源核验不等于临床审阅；后者仍然是 stable release 前的重要步骤。

---

## 数据和隐私

LullSense 自己没有云端后台。

本地只会保存少量跨会话有用的状态，例如：

- 孩子的生日 / 月龄信息
- 明确保存的长期家庭约束
- 当前正在尝试的小实验

**原始睡眠记录不会被写入 LullSense 的本地状态。**

第一次保存信息时会明确告知用户；记忆可以关闭，已经保存的状态也可以查看或删除。

需要特别说明的是：**LullSense 运行在你选择的 AI agent / 模型里面。**  
因此，你在对话里输入的内容、主动提供的睡眠日志，以及连接工具返回的数据，仍可能由你所使用的 AI 模型提供方按照它自己的隐私政策处理。

更完整的数据边界见 [`DATA_HANDLING.md`](DATA_HANDLING.md)。

---

## 知识和证据是怎么组织的

LullSense 不把“论文里写的”“专业机构建议的”和“睡眠支持实践里常用的经验”混成一件事。

当前知识库分成四层：

| 层级 | 主要内容 | 怎么使用 |
|---|---|---|
| **A · Safety** | 安全睡眠、风险信号、低月龄安全边界 | 只接受指南、专业共识或系统综述等较高等级来源；安全规则优先级最高。 |
| **B · Development** | 睡眠时长、发育变化、nap transition、正常差异 | 用来提供背景和参考范围，不直接拿群体平均值给单个孩子定作息。 |
| **C · Behavioral** | bedtime、night waking、settling、sleep-training approaches | 尽量基于系统综述 / 睡眠医学文献，同时尊重家庭对不同方法的偏好。 |
| **D · Practice** | 怎么问问题、怎么处理现实约束、怎么复盘和支持家长 | 这部分属于实践方法，不冒充医学证据；经验规则会明确标注。 |

目前知识库包含 **56 条 claims、34 个 sources**，并通过 `scripts/validate_knowledge.py` 做 schema、来源和安全规则校验。

---

## 安全边界

LullSense 的安全设计不是在每句话后面加一句“请咨询医生”，而是尽量把边界放在真正需要的地方：

- **不诊断、不治疗、不替代儿科医疗。**
- 出现明确风险信号时，**暂停普通睡眠建议**，优先提醒家长寻求合适的专业帮助。
- 安全结论只能来自预先核验的权威来源，不能临时搜到一篇网页就当安全依据。
- wake window、schedule threshold、signal severity 等如果属于产品 heuristic，会明确这样标注。
- 对家长已经明确提到的疾病或状况，可以做一般性的教育说明，但不会反推“你家孩子就是这个问题”。
- LullSense 的对话方式本身也是一个需要真实家长和专业人士共同检验、不断修改的产品假设。

---

## 工作原理

LullSense 分成两部分：

1. **Sleep support reasoning**：负责对话、理解家庭情境、形成假设、结合证据，并给出一个现实可行的小调整。
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
                                  继续观察
```

仓库里的实现大致是：

```text
skills/lullsense/SKILL.md
   │
   ├─ references/*.md        16 份按需加载的参考资料
   ├─ knowledge/*.yaml       带版本的 claims / sources / heuristics
   │
   └─ baby_sleep/            可选、vendor-neutral 的纯 Python 分析引擎
        ├─ contract/         统一睡眠数据结构与 provenance
        ├─ ingest/           manual / CSV / JSON / Huckleberry export
        ├─ analyze/          特征提取 + personal baseline
        ├─ detect/           baseline-relative signal detectors
        ├─ review/           最近睡眠变化回顾
        ├─ predict/          下一次 nap / bedtime 范围预测
        └─ store/            profile / constraints / experiments
```

分析引擎和知识校验是 deterministic、可检查的；对话和支持部分由 LLM 驱动，但它使用的 reasoning framework、证据来源和 eval 标准都放在仓库里公开。

LullSense 的核心不依赖某一个 sleep tracker 或模型提供商。CSV、JSON、MCP，以及未来其他睡眠数据源，都应该只是可以替换的 adapter，而不是把整个产品绑在某一家厂商上。

---

## 希望和专业人士一起把它做得更好

LullSense 现在仍然处在 public alpha。

工程可以帮助我们测试代码、核验引用、做 eval，但**“什么才是真正好的睡眠支持”并不是单靠工程就能回答的问题。**

所以我们特别欢迎来自以下专业人士的指正：

- 婴幼儿睡眠顾问 / sleep consultant
- 儿科医生和其他儿童健康专业人士
- 儿童睡眠研究者
- postpartum doula / newborn care specialist
- 长期和真实家庭一起工作的育儿专业人士

我们尤其想听这些反馈：

- 哪些回答在真实咨询里真的有帮助？
- 哪些说法听起来合理，却可能误导家长？
- 哪些情况应该更早停止普通睡眠优化，转向专业评估？
- AI 适合承担哪些两次咨询之间的辅助工作？
- 哪些事情应该明确留给专业人士？
- LullSense 能不能帮助整理 sleep log、追踪方案执行、准备 follow-up，而不是干扰顾问和家长之间的关系？

我们并不认为 AI 可以替代好的专业支持。

我们更希望和真正做这件事的人一起找到合适的边界：

**让工具承担它擅长的部分，把真正需要经验、判断和人与人支持的部分留给专业人士。**

专业 review、批评、合作、workflow / integration 想法都非常欢迎。

---

## 仓库结构

| 路径 | 内容 |
|---|---|
| `skills/lullsense/` | Agent Skill 本体：`SKILL.md`、references、knowledge |
| `baby_sleep/` | 可选 Python analysis engine |
| `scripts/` | knowledge validator 和 CLI 入口 |
| `evals/` | detector / review eval、support rubric、安全测试场景 |
| `examples/` | 合成睡眠数据示例 |
| `tests/` | 自动化测试；push / PR 时由 GitHub Actions CI 执行 |
| `assets/` | Logo 与品牌素材 |

---

## 贡献与社区

Issue、PR、专业 review，以及来自家长和 builder 的真实使用反馈，都非常欢迎。

代码贡献需要 **DCO sign-off**（`git commit -s`），详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

医疗 / 安全内容需要经过人工审核。请保持示例和测试数据为 synthetic：请不要提交真实儿童的睡眠记录、姓名或其他敏感家庭信息。

贡献者需要遵守几条底线：

- 不编造引用或阈值
- 安全结论只能来自权威、已核验的来源
- `python scripts/validate_knowledge.py` 必须通过

---

## License

**Apache-2.0**

见 [`LICENSE`](LICENSE) 和 [`NOTICE`](NOTICE)。

LullSense 不复制商业睡眠产品或私人顾问的专有内容；公开实践资料只做归纳，并尽可能保留来源与证据边界。
