# 《原神》攻略站 · Google 自然排名零成本起步指南

> 目标：不花一分钱，让网站在 Google 搜「原神 抽卡模拟器」「原神 原石规划器」等**长尾词**时排到前面。
> 现状：网站已上线 `https://dcc502452e874bb0943f6b2a0046f415.bj7.agentos-app.net`（HTTP 200，可抓取）。
> 适用范围：纯静态站（index.html + assets/ + sitemap.xml + robots.txt）。

---

## 一、已经就绪的东西（不用再改）

| 项目 | 状态 |
|---|---|
| 站点上线 | ✅ CloudStudio 公网地址可访问 |
| `sitemap.xml` | ✅ 已生成，指向当前地址 |
| `robots.txt` | ✅ 已生成，指向当前 sitemap |
| `index.html` JSON-LD | ✅ 已标记 3 个工具（抽卡模拟器/原石规划器/元素反应演示） |
| 四版推广文案 | ✅ 米游社/B站/小红书/贴吧，带链接，复制即用 |
| `vercel.json` | ✅ 已加，可直接传 Vercel |

---

## 二、主线方案：部署到 Vercel（更稳的免费网址）

Vercel 免费档给你 `你的项目.vercel.app` 子域 + 全球 CDN + 自动 SSL，对 Google 抓取和自然排名是正资产，且**永久稳定**（不像沙箱可能消失）。

### 步骤
1. 注册免费 Vercel 账号：https://vercel.com （用 GitHub/邮箱都行，免费 Hobby 档足够）
2. 部署（二选一）：
   - **拖文件夹**：Vercel 后台「Add New → Project → Deploy」，直接把 `genshin-guide/` 整个文件夹拖进去；或
   - **CLI**：在 `genshin-guide/` 目录运行 `vercel`（需先 `npm i -g vercel`）。
3. 部署成功后会拿到地址，形如 `https://genshin-guide-xxx.vercel.app`
4. **改三处域名**（把 CloudStudio 地址换成你的 `.vercel.app` 地址）：
   - `index.html` 第 14 行 `<link rel="canonical" href="...">`
   - `sitemap.xml` 里的 `<loc>...</loc>`
   - `robots.txt` 里的 `Sitemap: ...`
   → 改完重新部署一次（Vercel 改文件会自动重新部署）
5. 继续看第三节提交 GSC。

---

## 三、提交 Google Search Console（让 Google 来抓）

> 不论用 CloudStudio 还是 Vercel 地址，这一步一样。下面以「已确定最终地址」为前提。

1. 打开 https://search.google.com/search-console 并用 Google 账号登录（免费）
2. 左侧「添加资源」→ 选 **网址前缀** → 填你的站点地址（含 `https://` 和结尾 `/`）→ 继续
3. **验证方式选「HTML 标记」**：
   - GSC 会给出一段 `<meta name="google-site-verification" content="一串码">`
   - 把那串 `content` 验证码发给我，我加进 `index.html` 的 `<head>` 里
   - 重新部署后，回 GSC 点「验证」
   - （若用 Vercel，改完文件推上去即自动重新部署；若用 CloudStudio，需重新走一次部署）
4. 验证通过后，左侧「站点地图」→ 填 `sitemap.xml` 的完整地址（如 `https://你的地址/sitemap.xml`）→ 提交
5. 左侧「网址检查」→ 粘贴首页地址 → 「请求编入索引」。这能加快首次收录。

> 验证必须登录你自己的 Google 账号，验证码也只有你能看到——这一步我替不了，但其余（加 meta 标签、改文件、部署）我来。

---

## 四、今天就能做的备选（不等 Vercel）

如果你不想先注册 Vercel，**现在就能用已上线的 CloudStudio 地址提交 GSC**：
- 第三节步骤里的「站点地址」直接填 `https://dcc502452e874bb0943f6b2a0046f415.bj7.agentos-app.net/`
- sitemap / robots / canonical 当前已指向它，不用改
- 提交后 Google 开始抓取收录，长尾词慢慢起量
- 之后想换 Vercel，再走第二节改三处 URL 即可（老地址可做 301 跳转到新地址，保住已积累的排名）

---

## 五、SEO 核心资产：长尾词清单

大站做不好「可交互工具」，这些词竞争小、意图精准，是你的胜负手。把站点内容往这些词靠：

**中文词（建议用在页面标题/H1/段落里，自然出现，别堆）**
- 原神 抽卡模拟器 在线
- 原神 十连 模拟 免费
- 原神 原石 规划器
- 原神 元素反应 演示
- 原神 零氪 开荒 日程表
- 原神 新手 30天 攻略
- 原神 配队 共鸣 提示
- 原神 班尼特 培养 攻略

**英文词（吃海外 Google 流量）**
- Genshin wish simulator
- Genshin resin planner
- Genshin elemental reaction demo
- Genshin beginner 30 day guide

> 注意：Google 惩罚关键词堆砌。让这些词**自然出现在对应板块的标题和正文**即可，不要硬塞。

---

## 六、外链分发（最强的免费排名信号）

把 `推广文案包.md` 里的四版文案发出去，外链指回站点：
- 米游社动态 / B站动态 / 小红书笔记 / 原神贴吧
- 原神 QQ 群、Discord 社群
- 钩子统一打「能玩的工具」（抽卡模拟 / 原石规划），比纯文章更容易被转发

外链质量 > 数量。一条来自米游社的链接，胜过几十条垃圾论坛。

---

## 七、零成本要点总结

| 动作 | 花费 | 谁来做 |
|---|---|---|
| 用 CloudStudio 当前地址提交 GSC | 0 | 你登录 GSC + 我加验证标签 |
| 部署到 Vercel 拿 .vercel.app | 0 | 你注册免费号，我打包好 |
| 发四版文案做外链 | 0 | 你发（或我代拟更多平台版） |
| 买 .com 域名做品牌 | ~55–70元/年（可选） | 等站有起色再买 |
| 买服务器 / DNS专业版 / 付费SSL | 0（都不需要） | — |

**一句话路线**：今天用 CloudStudio 地址提交 GSC 拿收录 → 顺手部署 Vercel 换更稳地址 → 发四版文案做外链 → 版本更新跟着更 → 有起色再花几十块买 .com。
