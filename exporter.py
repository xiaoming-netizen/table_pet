# exporter.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体（Windows 系统字体，按优先级尝试）
FONT_NAME = 'Helvetica'   # 兜底
_candidates = [
    ('SimSun',           'C:/Windows/Fonts/simsun.ttc'),
    ('MicrosoftYaHei',   'C:/Windows/Fonts/msyh.ttc'),
    ('SimHei',           'C:/Windows/Fonts/simhei.ttf'),
]
for name, path in _candidates:
    try:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
            FONT_NAME = name
            print(f"PDF 使用字体：{name}")
            break
    except Exception as e:
        print(f"字体 {name} 加载失败：{e}")


def export_markdown(text, stats, title, out_path):
    """导出翻译结果为 Markdown 文件"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title} - 中文翻译\n\n")
        f.write(f"> 翻译状态：**{stats['status']}**（成功 {stats['success']}/{stats['total']} 段）\n\n")
        f.write("---\n\n")
        f.write(text)


def _wrap_text(text, font, size, max_width):
    """按宽度把长文本拆成多行，用于 PDF 渲染"""
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue
        current = ''
        for char in paragraph:
            test = current + char
            if pdfmetrics.stringWidth(test, font, size) > max_width:
                lines.append(current)
                current = char
            else:
                current = test
        if current:
            lines.append(current)
    return lines


def export_pdf(text, stats, title, out_path):
    """导出翻译结果为 PDF 文件"""
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    margin = 50
    max_width = width - 2 * margin
    font_size = 11
    line_height = 18
    y = height - margin

    # 标题
    c.setFont(FONT_NAME, 16)
    c.drawString(margin, y, f"{title} - 中文翻译")
    y -= 28

    # 状态
    c.setFont(FONT_NAME, 10)
    c.drawString(margin, y, f"翻译状态：{stats['status']}（成功 {stats['success']}/{stats['total']} 段）")
    y -= 28

    # 正文
    c.setFont(FONT_NAME, font_size)
    for line in _wrap_text(text, FONT_NAME, font_size, max_width):
        if y < margin:
            c.showPage()
            c.setFont(FONT_NAME, font_size)
            y = height - margin
        c.drawString(margin, y, line)
        y -= line_height

    c.save()