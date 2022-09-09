'''mewdoc2md.py

Converts mew doc to markdown format. Note that this is a lossy conversion: you will lose some HTML-like formatting.
'''

def mewdoc2md(mewdoc: list, objects: dict={}) -> str:
    '''Converts mew doc to markdown format.
    @param mewdoc: The mew doc.
    @type mewdoc: list
    @return: The markdown-formatted string.
    '''
    assert mewdoc.get("type") == "doc", "The mew doc must be a list with type 'doc'."
    def parse_arr(mewdoc_arr: list, bullet_level=0) -> str:
        output = ""
        for item in mewdoc_arr:
            item_type = item.get("type", None)
            if item_type == "heading":
                level = item.get("attrs", {}).get("level", 1)
                content_string = parse_arr(item.get("content", []))
                output += f"{'#' * level} {content_string}\n\n"
            elif item_type == "paragraph":
                output += parse_arr(item.get("content", [])) + "\n\n"
            elif item_type == "text":
                text = item.get("text", "")
                if "marks" in item:
                    is_link = False
                    is_bold = False
                    is_italic = False
                    for mark in item["marks"]:
                        if mark["type"] == "link":
                            is_link = True
                            url = mark["attrs"]["href"]
                        elif mark["type"] == "bold":
                            is_bold = True
                        elif mark["type"] == "italic":
                            is_italic = True
                    if is_bold:
                        text = f"**{text}**"
                    if is_italic:
                        text = f"*{text}*"
                    if is_link:
                        text = f"[{text}]({url})"
                    if (is_bold or is_italic or is_link) and len(output) > 0:
                        text = f" {text} "
                output += text
            elif item_type == "embed_block":
                embed_type = item.get("attrs", {}).get("embedType", None)
                if embed_type == "link":
                    embed_id = item.get("attrs", {}).get("id", None)
                    if embed_id is not None:
                        embed = objects.get("embeds", {}).get(embed_id, {"url": "(Broken URL)", "title": "(Missing title)"})
                        output += f"[{embed['title']}]({embed['url']})\n\n"
                else:
                    raise(Exception(f"Unknown embed type: {embed_type}"))
            elif item_type == "image_block":
                # Look for the image in the objects
                image_id = item.get("attrs", {}).get("id", None)
                if image_id and "media" in objects and image_id in objects["media"]:
                    image = objects["media"][image_id]
                    output += f"![]({image['url']})\n\n"
            elif item_type == "bullet_list":
                bullet_level += 1
                output += parse_arr(item.get("content", []), bullet_level)
                bullet_level -= 1
            elif item_type == "list_item":
                output += f"{'  ' * (bullet_level-1)}- {parse_arr(item.get('content', []))}\n"
            elif item_type == "horizontal_rule":
                output += "---\n\n"
            elif item_type == "blockquote":
                bullet_level += 1
                output += "> " * bullet_level + parse_arr(item.get("content", []), bullet_level) + "\n"
                bullet_level -= 1
        return output
    markdown = parse_arr(mewdoc.get("content", []))
    return markdown

if __name__ == "__main__":
    import json
    import argparse
    import sys
    # python mewdoc2md.py post.json post.md
    parser = argparse.ArgumentParser(description='Convert mew doc to markdown.')
    parser.add_argument('input', type=str, help='The input file path.')
    parser.add_argument('-o', '--output', type=str, help='The output file path.', default="output.md", required=False)
    args = parser.parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        mewdoc = json.load(f)
    markdown = mewdoc2md(mewdoc)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(markdown)
    sys.exit(0)
