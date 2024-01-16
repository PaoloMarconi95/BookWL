from Config import CONFIG, LOGGER
import os


def save_html_to_file(wd, id):
    save_path = os.path.join(CONFIG.html_file_path, f'debug_{id}.html')
    LOGGER.info(f"Saving an html screenshot at {save_path}")
    with open(save_path, 'w+') as f:
            f.write(wd.page_source)


def save_screenshot(wd, id):
    save_path = os.path.join(CONFIG.png_file_path, f'debug_{id}.png')
    LOGGER.info(f"Saving a screenshot at {save_path}")
    wd.get_screenshot_as_file(save_path)