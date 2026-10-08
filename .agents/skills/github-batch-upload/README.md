# GitHub 批量上传 Skill 2.0

在已验证的 `lecture-notes/tools/github-batch-upload` 上升级，复用 `a170d65a5646eafb0798f12c741f1cc9b7efbbba`，保留原 53 项回归测试。完整目录可以交给其他 AI；无需第三方 Python 包。

新增持久冻结快照、工作区和候选提交恢复；同仓库所有分支的本地进程锁；检查远端后的有限超时/429/5xx重试；有限并发快照；分阶段耗时；敏感名称和明显凭据内容阻止；幂等仓库安装。原有哈希去重、单次暂存/提交/push 和远端完整性核验保持。

- [小型 Skill 入口](SKILL.md)
- [原生流程与恢复边界](references/workflow.md)
- [安装与环境边界](references/installation.md)
- [已连接 GitHub 回退流程](references/connector-fallback.md)
- [测试与来源记录](references/validation.json)
- [完整 ZIP](dist/github-batch-upload.zip) · [ZIP SHA256](dist/SHA256SUMS)

安装只复制此目录的索引文件到当前仓库 `.agents/skills/github-batch-upload`，不改 AGENTS、其他 skills、凭据或安全配置：

```bash
python3 scripts/install.py --repo /absolute/repo
```

运行：

```bash
python3 scripts/batch_upload.py manifest.json --source-root /authorized/input --checkpoint /private/batch-state --dry-run
python3 scripts/batch_upload.py manifest.json --source-root /authorized/input --checkpoint /private/batch-state --publish
```

LFS/大文件只检测并报告。原生运行已测 Linux/POSIX；Windows 可安装和读取，原生运行需既有 POSIX 环境。其他 saved environment 是否已加载必须分别核验，不以 Git 提交代替。未完成个人技能目录安装，也没有线上 GB 吞吐量或字节续传测试。

完整离线回归（本地合成 bare 仓库，不改生产仓库作测试）：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

源码原属用户私库，没有发现独立工具开源许可证；此包不额外授予开源许可。原历史测试日志保留在 lecture-notes 原目录，本包的验证记录只陈述本次实际运行。
