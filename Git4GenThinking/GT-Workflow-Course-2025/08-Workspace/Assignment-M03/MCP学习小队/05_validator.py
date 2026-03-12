import json
from jsonschema import Draft7Validator
def load_json(path: str) -> dict:
    # 读取 JSON 文件
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def main() -> None:
    schema = load_json("02_schema.json")                 # 载入数据契约（Schema）
    output = load_json("04_samples/structured_run_1.json")  # 载入模型输出（可改成循环）
    validator = Draft7Validator(schema)                  # 创建校验器
    errors = sorted(validator.iter_errors(output), key=lambda e: e.path)
    if not errors:
        print("✅ Schema 校验通过：输出可被下游系统直接消费")
        return
    print("❌ Schema 校验失败：发现以下问题：")
    for err in errors:
        print(f"- {list(err.path)}: {err.message}")
if __name__ == "__main__":
    main()