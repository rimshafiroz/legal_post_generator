import os
from dotenv import load_dotenv
load_dotenv()
from gnews import GNews
import datetime
import requests
from typing import Dict, Optional

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b-instruct")  # Default to a good free model

_UAE_HOLIDAY_CACHE: Dict[int, Dict[str, str]] = {}


def _fetch_uae_public_holidays_from_api(year: int) -> Dict[str, str]:
    """Fetch UAE public holidays for a given year using the Nager.Date public API.

    API: GET https://date.nager.at/api/v3/PublicHolidays/{year}/AE
    Returns mapping YYYY-MM-DD -> holiday name. Empty dict on failure.
    """
    try:
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/AE"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        results: Dict[str, str] = {}
        for item in data:
            date_str = item.get("date")  # e.g., "2025-12-02"
            name = item.get("localName") or item.get("name")
            if date_str and name:
                results[date_str] = name
        return results
    except Exception:
        return {}


def _uae_public_holidays_for_year(year: int) -> Dict[str, str]:
    """Return a mapping of YYYY-MM-DD -> holiday name for UAE for a given year.

    Tries dynamic lookup via Nager.Date; falls back to a minimal fixed set if the API fails.
    """
    if year in _UAE_HOLIDAY_CACHE:
        return _UAE_HOLIDAY_CACHE[year]

    api_map = _fetch_uae_public_holidays_from_api(year)
    if api_map:
        _UAE_HOLIDAY_CACHE[year] = api_map
        return api_map

    # Fallback minimal set (only a few fixed-date holidays)
    fallback = {
        f"{year}-01-01": "New Year's Day",
        f"{year}-12-01": "Commemoration Day",
        f"{year}-12-02": "UAE National Day (Day 1)",
        f"{year}-12-03": "UAE National Day (Day 2)",
    }
    _UAE_HOLIDAY_CACHE[year] = fallback
    return fallback


def get_today_uae_holiday_name(today: Optional[datetime.date] = None) -> Optional[str]:
    """Return the UAE holiday name for today if it is a public holiday, else None."""
    if today is None:
        today = datetime.date.today()
    year_map = _uae_public_holidays_for_year(today.year)
    return year_map.get(today.isoformat())


def fetch_trending_article(niche: str, target_date: Optional[datetime.date]) -> Dict[str, Optional[str]]:
    """Fetch a single trending article for the given niche and date, preferring UAE sources.

    Returns a dict with keys: 'title', 'url', 'published', 'publisher'.
    Falls back to generic niche label if nothing found.
    """
    # Prefer UAE-relevant content
    query = f"{niche} law UAE"

    use_period = None
    if target_date and target_date == datetime.date.today():
        use_period = '1d'

    gnews = GNews(language='en', country='AE', max_results=10)
    if use_period:
        gnews.period = use_period

    try:
        results = gnews.get_news(query)
    except Exception:
        results = []

    chosen = None
    if results and target_date:
        for item in results:
            published = item.get('published date') or item.get('published_date') or item.get('published')
            # Try to match yyyy-mm-dd substring
            if isinstance(published, str) and str(target_date) in published:
                chosen = item
                break
        if not chosen:
            chosen = results[0]
    elif results:
        chosen = results[0]

    if chosen:
        return {
            'title': chosen.get('title') or f"Latest updates in {niche}",
            'url': chosen.get('url'),
            'published': chosen.get('published date') or chosen.get('published_date') or chosen.get('published'),
            'publisher': (chosen.get('publisher') or {}).get('title') if isinstance(chosen.get('publisher'), dict) else None,
        }
    return {
        'title': f"Latest updates in {niche}",
        'url': None,
        'published': None,
        'publisher': None,
    }

def get_firm_context(niche, date_override: Optional[datetime.date] = None):
    trending_article = fetch_trending_article(niche, date_override or datetime.date.today())
    today_date = date_override or datetime.date.today()
    holiday_name = get_today_uae_holiday_name(today_date)
    return {
        "firm_name": "Al-Adl Legal",
        "location": "Dubai",
        "country": "UAE",
        "niche": niche,
        "trending": trending_article.get('title'),
        "trending_url": trending_article.get('url'),
        "trending_published": trending_article.get('published'),
        "trending_publisher": trending_article.get('publisher'),
        "date": today_date.isoformat(),
        "holiday_name": holiday_name,
        "is_holiday": bool(holiday_name),
    }
#     )

def build_prompt(context, num_posts=2):
    import random, time
    randomizer = f"Seed: {random.randint(1000,9999)} Time: {int(time.time())}"
    if context.get("is_holiday"):
        holiday_name = context.get("holiday_name", "UAE Public Holiday")
        return (
            f"You are a social media copywriter for a law firm in Dubai.\n"
            f"Firm: {context['firm_name']} (Located in {context['location']}, {context['country']})\n"
            f"Niche: {context['niche']}\n"
            f"Today is a public holiday in the UAE: {holiday_name}.\n"
            f"Date: {context['date']}\n"
            f"{randomizer}\n"
            f"Create {num_posts} short, punchy Instagram post ideas as a question or bold statement (not a headline or news summary). "
            f"Prefer engaging questions that spark participation; at least one post must be a question. "
            f"Theme every line around {holiday_name}.\n"
            f"Rules: one sentence per post, 10–16 words, no hashtags, no emojis, no quotes, no exclamation spam, no firm name, no promotion. "
            f"Start with action verbs or words like How/Can/Should/Do when asking a question. "
            f"Tone must be respectful and appropriate for the UAE. Only output the post text.\n"
            f"Each post must be completely different from the others—do not repeat ideas, wording, or structure. "
            f"Make each post suitable for direct overlay on a graphic, as a bold statement or fact, not a caption.\n"
            f"Format output as a numbered list, each post separated by a blank line."
        )
    else:
        return (
            f"You are a social media copywriter for a law firm in Dubai.\n"
            f"Firm: {context['firm_name']} (Located in {context['location']}, {context['country']})\n"
            f"Niche: {context['niche']}\n"
            f"Today's trending topic (hidden context, do not mention directly): {context['trending']}\n"
            f"Date: {context['date']}\n"
            f"{randomizer}\n"
            f"Create {num_posts} short, punchy Instagram post ideas as a question or bold statement (not a headline or news summary). "
            f"Make it sound like a real Instagram post, not a news article. "
            f"Do not use hashtags, quotes, or author names. "
            f"Do NOT mention the trending topic, news headline, or any context in your output. Only output the post text.\n"
            f"Examples: 'Is it legal to work 7 days a week?' or 'Can your employer fire you without notice?' or 'Know your rights: Overtime pay is mandatory.' "
            f"Each post must be completely different from the others—do not repeat ideas, wording, or structure. "
            f"Posts should be informative, thought-provoking, or spark discussion, but should NOT sound promotional or advertise the firm. "
            f"Make each post suitable for direct overlay on a graphic, as a bold statement or fact, not a caption.\n"
            f"Each post should be concise, unique, clear, and directly related to the trending topic.\n"
            f"Format output as a numbered list, each post separated by a blank line."
        )

def get_post_ideas(niche, num_posts=3, date_override: Optional[datetime.date] = None):
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY is not set in the .env"}

    context = get_firm_context(niche, date_override=date_override)
    prompt = build_prompt(context, num_posts=num_posts)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 1.2
    }
    try:
        response = requests.post(f"{OPENROUTER_API_BASE}/chat/completions", headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            return {"error": f"OpenRouter API error: {response.status_code} {response.text}"}
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        # Split output into posts
        posts = []
        for line in content.split('\n'):
            line = line.strip("- ").strip()
            if line and len(line) > 10 and not any(x in line.lower() for x in ["trending topic", "headline", "news article"]):
                posts.append(line)
        if len(posts) < num_posts:
            import re
            posts = re.split(r'\d+\. ', content)
            posts = [p.strip() for p in posts if p.strip() and len(p.strip()) > 10 and not any(x in p.lower() for x in ["trending topic", "headline", "news article"])]
        return posts[:num_posts]
    except Exception as e:
        return {"error": f"OpenRouter API error: {str(e)}"}

