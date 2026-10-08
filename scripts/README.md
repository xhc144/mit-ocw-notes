# 增量归档与校验

`archive_files.py` 不是全站爬虫。先由研究步骤给 `manifests/files.json` 填入已核查的课程、文件及许可元数据，再运行。

文件条目至少包括：`path`、`url`、`course_id`、`course_url`、`attribution`、`license`、`archive_allowed`。未确认许可时 `archive_allowed` 为 `false`。下载成功后追加 `sha256`、`bytes`、`downloaded_at`、`final_url`、`status` 和 `verification`。

只校验现有文件（默认无网络请求）：

```sh
python3 scripts/archive_files.py
```

增量下载已核查、尚不存在的官方 OCW 文件，记录结果：

```sh
python3 scripts/archive_files.py --download --write-manifest --jobs 4
```

完成下载或后续提交前重新校验：

```sh
python3 scripts/archive_files.py --write-manifest
```

安全边界：只允许 `https://ocw.mit.edu/`，重定向超出该主机即停止；HTTP 拒绝或网络失败不自动重试，不更换网络路径。默认单文件上限为 90 MiB，未购买或启用 LFS。已存在文件只校验，绝不静默覆盖；校验不匹配或缺失已记录校验和时要求人工复核。`.part` 保留为失败证据，不自动续写或当作成功文件。脚本拒绝重复目标路径和越界相对路径。

空清单校验通过只表示当前没有文件需要校验，不表示课程下载完成。学科完成进度另见 `manifests/subjects.json`。
