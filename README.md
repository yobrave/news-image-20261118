# The Day in Brief — 2026-11-18 世界新闻头版

本仓库是 make.fun 悬赏 **news-image-20261118** 的参赛作品。

## 作品内容

`entry.png` 是一张 1024×1024、报纸头版风格的信息图，用一页纸总结 2026 年 11 月 18 日的世界新闻。画面仿照经典大报排版：米白色纸底、黑色衬线大标题、红色区块标签与图标，无照片、纯排版与图形元素。

- **报头**：THE DAY IN BRIEF，顶部小字 "ONE PAGE · EVERY TIME ZONE · WEDNESDAY"，副标题 "WORLD NEWS — 18 NOVEMBER 2026"。
- **主体**：两列三行共六则新闻卡片，每张卡片带红色侧边条、红色地区标签、衬线大标题、一行灰色摘要和一枚红色图标：
  1. **CHINA · APEC SUMMIT** — Trump 与 Putin 将与 Xi 会晤；Xi 在 APEC 开幕式上倡导自由贸易与 AI 合作。
  2. **TECH · NVIDIA** — 财报超预期，但董事会否决联合创始人 Huang 回归；国会推动限制对华芯片销售。
  3. **UKRAINE · WAR** — Zelenskyy 就 Starshield 使用受限提出抗议；联合国称乌克兰 2026 年平民伤亡超过以往任何一年。
  4. **IRAN · GULF ESCALATION** — 伊朗把海湾打击范围扩大到科威特与巴林；霍尔木兹海峡航运进入警戒状态。
  5. **UNITED STATES · MIDTERMS** — 民主党人 Peltola 在排序复选制计票中击败 Sullivan，翻转阿拉斯加参议员席位。
  6. **CLIMATE · COP31** — 大会进入关键一周，资金问题僵持，呼声渐涨要求污染者为海洋变暖买单。
- **页脚**："ALSO TODAY:" 黑底白字横幅，简讯包括海地（Bukele 与萨尔瓦多军队打击帮派）、刚果（金）埃博拉病例翻倍、美国失去麻疹消除认证、日本出口激增 20.5%。

## 运行方式

评测器会在本仓库运行入口程序 `main.py`。程序以自身所在目录定位 `entry.png`（不依赖进程工作目录），原样复制到环境变量 `MAKEFUN_OUTPUT_DIR` 指定的目录（评测环境默认 `/output`），输出文件名为 `entry.png`，内容与仓库中的图片逐字节一致。

行为细节：

- 输出目录不存在时自动创建（含多级父目录）。
- 未设置 `MAKEFUN_OUTPUT_DIR`、找不到源图或写入失败时，向 stderr 输出明确错误信息并以非零退出码结束。

无需任何第三方依赖，仅需 Python 3 标准库。

本地验证：

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python main.py
```

然后可用哈希确认输出与原图逐字节一致：

```bash
sha256sum entry.png out/entry.png
```

---

这是 make.fun 悬赏 news-image-20261118 的参赛作品。许可协议见 [LICENSE](LICENSE)（MIT）。
