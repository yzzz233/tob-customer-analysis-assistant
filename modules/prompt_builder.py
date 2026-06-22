# Prompt 构造模块
# 负责将客户信息和规则分析结果组织成 DeepSeek 可理解的提示词

# 构造发送给 DeepSeek 的客户分析 Prompt
def build_prompt(customer_info, rule_analysis):
    questions_text = ""

    # 将售前问题列表转换成编号文本，便于放入 Prompt
    for index, question in enumerate(rule_analysis["follow_up_questions"], start=1):
        questions_text += f"{index}. {question}\n"

    prompt = f"""
    你是一名ToB软件实施/售前支持助理。
    请根据以下客户信息和规则分析结果，生成一份客户需求分析报告。

    【客户信息】
    公司名称：{customer_info["name"]}
    行业：{customer_info["industry"]}
    员工人数：{customer_info["employee_count"]}
    当前痛点：{customer_info["pain_point"]}
    现有系统：{customer_info["current_system"]}

    【规则分析结果】
    客户等级：{rule_analysis["customer_level"]}
    数字化成熟度：{rule_analysis["digital_maturity"]}
    实施难度：{rule_analysis["implementation_difficulty"]}
    推荐系统方向：{rule_analysis["recommended_system"]}
    核心痛点：{rule_analysis["priority_pain_point"]}
    下一步建议：{rule_analysis["next_action"]}

    【售前沟通问题】
    {questions_text}

    请输出以下内容：
    1. 客户现状分析
    2. 核心痛点分析
    3. 推荐系统方向
    4. 实施风险或难点
    5. 下一步跟进建议

    要求：
    - 语言自然，适合售前、实施、客户成功人员阅读
    - 不要编造客户没有提供的信息
    - 如果信息不足，请指出需要补充调研的问题
    - 只输出指定的五个部分，不要增加报告日期、分析人员等额外模板字段
    """
    return prompt