# <PROJECT_NAME>：从这里继续

- **项目 ID**：`<PROJECT_ID>`
- **当前阶段**：<用一句话说明当前阶段>
- **当前下一步**：<只写一条最具体的动作>
- **当前阻塞**：<没有则写“无”>

新环境按顺序读取，不要先遍历整个目录：

1. `AGENTS.md`：项目边界、工作规则、命令和验收标准。
2. `.ai/project.yaml`：项目身份、远程仓库和外部依赖。
3. `.ai/state.md`：真实进度、唯一下一步、阻塞和验证状态。
4. `.ai/decisions/`：长期决策。

## 离线检查

```bash
<PROJECT_OFFLINE_VERIFY_COMMAND>
```

跨环境交接以项目根目录的 `CONTINUE_PROMPT.md` 为准。
