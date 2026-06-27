import sqlite3
import json
from datetime import datetime


def get_connection(db_path):
    """
    创建并返回 SQLite 数据库连接。

    输入：
        db_path: 数据库文件路径，例如 data/customers.db。

    输出：
        sqlite3.Connection 连接对象。
    """
    conn = sqlite3.connect(db_path)
    return conn


def query_database(conn, sql, params=None):
    """
    执行 SQL 查询，并把查询结果转换为 list[dict]。

    输入：
        conn: SQLite 连接对象。
        sql: 要执行的查询语句。
        params: SQL 参数列表，用于安全传参，避免手动拼接 SQL。

    输出：
        查询结果列表，每一行都是一个字段名到字段值的字典。
    """
    if params is None:
        params = []

    cursor = conn.cursor()
    cursor.execute(sql, params)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # SQLite 默认返回 tuple；转换为 dict 后，分析流程可以用字段名读取客户信息。
    results = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        results.append(row_dict)

    return results


def load_customers_from_db(db_path):
    """
    从 customers 表中读取所有客户跟进数据。

    输入：
        db_path: SQLite 数据库路径。

    输出：
        客户记录列表，按 customer_id 升序排列，便于批量分析时结果稳定。
    """
    conn = get_connection(db_path)

    # 显式列出字段，避免表结构扩展后影响当前分析报告的字段范围。
    sql = """
    SELECT
        customer_id,
        customer_name,
        industry,
        employee_count,
        current_system,
        follow_up_note,
        budget,
        decision_maker,
        timeline,
        sales_stage
    FROM customers
    ORDER BY customer_id;
    """

    customers = query_database(conn, sql)

    conn.close()

    return customers


def get_customer_by_id(db_path, customer_id):
    """
    根据 customer_id 查询单个客户。

    输入：
        db_path: SQLite 数据库路径。
        customer_id: customers 表中的客户主键。

    输出：
        找到时返回客户字典；找不到时返回 None。
    """
    conn = get_connection(db_path)

    sql = """
    SELECT
        customer_id,
        customer_name,
        industry,
        employee_count,
        current_system,
        follow_up_note,
        budget,
        decision_maker,
        timeline,
        sales_stage
    FROM customers
    WHERE customer_id = ?;
    """

    results = query_database(conn, sql, [customer_id])

    conn.close()

    if len(results) == 0:
        return None

    return results[0]


def save_analysis_report(db_path, customer_id, analysis_result):
    """
    将客户分析结果保存到 analysis_reports 表。

    输入：
        db_path: SQLite 数据库路径。
        customer_id: 当前报告对应的客户 ID。
        analysis_result: Python dict，包含客户信息、完整度检查和 AI 分析结果。

    输出：
        无直接返回值。数据会写入 analysis_reports 表。
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    sql = """
    INSERT INTO analysis_reports (
        customer_id,
        analysis_result,
        created_at
    )
    VALUES (?, ?, ?);
    """

    # 数据库用 TEXT 保存报告，因此先把 dict 序列化为 JSON 字符串。
    analysis_json = json.dumps(
        analysis_result,
        ensure_ascii=False,
        indent=2
    )

    # 保存生成时间，方便后续追踪同一客户在不同时间的分析记录。
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        sql,
        [customer_id, analysis_json, created_at]
    )

    conn.commit()
    conn.close()

def insert_customers_to_db(db_path, customers):
    """
    将客户列表批量写入 SQLite 的 customers 表。

    输入：
        db_path: SQLite 数据库路径。
        customers: 从 JSON / Excel 读取到的客户字典列表。

    输出：
        无直接返回值。函数会打印成功导入和跳过重复的数量。

    去重规则：
    customer_name + follow_up_note 相同，则认为是重复客户记录，跳过插入。
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO customers (
        customer_name,
        industry,
        employee_count,
        current_system,
        follow_up_note,
        budget,
        decision_maker,
        timeline,
        sales_stage
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    check_sql = """
    SELECT customer_id
    FROM customers
    WHERE customer_name = ?
      AND follow_up_note = ?;
    """

    insert_count = 0
    skip_count = 0

    for customer in customers:
        customer_name = customer.get("customer_name")
        follow_up_note = customer.get("follow_up_note")

        # 先查重再插入，避免重复导入同一批 Excel / JSON 时产生相同跟进记录。
        cursor.execute(check_sql, [customer_name, follow_up_note])
        existing_customer = cursor.fetchone()

        if existing_customer is not None:
            skip_count += 1
            continue

        # 按数据库字段顺序组装元组，字段名保持与建表脚本一致。
        row = (
            customer.get("customer_name"),
            customer.get("industry"),
            customer.get("employee_count"),
            customer.get("current_system"),
            customer.get("follow_up_note"),
            customer.get("budget"),
            customer.get("decision_maker"),
            customer.get("timeline"),
            customer.get("sales_stage")
        )

        cursor.execute(insert_sql, row)
        insert_count += 1

    conn.commit()
    conn.close()

    print(f"成功导入 {insert_count} 条客户数据")
    print(f"跳过重复数据 {skip_count} 条")

def get_customer_by_name(db_path, customer_name):
    """
    根据客户名称查询单个客户。
    如果有多个同名客户，默认返回第一条。

    输入：
        db_path: SQLite 数据库路径。
        customer_name: 客户名称。

    输出：
        找到时返回第一条客户字典；找不到时返回 None。
    """
    conn = get_connection(db_path)

    sql = """
    SELECT
        customer_id,
        customer_name,
        industry,
        employee_count,
        current_system,
        follow_up_note,
        budget,
        decision_maker,
        timeline,
        sales_stage
    FROM customers
    WHERE customer_name = ?
    ORDER BY customer_id;
    """

    results = query_database(conn, sql, [customer_name])

    conn.close()

    if len(results) == 0:
        return None

    return results[0]

