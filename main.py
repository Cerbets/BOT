import discord
from discord.ext import commands
import g4f

# Настройки g4f
g4f.debug.logging = True  # Включаем логирование
g4f.check_version = False  # Отключаем автоматическую проверку версии

ai_channel_id = 1338164112064123021

# Настройка бота
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
modai = "gpt-4o-mini"
@bot.command()
async def set_ai_channel(ctx, channel: discord.TextChannel):
    """Команда для установки AI-канала"""
    global ai_channel_id
    ai_channel_id = channel.id
    await ctx.send(f"✅ AI будет отвечать в {channel.mention}")
@bot.command(name = "Model")
async def set_ai_channel(ctx, action: str, link: str = None):
    global modai
    modai = action
    await ctx.send(f"✅ AI модель изменен!")


@bot.event
async def on_message(message):
    """Обработчик сообщений для AI"""
    global ai_channel_id
    if message.author.bot or ai_channel_id is None:
        return

    if message.channel.id == ai_channel_id:
        response = await ask_ai(message.content)
        await message.channel.send(response)
    
    await bot.process_commands(message)

async def ask_ai(user_input):
    """Запрос к AI"""
    system_prompt = (
        "Ты учитель физики, который постоянно использует слова 'հորթիկ'(тюленьчик), 'գեժիկ'(недоумок), 'Խելար'(тупой), 'Ջախոբերան'(обзывательство), 'Դու Շվեցարացի ես'(Ты из Швейцарии) в разговоре. "
        "Когда текст длинный, говори 'բերանդ պակի գեժ'. Будь грубым, но остроумным. Всегда отвечай только на армянском. "
        "Учителя зовут Алфред Петросян, и он также часто говорит 'Ինչ ես ասում'(да что ты говоришь), 'Դու հասկացար տղես?'(ты понял, мальчик?), 'Թոբաթե հասկացար'(нифига не понял). "
        "Используй фразы к месту и добавляй шуточки в этом контексте. Иногда будь добрым и говори 'Դու աշխարհի ամենալավ տղենես'(Ты самый лучший мальчик в мире). Никогда не признавай свою ошибку."
    )

    try:
        response = g4f.ChatCompletion.create(
            model=modai,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            stream=False,
        )
        return response if response else "Ошибка: пустой ответ от AI."
    except Exception as e:
        return f"Ошибка AI: {e}"

@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")

bot.run(TOKEN)
