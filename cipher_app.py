# cipher_app.py
import streamlit as st

# Заголовок приложения
st.title("🧠 Криптографический тренажер")
st.markdown("### Изучи основы шифрования с помощью шифров Цезаря и Виженера")

# Выбор шифра в боковой панели
cipher_type = st.sidebar.selectbox(
    "Выбери шифр:",
    ("Шифр Цезаря", "Шифр Виженера")
)

# Функция для шифра Цезаря
def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    # Если режим 'decrypt', меняем направление сдвига
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if char.isalpha():
            # Определяем базовый код для буквы (для 'a' или 'A')
            base = ord('а') if char.islower() else ord('А')
            # Считаем с учетом русского алфавита (33 буквы)
            shifted = (ord(char) - base + shift) % 33
            result += chr(base + shifted)
        else:
            # Если символ не буква, оставляем как есть
            result += char
    return result

# Функция для шифра Виженера
def vigenere_cipher(text, key, mode='encrypt'):
    result = ""
    key_length = len(key)
    # Приводим ключ к нижнему регистру для удобства
    key = key.lower()
    key_index = 0

    for char in text:
        if char.isalpha():
            # Определяем сдвиг по букве ключа
            shift = ord(key[key_index]) - ord('а')
            if mode == 'decrypt':
                shift = -shift
            
            base = ord('а') if char.islower() else ord('А')
            shifted = (ord(char) - base + shift) % 33
            result += chr(base + shifted)
            
            # Переходим к следующей букве ключа, по кругу
            key_index = (key_index + 1) % key_length
        else:
            result += char
    return result

# Основная логика в зависимости от выбора
if cipher_type == "Шифр Цезаря":
    st.header("Шифр Цезаря")
    st.info("""
    **Принцип работы:** Каждая буква в тексте заменяется на другую букву, 
    находящуюся на фиксированное число позиций (ключ) дальше в алфавите. 
    Алфавит зациклен: после «я» идёт «а».
    """)
    
    user_text = st.text_area("Введите текст (русский язык):")
    shift = st.slider("Выберите шаг сдвига (ключ):", min_value=1, max_value=32, value=3)
    operation = st.radio("Выберите операцию:", ("Зашифровать", "Расшифровать"))
    
    if st.button("Выполнить"):
        if user_text:
            mode = 'encrypt' if operation == "Зашифровать" else 'decrypt'
            processed_text = caesar_cipher(user_text, shift, mode)
            st.success("Результат:")
            st.code(processed_text)
        else:
            st.error("Пожалуйста, введите текст.")

else: # Шифр Виженера
    st.header("Шифр Виженера")
    st.info("""
    **Принцип работы:** Это усложненный шифр Цезаря. 
    Для шифрования используется ключевое слово. 
    Каждая буква ключа определяет свой сдвиг для соответствующей буквы в тексте.
    """)
    
    user_text = st.text_area("Введите текст (русский язык):")
    user_key = st.text_input("Введите ключевое слово (только буквы):")
    operation = st.radio("Выберите операцию:", ("Зашифровать", "Расшифровать"))
    
    if st.button("Выполнить"):
        if user_text and user_key:
            if not user_key.isalpha():
                st.error("Ключ должен содержать только буквы!")
            else:
                mode = 'encrypt' if operation == "Зашифровать" else 'decrypt'
                processed_text = vigenere_cipher(user_text, user_key, mode)
                st.success("Результат:")
                st.code(processed_text)
        else:
            st.error("Пожалуйста, заполните все поля.")

# Информация о проекте в нижней части
st.markdown("---")
st.caption("Школьный проект по информатике. Разработка образовательного веб-приложения на Python.")