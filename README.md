# 英语作文高亮标记工具

这是一个用于为英语作文图片添加高亮标记的Python工具。

## 功能特点

- 支持四种不同的高亮标记样式：
  - 🔴 红色圆圈标记
  - 🔵 蓝色横线标记  
  - 🟢 绿色双横线标记
  - 🟡 黄色波浪线标记
- 自动生成图例说明
- 支持多种图片格式（PNG, JPG, JPEG等）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

## 文件结构

- `main.py` - 主程序入口
- `highlight_tool.py` - 高亮标记核心功能
- `legend_generator.py` - 图例生成功能
- `requirements.txt` - 项目依赖
- `README.md` - 项目说明
