# 项目主入口
# 负责串联客户数据读取、规则分析、Prompt 构造、DeepSeek 调用和报告输出

from modules.data_loader import load_customers
from modules.analyzer import build_analysis_input, rule_analyze_customer
from modules.prompt_builder import build_prompt
from modules.deepseek_client import call_deepseek_api
from modules.report_writer import build_customer_report, write_json_file

# 输入客户数据文件，支持 .json 或 .xlsx
# 例如："customers.json" 或 "customers.xlsx"
INPUT_FILE = "customers.json"

# 输出客户分析报告文件
OUTPUT_FILE = "customer_report.json"

customers = load_customers(INPUT_FILE)

if customers is not None:
    report_list = []

    for customer in customers:
        # 从原始客户数据中筛选出参与分析的字段
        analysis_input = build_analysis_input(customer)

        # 生成本地规则分析结果
        analysis_result = rule_analyze_customer(analysis_input)

        # 构造发送给 DeepSeek 的 prompt
        prompt = build_prompt(analysis_input, analysis_result)

        # 调用 DeepSeek 生成自然语言客户分析报告
        ai_report = call_deepseek_api(prompt)

        if ai_report is not None:
            # 组合最终客户报告
            customer_report = build_customer_report(
                analysis_input,
                analysis_result,
                ai_report
            )

            report_list.append(customer_report)
    
    # 保存所有客户分析报告
    write_json_file(report_list, OUTPUT_FILE)

    print(f"客户分析报告已保存到 {OUTPUT_FILE}")


else:
    print("没有读取到有效客户数据，程序结束")