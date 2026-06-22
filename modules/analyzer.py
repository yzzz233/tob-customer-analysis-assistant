# 客户规则分析模块
# 负责根据客户行业、规模、痛点和现有系统，生成初步分析结果
# 以下规则为项目演示用的初始规则，用于模拟 ToB 客户初步判断，不代表正式行业标准


# 从原始客户数据中提取参与分析的核心字段
def build_analysis_input(customer):
    analysis_input = {
        "name": customer["name"],
        "industry": customer["industry"],
        "employee_count": customer["employee_count"],
        "pain_point": customer["pain_point"],
        "current_system": customer["current_system"]
    }

    return analysis_input

# 项目演示规则：根据客户规模、行业、现有系统和痛点做初步判断
# 其中客户规模阈值、数字化成熟度判断和系统推荐方向，后续可根据真实业务调整
def rule_analyze_customer(customer):
    result = {}

    employee_count = customer["employee_count"]
    industry = customer["industry"]
    pain_point = customer["pain_point"]
    current_system = customer["current_system"]

    # 1. 客户等级判断
    if employee_count >= 300:
        result["customer_level"] = "高"
    elif employee_count >= 100:
        result["customer_level"] = "中"
    else:
        result["customer_level"] = "低"

    # 2. 推荐版本判断
    if employee_count >= 100:
        result["recommended_version"] = "企业版"
    else:
        result["recommended_version"] = "基础版"

    # 3. 数字化成熟度判断
    if "Excel" in current_system or "微信群" in current_system or "表格" in current_system:
        result["digital_maturity"] = "低"
    elif "进销存" in current_system or "CRM" in current_system:
        result["digital_maturity"] = "中"
    else:
        result["digital_maturity"] = "未知"

    # 4. 推荐系统方向
    if industry == "制造":
        result["recommended_system"] = "MES / WMS / ERP"
    elif industry == "电商":
        result["recommended_system"] = "WMS / CRM / AI客服"
    elif industry == "教育":
        result["recommended_system"] = "AI知识库 / AI客服 / CRM"
    else:
        result["recommended_system"] = "通用SaaS系统 / AI知识库"

    # 5. 实施难度判断
    if result["customer_level"] == "高" and result["digital_maturity"] == "低":
        result["implementation_difficulty"] = "高"
    elif result["customer_level"] == "中":
        result["implementation_difficulty"] = "中"
    else:
        result["implementation_difficulty"] = "低"

    # 6. 核心痛点
    result["priority_pain_point"] = pain_point

    # 7. 售前沟通问题清单
    if industry == "制造":
        result["follow_up_questions"] = [
            "当前是否已有 ERP、进销存或生产管理系统？",
            "库存数据是否能实时更新？",
            "生产进度目前由谁维护，是否依赖人工表格？",
            "是否存在订单、库存、生产数据不同步的问题？"
        ]
    elif industry == "电商":
        result["follow_up_questions"] = [
            "当前订单主要来自哪些平台？",
            "是否存在多平台订单统一管理问题？",
            "客服问题是否有大量重复咨询？",
            "库存和订单是否能自动同步？"
        ]
    elif industry == "教育":
        result["follow_up_questions"] = [
            "学员问题主要集中在哪些类型？",
            "是否已有 FAQ 或知识库文档？",
            "老师或客服每天需要重复回答多少问题？",
            "是否希望通过 AI 客服降低人工答疑压力？"
        ]
    else:
        result["follow_up_questions"] = [
            "当前主要业务流程是如何管理的？",
            "是否存在大量人工录入或重复沟通？",
            "是否已有系统沉淀业务数据？",
            "最希望优先解决的问题是什么？"
        ]

    # 8. 下一步跟进建议
    if industry == "制造":
        result["next_action"] = "建议先梳理库存、生产、订单三个核心流程，确认是否需要优先建设 MES / WMS / ERP。"
    elif industry == "电商":
        result["next_action"] = "建议先梳理订单、库存、客服三个环节，评估是否需要 WMS、CRM 或 AI客服能力。"
    elif industry == "教育":
        result["next_action"] = "建议先整理高频学员问题和现有资料，评估是否适合建设 AI知识库或 AI客服。"
    else:
        result["next_action"] = "建议先进行业务流程访谈，明确核心痛点和优先数字化场景。"

    return result
