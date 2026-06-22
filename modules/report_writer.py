# 报告生成与写入模块
# 负责组合客户报告结构，并将最终报告保存为 JSON 文件

import json

# 组合单个客户的最终报告结构
def build_customer_report(analysis_input, analysis_result, ai_report):
    report = {
        "customer_info": analysis_input,
        "rule_analysis": analysis_result,
        "ai_report": ai_report
    }

    return report

# 写入 JSON 文件；如果文件已存在，会覆盖原文件
def write_json_file(data,file_name):
    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(data,file,ensure_ascii=False,indent=4)
