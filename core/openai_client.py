import requests
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import os

def generate_cover_letter(resume_text: str, job_desc: str, model: str = "deepseek/deepseek-r1-0528:free", 
                         tone: str = "Профессиональный", word_count: int = 250) -> str:
    """Генерация сопроводительного письма с учетом выбранного количества слов"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("API ключ OpenRouter не найден")

    # Строгий промт с учетом выбранного количества слов
    prompt = f"""
    Напиши сопроводительное письмо на русском языке строго на {word_count} слов.
    Точное количество слов должно быть {word_count} (±3 слова).
    
    Технические требования:
    1. Только русский язык (никаких англицизмов)
    2. Стиль: {tone.lower()}
    3. Формат:
       - Приветствие (1 предложение)
       - Основная часть ({word_count - 50} слов)
       - Заключение (1-2 предложения)
    4. англицизмов быть не
    Информация о кандидате:
    {resume_text[:3000]}
    
    Описание вакансии:
    {job_desc[:3000]}
    
    Важно:
    - Не используй слова "CV", "HR" и другие англицизмы
    - Строго соблюдай указанный объем
    - Избегай шаблонных фраз
    - Делай письмо персонализированным
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://cover-letter-generator.example.com",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,  # Более строгий контроль
        "max_tokens": 1500
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        
        letter = response.json()["choices"][0]["message"]["content"]
        return _post_process_letter(letter, word_count)
    except Exception as e:
        raise ValueError(f"Ошибка генерации: {str(e)}")

def _post_process_letter(letter: str, target_word_count: int) -> str:
    """Пост-обработка письма"""
    # Удаляем служебные комментарии ИИ
    letter = letter.split("---")[0].strip()
    
    # Проверяем количество слов
    current_words = len(letter.split())
    if abs(current_words - target_word_count) > 5:
        letter = _adjust_word_count(letter, target_word_count)
    
    return letter

def _adjust_word_count(text: str, target: int) -> str:
    """Корректировка количества слов"""
    words = text.split()
    if len(words) > target:
        return ' '.join(words[:target])
    return text