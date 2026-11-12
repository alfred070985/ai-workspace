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

## 校验

```bash
python3 scripts/validate.py
```

该校验会检查必要模板、项目 ID 格式以及登记表中是否存在本机绝对路径。
