# <PROJECT_ID> 首次 Git 同步

- 远程仓库：`<REPO_URL>`
- 远程状态：<not_created-or-active>
- 首次本地提交：<COMMIT_HASH>
- 状态更新时远程提交：<COMMIT_HASH>
- 同步时间：<YYYY-MM-DD>

## 推送前检查

```bash
git status --short --branch
git remote -v
git lfs track   # 如项目使用 LFS
```

## 首次推送

远程必须是空仓库，不初始化 README、License 或 `.gitignore`。

```bash
git remote add origin <REPO_URL>
git push -u origin main
```

## 推送后核验

```bash
git ls-remote --symref origin HEAD main
git lfs ls-files       # 如项目使用 LFS
git lfs push --dry-run origin main
```

## 后续规则

1. 每次暂停前更新 `.ai/state.md` 并推送。
2. 不使用 `git reset --hard`、`git clean` 或覆盖未提交改动。
3. 其他电脑克隆后拉取 LFS 实际内容。
4. 跨环境入口以项目根目录的 `CONTINUE_PROMPT.md` 为准。
