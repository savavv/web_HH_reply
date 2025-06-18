import requests

def fetch_hh_vacancy(vacancy_id: str) -> dict:
    """Получает описание вакансии по ID."""
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    response = requests.get(url, headers={"User-Agent": "CoverLetterGenerator/1.0"})
    response.raise_for_status()  # Проверка на ошибки
    data = response.json()
    return {
        "title": data.get("name", ""),
        "description": data.get("description", ""),
        "skills": [skill["name"] for skill in data.get("key_skills", [])],
        "company": data.get("employer", {}).get("name", "")
    }