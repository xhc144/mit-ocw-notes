# 审查记录的适用范围

原50页版本由提交 `9f485afd58aef15e5747ff0503097f88e6ad1f54` 保存，原14章源文件在本次扩编中不改写。其历史数学和视觉审查证明只适用于当时的PDF，不充当扩编后PDF的逐页审查。历史版输出可从该提交读取。

`assessment-review/*-inventory.json` 冻结原题编号、最末子问、实际PDF定位；`*-source-review.md` 记录源错、许可边界和重复题。`*-chinese-review.*`、`ps-text-review.json` 是三个独立Sol审稿人的新题解数学与覆盖审查，包含实际查看版本的源文件哈希。新PDF的编译、链接、最终逐页视觉及ZIP重编分别以当前 `validation-report.json`、`pdf-audit.json`、`visual-review.json`、`zip-rebuild.json` 的实际PDF哈希为准。

源图PNG和编译缓存仅供审查运行，不发布、不进入干净源码ZIP。数学图均为可编辑TikZ，官方PDF原件保持原字节。自动验证与人工数学、视觉检查分别记录，不能互相替代。
