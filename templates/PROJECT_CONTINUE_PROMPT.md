# 项目续作指令模板

项目接入并首次推送后，把下面整段发给其他设备或其他代理：

```text
你将成为 <PROJECT_ID> 在当前设备、当前应用载体上的续作代理。不要假设你能看到其他设备或其他应用里的历史会话；以 Git 仓库为唯一事实源。

项目 ID：<PROJECT_ID>
项目仓库：<REPO_URL>
续作分支：<BRANCH；如果不确定填 auto>
共享控制仓库：git@github.com:alfred070985/ai-workspace.git

> 续作标准第一步（控制仓库优先）：若本机尚未 clone 控制仓库，先 `git clone git@github.com:alfred070985/ai-workspace.git ~/ai-workspace/control`，读其 README + CONTINUE_PROMPT 搭好 `~/ai-workspace/{control,projects,shared,local}` 框架，再 clone 业务项目仓库。控制仓库定义了目录规范与续作协议，必须先就位（见 `MULTI_MACHINE_RULES.md` R10）。

请严格执行以下恢复协议：

1. 工作范围仅限 <PROJECT_ID> 项目根目录，不得遍历父目录、兄弟项目或整盘寻找上下文。
2. 如果本机登记了该项目，使用登记路径；否则将项目仓库克隆到当前系统用户目录下的 ai-workspace/projects/<PROJECT_ID>。
3. 如果目录已存在，先核对 Git 远程地址。存在未提交改动、远程地址不符或项目身份不符时，停止并报告；不得 reset --hard、clean、覆盖或擅自暂存改动。
4. 安全获取远程更新：拉取采用 **merge**（保留双方改动、非破坏），而非 rebase / force；切到目标分支后执行等效于 `git pull` 的合并式更新。若交付清单等配置文件被多机并发改动，按"文件路径"upsert 解决，保留双方真实补登内容（R5 / R11）。
5. 项目使用 Git LFS 时，执行 git lfs pull，确认实际大文件已下载；只有指针时不得继续数据分析。
6. 首先只读取 START_HERE.md、AGENTS.md、.ai/project.yaml、.ai/state.md。核对 project_id 必须为 <PROJECT_ID>。
7. 运行项目声明的离线验证命令；不要连接生产服务，除非 AGENTS.md 明确允许并已完成环境检查。
8. 外部技能或能力包不复制凭证；按当前应用配置环境变量或本机软链接，无法确认路径时只问我这一项。若提示无 GitHub 权限：用 SSH 密钥（新机 `ssh-keygen` 生成公钥加入 GitHub）或 Personal Access Token（GitHub Settings → Developer settings 生成，勾 `repo`）；生产库凭证（如 `config.local.yaml`）需手动从旧机安全拷贝到新机同路径，永不进 Git（R9）。
9. 用不超过六行告诉我：项目、分支、当前 HEAD 提交、已完成、唯一下一步、阻塞。然后按 .ai/state.md 继续。
10. 每次暂停或完成阶段前，更新 .ai/state.md，运行真实验证，提交并推送当前分支；未成功推送必须明确说“尚未同步”。
11. 结束回复时给出实际 HEAD 提交号，使我可以直接转到下一台设备或另一个应用。

确认恢复完成后，直接继续 .ai/state.md 中的下一步。
```
