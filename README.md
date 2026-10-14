# Table Pet - 芯片手册翻译桌宠

一个可爱的桌面宠物，专门解决芯片数据手册（PDF）翻译慢的问题。拖拽PDF到桌宠身上，自动提取文字并翻译成中文，结果保存在 `output` 文件夹。

## ✨ 功能特点
- 🐾 桌面宠物：支持鼠标拖动、浮动动画
- 📄 拖拽翻译：将英文PDF拖到桌宠上，自动翻译
- 🌐 百度翻译API：国内网络环境友好，翻译稳定
- 📁 自动保存：翻译结果保存为 `.txt` 文件

## 🛠️ 技术栈
- Python 3.8+
- Tkinter (桌面界面)
- pdfplumber (PDF文字提取)
- requests (百度翻译API调用)
- Pillow (图片处理)

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/table-pet.git
cd table-pet