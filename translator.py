# translator.py
import translators as ts


def translate_text(text):
    """
    翻译英文文本为中文。
    返回: (translated_text, stats)
    """
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    result_parts = []
    success = 0
    failed = 0

    print(f"共 {len(chunks)} 段，开始翻译...")
    for i, chunk in enumerate(chunks):
        try:
            result = ts.translate_text(chunk, from_language='en', to_language='zh')
            if result and result.strip():
                result_parts.append(result)
                success += 1
                print(f"  第 {i+1}/{len(chunks)} 段完成")
            else:
                result_parts.append(f"【未翻译原文】\n{chunk}")
                failed += 1
                print(f"  第 {i+1}/{len(chunks)} 段失败（空结果）")
        except Exception as e:
            print(f"  第 {i+1}/{len(chunks)} 段失败：{e}")
            result_parts.append(f"【未翻译原文】\n{chunk}")
            failed += 1

    total = len(chunks)
    if failed == 0:
        status = "成功"
    elif success == 0:
        status = "失败"
    else:
        status = "部分成功"

    stats = {
        "total": total,
        "success": success,
        "failed": failed,
        "status": status,
    }
    return "\n\n".join(result_parts), stats