import os
import sys

# 当前脚本从 scripts 目录运行时，需要把项目根目录加入模块搜索路径。
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modules.data_loader import load_customers
from modules.sqlite_loader import insert_customers_to_db


DB_PATH = os.path.join(BASE_DIR, "data", "customers.db")
# 默认导入 Excel 示例数据；如需导入 JSON，可将文件名切换为 customers.json。
IMPORT_FILE = os.path.join(BASE_DIR, "data", "customers.xlsx")


def import_customers():
    """
    从 Excel / JSON 文件读取客户数据，并批量导入 SQLite 数据库。

    输入：
        无。导入文件路径由 IMPORT_FILE 常量指定。

    输出：
        无直接返回值。读取失败或数据为空时终止；成功时写入 customers 表。
    """
    # load_customers 会根据后缀自动选择 Excel 或 JSON 解析方式。
    customers = load_customers(IMPORT_FILE)

    if customers is None:
        print("客户数据读取失败，导入终止")
        return

    if len(customers) == 0:
        print("客户数据为空，导入终止")
        return

    # 入库函数内部会做去重，避免重复运行导入脚本时产生重复客户跟进记录。
    insert_customers_to_db(DB_PATH, customers)


if __name__ == "__main__":
    import_customers()
