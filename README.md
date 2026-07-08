# Unitree A1 仿真控制公开展示

这是一个面向作品集和中文岗位投递的 sanitized showcase 仓库，用 Unitree A1 主题的合成数据展示机器人仿真控制项目的工程表达方式：日志生成、字段校验、指标计算、MPC 风格诊断、图表生成、测试和对外说明。

所有 CSV、指标和图表均为 synthetic demo artifacts。它们用于说明可复现分析流程，不代表真实硬件性能，不披露原始非公开项目代码或数据。

## English Summary

This is a sanitized, runnable Unitree A1 robotics simulation-control showcase. It demonstrates synthetic log generation, parser validation, metrics, MPC-style diagnostics, plotting, tests, and interview-ready documentation. The repository does not claim real hardware results and does not include non-public source code, raw logs, checkpoints, SDK integrations, credentials, or internal paths.

## 这个仓库是什么

- 一个可运行的公开展示库，用于说明机器人项目中的数据接口、分析流程和工程边界。
- 一套 deterministic synthetic Unitree A1 600-step demo logs。
- 一个带 schema 校验的 CSV parser，缺字段时会给出明确错误。
- 一组 demo metrics：前向位移、速度跟踪误差、base height、姿态、MPC accept/reject、predicted support force、cost trend、contact duty factor 和运行时长。
- 一套可复现图表，适合面试或作品集讲解。
- 一组测试，覆盖 parser、metrics、pipeline smoke、600-step 字段和 model name 一致性。

## 这个仓库不是什么

这个仓库不是原始科研或实习代码库，不包含 Isaac、ROS、Unitree SDK、真实机器人日志、checkpoint、原始求解器代码、机器本地路径、凭据或内部服务细节。`src/a1_showcase/simple_sim.py` 是简化展示模拟，不是真实 Unitree A1 动力学模型。

## 展示页

GitHub Pages 入口：

https://zihanshen29.github.io/robot-a1-showcase/

展示页包含候选人信息、关键 synthetic/demo 指标卡片、3 张主要图表、毕设进度 Mermaid Gantt、GitHub 文档链接和统一 Showcase Series footer。

## Verified project metrics (thesis scope)

以下为毕设实测指标的文字引用；本仓库生成的 CSV、JSON 和图表仍为 synthetic demo artifacts，不与这些实测数字混作同一数据源。

| Metric | Verified thesis-scope value |
| --- | --- |
| 600-step corrected replay | PPO `model_298.pt` +0.9338 m; hardcoded diagonal-trot baseline +0.9339 m; MPC defaults +0.7915 m |
| 1200-step pressure test | Policy and baseline both failed around 872 steps, pointing to a shared control-stack issue rather than a pure RL issue |
| Root-cause chain | yaw drift about 0.9 deg/step without anchor -> CoM projection drift along FL-to-RR support line (corr=0.98) -> roll/pitch recovery degradation -> FR frictionCone cost spike -> solver rejection -> fall |
| Yaw-anchor experiment | Survived 1199 steps, but accept was only 164/1199, so it was treated as a failed branch: longer survival did not mean healthier control |
| Debugging scale | 16 training-system debugging iterations; key finding: `mpc_rate_div` from 6 to 1 |
| Implementation scale | About 2,500 lines of custom code; 80+ analysis scripts; 112 CSV files; 50+ documents |
| Control setup | 50 Hz control, 0.005 s physics step, 54-D observation with MPC health, 5-D gait action, 35-step MPC contact preview of about 0.7 s, Windows-to-WSL2 TCP bridge, Crocoddyl FDDP |

口径纪律：600 steps 是短时域验证，1200 steps 是压力测试；不能把该结果表述为通用四足行走已解决，也不能暗示实机部署。

## 架构

```mermaid
flowchart LR
    G["Simplified Unitree A1 Demo Simulation"] --> A["Synthetic / Sanitized Unitree A1 Logs"]
    A --> B["Log Parser"]
    B --> C["Metrics Module"]
    C --> D["Plot Generator"]
    D --> E["Demo Figures"]
    B --> H["MPC Diagnostics Summary"]
    E --> F["Interview Notes"]
```

## 状态矩阵

| 能力 | 本仓库包含 | 边界 |
| --- | --- | --- |
| Unitree A1 demo data | 是，synthetic CSV logs | 不是真实硬件遥测 |
| 日志解析 | 是，带 schema 校验 | 不是非公开日志格式解析器 |
| MPC 诊断 | 是，accept/reject、cost、support-force 风格字段 | 不是生产 MPC 求解器 |
| 图表 | 是，600-step demo plots | 不是实验结果 |
| 长时域运动稳定性 | 作为限制讨论 | 不宣称已解决 |
| 真实机器人验证 | 明确不在范围内 | 无硬件部署声明 |
| 开门任务 | 作为未来/边界上下文讨论 | 未实现、未评估 |

## 快速开始

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[test]"
python scripts\generate_sample_data.py
python scripts\run_demo_pipeline.py
pytest
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
python scripts/generate_sample_data.py
python scripts/run_demo_pipeline.py
pytest
```

## Demo Pipeline

1. `scripts/generate_sample_data.py` 在 `data/sample_logs/` 下创建 deterministic CSV logs。
2. `scripts/parse_logs.py` 校验必需字段，并写出 `outputs/metrics/parsed_summary.csv`。
3. `scripts/run_demo_pipeline.py` 计算指标并写出 A1 figures。
4. `pytest` 检查 parser、metrics、600-step 数据字段、model-name 一致性和端到端 smoke 行为。

## 生成图表

A1 pipeline 会在 `outputs/figures/` 下写出以下图表：

- `a1_600_step_forward_displacement.png`
- `a1_base_height.png`
- `a1_roll_pitch.png`
- `a1_mpc_accept_reject.png`
- `a1_predicted_support_force.png`
- `a1_cost_trend.png`
- `a1_velocity_tracking.png`
- `a1_metrics_summary.png`

展示页使用 `docs/images/` 中复制的 3 张关键图：forward displacement、MPC accept/reject、cost trend。页面说明聚焦数据接口、指标计算、诊断图表和工程复盘。

## 仓库结构

```text
robot-a1-showcase/
|-- README.md
|-- pyproject.toml
|-- requirements.txt
|-- data/
|   |-- README.md
|   `-- sample_logs/
|-- docs/
|   |-- images/
|   |-- architecture.md
|   |-- a1_interview_all_questions_zh.html
|   |-- a1_interview_core_concepts_zh.html
|   |-- index.html
|   |-- interview_talking_points.md
|   |-- limitations_and_ethics.md
|   `-- project_overview.md
|-- src/
|   `-- a1_showcase/
|-- scripts/
|-- tests/
`-- outputs/
```

## 面试讲解重点

- 我把一个不适合直接公开的 Unitree A1 仿真控制项目，整理成了可运行、可测试、可解释的公开 showcase。
- 核心工程链路是：生成或接收日志，校验字段，计算指标，可视化诊断，并用测试保护流程。
- 600-step 图表便于快速检查 tracking、base-height、support-force、cost 和 accept/reject 行为；毕设实测口径中 PPO 为 +0.9338 m，hardcoded baseline 为 +0.9339 m。
- MPC accept/reject 与 predicted support-force 图能把高层 gait intent 和 feasibility-style diagnostics 联系起来。
- 1200-step pressure test 的关键结论是约 872 step 共同失败窗口，后续优化方向在共享控制栈与 MPC 侧，而不是简单归因 RL。
- 项目对边界保持诚实：长时域鲁棒性、真实机器人验证和开门任务迁移都没有在这个公开 demo 中宣称完成。
- 如果未来有可公开的 Unitree A1 或仿真器日志，可以在脱敏审查后复用同一 parser contract 接入。

## 限制与合规

本仓库避免不受支持的性能声明，不把 synthetic metrics 包装成真实实验，不包含非公开实现细节，也不暗示实机部署。目标是展示工程判断、分析结构、可复现性和沟通质量，同时保护源项目。
