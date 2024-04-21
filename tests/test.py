import os
import shutil

static_dir = "contents/static/"
if not os.path.exists(static_dir):
    shutil.copytree("templates/static", static_dir)
