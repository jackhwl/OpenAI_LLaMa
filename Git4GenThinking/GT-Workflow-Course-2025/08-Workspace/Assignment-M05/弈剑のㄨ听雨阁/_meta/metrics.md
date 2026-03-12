 # 📈 知识库核心指标 (Key Metrics)

```dataviewjs
// 1. 获取概念库的数据
let pages = dv.pages('"concepts"');
let totalNotes = pages.length;

// 2. 计算总链接数 (出链)
let totalLinks = 0;
for (let p of pages) {
    totalLinks += p.file.outlinks.length;
}

// 3. 计算指标
let linkDensity = totalLinks / totalNotes; // 链接密度
let orphans = pages.where(p => p.file.inlinks.length == 0).length; // 孤儿数
let orphanRate = (orphans / totalNotes) * 100; // 孤儿率

// 4. 定义评分标准
let score = 0;
if (linkDensity > 3) score += 40;
else score += (linkDensity / 3) * 40;
if (orphanRate < 10) score += 40;
else score += (10 / orphanRate) * 40;
score += 20; // 基础分

// --- 显示结果 ---

dv.header(2, "🧠 系统智商评分: " + score.toFixed(1) + " / 100");

dv.table(
    ["指标 (Metric)", "当前值 (Value)", "目标值 (Target)", "状态"],
    [
        ["📚 概念总数", totalNotes, "50+", "🌱 积累中"],
        ["🔗 链接密度 (Links/Note)", linkDensity.toFixed(2), "> 3.0", linkDensity > 3 ? "✅ 优秀" : "⚠️ 需加强"],
        ["🏚 孤立笔记率", orphanRate.toFixed(1) + "%", "< 10%", orphanRate < 10 ? "✅ 健康" : "🚨 警告"],
    ]
);
````
