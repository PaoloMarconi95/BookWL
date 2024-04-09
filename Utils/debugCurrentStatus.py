from Config import CONFIG, LOGGER
import os
import re


def sanitize_name(name: str) -> str:
    final_name = re.sub(r'[\\/:"*?<>|]', '_', name)
    return final_name


def save_html_to_file(wd, id):
    id = sanitize_name(id)
    if not os.path.isdir(CONFIG.html_file_path):
         os.mkdir(CONFIG.html_file_path)
    save_path = os.path.join(CONFIG.html_file_path, f'debug_{id}.html')
    save_path = save_path.replace(' ', '_')
    LOGGER.info(f"Saving an html screenshot at {save_path}")
    with open(save_path, 'w+') as f:
            f.write(wd.page_source)


def save_screenshot(wd, id):
    id = sanitize_name(id)
    if not os.path.isdir(CONFIG.png_file_path):
        os.mkdir(CONFIG.png_file_path)
    save_path = os.path.join(CONFIG.png_file_path, f'debug_{id}.png')
    LOGGER.info(f"Saving a screenshot at {save_path}")
    wd.get_screenshot_as_file(save_path)