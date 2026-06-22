# ToB客户需求分析与方案推荐助手

## 项目简介

本项目是一个面向 ToB 售前支持、软件实施和客户成功场景的客户需求分析与方案推荐 AI 应用工程实践项目。

项目模拟企业在售前/实施阶段对客户进行结构化分析的流程，用于解决客户信息分散、方案依赖人工经验、分析标准不统一等问题。系统从 JSON 或 Excel 文件读取客户资料，先通过本地规则生成客户等级、数字化成熟度、实施难度、推荐系统方向和售前沟通问题，再调用 DeepSeek API 生成自然语言客户分析报告，最终将结构化分析结果与 AI 报告保存为 JSON 文件。

本项目用于模拟真实 ToB 业务场景中的客户初步分析流程。代码中的客户分层阈值、数字化成熟度判断和系统推荐规则为项目演示规则，不代表正式行业标准，后续可结合真实业务数据和行业经验持续优化。

## 项目亮点

- 模拟 ToB 售前 / 实施阶段的客户分析业务流程
- 采用“本地规则分析 + 大模型生成”的混合架构
- 支持 JSON / Excel 多数据源客户信息输入
- 将数据读取、规则分析、Prompt 构造、API 调用和报告输出拆分为独立模块
- 使用 DeepSeek API 生成自然语言客户需求分析报告
- 使用环境变量管理 API Key，避免将密钥写入代码

## 项目功能

- 支持读取 JSON 和 Excel 格式的客户数据，适配常见客户信息整理方式
- 提取客户名称、行业、员工人数、当前痛点和现有系统等关键字段
- 基于本地演示规则生成结构化客户分析结果：
  - 客户等级
  - 推荐版本
  - 数字化成熟度
  - 实施难度
  - 推荐系统方向
  - 核心痛点
  - 售前沟通问题
  - 下一步跟进建议
- 根据客户信息和规则分析结果构造 Prompt
- 调用 DeepSeek API 生成自然语言客户分析报告
- 将客户信息、规则分析结果和 AI 报告写入 `customer_report.json`

## 技术栈

- Python
- Requests
- OpenPyXL
- JSON
- DeepSeek Chat Completions API

## 项目结构

```text
09_ToB客户需求分析与方案推荐助手_v1.0项目拆分版/
├── modules/
│   ├── __init__.py
│   ├── analyzer.py          # 客户字段提取和本地规则分析
│   ├── data_loader.py       # JSON / Excel 数据读取
│   ├── deepseek_client.py   # DeepSeek API 调用
│   ├── prompt_builder.py    # Prompt 构造
│   └── report_writer.py     # 报告结构组合和 JSON 写入
├── .env.example             # API Key 环境变量示例，不包含真实密钥
├── .gitignore
├── customers.json           # JSON 输入示例
├── customers.xlsx           # Excel 输入示例
├── customer_report.json     # 程序输出文件
├── main.py                  # 项目主入口
├── requirements.txt         # Python 依赖
└── README.md
```

## 运行方式

### 1. 进入项目目录

```bash
cd 04_项目实战/09_ToB客户需求分析与方案推荐助手_v1.0项目拆分版
```

### 2. 安装依赖

运行项目前需要安装 `requirements.txt` 中的依赖：

```bash
pip install -r requirements.txt
```

### 3. 设置 DeepSeek API Key

程序通过环境变量 `DEEPSEEK_API_KEY` 读取 API Key，请勿将真实 API Key 直接写入 Python 代码或提交到 GitHub。

`.env.example` 只是环境变量格式示例：

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

该文件不包含真实 API Key。当前项目不会自动加载 `.env` 文件，需要在运行程序的终端中设置环境变量。

Windows 用户环境变量：

在系统环境变量中新增用户变量：

变量名：
DEEPSEEK_API_KEY

变量值：
你的真实 DeepSeek API Key

设置完成后，重新打开 CMD / PowerShell / Cursor 终端。

也可以在当前 CMD 窗口临时设置：
```cmd
set DEEPSEEK_API_KEY=你的真实_API_Key
```

Windows PowerShell：

```powershell
$env:DEEPSEEK_API_KEY="你的真实_API_Key"
```

Linux / macOS：

```bash
export DEEPSEEK_API_KEY="你的真实_API_Key"
```

### 4. 选择输入文件

在 `main.py` 的配置区设置输入文件：

```python
INPUT_FILE = "customers.json"
```

使用 Excel 时改为：

```python
INPUT_FILE = "customers.xlsx"
```

### 5. 运行项目

```bash
python main.py
```

程序运行完成后，会在当前目录生成或覆盖：

```text
customer_report.json
```

## 输入数据格式

每个客户需要包含以下字段：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `name` | 客户名称 | 重庆某制造公司 |
| `industry` | 所属行业 | 制造 |
| `employee_count` | 员工人数 | 500 |
| `pain_point` | 当前主要痛点 | 库存管理混乱，生产进度不透明 |
| `current_system` | 当前使用的系统或管理方式 | Excel手工管理 |

### JSON 示例

```json
[
    {
        "name": "重庆某制造公司",
        "industry": "制造",
        "employee_count": 500,
        "pain_point": "库存管理混乱，生产进度不透明",
        "current_system": "Excel手工管理"
    }
]
```

### Excel 格式

Excel 第一行必须是字段名，后续每一行代表一个客户。字段名应与 JSON 格式一致：

```text
name | industry | employee_count | pain_point | current_system
```

当前代码读取工作簿中的活动工作表。

## 输出结果说明

输出文件为 `customer_report.json`，每个客户的报告包含三部分：

- `customer_info`：参与分析的客户信息
- `rule_analysis`：本地规则生成的结构化分析结果
- `ai_report`：DeepSeek API 生成的自然语言报告

示例结构：

```json
[
    {
        "customer_info": {
            "name": "重庆某制造公司",
            "industry": "制造",
            "employee_count": 500,
            "pain_point": "库存管理混乱，生产进度不透明",
            "current_system": "Excel手工管理"
        },
        "rule_analysis": {
            "customer_level": "高",
            "recommended_version": "企业版",
            "digital_maturity": "低",
            "recommended_system": "MES / WMS / ERP",
            "implementation_difficulty": "高",
            "priority_pain_point": "库存管理混乱，生产进度不透明",
            "follow_up_questions": [
                "当前是否已有 ERP、进销存或生产管理系统？",
                "库存数据是否能实时更新？",
                "生产进度目前由谁维护，是否依赖人工表格？",
                "是否存在订单、库存、生产数据不同步的问题？"
            ],
            "next_action": "建议先梳理库存、生产、订单三个核心流程，确认是否需要优先建设 MES / WMS / ERP。"
        },
        "ai_report": "DeepSeek 生成的自然语言客户分析报告"
    }
]
```

示例仅用于说明输出结构，实际内容取决于输入数据、本地规则和 API 返回结果。

## 项目流程

项目整体采用“数据读取 → 规则分析 → Prompt 构造 → 大模型生成 → 报告输出”的处理链路：

```text
读取 JSON / Excel 客户数据
        ↓
提取参与分析的客户字段
        ↓
执行本地演示规则分析
        ↓
构造 DeepSeek Prompt
        ↓
调用 DeepSeek API
        ↓
组合结构化结果与自然语言报告
        ↓
写入 customer_report.json
```

如果某个客户的 API 调用失败，该客户不会被加入最终报告，程序会继续处理后续客户。

## 后续优化方向

- 增加输入字段完整性和数据类型校验
- 完善空 Excel、异常表头和接口返回格式异常的处理
- 将客户分层阈值、行业规则和系统推荐规则迁移到独立配置文件
- 增加 API 请求超时、重试和更完整的错误处理
- 支持自动加载本地 `.env` 配置
- 增加单元测试和更多输入样例
- 后续可接入行业方案文档或产品资料，结合 RAG 生成更贴近业务场景的客户分析报告
- 根据真实客户沟通和项目交付经验，持续优化规则分析逻辑和 Prompt
