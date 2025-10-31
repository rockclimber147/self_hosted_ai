import os
from dotenv import load_dotenv
load_dotenv()

from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

class SmolVLM2Wrapper:
    def __init__(self, model_path, device=None, dtype=torch.float32):
        self.model_path = model_path
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = dtype
        self.processor = AutoProcessor.from_pretrained(model_path)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_path,
            torch_dtype=dtype,
            _attn_implementation="eager"
        ).to(self.device)

    def summarize_video(self, video_path, prompt_text="Summarize what happens in this video.", max_tokens=128):
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "video", "path": video_path},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ]

        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device, dtype=self.dtype)

        generated_ids = self.model.generate(**inputs, do_sample=False, max_new_tokens=max_tokens)

        generated_texts = self.processor.batch_decode(generated_ids, skip_special_tokens=True)
        return generated_texts[0]