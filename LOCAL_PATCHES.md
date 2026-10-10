# Locally-carried patches on `main`

## Fork 身份（2026-10-09）

- 自维护线：**`origin` = https://github.com/849506054/ponytail-hermes**（本仓库的 `main` 就是我们自己的线，2026-10-09 起与上游分道扬镳）
- `upstream` = `DietrichGebert/ponytail`：只作只读参考，不再跟版、不往上推
- 基线：上游 `9cc65d0`（v5.1.0，含 neutral `shortcut:` 标记）＋本文件的改动
- 维护口径：改动直接落 `main` 并推 `origin`；本文件从"补丁 vs 上游"转为**改动日志**（下面各节按时间倒序保留历史）
- 版本口径（2026-10-09 用户定）：**5.1.0 就是本仓的第一个维护版**，后续迭代在这个版本基础上于本仓进行
- 生效状态（2026-10-10 起）：skill 与命令注册随 gateway 重启进运行进程；`skills/*/SKILL.md` 由使用方按需加载。

## 注入机制摘除（2026-10-10，本地决策）

- 需求（用户定）：Ponytail 不出现在日常会话里——「把这一块直接摘除掉」。同一个需求分两轮落地：先摘收尾句，同日再摘整条注入。
- 改动面：
  - `__init__.py`：删掉整条注入路径——档位常量与归一化、`_config_dir` / `_default_mode`、`_mode_marker`、`_strip_frontmatter`、`_filter_skill_body_for_mode`、`_fallback_instructions`、`build_injected_context`、`_pre_llm_call` 及 `pre_llm_call` 钩子注册、`/ponytail` 档位命令；`register()` 只做 skill 注册 + `pre_gateway_dispatch` + 五个命令。
  - `plugin.yaml`：`provides_hooks` 只余 `pre_gateway_dispatch`；`provides_commands` 去掉 `ponytail`；描述改为按需加载。
  - `skills/ponytail/SKILL.md`：删档位表、`argument-hint`、`Levels:` 描述、`Switch level` 句；保留规则本体、作用域行与 "stop ponytail" 退出语。
  - `skills/ponytail-help/SKILL.md`：整卡重写为技能表 + 调用方式。
  - `skills/ponytail-gain/SKILL.md`、`skills/ponytail-debt/SKILL.md`：删档位/模式表述。
  - `README.md`：删档位、配置面、收尾句与「每会话激活」描述；命令表去掉 `/ponytail` 行。
- 保留交付面：`ponytail` skill 本体 + 五个命令（review / audit / debt / gain / help）。
- 生效路径：钩子注册随 gateway 重启进运行进程；已注入过旧块的会话在压缩或新会话前持有旧文案。
- 验证：`verify_ponytail_patches.py`（规则在场 / 三处删除串缺席 / 无注入机件 / 注册面完整 / 命令改写）+ `py_compile` + stub ctx 上真跑 `register()`。
- 版本：维持 5.1.0（本仓维护版号，与前两次迭代同口径）。

## ~~作用域收窄 + 收尾句摘除（2026-10-10）~~ 已被同日的「注入机制摘除」取代

- 当时做法：正文补作用域行 `Scope: coding and build work only…`；收尾句及其 `PONYTAIL_FOOTER` / `footer` 开关整体摘除；描述补回 non-coding 排除。
- 留存：作用域行与描述里的 non-coding 排除仍在 `skills/ponytail/SKILL.md`。

## ~~__init__.py — PR #787 (fix(hermes): avoid repeated context injection)~~ 已销项（2026-10-04 上游合并）

- **状态：已上游化**。PR #787 merged（merge commit `9410bcb`），随 v4.10.3 发布；升级后 `git pull` 吸收，本地 #787 diff 丢弃。工作树中 `_pre_llm_call` 的去重守卫（api_content marker 检查）现全部来自上游。
- 历史（应用日期 2026-09-08）：
- 上游：https://github.com/DietrichGebert/ponytail/pull/787（已于 2026-10-04 前合并）
- 基线：974d940（v4.9.0 线，main）
- 内容：`_pre_llm_call` 读取 `conversation_history[*].api_content` 中最近的模式标记
  （`PONYTAIL MODE ACTIVE — level: <mode>`），同模式跳过注入、模式变化才重注入——
  消除 Hermes 每轮 ~5.4KB 全量规则重复注入（Hermes 将 hook context 持久化到
  api_content，N 轮会话累积 N 份）。
- 本地验证：py_compile + PR 附带测试断言（首次注入/同模式跳过/切换重注入/切换后跳过）全过
- 补丁文件：/opt/data/backups/ponytail-pr787-local.patch
- 升级前评估：PR #787 合并进 upstream main 后，`git pull` 即可吸收，本地 diff 丢弃；
  未合并而要升级时先 `git stash` / 重放补丁文件再对齐。

## __init__.py + skills/ponytail/SKILL.md — patch 循环纪律（本地规则）

> 口径更新（2026-10-10）：本节「升级前评估 / 升级流程」写的是**跟版口径，已作废**——本仓自 2026-10-09 起为自治型 fork（见文首「Fork 身份」），`upstream` 只读参考、不跟版不重放。正文原样保留作 2026-09-08 历史快照。

- 应用日期：2026-09-08（v5.0.0 基线 2026-10-08 重放）
- 来源：Responses 适配任务复盘（同定点补丁连续失败 ~6 次均为补丁自身引入的错误，
  返工占任务近半时间）；与上游 PR #758 的 bounded-check 方向一致但独立成文
- 内容：`_fallback_instructions()` 尾部 + SKILL.md「The smallest complete change」段的
  bug-fix bullet 之后各一条——同一定点补丁连续 3 次失败（编译/lint/测试）即停止微补丁，
  重读整个函数/分支后一次性重写该块
- 本地验证：`python3 /opt/data/skills/software-development/hermes-plugin-upgrade/scripts/verify_ponytail_patches.py /opt/data/plugins/ponytail`
  （3 次补丁纪律注入 / 三处违规串缺席 / 模式过滤互斥 / 去重守卫回归）全过 + py_compile
- 可重放补丁：/opt/data/backups/ponytail-init-full-20261008-120639.patch、
  /opt/data/backups/ponytail-skill-full-20261008-120639.patch（当前全量 diff，取代 20261004 两版）
- 升级前评估：纯新增行，upstream 合并同类规则或重构 SKILL.md 时以 upstream 为准重放；
  **升级流程**：新 tag/远端更新 → `hermes-plugin-upgrade` skill 全流程
  （评估远端 diff 是否触及 `_pre_llm_call`/`_fallback_instructions`/SKILL.md →
  stash 或重放补丁文件 → py_compile + 上面的断言集 → 重启 gateway 生效）
- 生效方式：SKILL.md 每轮注入时现读磁盘 → 新会话即时生效；`__init__.py` 改动需重启 gateway

## 未合并的其他 open PR 筛查结论（2026-09-08）

其余 open PR（#822/#813/#797/#827/#829/#828 等）均只改 `hooks/*.js`
（Claude/Codex/Copilot/Kiro/pi 的 JS hook 体系），不触及 Hermes Python 适配器
（本插件的安装形态），无需本地合并。

### 2026-10-04 v4.10.2 (54e00c3) → v4.10.3 (c982cd4)

- 方式：`git stash push` 本地补丁 → `git merge origin/main`（17 提交）→ `git stash pop`；唯一冲突在 `_pre_llm_call` 的一行注释（上游 #787 已合并，本地 #787 实现与之逐字同形）→ 取上游，**#787 本地补丁销项**
- PR #787 merged（merge commit 9410bcb）→ 去重守卫现由上游维护
- 仍携带 2 条本地规则：`__init__.py` `_fallback_instructions` 补丁循环纪律（上游 SKILL.md 已有同类规则，fallback 无 → 继续携带）；SKILL.md 三处删除（上游 4.10.3 仍含 `Ship the lazy version`/`Never stall on an answer`/`Ship the one-liner`）+ 循环纪律段
- 新的可重放全量 diff：`/opt/data/backups/ponytail-init-full-20261004-102228.patch`、`/opt/data/backups/ponytail-skill-full-20261004-102228.patch`（取代 10-03 两版）；`ponytail-pr787-local.patch` 已作废可删
- 备份：`/opt/data/backups/ponytail-v4.10.2-<ts>`（整目录）+ stash 已 drop
- 验证：`py_compile` OK、`verify_ponytail_patches.py` 全过（含 #787 守卫断言，现测上游实现）、`git status` 仅剩两补丁文件 + LOCAL_PATCHES.md
- 生效：`__init__.py` 磁盘内容已变 → 需重启 gateway 才加载新模块（当前运行进程仍是 v4.10.2 字节码；功能等价，本地守卫行为相同）；SKILL.md 每轮现读，新会话即时生效
- HEAD=c982cd4=origin/main；plugin.yaml version 4.10.3；本地无 v4.10.3 tag（cron 检测用 origin/main 版本号即可）

### 2026-10-03 v4.10.0 (e3ba2aa) → v4.10.2 (54e00c3)

- 方式：`git stash push -- __init__.py skills/ponytail/SKILL.md` → `git merge --ff-only origin/main` → `git stash pop`（自动合并 `__init__.py` 无冲突）
- 上游提交（v4.10.0..v4.10.2，共 16 提交）：OpenCode 2 插件 API 移植、hooks 系列修复（POSIX 守卫、stdin fallback timer、regex 回溯时盒、plugin root 插值）、`pi` extension 修复、docs/版本号
- 上游触及本地补丁文件的情况：`skills/ponytail/SKILL.md` **零 diff**（补丁原样保留）；`__init__.py` 有 10+/2- 改动，全在 `_filter_skill_body_for_mode`（**与本地补丁的 `_fallback_instructions` / `_pre_llm_call` 不同函数**）→ 无冲突，补丁原样保留
- 上游 v4.10.2 内含 PR #875（`example_label` 正则要求引号值 + `re.split` 保留尾部换行）：前者防「规则 bullet 首词是模式名被误当 worked example 删掉」，后者补 `splitlines()` 丢尾换行的差 1 字节。**与本地补丁同向，不再需要本地实现**；本机 SKILL.md 的规则行（`- Deletion over addition. ...`）实测未被误删
- 三处删除串（`Ship the lazy version` / `Never stall on an answer` / `Ship the one-liner`）上游 SKILL.md 仍在（各 1 命中）→ SKILL.md 补丁继续携带
- PR #787 仍未合并（`state: open, merged: false`，2026-10-03 查）→ `__init__.py` 的 #787 补丁继续携带
- 新的可重放全量 diff：`/opt/data/backups/ponytail-init-full-20261003_093213.patch`、
  `/opt/data/backups/ponytail-skill-full-20261003_093213.patch`（**取代** 09-15 两个版本，`git apply --check --reverse` 均通过；`ponytail-pr787-local.patch` 基线为 v4.9.0 行号，已被这两个全量 diff 取代，不再单独重放）
- 备份：`/opt/data/backups/ponytail-v4.10.0-20261003_093114`（整目录）
- 验证：`py_compile` OK + `git describe --tags --exact-match` = `v4.10.2` + 断言集全过
  （断言脚本 `/opt/data/work/ponytail-upgrade/verify_ponytail_patches.py`：lite/full/ultra 注入含 3 次补丁纪律、
  review 与 fallback 不含三处删除串、`off` 空串、lite/ultra 表格行互斥、full 规则行未被过滤误删、
  #787 去重守卫「同模式→None / 模式变化→注入 / 无历史→注入 / 最新标记优先」）
- 注入文本前后对比：lite 5367→5368、full 5394→5395、ultra 5409→5410（+1 字节 = 上游尾部换行修复），review/off 不变
- 生效：`__init__.py` 字节已变（含上游 v4.10.2 改动）→ **需重启 gateway** 加载新模块；SKILL.md 每轮现读磁盘，新会话即时生效
- 坑位：本地 tag `v4.10.1` 在 `git fetch` 前已存在但 `origin/main` 当时是 v4.10.0 线；升级时上游已推进到 v4.10.2 → **以 `origin/main` 最新稳定 tag 为准**，不按 cron 报告里写死的版本号

### 2026-09-15 v4.9.0 (974d940) → v4.10.0 (e3ba2aa)

- 方式：`git merge --ff-only origin/main`（11 提交：Cursor native hooks 的 JS/JSON + docs/README 徽标 + plugin.yaml 版本号）
- tag 说明：`v4.10.0` 指向 `1d95ff7`，本地 HEAD `e3ba2aa` 是同一 release 的另一提交，`git diff v4.10.0 HEAD` 为空（树完全一致）→ 内容等价，`git describe --tags --exact-match` 会失败属正常，不要据此判定升级失败
- 上游是否触及本地补丁文件：`git diff HEAD..v4.10.0 -- __init__.py skills/ponytail/SKILL.md` 为空 → 两处补丁**原样保留**，升级前后 sha256 一致（`dad381784dee97d8` / `2a4677d00ff87648`）
- 三处删除串上游仍在（`Ship the lazy version` / `Never stall on an answer` / `Ship the one-liner` 各 1 命中）→ SKILL.md 补丁继续携带；PR #787 仍未合并（`git log v4.10.0` 无对应提交）→ `__init__.py` 补丁继续携带
- 新的可重放全量 diff：`/opt/data/backups/ponytail-init-full-20260915_074436.patch`、
  `/opt/data/backups/ponytail-skill-full-20260915_074436.patch`（**取代** 09-09 / 09-12 两个版本，`git apply --check --reverse` 均通过）
- 备份：`/opt/data/backups/ponytail-v4.9.0-20260915_074436`（整目录）
- 验证：`py_compile` OK + 断言集全过 —— full/lite/ultra 注入含「同一补丁连续 3 次失败即重写该块」；三处删除串在 full/lite/ultra/review 与 `_fallback_instructions()` 中均不存在；`off` 空串；lite/ultra 表格行只在对应模式；#787 去重守卫（同模式返回 `None`、模式变化重注入、无历史/无标记时正常注入）
- 生效：`__init__.py` 与 `SKILL.md` 字节未变（补丁早已部署）→ **无需重启 gateway**；`hermes plugins list` 已显示 ponytail 4.10.0
- 坑位（已同步 `hermes-plugin-upgrade` skill）：`hermes plugins update ponytail` 会跑**仓库级**安全扫描，整包 97 findings（全在 README/benchmarks/docs/examples/tests/.github）判 **DANGEROUS → 自动 disable 插件**；运行时路径（`__init__.py` / `skills/ponytail` / `commands/`）零命中，复核后 `hermes plugins enable ponytail` 恢复（未授予 tool-override）。附带生成占位 `.env`（`ANTHROPIC_API_KEY=sk-ant-...`，promptfoo 用，Hermes 不加载）
- `core.fileMode=false` 已设置：ff-merge 后有 26 个文件显示为 mode-only 改动（容器 644↔755），设后 `git status` 只剩两处真实补丁 + 未跟踪的 `LOCAL_PATCHES.md`

## v4.13.0 升级（2026-10-06，`v4.10.3-10-gc982cd4` → `v4.13.0-2-g552acd5`）

- 方式：`git merge --ff-only origin/main`（54 提交；含 release tag `v4.13.0` = `08e952d`，HEAD 落在其后 2 个 chore 提交，与历次「跟 main」一致）
- 上游触面评估：`skills/ponytail/SKILL.md` **未被触及**；`__init__.py` 被 3 个提交改过（`31e7229` BOM、`00f1aa3` 模式归一、`944b5dc` 测试隔离），均在配置读取/模式归一区，**不涉 `_fallback_instructions`** → 两处补丁原样重放
- 重放：`git stash push -- __init__.py skills/ponytail/SKILL.md` → ff → `git stash pop` **无冲突**；diff 规模与升级前逐项一致（2 文件 11 insertions / 3 deletions）
- 可重放补丁：`/opt/data/backups/ponytail-local-diff-20261006-084234.patch`（全量 tracked diff）
- 验证：`py_compile` OK；`python3 /opt/data/work/ponytail-upgrade/verify_ponytail_patches.py /opt/data/plugins/ponytail` → **PASS（全部断言）**；`git stash list` 空
- 清单版本位：`plugin.yaml` / `package.json` 已是上游的 `4.13.0`（本次上游改动了 `__init__.py` → **需重启 gateway 生效**）
- 生效状态：**已生效**（2026-10-06 08:46 重启 gateway → `hermes plugins list` 显示 ponytail **4.13.0**；重启后重跑断言集 PASS；本地 diff 仍在：`__init__.py` + `skills/ponytail/SKILL.md`）

## v5.0.0 升级（2026-10-08，`v4.13.0-2-g552acd5` → `v5.0.0` = `b088b2d`）

- 方式：`git stash push -- __init__.py skills/ponytail/SKILL.md` → `git merge --ff-only origin/main`（含 #1061「Ponytail 5, rebuilt rules」+ #1062 release）→ 按新基线手工重放
- 上游触面：`skills/ponytail/SKILL.md` **整篇重写**（134 行变动、113 删减）→ 三处「先做后问」违规串上游已自行删除，**SKILL.md 删除类补丁销项**；`__init__.py` 的 `_fallback_instructions` 文案重写，本地循环纪律需重放（v5.0.0 SKILL.md 无同类规则 → 继续携带）
- 重放结果：本地 diff 由 11 insertions/3 deletions 缩到 **4 insertions/1 deletion**（SKILL.md 只剩 1 条循环纪律 bullet，落在「The smallest complete change」段的 bug-fix bullet 之后）
- 验证：py_compile OK；`verify_ponytail_patches.py` PASS（断言按 v5.0.0 文案更新：lite「Build what was asked」/ ultra「Also question the request」/「Deletion beats addition」）；脚本归位 skill `scripts/` 并同步工作区副本
- 备份：`/opt/data/backups/ponytail-v4.13.0-20261008_120510`（整目录）+ `ponytail-v4.13.0-local-20261008_120510.patch`（升级前本地全量 diff）
- 生效状态：**已生效**（2026-10-09 01:36:01 gateway 重启，晚于 `__init__.py` 落盘 2026-10-08 12:06 → v5.0.0 模块已在运行进程；SKILL.md 每轮现读，注入文本本来就是 v5.0.0）

## SKILL.md 去重（2026-10-09，本地决策）

- 决策口径：**重复面保留在 `AGENTS.md` / `USER.md` 已有的表述，插件侧摘除**；非重复面一律不动。
- 摘除内容（逐句核对后的整句重复）：阶梯第 1 级「Does it need to exist…」、第 6 级「Otherwise: the minimum code that works.」、bullet「No abstraction, wrapper… nobody asked for.」与「Deletion beats addition.」、「The shortest working diff wins…」、「Bug fix: before you edit, grep every caller…」、「Before you write」末句「That is scope. Extra features are not.」；阶梯重编号为 1-4。
- 保留未动：persona、收尾句（footer）、阶梯第 2/3/4/5 级、`ponytail:` 注释约定、3 连败停手重读、移动/合并保留错误处理、同尺寸取边界正确、非平凡逻辑带自检、Never cut 安全底线、档位表与档位机制。
- 效果：注入体积 full **3107 → 2459** 字符（lite 2514 / ultra 2528 / off 0），footer 在 lite/full/ultra 均保留。
- 验证：`verify_ponytail_patches.py` PASS（新增「重复面已摘除」断言；模式过滤断言改用「Keep the structure the codebase already has」）+ py_compile OK。
- diff 形状：`skills/ponytail/SKILL.md` 7 insertions / 10 deletions（含阶梯重编号）；`__init__.py` 4 insertions / 1 deletion（`_fallback_instructions` 未同步，仅在 SKILL.md 读不到时兜底）。
- 备份：`/opt/data/backups/ponytail-dedup-20261009/`（SKILL.md + `__init__.py` + 校验脚本）。
- 生效：SKILL.md 每轮现读 → **已生效**。
- 其它 agent 的分发件当时保留 → 当晚随下一节一并移除。

## 非 Hermes 客户端适配件移除（2026-10-09，fork 口径）

- 依据：仓库已定为 `ponytail-hermes`，其它 agent / 客户端的适配面不再需要。
- 移除（95 个文件）：客户端配置目录 `.agents`、`.claude-plugin`、`.clinerules`、`.codex-plugin`、`.cursor`、`.devin-plugin`、`.grok-plugin`、`.kimi-plugin`、`.kiro`、`.openclaw`、`.opencode`、`.qoder`、`.qoder-plugin`、`.windsurf`；扩展清单 `gemini-extension.json`、`opencode.json`、`pi-extension/`、`plugin.json`；JS hook 层与工具 `hooks/`、`scripts/`、`commands/*.toml`、`package.json`；JS 测试套件 `tests/`；仓库 CI 与 Copilot 说明 `.github/`；客户端安装文档 `INSTALL.md`、`after-install.md`、`docs/`、`i18n/`。
- 留存：`skills/`（注入文本 + 六个命令 skill）、`__init__.py`、`plugin.yaml`、`benchmarks/`（README 数字的出处）、`examples/`、`assets/`、`README.md`、`AGENTS.md`、`LICENSE`、`LOCAL_PATCHES.md`。
- README 同步：去掉 i18n 语言链接、客户端安装段与多宿主命令说明，改为单一安装口径 `hermes plugins install 849506054/ponytail-hermes` 与 fork 标识。
- 内联引用同步：`__init__.py` 里指向 `hooks/ponytail-instructions.js` 的注释改为只引 `#571`。
- 验证：`verify_ponytail_patches.py` PASS；`inspect_ponytail_injection.py` 逐档体积不变（full 2468 / lite 2523 / ultra 2537）；py_compile OK；`hermes plugins list`（新进程）读到 ponytail **enabled / 5.1.0**，六个命令与四档注册完整。
- 备份：`/opt/data/backups/ponytail-hermes-20261009-client-adapters.tar.gz`（135 条目；git 历史同样可回溯）。

## ~~页脚显示开关（2026-10-09，本地新增）~~ 已撤销（2026-10-10）

- 当时做法：`__init__.py` 加 `FOOTER_SENTENCE` 与 `PONYTAIL_FOOTER` / `config.json` 的 `footer` 开关，去重守卫改比 (档位, 页脚状态)。
- 撤销：收尾句本身就是"管我怎么说话"的规则，按用户口径连句子与开关一并摘除（见本文件「作用域收窄 + 收尾句摘除」节）；该开关在本机只用过默认态，无外部依赖。

