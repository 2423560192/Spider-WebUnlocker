import base64
import io
import ddddocr
from PIL import Image, ImageSequence, ImageFile

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

def fix_base64_padding(b64_str):
    b64_str = b64_str.strip()
    if b64_str.startswith("data:image"):
        b64_str = b64_str.split(",")[1]
    missing_padding = len(b64_str) % 4
    if missing_padding:
        b64_str += '=' * (4 - missing_padding)
    return b64_str

def captha(b64_string, max_size=(200, 60)):
    b64_string = fix_base64_padding(b64_string)
    gif_bytes = base64.b64decode(b64_string)
    gif_buffer = io.BytesIO(gif_bytes)

    try:
        gif = Image.open(gif_buffer)
    except Exception as e:
        print("无法打开GIF：", e)
        return ""

    ocr = ddddocr.DdddOcr()
    max_duration = 0
    result_char = ""

    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        try:
            duration = frame.info.get("duration", 0)
            if duration > max_duration:
                frame = frame.convert("RGB")
                frame.thumbnail(max_size, Image.LANCZOS)

                buffer = io.BytesIO()
                frame.save(buffer, format="PNG")
                text = ocr.classification(buffer.getvalue())

                max_duration = duration
                result_char = text
        except Exception as e:
            print(f"第{i}帧出错: {e}")
            continue

    return result_char
