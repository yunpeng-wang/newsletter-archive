import email
from email import policy
from email.utils import parsedate_to_datetime
import base64
from pathlib import Path
import json
from bs4 import BeautifulSoup as BS
from bs4 import Tag


def eml_to_html(eml_path):
    # 1. 读取 EML 文件
    with open(eml_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    # 2. 提取邮件元数据（包括时间）
    raw_date = msg.get(
        "Date"
    )  # 获取原始时间字符串，例如: "Mon, 21 Sep 2026 14:30:00 +0800"
    # 将邮件的原始时间转换为 Python 的 datetime 对象，方便你后续存入数据库或格式化输出
    mail_datetime = parsedate_to_datetime(raw_date) if raw_date else None
    # 格式化为你想要的样式，例如: "2026-09-21 14:30:00"
    formatted_date = (
        mail_datetime.strftime("%Y-%m-%d %H:%M:%S") if mail_datetime else "未知时间"
    )

    # 获取作者
    sender = msg.get("From", "未知发件人")

    # 3. 获取原生的 HTML 正文
    html_part = msg.get_body(preferencelist=("html",))
    if not html_part:
        # 如果邮件没有 HTML 格式，则取纯文本
        text_part = msg.get_body(preferencelist=("plain",))
        return f"<body><pre>{text_part.get_content()}</pre></body>" if text_part else ""

    html_content = html_part.get_content()

    # 4. 自动处理内联图片 (处理邮件中那些 cid:xxxx 的图片链接)
    # 遍历邮件的所有附件/内嵌资源，将图片转为 Base64 并替换到 HTML 中
    for part in msg.walk():
        if part.get_content_maintype() == "image":
            content_id = part.get("Content-ID")
            if content_id:
                # 清洗 cid 标签，去掉两侧的尖括号 < >
                cid = content_id.strip("<>")
                # 转换图片为 Base64
                img_data = base64.b64encode(part.get_payload(decode=True)).decode(
                    "utf-8"
                )
                mime_type = part.get_content_type()
                base64_src = f"data:{mime_type};base64,{img_data}"

                # 替换 HTML 中的原图片引用
                html_content = html_content.replace(f"cid:{cid}", base64_src)

    return html_content, formatted_date, sender


def inject_content(html):
    soup = BS(html, "html.parser")
    head = soup.head

    if isinstance(head, Tag):
        css = soup.new_tag("link", rel="stylesheet", href="../assets/css/news.css")
        js = soup.new_tag("script", src="../assets/js/news.js", defer=None)

        head.append(css)
        head.append(js)
    else:
        print("Error. head is not Tag")

    return str(soup.prettify())


if __name__ == "__main__":
    TOOL_PATH = Path(__file__).resolve()
    html_folder = TOOL_PATH.parent.parent / "news"
    json_path = TOOL_PATH.parent.parent / "assets" / "data" / "htmls.json"

    eml_folder = Path(r"/Users/wang/Downloads")

    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            json_dict = json.load(f)
    else:
        json_dict = {}

    for file in eml_folder.glob("*.eml"):
        file_name = str(file.stem) + ".html"

        html_for_web, date, sender = eml_to_html(str(file))

        dataname = date.replace(":", "").replace("-", "").replace(" ", "-")
        title = str(file.stem).replace("_", ":")
        href = r"./news/" + dataname + ".html"
        author = sender.split(" ")
        json_dict[dataname] = {
            "title": f"{title}",
            "date": f"{date}",
            "href": f"{href}",
            "author": f"{author[0] + ' ' + author[1]}",
        }

        html_for_web = inject_content(html_for_web)

        with open(html_folder / (dataname + ".html"), "w", encoding="utf-8") as f:
            f.write(html_for_web)
        print(f"{file_name} --> Converted")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_dict, f, indent=2, ensure_ascii=False)
