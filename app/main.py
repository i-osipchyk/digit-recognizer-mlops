from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image
import io

app = FastAPI()

# Connect application to frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def predict(image: Image.Image):
    """
    Predicts a digit from a given image
    :param image: image to make predictions on
    :return: prediction made by the model
    """
    return 0


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """
    Returns homepage
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict_image(image: UploadFile = File(...)):
    """
    Preprocess uploaded image and makes a prediction
    :param image: uploaded image
    :return: prediction in json format
    """
    if image.content_type not in ["image/png", "image/jpeg", "image/bmp", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")

    contents = await image.read()
    image = Image.open(io.BytesIO(contents)).convert("L")  # Convert image to grayscale
    prediction = predict(image)
    return JSONResponse(content={"prediction": prediction})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
