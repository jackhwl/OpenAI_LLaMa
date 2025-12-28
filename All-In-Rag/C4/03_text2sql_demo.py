import os
import sys
import sqlite3

# 添加text2sql模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'text2sql'))

from text2sql.text2sql_agent import SimpleText2SQLAgent


def setup_demo():
    """设置演示环境"""
    print("=== Text2SQL框架演示 ===\n")
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    # if not api_key:
    #     print("先设置DEEPSEEK_API_KEY环境变量")
    #     return None
    
    # 创建演示数据库
    print("创建演示数据库...")
    db_path = create_demo_database()
    
    # 初始化Text2SQL代理
    print("初始化Text2SQL代理...")
    agent = SimpleText2SQLAgent(api_key=api_key)
    
    # 连接数据库
    print("连接数据库...")
    if not agent.connect_database(db_path):
        print("数据库连接失败!")
        return None
    
    # 加载知识库
    print("加载知识库...")
    try:
        agent.load_knowledge_base()
        print("知识库加载成功!")
    except Exception as e:
        print(f"知识库加载失败: {str(e)}")
        return None
    
    return agent, db_path


def create_demo_database():
    """创建演示数据库"""
    db_path = "text2sql_demo.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            city TEXT
        )
    """)
    
    # 创建产品表
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    
    # 创建订单表
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT,
            total_price REAL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # 插入示例数据
    users_data = [
        (1, '张三', 'zhangsan@email.com', 25, '北京'),
        (2, '李四', 'lisi@email.com', 32, '上海'),
        (3, '王五', 'wangwu@email.com', 28, '广州'),
        (4, '赵六', 'zhaoliu@email.com', 35, '深圳'),
        (5, '陈七', 'chenqi@email.com', 29, '杭州'),
    ]
    
    products_data = [
        (1, 'iPhone 15', '电子产品', 7999.0, 50),
        (2, 'MacBook Pro', '电子产品', 12999.0, 20),
        (3, 'Nike运动鞋', '服装', 599.0, 100),
        (4, '办公椅', '家具', 899.0, 30),
        (5, '台灯', '家具', 199.0, 80),
        (6, 'iPad', '电子产品', 3999.0, 40),
        (7, 'Adidas外套', '服装', 399.0, 60),
    ]
    
    orders_data = [
        (1, 1, 1, 1, '2024-01-15', 7999.0),
        (2, 2, 3, 2, '2024-01-16', 1198.0),
        (3, 3, 5, 1, '2024-01-17', 199.0),
        (4, 1, 2, 1, '2024-01-18', 12999.0),
        (5, 4, 4, 1, '2024-01-19', 899.0),
        (6, 5, 6, 1, '2024-01-20', 3999.0),
        (7, 2, 7, 1, '2024-01-21', 399.0),
    ]
    
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users_data)
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products_data)
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", orders_data)
    
    conn.commit()
    conn.close()
    
    print(f"演示数据库已创建: {db_path}")
    return db_path


def run_demo_queries(agent):
    """运行演示查询"""
    demo_questions = [
        "查询所有用户的姓名和邮箱",
        "年龄大于30的用户有哪些",
        "哪些产品的库存少于50",
        "查询来自北京的用户的所有订单",
        "统计每个城市的用户数量",
        "查询价格在500-8000之间的产品"
    ]
    
    print("\n开始运行演示查询...\n")
    
    success_count = 0
    
    for i, question in enumerate(demo_questions, 1):
        print(f"问题 {i}: {question}")
        print("-" * 60)
        
        try:
            result = agent.query(question)
            
            if result["success"]:
                print(f"成功! SQL: {result['sql']}")
                
                if isinstance(result["results"], dict) and "rows" in result["results"]:
                    count = result["results"]["count"]
                    print(f"返回 {count} 行数据")
                    
                    # 显示前2行数据
                    if count > 0:
                        for j, row in enumerate(result["results"]["rows"][:2]):
                            row_str = " | ".join(f"{k}: {v}" for k, v in row.items())
                            print(f"  {j+1}. {row_str}")
                        
                        if count > 2:
                            print(f"  ... 还有 {count - 2} 行")
                else:
                    print(f"结果: {result['results']}")
                
                success_count += 1
                
            else:
                print(f"失败: {result['error']}")
                print(f"SQL: {result['sql']}")
                
        except Exception as e:
            print(f"执行错误: {str(e)}")
        
        print()
    
    # 输出统计
    total_count = len(demo_questions)


def cleanup(agent, db_path):
    """清理资源"""
    print("\n清理资源...")
    
    if agent:
        agent.cleanup()
    
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"已删除演示数据库: {db_path}")


def main():
    """主函数"""
    # 设置演示环境
    setup_result = setup_demo()
    
    if setup_result is None:
        return
    
    agent, db_path = setup_result
    
    try:
        # 运行演示查询
        run_demo_queries(agent)
        
    finally:
        # 清理资源
        cleanup(agent, db_path)


if __name__ == "__main__":
    main() 