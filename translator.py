# translator.py
import translators as ts

def translate_text(text):
    """使用 translators 库进行翻译，无需 API Key"""
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    result_all = ""
    print(f"共 {len(chunks)} 段，开始翻译...")

    for i, chunk in enumerate(chunks):
        try:
            result = ts.translate_text(chunk, from_language='en', to_language='zh')
            result_all += result + "\n"
            print(f"  第 {i+1}/{len(chunks)} 段完成")
        except Exception as e:
            print(f"  第 {i+1} 段失败：{e}")
            result_all += f"[失败] {chunk[:50]}...\n"

    return result_all