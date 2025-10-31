import os
from dotenv import load_dotenv
load_dotenv()

from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

class SmolVLM2Wrapper:
    def __init__(self, model_path, device=None, dtype=torch.float32):
        """
        Initialize the AI model and processor.

        Args:
            model_path (str): Path or Hugging Face model ID
            device (str, optional): 'cpu' or 'cuda'. Default auto-detect
            dtype (torch.dtype): torch.float32 (CPU) or torch.bfloat16/float16 (GPU)
        """
        self.model_path = model_path
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = dtype

        # Load processor
        self.processor = AutoProcessor.from_pretrained(model_path)

        # Load model
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_path,
            torch_dtype=dtype,
            _attn_implementation="eager"
        ).to(self.device)

    def summarize_video(self, video_path, prompt_text="Summarize what happens in this video.", max_tokens=128):
        """
        Summarize a video.

        Args:
            video_path (str): Local path to .mp4
            prompt_text (str): Instruction for the model
            max_tokens (int): Max number of output tokens

        Returns:
            str: Generated text summary
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "video", "path": video_path},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ]

        # Preprocess
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device, dtype=self.dtype)

        # Generate
        generated_ids = self.model.generate(**inputs, do_sample=False, max_new_tokens=max_tokens)

        # Decode
        generated_texts = self.processor.batch_decode(generated_ids, skip_special_tokens=True)
        return generated_texts[0]

# Initialize once (reuse for multiple requests)
ai_model = SmolVLM2Wrapper(
    model_path="HuggingFaceTB/SmolVLM2-256M-Video-Instruct",
    device="cpu",
    dtype=torch.float32
)

# Summarize a video
summary = ai_model.summarize_video("test.mp4", prompt_text="Is there a squirrel in this video?")
print(summary)
summary = ai_model.summarize_video("test.mp4", prompt_text="Is there a bear in this video?")
print(summary)