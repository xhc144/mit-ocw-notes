# 中文书稿来源与改编范围

中文改编与编者解答采用 CC BY-NC-SA 4.0；完整法律文本见 licenses/CC-BY-NC-SA-4.0.txt。MIT及原作者不为本项目背书。没有复制商业教材题面，没有把编者解答标为官方解答。英文原件只留在仓库，此精简源码包不重复收录。

第1—15章保持上一105页版本；第16章三份18.S190题单24道大题/33显式末级子问，第17章六讲18.900理解题22道，第18章18.901 PS5六空间加三操作的126性质判定。原58编者题另计。严格不等号版PS3第7、8题保留并给非紧反例，非严格修正版另列。所有新增图由TikZ重绘，原PDF图形只作核查依据。

## 课程、作者与许可

| 课程及学期 | 原作者及记录者 | 原课程链接 |
|---|---|---|
| 18.102-spring2021 | Casey Rodriguez (lecturer); Andrew Lin (notes) | https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/ |
| 18.900-spring2023 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/ |
| 18.901-fall2004 | James Munkres | https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/ |
| 18.904-spring2011 | Andrew Snowden | https://ocw.mit.edu/courses/18-904-seminar-in-topology-spring-2011/ |
| 18.905-fall2016 | Haynes Miller (instructor); Sanath Devalapurkar (LaTeX record); Xianglong Ni (images) | https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/ |
| 18.950-fall2008 | Paul Seidel | https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/ |
| 18.965-fall2004 | Tomasz S. Mrowka | https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/ |
| 18.s190-iap2023 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/ |

## 原文件清单

下表为仓库中实际原件的逐文件页数与来源；页数是PDF物理页数，包含OCW来源页。只有这些记录不表示全部原件正文均已译入。各章开头说明实际选段和编者补充；原课程信息附各自Syllabus及Calendar链接。18.900第6讲仅为31.5题依赖图，其他题没有因此扩张；第40讲是OCW公开材料但2023春课堂略过。18.901 PS0—4及周练只有商业教材题号，缺完整题面；18.900正式PS及考试不公开。18.950十份作业另见独立微分几何分册，不重写。

| 仓库原件 | 物理页 | 原作者 | 官方文件链接 | SHA-256 |
|---|---:|---|---|---|
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_lec1.pdf` | 8 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec1.pdf | `01c746c0f543b62983745d79ca6aff8f9016287775ff1ea271b908f2748e2e25` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_lec2.pdf` | 8 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec2.pdf | `fe2c3ee55101ecd2229e8df45540a1c0bacfcbd3065bea05ed232a1c04878efb` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_lec3.pdf` | 8 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec3.pdf | `e9a63d2e8ebab205574982a0f194eea6f094d9ab18957956e1334b0fd3892292` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_lec4.pdf` | 6 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec4.pdf | `917e29c6b155f66db57c5de43a5f123a32aa5d62f29652511223aa716ba983a8` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_lec5.pdf` | 7 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec5.pdf | `c287459af0f1193221a11afab89c86805401bc63cee35509ff71005abe1eae44` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_lec6.pdf` | 6 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec6.pdf | `4b5903f7711bf0927549366a8240bd7f7a64235e0f53f3b4181808758ee52c13` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_pset1.pdf` | 3 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_pset1.pdf | `f068753a549055ebf7505a24ee94b30bc8333dab681c9053a2276198e9e086d6` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_pset2.pdf` | 3 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_pset2.pdf | `614fb99b2f6fec2dfc6bf7fe7f3b4ae261185973a820560a08f4d86f812a7dba` |
| `sources/18.s190-iap2023/pdf/mit18_s190iap23_pset3.pdf` | 3 | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_pset3.pdf | `bc968a2d5704e20a05005b6c606bf6bf7aaf1372d232926c9f0f5c058069c03a` |
| `sources/18.s190-iap2023/tex/mit18_s190iap23_lec1t.tex` | — | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec1t.tex | `e21a1780aba8ad340b9bde81a6a3cd194c88ad448fbbb6a242e7f3669534322a` |
| `sources/18.s190-iap2023/tex/mit18_s190iap23_lec2t.tex` | — | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec2t.tex | `04b5a0156dda2cb7fb11e996c47ecdf509f1f83317ede76af76d9665e8fd24c4` |
| `sources/18.s190-iap2023/tex/mit18_s190iap23_lec3t.tex` | — | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec3t.tex | `d239eaadc550d22a246d69307096a873567395c3253596a7e22d562f69297512` |
| `sources/18.s190-iap2023/tex/mit18_s190iap23_lec4t.tex` | — | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec4t.tex | `8af278db28292df13338225182eee7cf5972fb4880ec28b36829b75cb8ea71c9` |
| `sources/18.s190-iap2023/tex/mit18_s190iap23_lec5t.tex` | — | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec5t.tex | `c6bf511b3764eea44b168feeb42e9a01f43a70cfbf174c8bb689c3960c8a882f` |
| `sources/18.s190-iap2023/tex/mit18_s190iap23_lec6t.tex` | — | Paige Bright | https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/mit18_s190iap23_lec6t.tex | `6422594da4cffca549f0c3507959a723a3939ba60b6d7f022976e6ce23075955` |
| `sources/18.901-fall2004/pdf/4cb6350106757012459166df979b6643_notes_d.pdf` | 3 | James Munkres | https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/4cb6350106757012459166df979b6643_notes_d.pdf | `e343743e51e90c87a78c83ba97cfe2f813da7366a78d53989b265692a85fc711` |
| `sources/18.901-fall2004/pdf/bdcbc277a4da063b13550baf12206a6f_notes_k.pdf` | 5 | James Munkres | https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/bdcbc277a4da063b13550baf12206a6f_notes_k.pdf | `29d65311ce55905a19d787984c75b88f064c64a60fdccd574619fc4502def39a` |
| `sources/18.901-fall2004/pdf/e319b3a36ca774261b6b8c45e11804c2_notes_c.pdf` | 2 | James Munkres | https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/e319b3a36ca774261b6b8c45e11804c2_notes_c.pdf | `acec8fba72d563f979d7c16ae71ddb354ec057fe2d7c54c15cb35b2d26396c0c` |
| `sources/18.102-spring2021/pdf/MIT18_102s21_lec3.pdf` | 5 | Casey Rodriguez (lecturer); Andrew Lin (notes) | https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/f168e97ce4839083e546555a6a994697_MIT18_102s21_lec3.pdf | `d84dff4879c3c09b160d67eb69ae0de29ee3fe83c4bf885a44670681a6b9b593` |
| `sources/18.901-fall2004/pdf/notes_g.pdf` | 9 | James Munkres (instructor; source PDFs lack author metadata) | https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/534f34d4acff6e5733e89234c5e397bf_notes_g.pdf | `be8e6ed2755cd5d741a830faa06c7f9092d2b6e39fd17e606ea2967f8a58bb72` |
| `sources/18.905-fall2016/pdf/mit18_905f16_lec5.pdf` | 5 | Haynes Miller (instructor); Sanath Devalapurkar (LaTeX record); Xianglong Ni (images) | https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/8503170411716ef15d51a6b8b2bc3536_MIT18_905F16_lec5.pdf | `93ebdff23f26213525461c0c8748c7ab878406b7216e1a694df8b13b9c54f901` |
| `sources/18.905-fall2016/pdf/mit18_905f16_lec14.pdf` | 5 | Haynes Miller (instructor); Sanath Devalapurkar (LaTeX record); Xianglong Ni (images) | https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/bd586cc1ab67e339ff3a6bc13609241f_MIT18_905F16_lec14.pdf | `f66e90131b531bc6015d6199551f98a52be46432672b55009d9242efba2f8478` |
| `sources/18.905-fall2016/pdf/mit18_905f16_lec18.pdf` | 5 | Haynes Miller (instructor); Sanath Devalapurkar (LaTeX record); Xianglong Ni (images) | https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/1df7278a926d432190b76eb78b5d417e_MIT18_905F16_lec18.pdf | `38728d5c0c5d5bff8f40f54e2cf4f7f9f12f4528803cac21875f56c58afed484` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec4_pdf.pdf` | 5 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec4.pdf | `d8a4be647c2eee13deeaef9e4759a772daf368a1e248379d9fbaf5c0c2afa57e` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec29_pdf.pdf` | 5 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec29.pdf | `7743654402c859242156cd9fe53f8de2d16121c96295f7dfa68a9ad86e3e2c55` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec30_pdf.pdf` | 5 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec30.pdf | `00fcb374381a4cd1de54b59239a494e2bd577164155b1226ed1c570c167d3972` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec31_pdf.pdf` | 5 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec31.pdf | `cd4dcbbfcbddd1c428070fcee3042a965317d18f3bb72d7846b09d4f3e2c2f86` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec33_pdf.pdf` | 5 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec33.pdf | `8fee491ead6faa829ba45c890afe81adfb791dd7f6f016c5018658ee98b3a9ee` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec40_pdf.pdf` | 5 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec40.pdf | `e70b8914645ae59f0152b92b155d2eaaaa1e37f17410e11d93566cffd9db8245` |
| `sources/18.965-fall2004/pdf/lecture1.pdf` | 4 | Tomasz S. Mrowka | https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/34fad8f392208544e2b1e9794c33cbe7_lecture1.pdf | `5a6433da86a8d5d5c4031b79d5b2ef5ae5f15b7a05bc0b4e3ce1c68761ec5920` |
| `sources/18.965-fall2004/pdf/lecture2.pdf` | 2 | Tomasz S. Mrowka | https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/b481a27fb1583bbaf43153bcaf0643fe_lecture2.pdf | `894fb86d9ead48f10ad6b80874da32367da672b0b4897ee8cb3cc7b2679f874d` |
| `sources/18.965-fall2004/pdf/lecture4.pdf` | 4 | Tomasz S. Mrowka | https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/55a7137272a97179db2a80b6e20d5de0_lecture4.pdf | `2561c0859ab342abcbc011b5e74191a79c3bfcdfd04f1b5d3b27375eb6d8d4d8` |
| `sources/18.950-fall2008/pdf/ch4_revised.pdf` | 13 | Paul Seidel | https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/624f231226f7c15ddce6ba6dfad2db64_ch4_revised.pdf | `f7af9abd1fcacf69972c21dfedd6201b63696929da64f9c17f4579c061c2b8a9` |
| `sources/18.900-spring2023/pdf/mit18_900s23_q4.pdf` | 2 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_q4.pdf | `88811f65492259bec386a7e3d11dd90dad6274f08ddf258c0d4c9bc43d25bff7` |
| `sources/18.900-spring2023/pdf/mit18_900s23_q29.pdf` | 2 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_q29.pdf | `8381a63751cceee413453faf2039cec350ed95a74c441cf33203cd72e8126296` |
| `sources/18.900-spring2023/pdf/mit18_900s23_q30.pdf` | 2 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_q30.pdf | `67d9bd77d24ab6f5a760a0de36480398374fe752797b5f5f47f543376dae158a` |
| `sources/18.900-spring2023/pdf/mit18_900s23_q31.pdf` | 2 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_q31.pdf | `63db62ffd2b8fdc2a73215ddcbadd7817909986b88190cad37ef443377730eaa` |
| `sources/18.900-spring2023/pdf/mit18_900s23_q33.pdf` | 2 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_q33.pdf | `06c14169f6a5d6d1f915e8418ddf95f9f9df2627f09b6b774db152bba40203ee` |
| `sources/18.900-spring2023/pdf/mit18_900s23_q40.pdf` | 2 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_q40.pdf | `287e32783d5a2b59b2ad05c1fba141c85429ca124ccceaeb93e716039deada2e` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec6.pdf` | 7 | Paul Seidel | https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec6.pdf | `d0d41248b9b17f8f7a07a731a4f512274c162ddfd3205fb6b549429b272ea4ca` |
| `sources/18.901-fall2004/pdf/problemset_5.pdf` | 2 | James Munkres | https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/d6c5d6d30bf26300b6f1b2c278791796_problemset_5.pdf | `1950c59a93c354767207cef3211b22931266fb97ce0b26eedc3927af40ed4de9` |

## 固定模板与运行依赖

用户提供 math-latex-typesetting v4.0.0 的锁定王者适配类保留在 main.tex；只增加内容与数学宏，不更改版式。字体和TeX宏包为外部运行依赖，不包含在本包，也不以本改编许可替代它们原有许可。

## 其他证明来源

PS5不可数积的非正规性使用Stone闭集反例，本文已展开有限坐标递归证明。A. H. Stone, “Paracompactness and product spaces”, Bulletin of the American Mathematical Society 54 (1948), 977–982；N. Noble, Poorly Separated Infinite Normal Products, §6.1, https://arxiv.org/abs/2002.02483 。相关论文只作为数学核查依据，没有把受限原件放入本源码包。
