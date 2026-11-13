# ai-workspace

这是跨设备、跨应用续作体系的**私有控制仓库**。它不保存具体项目的业务数据，只保存：

- 多项目登记表；
- 通用续作指令；
- 新项目接入模板；
- 本机路径与技能适配规范。

## 推荐目录

```text
~/ai-workspace/
├── control/                  # 本仓库的本地克隆
├── projects/
│   └── <project-id>/         # 各项目自己的 Git 仓库
├── shared/                   # 本机外部能力包的软链接
└── local/                    # 各电脑自己的路径登记，不进 Git
```

## 快速使用

### 1. 克隆控制仓库

```bash
git clone git@github.com:alfred070985/ai-workspace.git ~/ai-workspace/control
```

### 2. 登记项目

每个长期项目在 `registry.yaml` 中登记一条逻辑记录：

```yaml
projects:
  prj-demo:
    name: 示例项目
    repo: git@github.com:alfred070985/prj-demo.git
    repo_status: active
    default_branch: main
    entry: START_HERE.md
```

登记表只保存项目 ID、仓库地址、默认分支和入口文件，**不保存本机绝对路径**。

### 3. 接入新项目

在项目根目录中，把 `templates/PROJECT_ONBOARDING_PROMPT.md` 的整段指令发给当前代理。它会在项目仓库中生成标准续作结构。

### 4. 跨环境继续项目

项目首次推送后，使用项目自己的 `CONTINUE_PROMPT.md`。也可以参考仓库根目录的通用版本 `CONTINUE_PROMPT.md`。

## 固定规则

1. 每个长期项目一个独立私有仓库。
2. 项目续作状态保存在项目自己的 `.ai/state.md`，不保存在本控制仓库。
3. 历史聊天不是事实源；Git 仓库和项目入口文件才是事实源。
4. 新环境必须显式提供 `project_id`，不得通过扫描兄弟目录猜测项目。
5. 各电脑真实路径保存在本机 `local/`，不要提交。
6. 外部技能或能力包优先通过软链接或环境变量适配；不要复制带本机凭证的能力包。
7. 项目暂停前必须更新状态、提交并推送；未推送不得声称已跨设备同步。
8. **项目仓库必须自包含**：脚本 / 工具使用仓库相对路径（基于 `__file__`，禁止写死本机绝对路径），重生成所需源数据提交进仓库（大文件走 Git LFS），不得依赖本机桌面 / 下载等散落文件。详见 [`MULTI_MACHINE_RULES.md`](./MULTI_MACHINE_RULES.md) 的 R1–R3。
9. **交付登记即时且幂等**：交付物创建即登记进交付清单（相对路径、字节数、SHA256），清单按文件路径 upsert（同一文件只一行），不得事后补登或盲目追加；归档 / 汇总文档随状态实时更新，不得保留与现状相反的旧结论。详见 [`MULTI_MACHINE_RULES.md`](./MULTI_MACHINE_RULES.md) 的 R4–R8。
10. **续作框架显式说明新环境认证引导**：GitHub 用 SSH 密钥或 PAT 获取；生产库凭证需手动从旧机拷贝且永不进 Git；并区分"仓库内自包含的数据/脚本"与"需本机准备的认证钥匙"。详见 [`MULTI_MACHINE_RULES.md`](./MULTI_MACHINE_RULES.md) 的 R9–R12。

## 跨设备续作范式规则

所有"需要跨设备 / 跨应用可续作"的项目，都受 [`MULTI_MACHINE_RULES.md`](./MULTI_MACHINE_RULES.md) 约束。该文件把一次真实跨机续作中暴露的遗漏（脚本硬编码绝对路径、源数据未入仓、交付清单漏登、归档文档过时、新机认证盲区、控制仓库未先 clone、多机并行 CSV 冲突）提炼为 R1–R12 范式规则，并在项目接入模板与续作模板中内化。

## 校验

```bash
python3 scripts/validate.py
```

该校验会检查必要模板、项目 ID 格式以及登记表中是否存在本机绝对路径。
