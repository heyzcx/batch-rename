# batch-rename

按通配符批量重命名文件：替换子串、加前缀/后缀、改大小写、改扩展名、加序号——零依赖 Python 命令行工具。

## 安装

只需要 Python 3.8+，无需安装任何依赖：

```bash
git clone https://github.com/heyzcx/batch-rename.git
cd batch-rename
```

## 用法

```bash
# 先预览（强烈建议）：把 IMG_01.jpg 改成 2026-vacation_01.jpg
python rename.py photos/ "*.jpg" --replace IMG_ vacation_ --prefix 2026- --dry-run

# 确认无误后执行（去掉 --dry-run）
python rename.py photos/ "*.jpg" --replace IMG_ vacation_ --prefix 2026-

# 全部小写 + 加 3 位序号（从 1 开始）
python rename.py docs/ "*.txt" --lower --number --start 1 --pad 3

# 改扩展名
python rename.py . "*.md" --ext txt
```

## 选项

| 选项 | 说明 |
| --- | --- |
| `--replace OLD NEW` | 把文件名中的 OLD 换成 NEW |
| `--prefix TEXT` | 在文件名前加 TEXT |
| `--suffix TEXT` | 在文件名前（扩展名之前）加 TEXT |
| `--lower` / `--upper` | 文件名转小写 / 大写 |
| `--number` | 在文件名后加序号（`--start` 起始值，默认 1；`--pad` 补零宽度，默认 3；`--separator` 分隔符，默认 `_`） |
| `--ext EXT` | 改扩展名，如 `txt`；传空字符串则去掉扩展名 |
| `--dry-run` | 只显示计划，不实际重命名 |

## 安全

- 目标文件名已存在时跳过，不会覆盖任何文件。
- 先用 `--dry-run` 预览，确认后再执行。

## 测试

```bash
python test_rename.py   # 6 项冒烟测试
```
