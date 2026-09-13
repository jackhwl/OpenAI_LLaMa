# MIT 与 Apache-2.0 开源许可证核心差异

## 研究结论

MIT 与 Apache-2.0 都属于宽松型、非 Copyleft 开源许可证，均允许商业使用、修改、分发及闭源再发布，也不强制公开修改后的源代码。

| 维度 | MIT | Apache-2.0 |
|---|---|---|
| 许可证复杂度 | 简短，合规要求较少 | 条款详细，合规要求更多 |
| 专利授权 | 没有明确的专利授权条款 | 贡献者明确授予相关专利许可 |
| 专利诉讼 | 无专门规定 | 对作品提起专利诉讼可能导致相关专利许可终止 |
| 再分发要求 | 保留版权声明和许可证文本 | 提供许可证、保留适用通知，并标明修改过的文件 |
| `NOTICE` 文件 | 无此机制 | 原作品包含 `NOTICE` 时，须保留其中适用的归属声明 |
| 商标 | 没有专门规定，但不代表授予商标权 | 明确不授予商标、商号或产品名称使用权 |
| 外部贡献 | 未规定默认贡献许可机制 | 有意提交并纳入项目的贡献默认采用 Apache-2.0，另有约定除外 |
| GPL 兼容性 | 通常兼容 GPLv2 和 GPLv3 | 兼容 GPLv3，但不兼容 GPLv2-only |
| 典型场景 | 小型项目、示例代码、追求最低采用门槛 | 多贡献者、企业参与、专利风险较高的项目 |

选择建议：

- 希望许可证简单、降低下游采用和合规成本时，选择 MIT。
- 希望获得明确的贡献者专利授权及更完整的贡献规则时，选择 Apache-2.0。
- 多贡献者、SDK、基础设施或企业开源项目通常更适合 Apache-2.0。
- 两种许可证都允许他人基于代码构建闭源商业产品。
- MIT 并非必然“没有任何专利保护”，准确说法是它没有明文专利授权；是否存在默示授权取决于具体事实和司法辖区。

## 资料来源

1. [Open Source Initiative：MIT License](https://opensource.org/license/mit)
2. [Apache Software Foundation：Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
3. [Apache Software Foundation：License FAQ](https://www.apache.org/foundation/license-faq.html)
4. [GNU：Various Licenses and Comments about Them](https://www.gnu.org/licenses/license-list.html)
5. [Choose a License：MIT](https://choosealicense.com/licenses/mit/)
6. [Choose a License：Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)

## 待确认事项

- 项目是否涉及项目方或贡献者持有的相关专利。
- 是否计划接受大量外部或企业贡献。
- 依赖项中是否包含 `GPL-2.0-only` 代码。
- 是否会分发二进制、容器、移动应用或嵌入式固件。
- 第三方依赖是否包含必须保留的 `NOTICE`、版权或归属信息。
- 是否需要另行保护项目名称、Logo 或商标。
- 是否需要使用 CLA 或 DCO 管理外部贡献。
- 如果专利、GPL 兼容性或商业分发构成关键风险，应由专业律师复核。

以上内容是许可证文本与公开资料的技术性比较，不构成法律意见。
