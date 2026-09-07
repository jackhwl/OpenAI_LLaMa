import sys, ast

def check_file(path):
    with open(path) as f:
        tree = ast.parse(f.read())
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            lines = node.end_lineno - node.lineno
            if lines > 30:
                issues.append(f"{node.name}: {lines} lines (consider splitting)")
    return issues

if __name__ == '__main__':
    for issue in check_file(sys.argv[1]):
        print(issue)