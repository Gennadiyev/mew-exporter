from loguru import logger
import json
import os
import shutil
import sys
from tqdm import tqdm
from mewpy.api import *
from mewdoc2md import mewdoc2md
import zipfile

@logger.catch
def export(args: dict):
    # Login
    phone, password = args.phone, args.password
    login_response = login(phone, password)
    if login_response.get("token") is None:
        logger.exception("Login failed, got response: {}".format(login_response))
    token = login_response["token"]
    user_id = login_response["id"]
    username = login_response["name"]
    logger.info(f"Logged in as {username} ({user_id})")
    logger.debug(f"Token: {token}")
    # Get thoughts
    all_thoughts = get_all_user_thoughts(user_id, token)
    thoughts = all_thoughts.get("entries", [])
    logger.info(f"Got {len(thoughts)} thoughts")
    # Dump to json file if needed
    if args.json:
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(all_thoughts, f, indent=4, ensure_ascii=False)
            logger.info("Dumped all thoughts to output.json")
    assert "objects" in all_thoughts and "entries" in all_thoughts, "Invalid thoughts list."
    # Parse thoughts
    output_dir = args.dir
    os.makedirs(output_dir, exist_ok=True)
    # Save each thought
    node_name_cache = {}
    for thought in thoughts:
        assert "node_id" in thought and "topic_id" in thought and "id" in thought and "status" in thought, "Invalid thought: {}".format(thought)
        # Get node name
        node_id = thought["node_id"]
        if node_id not in node_name_cache:
            node_name = get_node_info(node_id, {"authorization": f"Bearer {token}"}).get("name", "Unknown Node")
            node_name_cache[node_id] = node_name
        else:
            node_name = node_name_cache[node_id]
        # Get topic name
        topic_id = thought["topic_id"]
        topic_name = all_thoughts["objects"]["topics"].get(topic_id, {"name": "Unknown Topic"})["name"]
        # Create directory
        thought_dir = os.path.join(output_dir, node_name, topic_name)
        os.makedirs(thought_dir, exist_ok=True)
        # Create thought file
        thought_id = thought["id"]
        thought_file = os.path.join(thought_dir, f"{thought_id}.md")
        thought_text = thought["status"] + "\n"
        # Check special type
        if len(thought.get("media", [])) > 0:
            # Thought with images
            for media_id in thought["media"]:
                url = all_thoughts["objects"]["media"].get(media_id, {"url": ""})["url"]
                thought_text += f"\n![]({url})\n"
        elif len(thought.get("embeds", [])) > 0:
            # Thought with URL embed
            for embed_id in thought["embeds"]:
                embed = all_thoughts["objects"]["embeds"].get(embed_id, {"url": "", "title": ""})
                thought_text += f"\n[{embed['title']}]({embed['url']})\n"
        elif thought.get("post_content") != "":
            # Thought with post content
            post_cover = thought["post_cover"]
            if post_cover is not None:
                url = all_thoughts["objects"]["media"].get(post_cover, {"url": ""})["url"]
                thought_text += f"\n![]({url})\n\n"
            md = mewdoc2md(json.loads(thought["post_content"]), all_thoughts["objects"])
            thought_text += f"\n{md}\n"
        with open(thought_file, "w", encoding="utf-8") as f:
            logger.info("Writing: {}".format(thought_file))
            f.write(thought_text)
    # Download all images if needed
    if args.images:
        logger.info("Downloading images...")
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        for media_id, media in tqdm(all_thoughts["objects"]["media"].items()):
            url = media["url"]
            save_path = os.path.join(images_dir, f"{media_id}.jpg")
            if not os.path.exists(save_path):
                with open(save_path, "wb") as f:
                    shutil.copyfileobj(requests.get(url, stream=True).raw, f)
    # Zip if needed
    if args.zip is not None:
        logger.info("Compressing...")
        zipf = zipfile.ZipFile(args.zip, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()



if __name__ == "__main__":
    import argparse
    from datetime import datetime
    parser = argparse.ArgumentParser(description='Export Mew thoughts.', epilog="Example: python3 export.py 10010001000 mypassw0rd\n\nThis program is not affilliated with Mew official.")
    parser.add_argument('phone', type=str, help='Mew phone number')
    parser.add_argument('password', type=str, help='Mew password')
    parser.add_argument('-d', '--dir', type=str, help='The directory to save thoughts', default='export-mew')
    parser.add_argument('-z', '--zip', type=str, help='Also compress the folder to a zip file.', default=None)
    parser.add_argument('-i', '--images', action='store_true', help='Download images.')
    parser.add_argument('-j', '--json', action='store_true', help='Save JSON source file (for debugging purpose).')
    args = parser.parse_args()
    date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger.add("log-{}.log".format(date_string), backtrace=True, diagnose=True)
    export(args)

