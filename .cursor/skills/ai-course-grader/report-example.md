# 评卷报告 — Phase 1 / 02_streaming.py

## 练习信息
- **对应 example**: `phase1_api_basics/example/02_openai_streaming.py`
- **必做变式**: AI 专家流式问答，统计 chunk 数与耗时
- **评分依据**:
  - stream=True 并遍历 chunk
  - 处理 delta.content 为 None
  - AI 专家 system persona
  - 统计 chunk 数量与耗时
  - 通义千问环境变量配置

## 分项得分
| 维度 | 得分 | 说明 |
|------|------|------|
| 核心功能 | 40/45 | 流式遍历与拼接正确；缺 choices 空列表时的稳健处理 |
| 必做变式 | 28/30 | persona + 统计已实现；多轮对话为加分交互 |
| 工程规范 | 13/15 | 环境变量正确；存在未使用的 import |
| 代码质量 | 8/10 | 结构清晰；循环略长可拆分 |
| **合计** | **89/100** | |

## 检查项明细
- [x] stream=True 并遍历 chunk — 已实现
- [x] delta.content 判空 — 使用 if 判断
- [x] AI 专家 persona — system 消息已设置
- [x] chunk 统计与耗时 — 打印 chunk_cnt 与 total_time
- [x] 通义千问配置 — DASHSCOPE_API_KEY / BASE_URL
- [ ] 文件头完成日期 — 尚未填写

## 优点
- 多轮对话循环完整，符合 AI 专家 Agent 主线
- chunk 统计与平均耗时计算正确

## 待改进
1. 删除未使用的 `assistants`、`Messages` import（-2 工程规范）
2. 在文件头填写完成日期，自检项勾选为 `[√]`
3. chunk 为 0 时避免除零（边界情况）

> 注：改进建议只写入评卷意见块，不直接修改学员代码。

## 结论
**通过 ✅**

练习目标与必做变式均已达成。补全文件头元信息后可勾选 PRACTICE_LOG。
