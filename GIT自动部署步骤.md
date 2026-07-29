# 原神攻略站 · Git 自动部署到 Vercel 步骤

> 目标：把 `genshin-guide/` 变成 Git 仓库，连上 GitHub + Vercel，**以后我改完文件，只需一条 `git push`，Vercel 自动重新部署**，不用再手动拖文件夹。

本地仓库已经帮你初始化并提交了（commit `383ec67`）。你只需完成「连 GitHub」和「连 Vercel」这两步。

---

## 第 1 步：装 GitHub CLI 并登录（推荐，最省事）

1. 下载安装 GitHub CLI：https://cli.github.com/ （Windows 选 exe 安装包）
2. 打开 **Git Bash**（或 PowerShell），登录你的 GitHub 账号：
   ```bash
   gh auth login
   ```
   按提示选：GitHub.com → HTTPS → 用浏览器登录（会自动打开网页授权）
3. 一键创建 GitHub 仓库并推送（在仓库目录里执行）：
   ```bash
   cd "E:/workbuddy/2026-07-29-09-05-15/genshin-guide"
   gh repo create genshin-guide --private --source=. --remote=origin --push
   ```
   这条命令会：在 GitHub 建一个名为 `genshin-guide` 的私有仓库 → 关联本地 → 直接 push 上去。

> 不想装 CLI？备选方案：去 github.com 网页「New repository」建一个**空仓库**（别勾 README），然后执行：
> ```bash
> cd "E:/workbuddy/2026-07-29-09-05-15/genshin-guide"
> git remote add origin https://github.com/你的用户名/genshin-guide.git
> git branch -M main
> git push -u origin main
> ```
> 注意：HTTPS 方式 push 时 GitHub 不再接受密码，需用 **Personal Access Token**（在 GitHub → Settings → Developer settings 生成，权限勾 repo）当密码填。

---

## 第 2 步：在 Vercel 导入这个 GitHub 仓库（从此自动部署）

1. 打开 https://vercel.com ，登录 `kyle-eac8`
2. 点 **「Add New…」→「Project」**
3. 在「Import Git Repository」里选 **GitHub**，授权 Vercel 访问（首次会弹授权页）
4. 找到 `genshin-guide` 仓库，点 **Import**
5. Framework Preset 选 **Other** / 不动（静态站会自动识别），直接点 **Deploy**
6. 部署完拿到新地址，例如 `https://genshin-guide-xxxx.vercel.app`

✅ 完成！之后**只要 `git push`，这个地址就自动更新**，不用再拖文件夹。

> 旧的 `genshin-guide-three.vercel.app`（Drop 上传版）现在可以不管，也可在 Vercel 项目设置最底部「Delete Project」删掉。

---

## 第 3 步（以后常用）：我改完文件，你只需 push

以后我在这个文件夹里改好内容后，你（或我，若你的 GitHub 凭证已缓存）执行：

```bash
cd "E:/workbuddy/2026-07-29-09-05-15/genshin-guide"
git add -A
git commit -m "更新：说明这次改了啥"
git push
```

push 成功 → 几秒后 Vercel 自动重新部署 → 线上就是最新版。

---

## 注意事项

- **commit 作者邮箱**：本地仓库默认设的是 `kyle@users.noreply.github.com`（GitHub 的隐私邮箱格式）。若想让贡献图算到你账号，先确认该邮箱已加到 GitHub → Settings → Emails；或改成本地真实邮箱：
  ```bash
  git config user.email "你真实的github邮箱"
  ```
- **域名**：当前站点文件里的域名是 `genshin-guide-three.vercel.app`。第 2 步导入后若 Vercel 给了新地址，把新地址发我，我把 `index.html`(canonical/hreflang/JSON-LD/og:url)、`sitemap.xml`、`robots.txt` 三处域名一次性改掉再 push。
- **私有仓库**：上面用 `--private` 是私有的，Vercel 仍能访问（你授权过）。想公开也行，把 `--private` 去掉即可。
