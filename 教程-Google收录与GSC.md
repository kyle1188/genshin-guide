# 教程二：Google 收录与 Google Search Console（GSC）

> 适用：已部署上线的网站（如 `https://genshin-guide-one-five.vercel.app`）。
> 目标：让 Google 收录你的站，并尽量在搜索中排名靠前。
> 前置：网站已上线 + 你有 Google 账号。

---

## 一、添加资源并验证（必须你亲自登录 Google）

1. 打开 https://search.google.com/search-console
2. 左上角 **「添加资源」** → 选 **「网址前缀」**（不是网域）
3. 输入完整地址（含 `https://`）：
   ```
   https://genshin-guide-one-five.vercel.app
   ```
   → 点 **继续**

---

## 二、验证方式：选「HTML 标记」（最简单）

> ⚠️ 别选「HTML 文件」——那要往根目录塞一个空文件。选 **HTML 标记** 只需在 `<head>` 加一行。

1. 在验证方法里选 **「HTML 标记」**
2. 复制它给的那段代码里的 `content` 值，类似：
   ```
   t29bkbqCvDTtmfzURdty0JUkleAxCjlziuu5_54Lg_A
   ```
3. **把这串字符发给帮你部署的人**（或自己加）：
   在 `index.html` 的 `<head>` 里，`<meta name="theme-color">` 之后加一行：
   ```html
   <meta name="google-site-verification" content="t29bkbqCvDTtmfzURdty0JUkleAxCjlziuu5_54Lg_A" />
   ```
4. 提交推送：
   ```bash
   git add -A && git commit -m "seo: add GSC verification" && git push
   ```
   （若 Vercel 盯 main：`git push origin master:main`）
5. 等 Vercel 重新部署完（1–2 分钟），回 GSC 点 **「验证」** → 显示 ✅ 已验证。

> 想确认线上是否生效，可用 curl 抓 HTML 看有没有这段 meta：
> ```bash
> curl -s https://你的地址/ | grep google-site-verification
> ```

---

## 三、提交站点地图 sitemap.xml（核心收录入口）

1. GSC 左侧菜单 → **「站点地图」**
2. 输入框填  `sitemap.xml`  → 点 **提交**
3. 状态显示 **「成功」** → Google 会按地图里的链接自动抓取全部页面。

> 提交前确认 sitemap.xml 里所有链接都指向**当前真实域名**（我们曾踩坑：英文版链接漏改成旧 CloudStudio 地址）。本地全局搜一遍旧域名再推：
> ```bash
> grep -rn "旧域名\|agentos-app" .
> ```

---

## 四、请求编入索引（加速，可选）

1. 左侧 → **「网址检查」**
2. 粘贴首页地址 → 回车
3. 点 **「请求编入索引」**（Request indexing）

> ⚠️ **每日配额限制**：GSC 这个功能每天只能点几次，超了会报「超出了配额 / 今天已超出每日配额，请明天再试」。
> **这不是网站问题，是 Google 的限流**。即使今天点不了，只要 sitemap 已提交，Google 几天内也会自动收录。明天配额重置再点一次即可。

---

## 五、让排名更靠前（你的原目标）

光收录不够，要超过靠前攻略站，核心打法：**长尾词 + 外链**，大站做不好的地方我们正好强。

| 策略 | 具体动作 |
|------|----------|
| **长尾词命中** | 抽卡模拟器、原石规划器、元素反应演示、零氪开荒日程——这些「工具词」大站多是纯文字，我们是可交互独家内容 |
| **多语覆盖** | 英文版（Genshin starter guide / gacha simulator）吃海外 Google 流量；已配 `hreflang` 让中英文各搜各的 |
| **外链分发** | 把站点链接发到米游社 / B站 / 小红书 / 贴吧 / Reddit，每篇带链接 = 给 Google 投票 |
| **结构化数据** | 页面已加 JSON-LD，帮助 Google 理解内容类型 |
| **持续更新** | 用 Git 部署随便改，更新频率高利于排名 |

---

## 六、排错速查

| 现象 | 原因 | 解决 |
|------|------|------|
| GSC 报「找不到验证文件」 | 选了 HTML 文件法但没放文件 | 改用 HTML 标记法，加 meta 标签 |
| 验证失败（已加 tag） | Vercel 还没重新部署完 | 等 1–2 分钟再点验证 |
| 「超出了配额」 | 当天请求索引次数用尽 | 明天再试，不影响收录 |
| sitemap 提交报错 | XML 格式错 / 链接域名不对 | 本地核对 XML，旧域名全局替换 |
| 搜 `site:域名` 看不到 | 还没被收录 / 刚提交 | 等几天，先请求编入索引 |

---

## 七、检查收录进度

- GSC 左侧 **「效果」** 看曝光/点击
- 直接 Google 搜： `site:genshin-guide-one-five.vercel.app`
- 几天后能看到你的页面，说明已收录成功。
