import streamlit as st
from core.utils import extract_hh_vacancy_id
from core.hh_api import fetch_hh_vacancy
from core.openai_client import generate_cover_letter
from core.resume_parser import parse_resume

# Настройки страницы
st.set_page_config(
    page_title="Генератор Cover Letter",
    page_icon="✉️",
    layout="wide"
)

# Заголовок
st.title("📝 Умный генератор сопроводительных писем")
st.markdown("""
Создайте идеальное сопроводительное письмо на основе вашего резюме и вакансии с hh.ru
""")

# Блок загрузки
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader(
        "Загрузите ваше резюме",
        type=["pdf", "docx", "doc", "txt"],
        help="Поддерживаемые форматы: PDF, DOC, DOCX, TXT"
    )
with col2:
    job_url = st.text_input(
        "Ссылка на вакансию hh.ru",
        placeholder="https://hh.ru/vacancy/12345678"
    )

# Настройки генерации
with st.sidebar:
    st.header("Настройки генерации")
    model_choice = st.selectbox(
        "Модель ИИ",
        ["moonshotai/kimi-dev-72b:free", "deepseek/deepseek-r1-0528-qwen3-8b:free"],
        index=0
    )
    tone_choice = st.selectbox(
        "Стиль письма",
        ["Профессиональный", "Креативный", "Формальный"],
        index=0
    )
    word_count = st.slider(
        "Количество слов в письме",
        min_value=150,
        max_value=500,
        value=250,
        step=25
    )

# Генерация письма
if st.button("✨ Сгенерировать письмо", type="primary"):
    if not resume_file or not job_url:
        st.error("Пожалуйста, загрузите резюме и укажите ссылку на вакансию")
    else:
        try:
            # Шаг 1: Парсинг резюме
            with st.spinner("Анализируем резюме..."):
                resume_text = parse_resume(resume_file)
                if not resume_text.strip():
                    raise ValueError("Резюме не содержит текста")
            
            # Шаг 2: Получение данных вакансии
            with st.spinner("Получаем данные вакансии..."):
                vacancy_id = extract_hh_vacancy_id(job_url)
                job_data = fetch_hh_vacancy(vacancy_id)
            
            # Шаг 3: Генерация письма
            with st.spinner("Генерируем письмо..."):
                try:
                    letter = generate_cover_letter(
                    resume_text=resume_text,
                    job_desc=job_data['description'],
                    word_count=word_count,  # Передаем выбранное значение
                    tone=tone_choice,
                    model=model_choice
                )
                    
                        
                    word_count = len(letter.split())
                    st.info(f"Сгенерировано писем: {word_count} слов")
                    
                except ValueError as e:
                    st.error(f"Ошибка: {str(e)}")
                    st.stop()
    
            
            # Показ результата
            st.success("✅ Письмо готово!")
            st.subheader("Результат:")
            edited_letter = st.text_area(
                "Вы можете отредактировать письмо:",
                letter,
                height=400
            )
            actual_words = len(letter.split())
            if abs(actual_words - word_count) > 10:
                st.warning(f"Письмо содержит {actual_words} слов (запрошено {word_count})")
            # Кнопки скачивания
            st.download_button(
                "💾 Скачать как TXT",
                edited_letter,
                file_name=f"Cover_Letter_{vacancy_id}.txt"
            )
            
        except Exception as e:
            st.error(f"Произошла ошибка: {str(e)}")
            st.info("""
            Попробуйте:
            1. Проверить формат файла
            2. Убедиться, что ссылка на вакансию корректна
            3. Попробовать другой файл резюме
            """)

# Инструкция
with st.expander("ℹ️ Как использовать"):
    st.markdown("""
    1. **Загрузите резюме** в формате PDF, DOC или DOCX
    2. **Вставьте ссылку** на вакансию с hh.ru
    3. **Настройте параметры** генерации
    4. **Нажмите кнопку** "Сгенерировать"
    5. **Проверьте** и при необходимости отредактируйте письмо
    6. **Скачайте** готовый результат
    """)