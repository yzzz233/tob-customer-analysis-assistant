import sqlite3
import os


# 脚本位于 scripts 目录下，因此向上一级定位到项目根目录，再拼出数据库路径。
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "customers.db")


def init_database():
    """
    初始化 SQLite 数据库和项目所需数据表。

    输入：
        无。数据库路径由 DB_PATH 常量指定。

    输出：
        无直接返回值。执行后会创建 data/customers.db、customers 表和 analysis_reports 表。
    """
    # 确保 data 目录存在，避免首次运行时因为目录缺失导致数据库创建失败。
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # customers 表保存客户跟进原始数据，是后续完整度检查和 AI 分析的基础。
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        industry TEXT,
        employee_count INTEGER,
        current_system TEXT,
        follow_up_note TEXT NOT NULL,
        budget TEXT,
        decision_maker TEXT,
        timeline TEXT,
        sales_stage TEXT
    )
    """)

    # analysis_reports 表保存每次 AI 分析结果，便于后续查看历史报告或做二次展示。
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_reports (
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        analysis_result TEXT,
        created_at TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    conn.commit()
    conn.close()

    print("数据库初始化完成：data/customers.db")
    print("已创建 customers 表和 analysis_reports 表")


if __name__ == "__main__":
    init_database()
