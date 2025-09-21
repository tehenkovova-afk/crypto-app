import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Заголовок приложения
st.title("🔐 Криптографический тренажер: Шифр Цезаря")
st.markdown("### Изучи основы шифрования с помощью классического шифра Цезаря")

# Загрузка изображений (примеры URL, можно заменить на свои)
def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# Попытка загрузить изображения (запасной вариант - локальные пути)
try:
    caesar_img = load_image_from_url("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Caesar3.svg/800px-Caesar3.svg.png")
    cipher_wheel = load_image_from_url("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/CipherDisk2000.jpg/800px-CipherDisk2000.jpg")
    ancient_cipher = load_image_from_url("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Enigma_rotors_with_alphabet_rings.jpg/800px-Enigma_rotors_with_alphabet_rings.jpg")
except:
    caesar_img = None
    cipher_wheel = None
    ancient_cipher = None

# Правильный русский алфавит
RUSSIAN_ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

# Функция для шифра Цезаря
def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        char_lower = char.lower()
        if char_lower in RUSSIAN_ALPHABET:
            # Определяем регистр
            is_upper = char.isupper()
            
            # Находим позицию в алфавите
            char_pos = RUSSIAN_ALPHABET.index(char_lower)
            
            # Вычисляем новую позицию
            new_pos = (char_pos + shift) % len(RUSSIAN_ALPHABET)
            
            # Получаем новую букву
            new_char = RUSSIAN_ALPHABET[new_pos]
            if is_upper:
                new_char = new_char.upper()
            
            result += new_char
        else:
            # Если символ не русская буква, оставляем как есть
            result += char
    return result

# Боковая панель с информацией
st.sidebar.title("О шифре Цезаря")
st.sidebar.info("""
**Шифр Цезаря** — один из древнейших известных шифров, 
использовавшийся Юлием Цезарем для защиты переписки.

**Принцип работы:** Каждая буква в тексте заменяется на другую букву, 
находящуюся на фиксированное число позиций (ключ) дальше в алфавите. 
Алфавит зациклен: после «я» идёт «а».
""")

# Показать изображение шифра Цезаря, если доступно
if caesar_img:
    st.sidebar.image(caesar_img, caption="Схема шифра Цезаря", use_column_width=True)
else:
    st.sidebar.warning("Изображение схемы шифра недоступно")

# Основной интерфейс
st.header("Шифратор/Дешифратор Цезаря")

# Ввод данных
col1, col2 = st.columns(2)

with col1:
    user_text = st.text_area("Введите текст (русский язык):", "ПРИВЕТ МИР", height=100)

with col2:
    shift = st.slider("Выберите шаг сдвига (ключ):", min_value=1, max_value=32, value=3)
    operation = st.radio("Выберите операцию:", ("Зашифровать", "Расшифровать"))

# Кнопка выполнения
if st.button("Выполнить преобразование", type="primary"):
    if user_text:
        mode = 'encrypt' if operation == "Зашифровать" else 'decrypt'
        processed_text = caesar_cipher(user_text, shift, mode)
        
        st.success("Результат:")
        st.code(processed_text)
        
        # Показать дополнительную информацию
        with st.expander("Показать детали преобразования"):
            st.write(f"**Исходный текст:** {user_text}")
            st.write(f"**Ключ (сдвиг):** {shift}")
            st.write(f"**Режим:** {operation}")
            st.write(f"**Алфавит:** {RUSSIAN_ALPHABET}")
    else:
        st.error("Пожалуйста, введите текст.")

# Дополнительная информация о шифре
st.markdown("---")
st.header("Историческая справка")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Происхождение шифра")
    st.write("""
    Шифр Цезаря назван в честь римского императора Гая Юлия Цезаря,
    который использовал его для секретной переписки со своими генералами.
    
    Это один из самых простых и известных шифров, являющийся разновидностью
    шифра подстановки, где каждая буква в открытом тексте заменяется буквой,
    находящейся на некотором постоянном числе позиций левее или правее неё в алфавите.
    """)

with col2:
    if cipher_wheel:
        st.image(cipher_wheel, caption="Шифровальный диск - механическая реализация шифра Цезаря", use_column_width=True)
    else:
        st.info("Шифровальный диск - механическая реализация шифра Цезаря")

# Раздел криптоанализа
st.markdown("---")
st.header("Криптоанализ шифра Цезаря")

st.write("""
Несмотря на свою историческую значимость, шифр Цезаря не обеспечивает 
серьезной защиты информации по современным меркам. Его можно легко взломать 
с помощью следующих методов:
""")

st.markdown("""
1. **Метод грубой силы (brute force)** - перебор всех возможных ключей (всего 32 для русского алфавита)
2. **Частотный анализ** - анализ частоты появления букв в зашифрованном тексте
3. **Поиск известных слов** - поиск в тексте часто встречающихся слов и словосочетаний
""")

if ancient_cipher:
    st.image(ancient_cipher, caption="Исторические шифровальные устройства", use_column_width=True)

# Практический пример взлома
st.subheader("Попробуйте взломать шифр:")
sample_encrypted = caesar_cipher("секретное сообщение которое нужно расшифровать", 7, 'encrypt')
st.code(f"Зашифрованный текст: {sample_encrypted}")

if st.button("Показать возможные варианты расшифровки"):
    st.write("Возможные варианты (перебор ключей):")
    
    for test_shift in range(1, 33):
        decrypted = caesar_cipher(sample_encrypted, test_shift, 'decrypt')
        st.write(f"Ключ {test_shift}: {decrypted}")

# Информация о проекте
st.markdown("---")
st.caption("Школьный проект по информатике. Разработка образовательного веб-приложения на Python.")
