import os

from modules.customer_analyzer import (
    analyze_customer_by_id,
    analyze_customer_by_name,
    analyze_all_customers
)
from modules.report_writer import write_json_file


# 项目根目录和常用文件路径统一放在入口文件中，方便运行时定位数据库和报告文件。
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "customers.db")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "customer_analysis_report.json")


def main():
    """
    主程序入口：根据 mode 选择客户分析方式，并把分析结果写入 JSON 文件。

    mode 可选值：
        "by_id": 按 customer_id 分析单个客户，适合定位某条数据库记录。
        "by_name": 按客户名称分析单个客户，适合演示或快速查询指定客户。
        "all": 分析数据库中的全部客户，适合批量生成售前跟进建议。

    输出：
        无直接返回值。分析成功后会生成 data/customer_analysis_report.json。
    """
    # 当前默认批量分析全部客户；演示单客户流程时可切换为 "by_id" 或 "by_name"。
    mode = "all"

    if mode == "by_id":
        # 按数据库主键查询，适合客户 ID 明确且需要精准定位的场景。
        report = analyze_customer_by_id(DB_PATH, 1)

        if report is not None:
            write_json_file(report, OUTPUT_FILE)
            print(f"JSON 报告已保存到：{OUTPUT_FILE}")

    elif mode == "by_name":
        # 按客户名称查询，适合客户成功或售前同事按公司名快速查看建议。
        report = analyze_customer_by_name(DB_PATH, "云仓电商")

        if report is not None:
            write_json_file(report, OUTPUT_FILE)
            print(f"JSON 报告已保存到：{OUTPUT_FILE}")

    elif mode == "all":
        # 批量分析会逐个读取数据库客户，生成一个报告列表，便于统一归档或展示。
        reports = analyze_all_customers(DB_PATH)

        if len(reports) > 0:
            write_json_file(reports, OUTPUT_FILE)
            print(f"JSON 报告已保存到：{OUTPUT_FILE}")

    else:
        print("未知运行模式，请检查 mode 设置")

if __name__ == "__main__":
    main()
