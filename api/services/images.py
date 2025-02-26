import os
from pathlib import Path
from uuid import uuid4

from config.config import settings


async def save_image(file, url):
    file_name = f"{uuid4().hex}{file.filename}"
    file_path = os.path.join(url, file_name)

    Path(url).mkdir(parents=True, exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path
