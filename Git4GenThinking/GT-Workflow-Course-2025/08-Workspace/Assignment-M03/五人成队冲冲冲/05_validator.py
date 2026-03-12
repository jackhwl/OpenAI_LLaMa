# 05_validator.py
# 目的：用 JSON Schema 对模型输出做“确定性校验”，把“格式/字段/类型错误”自动暴露出来
import json
import os, sys
from jsonschema import Draft7Validator

BASE = os.path.dirname(os.path.abspath(__file__))   # ← 锚点：脚本所在文件夹


def load_json(file_name: str) -> dict:
    """自动定位到脚本同目录，再读文件"""
    path = os.path.join(BASE, file_name)            # ← 绝对路径
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
    
def validate_one(sample_path: str, schema: dict) -> None:
    """校验单个文件，打印结果"""
    output = load_json(sample_path)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(output), key=lambda e: e.path)

    if not errors:
        print(f"✅ {sample_path}：Schema 校验通过")
        return

    print(f"❌ {sample_path}：发现以下问题：")
    for err in errors:
        print(f"  - {list(err.path)}: {err.message}")

def main() -> None:
    schema = load_json("02_schema.json")
    # 循环 1/2/3 三个文件
    for idx in range(1, 4):
        sample_path = f"04_samples/structured_run_{idx}.json"
        validate_one(sample_path, schema)
        print()   # 空行隔开不同文件报告

if __name__ == "__main__":
    main()