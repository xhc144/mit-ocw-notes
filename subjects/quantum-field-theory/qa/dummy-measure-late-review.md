# 作业8积分变量修复复核

结论：修复正确。已实际渲染并用`view_image(detail="original")`查看MIT OCW作业8原PDF第2页，式(17)明确使用`d³k/(2π)³`，其产生/湮灭算符、旋量、能量与相位全用同一动量k。

主文件第137行宏`\intp`固定展开为`\int\frac{\mathrm d^3p}{(2\pi)^3}`，不会随正文自动改积分变量。原模式式据此印成d³p却保留k型被积函数，确实有哑变量绑定错误。当前ps08第13行显式改成`\int\frac{\mathrm d^3k}{(2\pi)^3}`，与源式及上下文一致；归一化`1/√(2E_k)`与原相位转换均未改变。

## 版本与核查证据

- 修复前root快照SHA-256：`08271a420e9950dc76b3f141dee17f783b00256a505899ad01ca9df1563c8654`
- 修复后正文SHA-256：`0087707d5fcbc73412135e76397ca5d9ed2be6858b7a5eee316d008947a03349`
- 只把新显式测度恢复成旧`\intp`一次后，重新计算SHA-256恰等于修复前root快照：已验证。故该root补丁仅替换这一处积分测度。
- 原作业PDF SHA-256：`07ccd2728d93c1a84aa73b9ec59d5c533c2b146e3e2b5d09e752af6f8f325412`
- 匹配官方解PDF SHA-256：`d8a6193c39c079dba7cc55ed798c7a7a8a8024eb4ad136b36a496382821c74f0`
- 题源：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset08.pdf （第2页式17）
- 晚组`qa/assessment-8323-late.json`已为全部六套记录新增当前`final_sha256`，保留既有`sha256`历史字段，并说明此前编译/审读证据不自动绑定到改变后的版本。

## PDF视觉证据边界

先前`visual-pages-107-127.json/md`保持绑定旧冻结PDF SHA-256 `e3c107111e5e741d037a0638d7ec332f22cdc484fca8a96a307cd9246267aaaf`，未改写成新PDF结论。root正在重编译，新旧未变像素页需要逐页哈希对应才能复用既有视觉证据；实际改变页应重新打开检查。本报告是源式及单处补丁复核，不声称已经看过重编译后的页图。
