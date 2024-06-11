from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import uvicorn


app = FastAPI()

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("hieudinhpro/BERT_Sentiment_Vietnamese")
model = AutoModelForSequenceClassification.from_pretrained("hieudinhpro/BERT_Sentiment_Vietnamese")

class TextInput(BaseModel):
    text: str

@app.post("/predict")
async def predict(input: TextInput):
    # Tokenize input text
    inputs = tokenizer(input.text, return_tensors="pt", truncation=True, padding=True)
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get predicted class
    logits = outputs.logits
    predicted_class_id = logits.argmax().item()

    return {"predicted_class_id": predicted_class_id}

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
