# JavDB 日本电影排行榜本地分析工具

## 项目简介

本工具用于分析用户本地保存的 JavDB 日本电影排行榜 HTML 文件，支持"历年总排名"与"指定年份排名"两种模式。工具会自动解析 HTML，提取电影编号、名称、评分，并与本地电影文件夹比对，分析排名变化，最终生成包含本地存在状态和排名变化的 Excel 报告。

## 目录结构

```
javdb_ranking_tool/
├── javdb_ranking_tool.py          # 主程序入口
├── config.ini                     # 配置文件（自动生成）
├── modules/                       # 功能模块目录
│   ├── config_manager.py
│   ├── html_reader.py
│   ├── html_parser.py
│   ├── local_scanner.py
│   ├── data_processor.py
│   └── excel_writer.py
├── ranking_history_all_time.json  # 历年总排名历史数据（自动生成）
├── ranking_history_2025.json      # 2025年排名历史数据（自动生成）
├── javdb_htmls/                   # HTML文件根目录（用户自建）
│   ├── all_time/                  # 历年总排名子文件夹
│   │   ├── ranking_page1.html
│   │   └── ...
│   ├── 2025/                      # 2025年排名子文件夹
│   │   ├── ranking_page1.html
│   │   └── ...
│   └── ...
└── javdb_rankings_all_time.xlsx   # Excel报告（自动生成）
└── javdb_rankings_2025.xlsx       # Excel报告（自动生成）
```

## 依赖安装

请确保已安装 Python 3.7 及以上版本。

安装依赖包：

```bash
pip install beautifulsoup4 openpyxl
```

## 使用方法

1. **准备 HTML 文件**
   - 在 `javdb_htmls` 目录下，按 `all_time` 或年份（如 `2025`）新建子文件夹。
   - 每个子文件夹内放置 7 个排行榜 HTML 文件，命名为：
     - `ranking_page1.html`
     - `ranking_page2.html`
     - ...
     - `ranking_page7.html`

2. **准备本地电影文件夹**
   - 指定你存放本地电影的文件夹路径。

3. **首次运行配置**
   - 运行主程序时会自动生成 `config.ini`，并提示输入 HTML 根目录和本地电影文件夹路径。

4. **运行主程序**

```bash
python javdb_ranking_tool.py
```

- 启动后会提示选择"历年总排名"或"指定年份"。
- 按提示输入后，工具会自动处理并生成 Excel 报告。

5. **命令行参数（可选）**

可用参数覆盖配置文件：

```bash
python javdb_ranking_tool.py --html_root_folder "./javdb_htmls" --local_movie_folder "/path/to/movies"
```

## 生成结果

- Excel 报告文件名如：`javdb_rankings_all_time.xlsx`、`javdb_rankings_2025.xlsx`
- 报告包含：名次、电影编号、电影名称、评分、本地是否存在、排名变化
- 历史数据文件名如：`ranking_history_all_time.json`、`ranking_history_2025.json`

## 注意事项

- **HTML 文件夹结构和命名需严格遵守上述约定。**
- **首次运行新版本建议删除旧的历史 JSON 文件**，以避免字段不兼容。
- 如遇找不到文件、解析失败等问题，请检查路径和 HTML 文件内容。
- "本地是否存在"仅根据电影编号在文件名中的出现与否判断。

## 常见问题

- **FileNotFoundError**：请检查 HTML 文件夹路径和文件命名是否正确。
- **Excel 无数据**：请检查 HTML 文件内容和结构是否与解析规则匹配。
- **JSONDecodeError**：请删除损坏的历史 JSON 文件，程序会自动生成新的。

## 联系与反馈

如有问题或建议，欢迎提交 issue 或联系作者。 