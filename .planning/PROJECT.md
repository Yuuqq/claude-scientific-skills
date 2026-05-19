# claude-scientific-skills

## What This Is

一个面向科研人员（用 Claude 做研究的博士/教授）的 Claude Code 技能市场（plugin marketplace），目前包含 67 个科学类 skill，覆盖科学写作、机器学习、数据分析等领域。本次工作的目标是把这批存量技能从"参差不齐"打磨成"对科研人员真正实用的好技能"——让科研人员可以放心地把这些 skill 用在真实研究产出上。

## Core Value

**任何一个 skill 拿出来，科研人员都能放心用在真实研究产出上**——内容经得起审稿人推敲，代码不会跑到一半崩，描述能让 Claude 在该用的时候正确触发。如果其它一切都失败，这一条必须成立。

## Requirements

### Validated

<!-- 已发布并被证明有价值。 -->

- ✓ 插件市场架构（marketplace.json + 声明式 skill 加载）— existing
- ✓ Skill 标准化目录结构（SKILL.md / references/ / scripts/ / assets/）— existing
- ✓ 67 个 skill 已具备基础内容骨架 — existing

### Active

<!-- 当前阶段范围。本次工作要交付的内容。 -->

- [ ] 制定一份"好 skill"的结构化验收 rubric，覆盖 4 个维度：学术严谨性、真实场景覆盖、清晰可发现、代码可运行
- [ ] rubric 来源以外部调研为基础（Anthropic 官方 skill 规范 + 优秀社区 skill + 科研工具质量标准）+ 项目现状交叉验证
- [ ] 用 rubric 对全部 67 个现有 skill 做静态审计，每个 skill 输出问题清单 + 严重程度分级
- [ ] 根据审计结果集中修复存量 skill，直到全部通过 rubric
- [ ] 在审计中识别"不该存在"的 skill（质量过低、重复、过时）并执行合并或删除
- [ ] 修复后用同一份 rubric 重新验收，所有保留的 skill 必须通过

### Out of Scope

<!-- 显式排除项，附理由。 -->

- 新增 skill — 本次只改造存量，新增不在范围内
- 实际运行 scripts/ 验证代码（在隔离环境装依赖跑通）— 仅做静态检查，等到具体修复阶段如有必要再单独评估
- 端到端真实科研任务回归测试 — 验收方式选定为结构化 checklist，不做 E2E 任务级验证
- 领域内技术栈大改（重新选 Python 库、改写文档结构等）— 本次专注"质量提升"而非"重构"
- 国际化 / 多语言 SKILL.md — 现状是英文为主，不在本次范围

## Context

- **代码库性质**：纯文档/内容仓库，没有运行时也没有编译产物。Claude 通过 marketplace.json 按需加载 SKILL.md 作为 prompt context。
- **现状底班未知**：67 个 skill 的实际质量分布不清楚——这正是为什么"先全面审计再集中修复"是合理的策略。审计本身会产出关键信息，决定后半段工作量。
- **codebase 已映射**：`.planning/codebase/` 下已有 ARCHITECTURE.md、STACK.md、CONVENTIONS.md、CONCERNS.md 等，可作为审计起点参考。
- **科研用户的零容忍性**：科研人员不像普通工程用户——一个统计方法用错、一个公式有误、一个引用过时，整篇论文都可能受牵连。这决定了"学术严谨性"维度的判定必须谨慎。
- **rubric 是杠杆点**：所有后续工作都以 rubric 为标尺。rubric 写得粗糙，审计结果就不可信，修复也无方向。这是项目的最高杠杆环节。

## Constraints

- **Tech stack**: 不引入新的运行时依赖 — 项目本质是文档仓库，保持轻量
- **决策模式**: Claude 自动审计 + 修复，用户在关键节点抽查 — 不要求逐个 skill 人工过目，但 rubric 起草 / 严重 bug 修复 / 删除决策 等节点需用户确认
- **审计验证深度**: 仅静态检查代码（语法、import、明显 bug）— 不在隔离环境实际运行，避免依赖管理与环境配置成本
- **范围弹性**: 67 个 skill 的范围不锁死 — 审计中识别出的低质量/重复 skill 允许合并或删除
- **领域平等**: 不预设领域优先级 — 67 个 skill 一视同仁，不优先 ML 或写作

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 只改造存量、不新增 skill | 用户明确表示"让这些技能变成好技能"，焦点是质量提升而非覆盖扩展 | — Pending |
| 4 维 rubric（严谨性 / 场景 / 可发现性 / 可运行性）全部必须项 | 用户在 4 个维度全选，意味着任一维度未达标都算不合格 | — Pending |
| rubric 先做外部调研再起草 | 避免闭门造车，参考 Anthropic 官方规范和优秀社区案例 | — Pending |
| 代码可运行性仅做静态检查 | 平衡审计成本与验证深度；如静态检查发现疑点再考虑实跑 | — Pending |
| 全量审计先于集中修复 | 修复策略需要全局问题分布作输入；先审计才能合理排序与分批 | — Pending |
| 允许审计中合并/删除 skill | 范围弹性能让最终结果更聚焦，避免为低价值内容投入 | — Pending |
| 决策模式 = Claude 自动 + 用户抽查 | 67 个 skill 全人工过目成本过高；但关键决策节点（rubric / 删除 / 大改）必须用户确认 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-20 after initialization*
