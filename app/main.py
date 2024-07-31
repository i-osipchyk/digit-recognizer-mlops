from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image
import io
import os
import tensorflow as tf
import numpy as np
from pathlib import Path

app = FastAPI()

# Determine the base directory
base_dir = Path(__file__).resolve().parent

# Paths to static and template directories
static_dir = base_dir / "static"
templates_dir = base_dir / "templates"

# Mount the static files and templates
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Load the model at startup
model_path = base_dir.parent / "models" / "digit-recognizer-model.keras"
model = tf.keras.models.load_model(model_path)


def predict(image: Image.Image):
    """
    Predicts a digit from a given image
    :param image: image to make predictions on
    :return: prediction made by the model
    """
    # Preprocess the image to match the model's input shape
    image = image.resize((28, 28))  # Resize to 28x28 if your model expects that size
    image_array = np.array(image)
    image_array = image_array / 255.0  # Normalize to [0, 1]
    image_array = np.expand_dims(image_array, axis=(0, -1))  # Add batch and channel dimensions
    prediction = model.predict(image_array)
    predicted_digit = np.argmax(prediction, axis=1)[0]
    return predicted_digit


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
    prediction = predict(image).item()
    return JSONResponse(content={"prediction": prediction})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
