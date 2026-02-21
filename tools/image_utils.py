# author: sawyer-shi

import base64
from io import BytesIO
from typing import Any

from PIL import Image


def encode_image_input(input_image: Any, max_bytes: int) -> str:
    if isinstance(input_image, str):
        if input_image.startswith("http://") or input_image.startswith("https://"):
            return input_image
        if input_image.startswith("data:"):
            return input_image

    if hasattr(input_image, "blob"):
        image_bytes = input_image.blob
    elif hasattr(input_image, "read") and callable(getattr(input_image, "read")):
        image_bytes = input_image.read()
        if isinstance(image_bytes, str):
            image_bytes = image_bytes.encode("utf-8")
    elif isinstance(input_image, bytes):
        image_bytes = input_image
    else:
        raise ValueError(f"不支持的图像数据类型: {type(input_image)}")

    if not isinstance(image_bytes, bytes):
        raise ValueError("图像数据必须是字节格式")

    image = Image.open(BytesIO(image_bytes))
    if image.mode == "RGBA":
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image = background
    elif image.mode == "P":
        image = image.convert("RGB")

    img_byte_arr = BytesIO()
    image_format = "PNG"
    image.save(img_byte_arr, format=image_format)
    data_bytes = img_byte_arr.getvalue()

    if len(data_bytes) > max_bytes:
        img_byte_arr = BytesIO()
        image_format = "JPEG"
        image.save(img_byte_arr, format=image_format, quality=95)
        data_bytes = img_byte_arr.getvalue()

    if len(data_bytes) > max_bytes:
        max_mb = int(max_bytes / 1024 / 1024)
        raise ValueError(f"输入图片大小超过{max_mb}MB限制")

    mime = "image/png" if image_format == "PNG" else "image/jpeg"
    img_base64 = base64.b64encode(data_bytes).decode("utf-8")
    return f"data:{mime};base64,{img_base64}"
