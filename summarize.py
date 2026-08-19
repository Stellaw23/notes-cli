from roam import get_today_uid, get_page
from llm import call_deepseek

today_uid = get_today_uid()
page = get_page(today_uid)

if page is None:
    print("今天还没有笔记")
else:
    prompt = f"把下面的笔记总结成几条要点：{page["markdown"]}"
    result = call_deepseek(prompt)
    print(result["choices"][0]["message"]["content"])
