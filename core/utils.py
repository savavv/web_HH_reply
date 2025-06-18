import re
from urllib.parse import urlparse

def extract_hh_vacancy_id(url: str) -> str:
    """
    Извлекает ID вакансии из любой ссылки hh.ru
    Примеры поддерживаемых форматов:
    - https://hh.ru/vacancy/12345678
    - https://spb.hh.ru/vacancy/12345678?from=search
    - https://hh.ru/vacancy/12345678?query=...
    """
    # Проверяем, что это вообще ссылка hh.ru
    if 'hh.ru' not in url and 'hh.ua' not in url:
        raise ValueError("Некорректная ссылка hh.ru")
    
    # Основной вариант: из пути /vacancy/{id}
    path_match = re.search(r'/vacancy/(\d+)', url)
    if path_match:
        return path_match.group(1)
    
    # Альтернативный вариант: из параметров (?vacancy=123)
    param_match = re.search(r'[?&]vacancy=(\d+)', url)
    if param_match:
        return param_match.group(1)
    
    # Если ничего не найдено
    raise ValueError("Не удалось извлечь ID вакансии из ссылки")


