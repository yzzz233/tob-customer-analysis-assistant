import json


def build_follow_up_prompt(customer, data_quality):
    """
    构造 ToB 客户跟进分析 prompt。

    输入：
        customer: 单个客户信息字典，包含行业、预算、跟进小记等字段。
        data_quality: 信息完整度检查结果，包含 known_fields、missing_fields、completeness_level。

    输出：
        可直接发送给 DeepSeek 的 prompt 字符串。

    作用：
        将结构化客户信息和完整度检查结果一起交给 AI，让建议既关注客户上下文，
        也提醒销售 / 售前不要在信息不足时过早生成方案。
    """

    # 将字典格式化为 JSON 文本，能让 AI 清楚区分字段名和字段值，减少误读。
    customer_text = json.dumps(customer, ensure_ascii=False, indent=2)
    data_quality_text = json.dumps(data_quality, ensure_ascii=False, indent=2)

    # prompt 明确角色、分析范围和 JSON 输出格式，便于后续代码稳定解析 AI 返回结果。
    prompt = f"""
      你是一名 ToB 售前支持 / 客户成功顾问。

      现在有一条客户跟进记录，请根据客户基础信息、CRM跟进小记和信息完整度检查结果，
      分析客户当前可能痛点、跟进优先级、缺失信息和下一步沟通建议。

      请注意：
      1. 不要编造未提供的信息。
      2. 如果信息不足，请明确指出需要进一步确认。
      3. 不要直接生成完整解决方案。
      4. 重点是帮助销售、客户成功或售前人员准备下一次沟通。
      5. 输出必须是 JSON 格式，不要输出多余解释文字。

      【客户信息】
      {customer_text}

      【信息完整度检查】
      {data_quality_text}

      请严格按以下 JSON 格式输出：

      {{
        "possible_pain_points": [
          "可能痛点1",
          "可能痛点2"
        ],
        "follow_up_priority": "高/中高/中/低",
        "priority_reason": "说明为什么是这个跟进优先级",
        "uncertain_points": [
          "当前还不能判断的信息1",
          "当前还不能判断的信息2"
        ],
        "next_questions": [
          "下一次沟通建议追问的问题1",
          "下一次沟通建议追问的问题2",
          "下一次沟通建议追问的问题3"
        ],
        "next_step_suggestion": "下一步跟进建议",
        "is_ready_for_solution": "是/否/暂不确定",
        "solution_readiness_reason": "说明当前是否适合进入方案沟通阶段"
      }}
      """

    return prompt
