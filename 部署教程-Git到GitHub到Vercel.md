# 教程一：从 Git → GitHub → Vercel 自动部署

> 适用：纯静态网站（HTML/CSS/JS 单文件或多文件），如本《原神》攻略站。
> 目标：改一次代码 → `git push` → 网站自动更新，网址永久不变。
> 前置：已装 Git、有 GitHub 账号、有 Vercel 账号（免费版即可）。

---

## 一、本地初始化（第一次做）

假设项目文件放在 `E:\workbuddy\项目名\`（**一律放 E 盘，别放 C 盘**）。

```bash
cd E:/workbuddy/项目名
git init
git add -A
git commit -m "initial"
```

> 首次提交前建议放一个 `vercel.json`，纯静态站用这个：
> ```json
> { "version": 2, "outputDirectory": "." }
> ```

---

## 二、登录 GitHub（只需做一次）

### 方法 A：用 GitHub CLI（推荐，最省事）
```bash
gh auth login
```
按提示选 GitHub.com → 选 HTTPS → 选「Login with a web browser」→ 它给一个一次性码，复制到浏览器授权即可。

### 方法 B：手动发 Personal Access Token（PAT）
1. GitHub 网页 → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate
2. 勾 `Contents: Read and write`
3. 把生成的 token 保存好，本地 push 时用户名填 GitHub 账号、密码填 token。

登录后让 git 走 gh 凭证（避免每次输密码）：
```bash
gh auth setup-git
```

---

## 三、建仓库并推送（一条命令）

```bash
gh repo create 项目名 --public --source=. --push
```

这条命令会自动：① 在 GitHub 建公开仓库 → ② 连 `origin` remote → ③ 推送当前分支。
仓库地址： `https://github.com/<你的账号>/<项目名>`

> 若仓库名已存在：`gh repo create 项目名 --public --source=. --remote=origin --push` 连已有仓库。

---

## 四、Vercel 关联部署（只需做一次）

1. 打开 https://vercel.com → 登录（点 **Continue with GitHub** 授权）
2. **Add New... → Project**
3. 在 **Import Git Repository** 里找到你的仓库 → 点 **Import**
4. 关键设置：
   - **Framework Preset** → 选 **Other**（纯静态站，不要选 Jekyll/Vite 等）
   - **Project Name** → 可自定义（最终地址 = `项目名.vercel.app`）
   - **Root Directory** → `./`
5. 点 **Deploy**

部署完拿到地址，如 `https://genshin-guide-one-five.vercel.app`。

---

## 五、统一域名（重要，避免 SEO 链接错乱）

拿到 Vercel 地址后，把代码里所有出现的**旧/占位域名**全局替换成新地址：

```bash
# 在 Linux/Git Bash 下批量替换（Windows 用 VS Code 全局替换更直观）
grep -rn "旧域名" index.html sitemap.xml robots.txt
# 确认后逐个改，或：
sed -i 's#旧域名#新域名#g' index.html sitemap.xml robots.txt
```

改完提交推送：
```bash
git add -A
git commit -m "fix: update domain"
git push
```

> ⚠️ **分支坑（我们踩过）**：GitHub 仓库默认分支可能是 `main`，而本地代码在 `master`，Vercel 默认拉 `main` 会部署成**另一个项目**。
> 解决：确保 Vercel 的 Production Branch 指向你的实际分支；或把代码推到 `main`：
> ```bash
> git push origin master:main --force
> ```
> 推送前务必把旧 `main` 备份：`git push origin <旧main的SHA>:refs/heads/backup-old-main`。

---

## 六、以后更新网站（日常）

你说"改 XX" → 我改完文件 → 执行：
```bash
git add -A
git commit -m "改动说明"
git push
```
Vercel 收到 webhook 自动重新部署，**你什么都不用做**，刷新网址就是新版。

> 若本地在 `master` 而 Vercel 盯 `main`，记得两个都推：
> ```bash
> git push origin master && git push origin master:main
> ```

---

## 七、排错速查

| 现象 | 原因 | 解决 |
|------|------|------|
| 线上不是我的站 | 分支错配（main/master） | 把代码推到 Vercel 实际拉的分支 |
| push 报 Connection reset | 网络抖动 | 重试；或 `git -c http.version=HTTP/1.1 push` |
| Vercel 地址每次都变 | 每次去 /new 新建项目 | 只首次 Import，之后只 push |
| 部署后内容没变 | CDN 缓存 | 等 1–2 分钟，加 `?v=1` 强刷 |
| 页面 404 | outputDirectory 设错 | vercel.json 设 `.`，Preset 选 Other |

---

## 八、换自己买的域名（可选，花钱）

1. 在域名商（如 Namecheap/阿里云）买 `.com`
2. Vercel 项目 → Settings → Domains → 添加域名
3. 按提示去域名商加 DNS 记录（CNAME / TXT）
4. 验证通过后，Vercel 自动签发 SSL，再把代码里域名替换成新域名推送。
