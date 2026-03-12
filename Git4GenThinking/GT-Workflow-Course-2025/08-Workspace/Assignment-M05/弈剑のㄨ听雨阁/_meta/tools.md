---
type: tool_registry
---

# 🧰 智能体工具箱

## 文件操作类 (File System)
- **create_note(title, content)**: 创建新笔记。
- **append_to_daily(text)**: 追加内容到今日日记。
- **move_file(path, new_path)**: 移动或重命名文件。

## 知识管理类 (Knowledge Graph)
- **merge_notes(note_a, note_b)**: 合并两个笔记内容（需人工确认）。
- **add_tag(file, tag)**: 为笔记添加标签。
- **find_orphans()**: 查找没有链接的孤立笔记。

## 外部能力类 (External)
- **web_search(query)**: (待集成) 联网搜索。