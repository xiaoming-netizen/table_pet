# pdf_reader.py
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """提取PDF中的所有文字"""
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total = len(pdf.pages)
            print(f"共 {total} 页，开始提取...")
            for i, page in enumerate(pdf.pages):
                t = page.extract_text()
                if t:
                    full_text += t + "\n"
                print(f"  第 {i+1}/{total} 页")
    except Exception as e:
        print(f"提取失败：{e}")
        return None
    return full_text if full_text.strip() else None