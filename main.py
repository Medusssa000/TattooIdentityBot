from telegram import InputMediaPhoto
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import TOKEN
from scores import SCORES
from results import RESULTS

# Зберігаємо відповіді користувачів
users = {}
current_question = {}

questions = [

    {
        "text": "Уяви, що ти заходиш у кімнату, де нікого не знаєш.\n\nЯке враження тобі хочеться залишити?",

        "answers": [
            ("🪨 Від мене має відчуватись впевненість. Навіть якщо я майже нічого не скажу.", "q1_a"),
            ("🌫️ Хочу, щоб люди подумали: «У ньому є щось, що хочеться розгадати.»", "q1_b"),
            ("🌪️ Хочу, щоб після знайомства атмосфера стала живішою.", "q1_c"),
            ("📐 Хочу, щоб люди одразу помітили цілісний образ і хороший смак.", "q1_d"),
        ]
    },

    {
        "text": "Ти починаєш працювати в новій команді.\n\nХто з цих людей буде дратувати тебе найбільше?",

        "answers": [
            ("🪨 Людина, яка багато говорить про великі цілі, але майже нічого не робить.", "q2_a"),
            ("📡 Людина, яка копіює інших і боїться показати власний характер.", "q2_b"),
            ("🌪️ Людина, яка живе за графіком і ніколи не дозволяє собі спонтанність.", "q2_c"),
            ("📐 Людина, яка робить усе абияк і каже: «Та й так нормально.»", "q2_d"),
        ]
    },

    {
        "text": "Який комплімент був би для тебе найціннішим?",

        "answers": [
            ("🪨 «Поруч із тобою почуваєшся спокійно.»", "q3_a"),
            ("📡 «Ти ні на кого не схожий.»", "q3_b"),
            ("🌫️ «У тобі є щось, що неможливо пояснити.»", "q3_c"),
            ("📐 «У тебе бездоганний смак.»", "q3_d"),
        ]
    },

    {
        "text": "Що для тебе означає стиль?",

        "answers": [
            ("🪨 Коли образ говорить про тебе ще до того, як ти почав розмову.", "q4_a"),
            ("🏛️ Коли за кожною деталлю стоїть історія.", "q4_b"),
            ("🌪️ Коли він викликає емоції й запам’ятовується.", "q4_c"),
            ("📐 Коли все виглядає настільки гармонійно, ніби інакше й бути не могло.", "q4_d"),
        ]
    },

    {
        "text": "Яке татуювання ти точно не зробиш?",

        "answers": [
            ("🪨 Те, яке через кілька років здаватиметься мені невдалим або втратить свою актуальність.", "q5_a"),
            ("📡 Те, яке вже є у половини Instagram.", "q5_b"),
            ("🏛️ Те, яке нічого не означає особисто для мене.", "q5_c"),
            ("📐 Те, де композиція виглядає непродуманою.", "q5_d"),
        ]
    },

    {
        "text": "Через 20 років ти хочеш подивитися на свої татуювання і подумати…",

        "answers": [
            ("🪨 «Я зробив правильний вибір.»", "q6_a"),
            ("🌫️ «Вони досі виглядають незвично й не схожі ні на що інше.»", "q6_b"),
            ("🌪️ «Я не боявся жити по-своєму.»", "q6_c"),
            ("🏛️ «У кожному з них досі є сенс.»", "q6_d"),
        ]
    },
    
    {
        "text": "Уяви, що ти можеш жити лише в одному з цих місць.\n\nЯке обереш?",

        "answers": [
            ("🪨 Будинок серед гір біля озера, де навколо лише природа й тиша.", "q7_a"),
            ("🌫️ Невеликий будинок на узбережжі Ісландії, де майже немає людей, лише океан, туман і вітер.", "q7_b"),
            ("🌪️ Пентхаус у центрі мегаполіса, де життя не зупиняється ні вдень, ні вночі.", "q7_c"),
            ("📐 Мінімалістичний будинок, спроєктований відомим архітектором, де кожна деталь має своє місце.", "q7_d"),
        ]
    },

    {
        "text": "У тебе є лише один вільний день у новій країні.\n\nЩо вибереш?",

        "answers": [
            ("🪨 Піднятися на найвищу точку міста й подивитися на нього зверху.", "q8_a"),
            ("🌫️ Просто блукати без карти й дивитися, куди приведе день.", "q8_b"),
            ("🌪️ Піти туди, де зараз найбільше життя: фестиваль, концерт чи вечірка.", "q8_c"),
            ("📐 Відвідати музей, галерею або сучасну архітектуру.", "q8_d"),
        ]
    },

    {
        "text": "Якби через багато років люди запам'ятали тебе лише за однією річчю, що б ти хотів залишити після себе?",

        "answers": [
            ("🪨 Людину, на яку завжди можна було покластися.", "q9_a"),
            ("📡 Ідею або стиль, який надихнув інших бути собою.", "q9_b"),
            ("🌪️ Історії про життя, сповнене пригод, ризику та яскравих моментів.", "q9_c"),
            ("🏛️ Міцну сім'ю, цінності й людей, які пам'ятатимуть мене з любов'ю.", "q9_d"),
        ]
    },
    
    {
        "text": "Якби ти був головним героєм фільму, який це був би жанр?",

        "answers": [
            ("🪨 Кримінальна драма про людину, яка відстоює свої принципи, навіть коли весь світ проти неї.", "q10_a"),
            ("🌫️ Психологічний трилер, у якому до самого фіналу неможливо зрозуміти головного героя.", "q10_b"),
            ("🌪️ Пригодницький фільм про мандрівника, який постійно шукає нові виклики й ризикує заради свободи.", "q10_c"),
            ("📡 Наукова фантастика про людину, яка створила щось настільки унікальне, що змінила цілу планету.", "q10_d"),
        ]
    },

    {
        "text": "Який музичний івент ти обереш без роздумів?",

        "answers": [
            ("🤘 Великий рок/метал фестиваль просто неба.", "q11_a"),
            ("🖤 Андеграундна техно-вечірка в старому заводі до самого ранку.", "q11_b"),
            ("🎤 Величезний стадіонний концерт Travis Scott, Kendrick Lamar чи іншого хіп-хоп артиста.", "q11_c"),
            ("✨ Шоу світової поп-зірки рівня The Weeknd, Dua Lipa чи Billie Eilish.", "q11_d"),
        ]
    },

    {
        "text": "Уяви, що ти можеш залишити після себе лише одну річ.\n\nЩо це буде?",

        "answers": [
            ("🪨 Репутація людини, яка завжди тримала слово.", "q12_a"),
            ("🌫️ Образ, який люди пам'ятатимуть, але ніколи не зможуть повністю пояснити.", "q12_b"),
            ("🌪️ Спогади про людину, яка прожила життя на повну й надихала інших не боятися ризикувати.", "q12_c"),
            ("📡 Власний стиль або ідею, які ще довго будуть надихати інших.", "q12_d"),
        ]
    }
    
    ]

       

async def show_question(query, index):

    question = questions[index]

    current_question[query.from_user.id] = index

    keyboard = []

    letters = ["A", "Б", "В", "Г"]

    for i, (_, code) in enumerate(question["answers"]):
        keyboard.append([
            InlineKeyboardButton(letters[i], callback_data=code)
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"🎌 *Питання {index + 1} із {len(questions)}*\n\n"
    text += f"{question['text']}\n\n"

    for i, (answer, _) in enumerate(question["answers"]):
        text += f"*{letters[i]}.* {answer}\n\n"

    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )



async def send_moodboard(query, winner):

    folders = {
        "Моноліт": "monolit",
        "Привид": "pryvyd",
        "Шторм": "shtorm",
        "Архітектор": "architect",
        "Хранитель": "hranytel",
        "Сигнал": "signal"
    }

    folder = folders[winner]

    media = []

    for i in range(1, 6):
        path = os.path.join("images", folder, f"{i}.jpg")

        media.append(
            InputMediaPhoto(
                media=open(path, "rb")
            )
        )

    await query.message.reply_media_group(media)   

    

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🚀 Почати тест", callback_data="start_test")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎌 *Яка енергія керує твоїм стилем?*\n\n"
        "Я допоможу знайти не просто стиль татуювання.\n"
        "Я допоможу зрозуміти, який образ уже живе всередині тебе.\n\n"
        "⏳ Тест займає приблизно 3 хвилини.\n\n"
        "Наприкінці ти отримаєш:\n"
        "• свій архетип\n"
        "• рекомендації по стилях\n"
        "• мудборд\n\n"
        "👇 Натискай кнопку нижче.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


 # Натиснули "Почати тест"
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    if query.data == "start_test":

        await show_question(query, 0)

    # Натиснули "Пройти ще раз"
    elif query.data == "restart":

        users.pop(query.from_user.id, None)
        current_question.pop(query.from_user.id, None)

        await show_question(query, 0)


    # Натиснули будь-яку відповідь
    elif query.data.startswith("q"):

        user_id = query.from_user.id

        if user_id not in users:
            users[user_id] = {}

        question_index = current_question[user_id]

        users[user_id][f"q{question_index + 1}"] = query.data

        next_question = question_index + 1

        if next_question < len(questions):
            await show_question(query, next_question)
            
        else:

            results = {
                "Моноліт": 0,
                "Привид": 0,
                "Шторм": 0,
                "Архітектор": 0,
                "Хранитель": 0,
                "Сигнал": 0,
            }

            for answer in users[user_id].values():

                if answer in SCORES:

                    for archetype, points in SCORES[answer].items():
                        results[archetype] += points

            winner = max(results, key=results.get)


            await query.edit_message_text(
                RESULTS[winner]
            )

            await send_moodboard(query, winner)

            keyboard = [
                [InlineKeyboardButton(
                    "🖤 Обговорити свою ідею",
                        url="https://t.me/medusssa_k"
                )],
                [InlineKeyboardButton(
                    "🔄 Пройти тест ще раз",
                    callback_data="restart"
                    )]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(
                "✨ Якщо хочеш створити татуювання, яке справді буде продовженням тебе — напиши мені.",
                reply_markup=reply_markup
            )


# Запуск
print(f"TOKEN exists: {TOKEN is not None}")
print(f"TOKEN length: {len(TOKEN) if TOKEN else 0}")
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("✅ Бот запущений...")

app.run_polling()