import os
import requests
from dotenv import load_dotenv
load_dotenv()

def get_firm_context(niche):
    return {
        "firm_name": "Al-Adhan Legal",
        "location": "Dubai",
        "country": "UAE",
        "niche": niche
    }

def build_prompt(context, num_posts=3):
    return (
        f"You are an AI assistant helping a law firm generate social media content.\n"
        f"Firm: {context['firm_name']}\n"
        f"Location: {context['location']}, {context['country']}\n"
        f"Niche: {context['niche']}\n"
        # f"Create {num_posts} professional and visually impactful social media posts for given firm name and location. Each post should reflect firm {context['niche']}, convey trust, integrity and commitment to clients. The tone must be expert yet approachable. Avoid legal jargon. Each post should be catchy,quote-style way, suitable to be placed on a graphic in 2-3 sentences. (Without suggesting visuals and captions and extra explanations about the post)\n"
        # f"Generate {num_posts} original, short, and professional graphic-ready social media post lines for this law firm.Each post should be 2-3 impactful lines that reflect the firm's niche, professionalism, empathy, and trustworthiness. Avoid using labels like [Quote] or [Tagline], and do not mention any author name.Do not suggest images or graphics. Don't add anything extra. Just output like: "
        f"Generate {num_posts} professional social media post for a law firm. Each post should be (2-3 lines) concise, authoritative, and suitable to place as text on an Instagram graphic. The tone must be expert and catchy. Avoid using labels like [Quote] or [Tagline], and do not mention any author name.Do not suggest images or graphics. Don't add anything extra. Just output like: "
    )
    

def get_post_ideas(niche):
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        return ["Error: TOGETHER_API_KEY is not set in the .env file."]

    context = get_firm_context(niche)
    prompt = build_prompt(context)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        # "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=data)
        output = response.json()["choices"][0]["text"]
        posts = [line.strip("- ").strip() for line in output.strip().split('\n') if line.strip()]
        return posts
    except Exception as e:
        return [f"Error: {str(e)}"]