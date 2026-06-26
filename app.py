from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import io
import os

app = FastAPI()

# 결과 이미지를 저장할 폴더 생성
UPLOAD_DIR = "./outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "가상 피팅 백엔드 서버 정상 작동 중"}

@app.post("/fitting")
async def create_fitting_image(
    human_image: UploadFile = File(...),
    cloth_image: UploadFile = File(...),
):

    human_data = await human_image.read()
    cloth_data = await cloth_image.read()

    human_img = Image.open(io.BytesIO(human_data)).convert("RGBA")
    cloth_img = Image.open(io.BytesIO(cloth_data)).convert("RGBA")

    resized_cloth = cloth_img.resize((int(human_img.width * 0.5), int(human_img.height * 0.5)))

    position = (
        (human_img.width - resized_cloth.width) // 2,
        (human_img.height - resized_cloth.height) // 2
    )

    human_img.paste(resized_cloth, position, resized_cloth)

    output_path = os.path.join(UPLOAD_DIR, "result.png")
    human_img.save(output_path)

    return FileResponse(output_path, media_type="image/png")