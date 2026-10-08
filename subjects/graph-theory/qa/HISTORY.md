# 图论验收记录的版本边界

初版为 56 个物理页，内容提交为 `21b19762fb555a27cfe9812d23139425404f317b`，远端核验回执提交为 `8569d16c8b39fa9c4edacb2aa235e32e051d0c99`。`upload-manifest.json`、`upload-selection.json`、`upload-receipt.json` 与三份 `visual-pages-*` 是这个旧版的历史证据，不代表新增官方评测题版。

当前扩编版正文为 157 个物理页。五份 `visual-expanded-*` 绑定同一个最终 PDF SHA-256，覆盖全部 157 页；六份 `assessments-review-*` 绑定新增题解的最终源文件，旧五份数学审稿仍绑定未修改的前 17 章。`course-metadata-review.md` 另核五门课程的参考信息。计数区分 256 个一级回答单元与 258 个末端小问，另有 75 个在线 Q。

五份 `assessments-inventory-*` 是写作前冻结的调查快照；其中待定状态不等于当前完成状态。当前范围和题号使用 `assessment-selection.json`，逐题完成与最终独审绑定使用 `assessment-completion.json`。6.042 作者 QA 在独审完成后仅追加嵌套小问计数证据；八个数学源文件没有因此改变，独审中的早先作者 QA 哈希保留其当时快照。

用户后来明确授权公开原仓库。原有 v2 工具仍保持仅允许私有仓库的限制，受阻的旧检查点未重新启动、删除或升级。本版使用用户授权的普通原生 Git 路径，仍冻结专属文件、保留实际远端父提交、使用非强制提交并验证全部远端字节；不把原生流程伪装成 v2 私有发布成功。最终转移清单和回执使用 `public-upload-manifest.json` 与 `public-upload-receipt.json`，对应当前版本。根主页由总协调代理独占维护。

`QUALITY.json`、`final-checks.json`、`package-manifest.json`、`clean-rebuild.json` 和 `release.json` 描述当前产物。实际模型审读、有限实例计算、自动排版、视觉、干净重编与远端验证分别记录，不冒称人类专家或形式化证明。
