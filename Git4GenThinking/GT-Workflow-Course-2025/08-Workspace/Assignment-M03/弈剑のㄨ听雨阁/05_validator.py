import argparse
import json
import sys
import os
import glob

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def resolve_inputs(inputs, globs):
    files = []
    for p in inputs:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in names:
                    if n.endswith(".json"):
                        files.append(os.path.join(root, n))
        else:
            files.append(p)
    for pattern in globs:
        files.extend(glob.glob(pattern, recursive=True))
    dedup = []
    seen = set()
    for f in files:
        fp = os.path.abspath(f)
        if fp not in seen and os.path.isfile(fp):
            seen.add(fp)
            dedup.append(fp)
    return dedup

def validate_with_jsonschema(schema, instance):
    try:
        import jsonschema
        from jsonschema import Draft7Validator
    except Exception:
        return None, ["Missing dependency: jsonschema. Install with: pip install jsonschema"]
    try:
        validator = Draft7Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
        formatted = []
        for e in errors:
            loc = "/".join([str(x) for x in e.path]) if e.path else ""
            formatted.append(f"{loc}: {e.message}")
        return True if not formatted else False, formatted
    except Exception as exc:
        return None, [f"Validator error: {exc}"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", default="02_schema.json")
    parser.add_argument("--inputs", nargs="*", default=[])
    parser.add_argument("--glob", nargs="*", default=["04_samples/structured_run_*.json", "./structured_run_*.json", "**/structured_run_*.json"])
    parser.add_argument("--show-pass", action="store_true")
    args = parser.parse_args()
    schema_path = os.path.abspath(args.schema)
    if not os.path.isfile(schema_path):
        print(f"Schema not found: {schema_path}")
        sys.exit(2)
    try:
        schema = load_json(schema_path)
    except Exception as exc:
        print(f"Failed to load schema: {exc}")
        sys.exit(2)
    targets = resolve_inputs(args.inputs, args.glob)
    if not targets:
        print("No input JSON files found.")
        sys.exit(2)
    any_fail = False
    for fp in targets:
        try:
            instance = load_json(fp)
        except Exception as exc:
            print(f"[FAIL] {fp}")
            print(f"load: {exc}")
            any_fail = True
            continue
        ok, msgs = validate_with_jsonschema(schema, instance)
        if ok is True:
            if args.show_pass:
                print(f"[OK] {fp}")
        elif ok is False:
            any_fail = True
            print(f"[FAIL] {fp}")
            for m in msgs:
                print(f"- {m}")
        else:
            any_fail = True
            print(f"[ERROR] {fp}")
            for m in msgs:
                print(f"- {m}")
    sys.exit(1 if any_fail else 0)

if __name__ == "__main__":
    main()
