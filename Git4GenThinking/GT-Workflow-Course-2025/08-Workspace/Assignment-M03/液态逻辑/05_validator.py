import json
from jsonschema import Draft7Validator

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    try:
        schema = load_json("02_schema.json")
    except Exception as e:
        print(f"❌ 无法加载02_schema.json: {e}")
        print("请确保文件存在且格式正确")
        return
    
    validator = Draft7Validator(schema)
    
    files_to_check = [
        "04_samples/structured_run_1.json",
        "04_samples/structured_run_2.json", 
        "04_samples/structured_run_3.json"
    ]
    
    print("🔍 JSON Schema 校验器")
    print("=" * 40)
    
    for file_path in files_to_check:
        print(f"\n检查: {file_path}")
        try:
            data = load_json(file_path)
            errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
            
            if not errors:
                print("   ✅ 通过")
            else:
                print("   ❌ 失败 - 发现问题:")
                for err in errors[:3]:
                    print(f"   - 字段{list(err.path)}: {err.message}")
        except FileNotFoundError:
            print(f"   ⚠️ 文件不存在")
        except Exception as e:
            print(f"   ⚠️ 错误: {e}")
    
    print("\n" + "=" * 40)
    print("✅ 校验完成")

if __name__ == "__main__":
    main()