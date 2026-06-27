# 报告生成与写入模块
# 负责将最终报告保存为 JSON 文件，便于 GitHub 展示、人工查看或后续系统接入。

import json

def write_json_file(data, file_name):
    """
    将分析报告写入 JSON 文件。

    输入：
        data: 单个报告 dict 或批量报告 list。
        file_name: 输出文件路径。

    输出：
        无直接返回值。文件已存在时会覆盖，保持当前运行结果最新。
    """
    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:
        # ensure_ascii=False 可以保留中文，indent=4 让报告更适合人工阅读和项目展示。
        json.dump(data, file, ensure_ascii=False, indent=4)
