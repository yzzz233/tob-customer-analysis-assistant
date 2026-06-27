from modules.sqlite_loader import (
    load_customers_from_db,
    get_customer_by_id,
    get_customer_by_name,
    save_analysis_report
)
from modules.data_quality_checker import check_data_quality
from modules.prompt_builder import build_follow_up_prompt
from modules.deepseek_client import call_deepseek_json_api



def analyze_customer(db_path, customer):
    """
    分析单个客户，并保存分析报告。

    输入：
        db_path: SQLite 数据库路径，用于保存分析报告。
        customer: 从数据库中查询出来的客户信息字典。

    输出：
        final_report: 包含客户信息、完整度检查和 AI 分析结果的字典。

    流程：
        1. 检查客户资料完整度。
        2. 构造 DeepSeek prompt。
        3. 调用 AI 生成售前跟进建议。
        4. 将完整报告保存到 analysis_reports 表。
    """
    print(f"正在分析客户：{customer['customer_name']}")

    # 先做信息完整度检查，让 AI 知道哪些信息可靠、哪些还需要销售继续确认。
    data_quality = check_data_quality(customer)

    # prompt 将客户原始信息和完整度结果组合起来，作为 AI 分析的完整上下文。
    prompt = build_follow_up_prompt(customer, data_quality)

    ai_analysis = call_deepseek_json_api(prompt)

    # 报告同时保留原始客户信息和 AI 结论，方便后续回溯 AI 是基于哪些信息判断的。
    final_report = {
        "customer_info": customer,
        "data_quality": data_quality,
        "ai_analysis": ai_analysis
    }

    save_analysis_report(
        db_path,
        customer["customer_id"],
        final_report
    )

    print(f"客户分析完成：{customer['customer_name']}")

    return final_report


def analyze_customer_by_id(db_path, customer_id):
    """
    根据 customer_id 查询并分析单个客户。

    输入：
        db_path: SQLite 数据库路径。
        customer_id: 要分析的客户 ID。

    输出：
        找到客户时返回分析报告；找不到时返回 None。
    """
    customer = get_customer_by_id(db_path, customer_id)

    if customer is None:
        print(f"未找到 customer_id = {customer_id} 的客户")
        return None

    return analyze_customer(db_path, customer)


def analyze_customer_by_name(db_path, customer_name):
    """
    根据 customer_name 查询并分析单个客户。

    输入：
        db_path: SQLite 数据库路径。
        customer_name: 要分析的客户名称。

    输出：
        找到客户时返回分析报告；找不到时返回 None。
    """
    customer = get_customer_by_name(db_path, customer_name)

    if customer is None:
        print(f"未找到 customer_name = {customer_name} 的客户")
        return None

    return analyze_customer(db_path, customer)


def analyze_all_customers(db_path):
    """
    分析数据库中的全部客户。

    输入：
        db_path: SQLite 数据库路径。

    输出：
        all_reports: 每个客户一份分析报告组成的列表；无客户时返回空列表。
    """
    customers = load_customers_from_db(db_path)

    if len(customers) == 0:
        print("customers 表中没有客户数据，请先导入客户数据")
        return []

    all_reports = []

    # 批量分析沿用单客户分析函数，保证按 ID、按名称和全量分析的报告结构一致。
    for customer in customers:
        final_report = analyze_customer(db_path, customer)
        all_reports.append(final_report)

    return all_reports
