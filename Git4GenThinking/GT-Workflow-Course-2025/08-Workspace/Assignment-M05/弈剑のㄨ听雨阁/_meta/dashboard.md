# 🎛 智能体控制台

## 🚧 待处理的概念 (Drafts)
> 自动扫描所有状态为 "draft" 的概念卡片

```dataview
TABLE created as "创建日期", tags as "标签"
FROM "concepts"
WHERE status = "draft"
SORT created DESC
```


```dataview
LIST
FROM "daily"
WHERE file.cday > date(today) - dur(7 days)
SORT file.name DESC
```

## 🎓 经验教训库 (Knowledge Base of Experience)
> 自动提取日记中打过“经验”标签的段落

```dataview
LIST rows.L.text
FROM #经验/成功 OR #经验/失败
FLATTEN file.lists AS L
WHERE contains(L.tags, "#经验")
```

```dataviewjs
// --- 🏥 系统健康体检 (System Health Monitor) ---

// 1. 定义配置：什么样的笔记算"老"？(这里设为 30 天)
const daysToOld = 30;
// 获取今天的日期用于比较
const today = dv.date("today");

// 2. 获取所有在 "concepts" 文件夹里的概念卡片
let allConcepts = dv.pages('"concepts"');

// 3. 筛选：找出"孤儿" (没有被任何笔记引用，且不是模板文件)
// filter 逻辑：入链数量(inlinks.length) 等于 0
let orphans = allConcepts
    .filter(p => p.file.inlinks.length == 0);

// 4. 筛选：找出"陈旧草稿"
// filter 逻辑：状态是 draft 且 最后更新时间早于 30 天前
let oldDrafts = allConcepts
    .filter(p => p.status == "draft")
    .filter(p => (today - p.file.mday).days > daysToOld);

// --- 5. 显示逻辑 (渲染界面) ---

dv.header(2, "🏥 系统健康诊断报告");

// A. 检查链接健康度
if (orphans.length > 0) {
    // 有问题：显示红色警告和列表
    dv.header(3, "⚠️ 发现 " + orphans.length + " 个孤立概念！");
    dv.paragraph("这些概念没有被其他笔记链接，可能会被遗忘：");
    
    // 列出这些文件的链接
    dv.list(orphans.file.link);
} else {
    // 没问题：显示绿色平安
    dv.paragraph("✅ 链接结构非常健康，所有概念都有关联。");
}

dv.span("<br>"); // 换行

// B. 检查写作进度
if (oldDrafts.length > 0) {
    // 有问题
    dv.header(3, "⚠️ 积压了 " + oldDrafts.length + " 篇陈旧草稿");
    dv.paragraph("这些草稿超过 " + daysToOld + " 天没动过了：");
    
    // 显示为简单的任务列表
    dv.taskList(oldDrafts.file.tasks, false); // 如果草稿里有任务也显示出来
    dv.list(oldDrafts.file.link);
} else {
    // 没问题
    dv.paragraph("✅ 写作进度良好，没有积压的陈旧草稿。");
}
```


## 🚨 安全监控 (Security Monitor)

```dataviewjs
// 获取今天修改过的文件
let todayChanges = dv.pages().where(p => p.file.mday >= dv.date("today"));

// 设定阈值
const threshold = 10;

if (todayChanges.length > threshold) {
    dv.header(3, "⚠️ 异常活跃警告");
    dv.paragraph("今日已有 **" + todayChanges.length + "** 个文件发生变更！");
    dv.paragraph("请确认这是否为您本人的操作？");
} else {
    dv.paragraph("✅ 今日变更量正常 (" + todayChanges.length + " files)");
}
````
