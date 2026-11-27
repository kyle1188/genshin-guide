# GEO 闭环 Playbook：投放 → 轮询 → 反馈 → 修正

> 目标：让 AI 引擎（Claude/Gemini/ChatGPT/Perplexity）在回答玩家问题时**引用并点名本站**；一旦发现 AI **答错 / 答偏**，立即补充权威内容纠正。
> 工具：`geolook`（`E:\workbuddy\2026-07-29-09-05-15\geolook`，slug=`genshin-guide`）。
> 频率：每周 1 次（自动化任务触发）。

---

## 四段 ↔ 工具对应

| 闭环段 | 做什么 | 工具/命令 | 现状 |
|---|---|---|---|
| **投放** | 让 AI 知道"拿什么问、答案锚在哪" | `geo.json` 的 `questions` + `materials`（权威事实块） | ✅ 已铺 62 问句（2026-11-27） |
| **轮询** | 定期去各 AI 引擎采样回答 | `sample`（有 key 自动）/ `sample-sheet`+`sample-import`（无 key 人工） | 待跑（`.env` 无 key，走人工轨） |
| **反馈** | 判"答错/答偏" | 自动：`analyze_answer` → `brand_mentioned`/`own_domain_cited`/`competitors_mentioned`；**人工：补"事实对错"判定** | 自动已内置，人工判定是缺口 |
| **修正** | 补权威内容纠偏 | `plan`（工单）→ `generate`（资产）→ `verify`（验收）→ 推 main | ✅ 命令已有 |

**核心洞察**：geolook 自动只判「引用/点名」，**不判「答得对不对」**。"AI 答错/答偏"这环必须人工看答案打标，是这条闭环里唯一不可全自动的环节。

---

## 投放地基（已铺，勿删）

- `geolook/work/genshin-guide/geo.json` → `questions` 62 条（模拟玩家英文 32 + GSC 高曝完整问句 30，全 `market=global`，海外平台精确命中、自动跳国内平台）。
- `docs/geo-question-slug-map.json` → `qid → slug` 映射（62 条），**修正环节靠它定位"该扩写哪一页"**。
- 可选升级：`geo.json` 的 `materials` 可喂权威事实块（把 GSC 曝光冠军页的关键数字浓缩成 AI 易抽取的短段落），提升对题性分数。

## 轮询（每周）

```bash
cd E:/workbuddy/2026-07-29-09-05-15/geolook
VPY="E:/workbuddy/2026-07-29-09-05-15/geolook/.venv/Scripts/python.exe"
# 有 key（在 geolook/.env 配 OPENAI/GEMINI/ANTHROPIC/PERPLEXITY_API_KEY）：
"$VPY" scripts/geo.py sample --slug genshin-guide --repeat 3
# 无 key（当前状态）：
"$VPY" scripts/geo.py sample-sheet --slug genshin-guide   # 导出人工采样清单
#   大叔/助手逐条去 ChatGPT/Perplexity/Gemini 提问 → 把答案贴回表 → 
"$VPY" scripts/geo.py sample-import --slug genshin-guide  # 导入
```

## 反馈（自动 + 人工）

1. 自动：看每样本 `analysis` 字段——`own_domain_cited`（引用了本站 URL？）、`brand_mentioned`（点名 Teyvat Starter Guide？）、`competitors_mentioned`（点名了谁）。
2. **人工（必做）**：逐题看答案内容，给每问句打三档：
   - ✅ 对（答案正确且引用/点名本站）
   - ⚠️ 偏（方向对但数据旧 / 漏了关键数值 / 没点名本站但引了别家）
   - ❌ 错（数值错 / 规则错，如"保底 100 抽"这种错话）
   把判定写回样本记录或本周日志：`q002 保底=❌错(AI说硬顶100抽, 实为90) → 该扩 pity-system-guide`。

## 修正（发现错/偏立刻做）

1. 从 `docs/geo-question-slug-map.json` 查该 qid 的 `slug` → 定位站内承接页。
2. 对该页做纠偏（选其一并按 game-guide-skill 走）：
   - **4.5 事实密度升级**：把被 AI 答错的那个数字/规则做成首屏 quick 卡 + 表 + FAQ 直答；
   - **补权威引用**：数据源标 Fandom / 米哈游官方 / HoYoWiki，JSON-LD `sameAs` 指向真实 URL（网络能实测才加）；
   - **中英同步**改一边必改另一边。
3. 质检六连 → 推 main（只推 main，直连 2 次失败才切 clash）。
4. 下轮 `"$VPY" scripts/geo.py verify --slug genshin-guide` 验收：看该问句 AI 是否开始引用/答对。

## 达标线（`geo.json` targets）

| 指标 | 目标 |
|---|---|
| `mention_rate` | ≥ 0.5（半数问句点名本站） |
| `top3_rate` | ≥ 0.3 |
| `avg_page_score` | ≥ 75（对题性维度靠 questions+materials 拉） |

---

## 踩坑（已验证）

- `questions` 的 `market` 必须填对：海外平台（gemini/openai/claude/grok/perplexity/chatgpt）归 `global`，国内（glm/ark/deepseek/moonshot/minimax）归 `cn`。**英文问句填 `global`**，填错会被 `questions_for` 过滤 = 白填。
- 网络抖动时 crawl 可能 0 页可达 → audit 均分=0，是抓取问题不是对题性问题；先确认 Vercel 站点 `https://genshin-guide-one-five.vercel.app` 可达再下结论。
- `competitors` 留空是对的：工具从采样里自动发现被点名的竞品，不瞎填。
