# Mew Exporter

**Mew will cancel its service by 30 Oct. 2022. This project will be of no use after that time.**

![The Unlicense badge](https://img.shields.io/badge/license-The%20Unlicense-lightgrey) [![](https://img.shields.io/badge/@Kunologist-Mew-345bac?logo=data:image/png;base64,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)](https://mew.fun/)

This tool exports your thoughts from [Mew](https://mew.fun/) to store them locally in [Markdown format](https://www.markdownguide.org/).

[Chinese (Simplified) / 简体中文](readme_zh-cn.md)

Features:

- Supports images, links, formatted text to markdown files.
- Downloads images from Mew servers: you get to keep not only text.
- Built-in compression: zip up your thoughts and keep them safe locally forever.

## Installation

Install [Python](https://www.python.org/downloads/), and use `pip` to install the dependencies:

```bash
pip install -r requirements.txt
```

Note that the packages have rather strict version requirements - this is intended for non-Python developers to avoid dependency hell, but if you know what you're doing, you can try to relax the requirements.

## Usage

The following command will export all your thoughts to the `export-mew` directory:

```bash
python3 export.py 12341234123 mySecretPassword
```

where `12341234123` is the phone number you used to register on Mew, and `mySecretPassword` is your Mew password.

## Advanced usage

See `python3 export.py --help` for more options.

- `-o` or `--output-dir`: specify the output directory (default: `export-mew`)
- `-z` or `--zip`: also compress the output directory to a zip file (disabled by default)
- `-i` or `--images`: download related images to the `images` folder under the output directory (disabled by default, which means no image will be downloaded if `-i` is not provided)
- `-j` or `--json`: save JSON source file (for debugging purposes) (disabled by default)
- `-q` or `--quiet`: quiet mode, nothing will spoil your console (disabled by default)
- `--no-log`: disable logging to file

*The tool also includes a separate `mewdoc2md.py` utility that converts a single Mew document to Markdown, so in case you have the JSON source file...*

## How come?

Everyone knows that Mew is not a mature forum website. We also like Mew for its niche community.

I always believe that users should **OWN** their data. Maybe one day, Mew will be temporarily down for some reasons, and gone were all our memories. To prevent these from happening, I wrote this tool.

[![My thought on Mew mentioning this idea](https://s1.ax1x.com/2022/09/10/vOiEdS.png)](https://mew.fun/Kunologist/thoughts/217638290853482496)

It might also help you to migrate your thoughts from Mew to other platforms, such as [Notion](https://www.notion.so/) or other personal blogs. This is especially useful when you use Mew as a blogging / sharing tool.

Note, I am not cursing Mew. Instead, I witness Mew's growth with all my heart. But for you - fellow Mew users - you are now backed with this tool to secure your data! Now you know that you are creating thoughts with no worries about losing them!
