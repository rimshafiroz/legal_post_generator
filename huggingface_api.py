import os
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_image_from_context(context, post_text=None, variant_index: int = 0):
    import hashlib, time
    unique_hash = hashlib.md5((str(context)+str(post_text)+str(time.time())).encode()).hexdigest()[:8] if post_text else str(int(time.time()))
    holiday_suffix = ""
    if context.get("is_holiday"):
        holiday_name = context.get("holiday_name", "UAE public holiday")
        holiday_suffix = (
            f" Incorporate tasteful celebratory accents appropriate for {holiday_name} in the UAE. "
            f"Use a dark base with elegant highlights such as soft gold, emerald green, deep red, or white accents. "
            f"Allow subtle bokeh lights, geometric patterns, or minimal confetti-like particles. "
            f"Avoid flags or literal text; keep it respectful, modern, minimal, and professional. "
        )

    # Style variants to diversify outputs between posts
    style_variants = [
        "glassmorphism, soft diagonal light streaks, dark blue gradients, subtle depth of field",
        "dark slate texture, minimal geometric linework, cyan-orange accent glows, asymmetric composition",
        "dramatic vignette spotlight, metallic highlights, elegant shadows, premium studio lighting",
    ]
    style_suffix = style_variants[variant_index % len(style_variants)]

    prompt = (
        f"Modern, clean, visually striking Instagram background for a law firm specializing in {context['niche']}. "
        f"The image should visually represent the field of {context['niche']} law, be unique, professional, and elegant. "
        f"Use a dark background for strong contrast with white text. "
        f"Do not include any people, faces, portraits, silhouettes, or human figures. "
        f"No illustrations, drawings, or depictions of people or faces. "
        f"No text, no headlines, no newspaper, document, or paper themes. "
        f"Only show objects, symbols, environments, or abstract representations related to {context['niche']} law. "
        f"Leave ample space for overlaying text. "
        f"The graphic should be perfectly suited for a social media post by a law firm. "
        f"Every image must be different and tailored to the specific legal niche: {context['niche']}. "
        f"{holiday_suffix}"
        f"Style: {style_suffix}. "
        f"Variation ID: {unique_hash}. "
        f"Make the image different every time."
    )
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    negative_prompt = (
        "people, person, face, human, silhouette, crowd, hands, portrait, selfie, text, watermark"
    )
    payload = {"inputs": prompt, "parameters": {"negative_prompt": negative_prompt, "guidance_scale": 7}}
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content)).convert("RGBA")
        else:
            print(f"HuggingFace API error: {response.status_code} {response.text}")
            return Image.new("RGBA", (1024, 1024), (7, 23, 52, 255))
    except Exception as e:
        print(f"Image generation failed: {e}")
        return Image.new("RGBA", (1024, 1024), (7, 23, 52, 255))