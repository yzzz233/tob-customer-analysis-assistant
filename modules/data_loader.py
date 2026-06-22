# 数据读取模块
# 负责从 JSON / Excel 文件中读取客户数据，并统一转换为 list[dict]

from openpyxl import load_workbook
import json

# 读取 Excel 文件，并将表格数据转换为 list[dict]
def load_excel_file(file_name):
    try:
        workbook = load_workbook(file_name)
        sheet = workbook.active

        # 读取 Excel 所有行，第一行为字段名，后续每一行代表一个客户
        rows = list(sheet.iter_rows(values_only=True))
        headers = rows[0]
        customers = []

        for row in rows[1:]:
            # 将表头和当前行数据一一配对，转换成客户字典
            customer = dict(zip(headers, row))
            customers.append(customer)

        return customers

    except FileNotFoundError:
        print(f"文件不存在,请先创建{file_name}")
        return None

# 根据文件后缀选择读取方式，支持 .json 和 .xlsx
def load_customers(file_name):
    if file_name.endswith(".json"):
        return load_json_file(file_name)

    elif file_name.endswith(".xlsx"):
        return load_excel_file(file_name)
        
    else:
        print("暂不支持该文件类型")
        return None

# 读取 JSON 文件，并返回 Python 数据结构
def load_json_file(file_name):
    try:
        with open(
            file_name,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print(f"文件不存在,请先创建{file_name}")
        return None

    except json.JSONDecodeError:
        print("JSON格式错误,请检查文件内容")
        return None
