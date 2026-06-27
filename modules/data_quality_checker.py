def check_data_quality(customer):
    """
    检查单个客户的信息完整度。

    输入：
        customer: 单个客户字典，通常来自 customers 表查询结果。

    输出：
        {
            "completeness_level": "低/中/高",
            "known_fields": [...],
            "missing_fields": [...]
        }

    作用：
        将客户字段分为“已知信息”和“缺失信息”，帮助 AI 判断当前是否适合进入方案沟通。
    """

    # 字段名是数据库和导入文件中的英文 key，中文标签用于报告展示和 prompt 阅读。
    field_labels = {
        "customer_name": "客户名称",
        "industry": "行业",
        "employee_count": "企业规模",
        "current_system": "已有系统",
        "follow_up_note": "跟进小记",
        "budget": "预算",
        "decision_maker": "决策人",
        "timeline": "上线时间",
        "sales_stage": "销售阶段"
    }

    known_fields = []
    missing_fields = []

    for field, label in field_labels.items():
        value = customer.get(field)

        # None 和空字符串都表示该客户信息暂未掌握，需要在下一次跟进中补齐。
        if value is None or value == "":
            missing_fields.append(label)
        else:
            known_fields.append(label)

    missing_count = len(missing_fields)

    # 用缺失字段数量粗略划分完整度，给售前跟进优先级和提问方向提供依据。
    if missing_count >= 5:
        completeness_level = "低"
    elif missing_count >= 2:
        completeness_level = "中"
    else:
        completeness_level = "高"

    return {
        "completeness_level": completeness_level,
        "known_fields": known_fields,
        "missing_fields": missing_fields
    }
