import os
from dotenv import load_dotenv
load_dotenv()

from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

# 1️⃣ Load the model
model_path = "HuggingFaceTB/SmolVLM2-256M-Video-Instruct"  # or your downloaded path
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    torch_dtype=torch.float32,
    _attn_implementation="eager"
).to("cuda" if torch.cuda.is_available() else "cpu")

# 2️⃣ Define the prompt
video_path = "test.mp4"  # your short local video
messages = [
    {
        "role": "user",
        "content": [
            {"type": "video", "path": video_path},
            {"type": "text", "text": "Is there a squirrel in this video?"}
        ]
    }
]

# 3️⃣ Preprocess input
inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device, dtype=torch.float32)

# 4️⃣ Generate output
generated_ids = model.generate(**inputs, do_sample=False, max_new_tokens=128)

# 5️⃣ Decode text
generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)
print("\nVideo Summary:\n", generated_texts[0])
