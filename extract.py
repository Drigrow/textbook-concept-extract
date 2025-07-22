import os
import re
from pathlib import Path
from collections import defaultdict
from openai import OpenAI

book_dir = Path(r"YOUR_PATH_TO_TEXTBOOK")
concept_md_path = Path(r"YOUR_PATH_TO_CONCEPT\concept.md")
output_dir = Path(r"./output")
output_dir.mkdir(exist_ok=True)

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def parse_concepts(md_path):
    concepts = defaultdict(list)
    current = None
    with open(md_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("**") and line.endswith("**"):
                title = line.strip("*").strip()
                if title.endswith(":"):
                    title = title.rstrip(":").strip()
                current = title
            elif current and re.match(r"^\d+\.", line):
                number_and_concept = line.split('.', 1)
                idx = number_and_concept[0].strip()
                concept_text = number_and_concept[1].strip()
                full_concept = f"{idx}. {concept_text}"
                concepts[current].append(full_concept)
    return concepts

book_concepts = parse_concepts(concept_md_path)

def extract_book_key(filename):
    sel_pattern = re.compile(r"选择性必修(\d)")
    norm_pattern = re.compile(r"必修(\d)")

    m = sel_pattern.search(filename)
    if m:
        return f"选择性必修{m.group(1)}"
    m = norm_pattern.search(filename)
    if m:
        return f"必修{m.group(1)}"
    return None


for pdf in book_dir.glob("*.pdf"):
    book_key = extract_book_key(pdf.name)
    if not book_key:
        print(f"⚠️ 未识别书籍: {pdf.name}")
        continue

    book_key_clean = book_key.strip()
    if book_key_clean not in book_concepts:
        print(f"⚠️ {book_key} 未在 concept.md 中定义")
        continue

    print(f"📘 正在处理: {pdf.name} ({book_key_clean})")
    try:
        file_obj = client.files.create(file=pdf, purpose="file-extract")
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        continue

    # 拼接概念列表
    concepts_str = "\n".join(book_concepts[book_key_clean])
    prompt = f"请从书中提取以下概念的定义，并按顺序分别给出定义：\n{concepts_str}"

    try:
        completion = client.chat.completions.create(
            model="qwen-long",
            messages=[
                {'role': 'system', 'content': f'fileid://{file_obj.id}'},
                {'role': 'user', 'content': prompt}
            ]
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"    ⚠️ 提取失败: {e}")
        answer = "提取失败"

    # 保存 Markdown
    md_lines = [
        f"# {book_key_clean} 概念定义",
        answer
    ]

    output_path = output_dir / f"{book_key_clean}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(md_lines))
    print(f"✅ 保存: {output_path}")

print("🎉 全部完成！")
