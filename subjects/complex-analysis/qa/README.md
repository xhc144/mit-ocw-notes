# 审查记录的适用范围

原50页版本由提交 `9f485afd58aef15e5747ff0503097f88e6ad1f54` 保存，原14章源文件在本次扩编中不改写。其历史数学和视觉审查证明只适用于当时的PDF，不充当扩编后PDF的逐页审查。历史版输出可从该提交读取。

`assessment-review/*-inventory.json` 冻结原题编号、最末子问、实际PDF定位；`*-source-review.md` 记录源错、许可边界和重复题。`*-chinese-review.*`、`ps-text-review.json` 是三个独立Sol审稿人的新题解数学与覆盖审查，包含实际查看版本的源文件哈希。新PDF的编译、链接、最终逐页视觉及ZIP重编分别以当前 `validation-report.json`、`pdf-audit.json`、`visual-review.json`、`zip-rebuild.json` 的实际PDF哈希为准。

源图PNG和编译缓存仅供审查运行，不发布、不进入干净源码ZIP。数学图均为可编辑TikZ，官方PDF原件保持原字节。自动验证与人工数学、视觉检查分别记录，不能互相替代。

当前源码ZIP只含中文编译所需的49个TeX输入、实际模板及构建依赖，不含英文原件、网页快照或审稿档案。这些档案继续保存在仓库及既有提交中。`package-boundary.json`记录包内清单、包装前后文件数/字节数和实际TeX依赖核对；`zip-rebuild.json`记录清理后的源码包在空目录重编与已验收124页PDF的逐页文字、像素及链接比较。本次仅修复包装边界，未重写正文或重新宣称数学审稿。
