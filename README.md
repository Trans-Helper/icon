# Trans-Helper Icon

Trans-Helper 图标生成器。通过 `main.py` 生成 SVG 和多尺寸 PNG。

---

## 快速开始

```bash
# 进入开发环境（提供 cairo 库）
nix develop

# 生成 SVG + PNG
uv run python main.py
```

## 输出

结果输出到 `output/` 目录：

| 文件                                    | 说明                     |
| --------------------------------------- | ------------------------ |
| `output.svg`                            | 全分辨率 SVG (1024×1024) |
| `icon-{16,32,48,64,96,128,256,512}.png` | 标准图标尺寸 PNG         |

## 持续集成

每次推送涉及 `main.py`、`pyproject.toml` 或 `uv.lock` 时，GitHub Workflow 会自动重新生成所有图标并提交到 `icon` 分支。
