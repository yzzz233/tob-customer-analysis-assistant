# AI辅助的ToB客户跟进分析与售前建议工具

## 项目简介

本项目是一个面向 ToB 客户成功、售前支持、实施助理场景的小型 AI 辅助工具。

它用于处理客户跟进记录：从 JSON / Excel 读取客户数据，导入 SQLite 数据库，对客户信息完整度进行检查，并调用 DeepSeek API 生成售前跟进建议。项目重点不是替代 CRM 系统，而是帮助销售、客户成功或售前人员在下一次沟通前快速梳理客户信息、发现缺失字段、准备追问问题和跟进方向。

当前示例数据均为模拟数据，不包含真实客户信息。

## 业务场景

在 ToB 售前和客户成功工作中，客户跟进信息常常分散在 Excel、JSON、CRM 备注或人工记录中。售前人员需要快速判断：

- 客户当前可能遇到什么业务问题；
- 客户信息是否足够完整；
- 哪些关键信息还需要继续确认；
- 这个客户是否值得优先跟进；
- 当前是否适合进入方案沟通阶段。

本项目围绕这些轻量场景构建，适合作为客户跟进分析、售前沟通准备、实施前需求初筛的 AI 工程练习项目。

## 核心功能

- 支持从 JSON / Excel 读取客户跟进数据；
- 支持将客户数据导入 SQLite 的 `customers` 表；
- 导入时根据 `customer_name + follow_up_note` 做简单去重；
- 支持按 `customer_id` 分析单个客户；
- 支持按 `customer_name` 分析单个客户；
- 支持批量分析全部客户；
- 支持客户信息完整度检查，输出 `known_fields`、`missing_fields`、`completeness_level`；
- 调用 DeepSeek API 生成可能痛点、跟进优先级、缺失信息、下一步追问问题、下一步跟进建议、是否适合进入方案阶段；
- 将分析结果保存到 SQLite 的 `analysis_reports` 表；
- 在 `data/customer_analysis_report.json` 生成 JSON 报告。

## 项目结构

```text
10_ToB客户跟进分析与售前建议助手 v1.1/
├── data/
│   ├── customers.json                  # JSON 示例客户数据
│   ├── customers.xlsx                  # Excel 示例客户数据
│   ├── customers.db                    # SQLite 数据库
│   └── customer_analysis_report.json   # 分析结果 JSON 报告
├── modules/
│   ├── __init__.py
│   ├── customer_analyzer.py            # 客户分析流程调度
│   ├── data_loader.py                  # JSON / Excel 数据读取
│   ├── data_quality_checker.py         # 客户信息完整度检查
│   ├── deepseek_client.py              # DeepSeek API 调用与结果解析
│   ├── prompt_builder.py               # AI Prompt 构造
│   ├── report_writer.py                # JSON 报告写入
│   └── sqlite_loader.py                # SQLite 查询、导入、保存报告
├── scripts/
│   ├── init_db.py                      # 初始化数据库和数据表
│   └── import_customers.py             # 导入客户数据到数据库
├── main.py                             # 主程序入口
├── requirements.txt                    # Python 依赖
└── README.md
```

## 技术栈

- Python
- SQLite
- Requests
- OpenPyXL
- JSON
- DeepSeek Chat Completions API

## 使用方式

### 1. 进入项目目录

```bash
cd "04_项目实战/10_ToB客户跟进分析与售前建议助手 v1.1"
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
python scripts/init_db.py
```

该脚本会创建：

- `data/customers.db`
- `customers` 表
- `analysis_reports` 表

### 4. 导入客户数据

默认导入文件为：

```text
data/customers.xlsx
```

运行导入脚本：

```bash
python scripts/import_customers.py
```

如需导入 JSON，可在 `scripts/import_customers.py` 中将 `IMPORT_FILE` 改为：

```python
IMPORT_FILE = os.path.join(BASE_DIR, "data", "customers.json")
```

导入时会根据 `customer_name + follow_up_note` 判断是否重复，重复记录会跳过。

### 5. 运行客户分析

```bash
python main.py
```

运行前可在 `main.py` 中修改 `mode` 变量，选择按 ID、按名称或批量分析：

```python
mode = "all"
```

可选模式：

- `by_id`：按 `customer_id` 分析单个客户；
- `by_name`：按 `customer_name` 分析单个客户；
- `all`：批量分析数据库中的全部客户。

分析完成后，结果会写入：

- SQLite：`analysis_reports` 表；
- JSON 文件：`data/customer_analysis_report.json`。

## 环境变量配置

项目通过环境变量读取 DeepSeek API Key，避免将密钥写入代码。

环境变量名称：

```text
DEEPSEEK_API_KEY
```

Windows PowerShell 示例：

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek API Key"
```

Windows CMD 示例：

```cmd
set DEEPSEEK_API_KEY=你的 DeepSeek API Key
```

Linux / macOS 示例：

```bash
export DEEPSEEK_API_KEY="你的 DeepSeek API Key"
```

以上示例命令通常只在当前终端会话中生效。如需长期生效，可以在操作系统中配置用户级或系统级环境变量。

请勿将真实 API Key 提交到 GitHub。

## 数据字段说明

`customers` 表和示例数据使用以下字段：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `customer_id` | 客户记录 ID，由 SQLite 自动生成 | 1 |
| `customer_name` | 客户名称 | 云仓电商 |
| `industry` | 所属行业 | 电商 |
| `employee_count` | 企业规模 / 员工数量 | 150 |
| `current_system` | 当前已有系统 | ERP / CRM / 进销存 |
| `follow_up_note` | 客户跟进小记 | 客户提到库存经常对不上 |
| `budget` | 预算信息 | 5万以内 |
| `decision_maker` | 决策人或关键角色 | 运营负责人 |
| `timeline` | 计划上线或推进时间 | 两个月内 |
| `sales_stage` | 当前销售阶段 | 初步沟通 / 需求沟通 |

完整度检查会根据这些字段判断：

- `known_fields`：已填写的信息；
- `missing_fields`：缺失的信息；
- `completeness_level`：信息完整度，当前分为 `低`、`中`、`高`。

当前导入去重字段为 `customer_name + follow_up_note`。其中 `follow_up_note` 是 AI 分析客户痛点、判断跟进优先级和生成下一步建议的重要输入，建议尽量记录清楚客户表达的业务问题和沟通背景。

## 示例输出说明

输出文件为：

```text
data/customer_analysis_report.json
```

单个客户的输出结构示例：

```json
{
  "customer_info": {
    "customer_id": 3,
    "customer_name": "云仓电商",
    "industry": "电商",
    "employee_count": null,
    "current_system": null,
    "follow_up_note": "客户提到库存经常对不上，订单处理效率低，想了解有没有系统可以统一管理。",
    "budget": "暂未明确",
    "decision_maker": null,
    "timeline": "一个月内想了解方案",
    "sales_stage": "初步沟通"
  },
  "data_quality": {
    "completeness_level": "中",
    "known_fields": [
      "客户名称",
      "行业",
      "跟进小记",
      "预算",
      "上线时间",
      "销售阶段"
    ],
    "missing_fields": [
      "企业规模",
      "已有系统",
      "决策人"
    ]
  },
  "ai_analysis": {
    "possible_pain_points": [
      "可能痛点1",
      "可能痛点2"
    ],
    "follow_up_priority": "高/中高/中/低",
    "priority_reason": "说明为什么是这个跟进优先级",
    "uncertain_points": [
      "当前还不能判断的信息1"
    ],
    "next_questions": [
      "下一次沟通建议追问的问题1",
      "下一次沟通建议追问的问题2"
    ],
    "next_step_suggestion": "下一步跟进建议",
    "is_ready_for_solution": "是/否/暂不确定",
    "solution_readiness_reason": "说明当前是否适合进入方案沟通阶段"
  }
}
```

实际输出内容会受到输入数据、信息完整度和 DeepSeek API 返回结果影响。

## 项目亮点

- 面向真实 ToB 客户成功 / 售前支持 / 实施助理工作流；
- 使用 SQLite 保存客户数据和分析报告，便于后续扩展查询和展示；
- 支持 Excel 和 JSON 两种常见数据来源；
- 在调用 AI 前先做信息完整度检查，避免在信息不足时直接生成方案；
- Prompt 明确要求 AI 不编造未提供信息，更适合售前沟通准备；
- 输出结构化 JSON，便于后续接入 Web 页面、报表展示或知识库方案生成流程；
- 示例数据为模拟数据，适合作为 GitHub 项目展示和学习练习。

## 后续优化方向

当前版本主要完成了客户跟进数据导入、信息完整度检查和 AI 售前跟进建议生成。后续可以在此基础上继续引入 RAG / 知识库能力，将项目从“客户跟进分析工具”进一步升级为“AI辅助方案推荐工具”。

计划优化方向包括：

1. 建立产品知识库

   将企业常见产品能力、功能模块、适用场景、部署方式、价格区间等信息整理成知识库，让 AI 在分析客户需求时能够结合具体产品能力进行判断。

2. 建立行业方案知识库

   按制造业、教育、电商、零售等行业整理典型痛点、常见系统需求、方案模板和实施关注点，让 AI 能够根据客户行业生成更贴近业务场景的建议。

3. 引入 RAG 检索增强生成

   在调用大模型前，先根据客户行业、痛点和已有系统，从产品知识库和行业方案库中检索相关内容，再交给 AI 生成更有依据的售前建议。

4. 从“跟进建议”升级为“初步方案建议”

   在当前输出可能痛点、跟进优先级、下一步问题的基础上，进一步生成推荐产品方向、适用功能模块、方案思路和实施注意事项。

5. 增加方案生成能力

   支持根据客户信息和知识库内容，生成结构化的初步方案草稿，例如：客户背景、业务痛点、推荐方案、核心功能、实施步骤和后续沟通重点。
