# 上传与发布步骤

1. 将压缩包内文件上传到仓库根目录，覆盖同名文件。
2. 图片目录必须保持为 `docs/assets/screenshots/`，文件名大小写不能改。
3. 如使用 Deploy from a branch：Settings → Pages → Branch 选 `main`，Folder 选 `/docs`，点击 Save。
4. 发布后访问 `https://alibabamayun888.github.io/fishing-game-source/`。
5. 将 `https://alibabamayun888.github.io/fishing-game-source/sitemap.xml` 提交到 Google Search Console 和 Bing Webmaster Tools。

如果你的账号 Actions 或 Pages 受限制，优先使用 Deploy from a branch，不需要上传 `.github/workflows/pages.yml`。
