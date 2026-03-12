# 05_validator.py
# 目的：用 JSON Schema 对模型输出做“确定性校验”，把“格式/字段/类型错误”自动暴露出来
import re
import os
import json
from jsonschema import Draft7Validator
def load_json(path: str) -> dict:
    # 读取 JSON 文件
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def main() -> None:
    schema = load_json("02_schema.json")                 # 载入数据契约（Schema）
    # 循环载入匹配正则匹配文件
    # 目标目录
    target_dir = "./04_samples/output"
    # 匹配文件名的正则（仅匹配 structured_run_数字.json）
    pattern = re.compile(r'^structured_run_.+\.json$')

    # 核心匹配逻辑：遍历目录+匹配文件名
    matched_files = [
        os.path.join(target_dir, f) 
        for f in os.listdir(target_dir) 
        if os.path.isfile(os.path.join(target_dir, f)) and pattern.match(f)
    ]
    for file in matched_files:
        print(f"匹配到文件：{file}")
        output = load_json(file)  # 载入模型输出
        validator = Draft7Validator(schema)                  # 创建校验器
        errors = sorted(validator.iter_errors(output), key=lambda e: e.path)
        if not errors:
            print("✅ Schema 校验通过：输出可被下游系统直接消费")
        else:
            print("❌ Schema 校验失败：发现以下问题：")    
            for err in errors:
                print(f"- {list(err.path)}: {err.message}")

if __name__ == "__main__":
    main()