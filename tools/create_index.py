from pathlib import Path
import json

TOOL_PATH = Path(__file__).resolve()
json_path = TOOL_PATH.parent.parent / "assets" / "data" / "htmls.json"
js_path = TOOL_PATH.parent.parent / "assets" / "js" / "data.js"


def natural_sort(items, key=None, reverse=False):
    import re

    def _natural_key(s):
        s = key(s) if key else s
        return [
            int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(s))
        ]

    return sorted(items, key=_natural_key, reverse=reverse)


def create_elements(title, date, author, href):
    fm = author.split(" ")[-1]
    text = "'" + f"""<article class="{fm}">
            <h1>{title}</h1>
            <div>
                <span>{date.split(" ")[0]}</span>
                <span>{author}</span>
            </div>
            <a href="{href}"></a>
        </article>""" + "',"

    return text.replace("\n", "").replace("  ", "")


if json_path.exists():
    with open(json_path, "r", encoding="utf-8") as f:
        json_dict = json.load(f)

    keys_list = natural_sort(list(json_dict.keys()), reverse=True)

    content = []
    for key in keys_list:
        content.append(
            create_elements(
                json_dict[key]["title"],
                json_dict[key]["date"],
                json_dict[key]["author"],
                json_dict[key]["href"],
            )
        )

    js_content = "const articleData = [\n  " + "\n  ".join(content) + "\n];"

    with open(js_path, "w") as f:
        f.write(js_content)
else:
    print("JSON data does not exist!")
