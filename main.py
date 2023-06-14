from fastapi import FastAPI
from pydantic import BaseModel
from utilities import *

app = FastAPI()

class ImageSample(BaseModel):
    sample:  str

@app.post("/predict")
async def predict(payload: ImageSample):
    img = convert_to_image(payload.sample)
    pixels = transform(img)
    pixels.unsqueeze_(0)
    with torch.no_grad():
        output = model(pixels)
        predictions = torch.softmax(output, dim=1)
    plot_class_distributions(predictions.squeeze().tolist(), class_names)
    string = convert_to_string('predictions.png')
    return string


@app.post("/viz")
def saliency_map(sample: ImageSample):
    image = convert_to_image(sample.sample)
    saliency(image, model)
    string = convert_to_string('saliency_map.png')
    return string

    


