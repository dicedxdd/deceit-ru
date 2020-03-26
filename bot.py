import discord
import asyncio
from discord.ext import commands
import random
from random import randint
from bs4 import BeautifulSoup
import requests 
from discord.utils import get
import youtube_dl
import os
import config
import datetime
from yandex_music import Client

import nekos

import io
import requests
from PIL import Image, ImageFont, ImageDraw



que = []

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

# Words
hello_words = ['hello', 'hi', 'привет', 'Привет', 'ку', 'Ку', 'Дарова', 'дарова']
answer_words = ['узнать информацию о сервере', 'какая информация', 'команды', 'команды сервера', 'что здесь делать?','что здесь делать', 'помощь', 'хелп']
goodbye_words = ['пока', 'бб', 'bb', 'bye', 'до встречи', 'пока всем', 'пока бот']
comm_words = ['как дела?', 'как дела', 'как ты?', 'как ты']

@client.event
async def on_member_join( member ):
	channel = client.get_channel( 684850433809973250 )

	role = discord.utils.get( member.guild.roles, id = 684811591035781141 )

	await member.add_roles ( role )
	await channel.send( embed = discord.Embed(description = f'Пользователь ``{member.name}``, присоединился к нам!', color = discord.Color.blue()))

@client.event
async def on_ready():
	print('Deceit Bot 1.0v подключен.')

	await client.change_presence(status = discord.Status.online, activity = discord.Game('чинит сервера'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, такой команды не существует.**', color=0xbbd3e0)) 

# Сказать от имени бота
@client.command()
@commands.has_permissions( administrator = True)
async def say(ctx, *, arg):

    await ctx.message.delete()
    await ctx.send(f'{arg}')

# Очистить
@client.command()
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
    
    channel_log = client.get_channel(684856831322882089) #Айди канала логов

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:white_check_mark: Удалено {amount} сообщений.**', color=0xbbd3e0))
    await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0xbbd3e0))

# Кик
@client.command()
@commands.has_permissions( administrator = True) 
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel(684856831322882089) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0xbbd3e0))
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0xbbd3e0)) 

# Бан    
@client.command()
@commands.has_permissions( administrator = True) 
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel(684856831322882089) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0xbbd3e0)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0xbbd3e0))

# Разговоры
@client.event

async def on_message(message):
	await client.process_commands(message)

	msg = message.content.lower()

	if msg in hello_words:
		await message.channel.send('Привет дорогой друг!')

	if msg in answer_words:
		await message.channel.send('Для получения доступа к информации и списку команд пропишите в чат ``!помощь (или !help/хелп/помощь/команды)``! Тс-с-с.')

	if msg in goodbye_words:
		await message.channel.send('Пока, спасибо что общался с нами.')

	if msg in comm_words:
		await message.channel.send('У меня хорошо! Разработчик вкрутил мне новые батарейки, так что я чувствую себя вполне хорошо! А у тебя как?')


# Мут
@client.command()
@commands.has_permissions( administrator = True) 
async def mute(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 684845600570605598) #Айди роли
        channel_log = client.get_channel(684856831322882089) #Айди канала логов

        await member.add_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0xbbd3e0)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0xbbd3e0))

# Размут
@client.command()
@commands.has_permissions( administrator = True) 
async def unmute(ctx,member: discord.Member = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 684845600570605598) #Айди роли
        channel_log = client.get_channel(684856831322882089) #Айди канала логов

        await member.remove_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0xbbd3e0)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был вернут доступ к чатам.**', color=0xbbd3e0))   

# Репорт
@client.command()
async def report(ctx,member: discord.Member = None,*,arg = None):

    channel = client.get_channel(684861344612352030) #Айди канала жалоб

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        await ctx.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}**', color=0xbbd3e0))
        await channel.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}\n:bust_in_silhouette: Автор жалобы: {ctx.author.mention}**', color=0xbbd3e0))

# Пинг
@client.command() 
async def ping(ctx):
    await ctx.send(embed = discord.Embed(description = f'**:gear: Ваш пинг:** { randint( 5, 100 ) }', color=0xbbd3e0))

# Калькулятор
@client.command()
async def math( ctx, a : int, arg, b : int ):

    try:

        if arg == '+':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a + b }', color=0xbbd3e0))  

        elif arg == '-':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a - b }', color=0xbbd3e0))  

        elif arg == '/':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a / b }', color=0xbbd3e0))

        elif arg == '*':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a * b }', color=0xbbd3e0))      

    except:
        
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: Произошла ошибка.**', color=0xbbd3e0)) 

# Орел и Решка
@client.command()
async def coin( ctx ):
    coins = [ 'орел', 'решка' ]
    coins_r = random.choice( coins )
    coin_win = 'орел'

    if coins_r == coin_win:
        await ctx.send(embed = discord.Embed(description= f''':tada: { ctx.message.author.name }, выиграл! 
            Тебе повезло у тебя: ``{ coins_r }``''', color = 0xbbd3e0))

    if coins_r != coin_win:
        await ctx.send(embed = discord.Embed(description= f''':thumbsdown:  { ctx.message.author.name }, проиграл! 
            Тебе не повезло у тебя: ``{ coins_r }``''', color = 0xbbd3e0)) 

# Войти в канал
@client.command(aliases=['подключиться', 'j'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        return await voice.move_to(channel)
    else:
        await channel.connect()
        await ctx.send("Бот подключился")

# Выйти из канала
@client.command(aliases=['отключиться', 'l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Бот отключился от канала {channel}")
        await ctx.send("Бот отключился")
    else:
        print("Бот не в голосе")
        await ctx.send("Я не могу выйти из пустоты!")

# Музыка
@client.command(aliases=['плей', 'pl'])
async def play(ctx, *, args):
    def check_queue():
        global args
        args = que.pop(0)
        if args.startswith('https://www.youtube.com/'):
            song_there = os.path.isfile('song.mp3')
            try:
                if song_there:
                    os.remove('song.mp3')
                    print('[log] Старый файл удален')
            except PermissionError:
                print('[log] Не удалось удалить файл')
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('[log] Загружаю музыку...')
                ydl.download([args])
            for file in os.listdir('./'):
                if file.endswith('.mp3'):
                    print(f'[log] Переименовываю файл: {file}')
                    os.rename(file, 'song.mp3')
            voice = get(client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio('song.mp3'),
                       after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.10
        else:
            song_there = os.path.isfile('song.mp3')
            try:
                if song_there:
                    os.remove('song.mp3')
                    print('[log] Старый файл удален')
            except PermissionError:
                print('[log] Не удалось удалить файл')
            res = client.search(args).best.result
            track_id = res.id
            track = client.tracks([track_id])[0]
            print('[log] Загружаю музыку...')
            track.download(filename='song.mp3', codec='mp3', bitrate_in_kbps=192)
            voice = get(client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio('song.mp3'),
                       after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.10
        return

    if args.startswith('https://www.youtube.com/'):
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                print('[log] Старый файл удален')
        except PermissionError:
            print('[log] Не удалось удалить файл')
        await ctx.send('Пожалуйста ожидайте')
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('[log] Загружаю музыку...')
            ydl.download([args])
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                print(f'[log] Переименовываю файл: {file}')
                os.rename(file, 'song.mp3')
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.10
    else:
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                print('[log] Старый файл удален')
        except PermissionError:
            print('[log] Не удалось удалить файл')
        await ctx.send('Пожалуйста ожидайте')
        res = client.search(args).best.result
        track_id = res.id
        track = client.tracks([track_id])[0]
        print('[log] Загружаю музыку...')
        track.download(filename='song.mp3', codec='mp3', bitrate_in_kbps=192)
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.10

# Очередь
@client.command(aliases=['очередь', 'q'])
async def queue(ctx, *, args):
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_playing():
        que.append(args)
        await ctx.send('Песня добавлена в очередь')
        print(que)
    else:
        pass

# Пауза
@client.command(aliases=['пауза', 'p'])
async def pause(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_playing():
        print("Музыка на паузе")
        voice.pause()
        await ctx.send("Музыка на паузе")
    else:
        print("Бот не проигрывает музыку.")
        await ctx.send("Я не проигрываю музыку.")

# Продолжить
@client.command(aliases=['продолжить', 'r'])
async def resume(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_paused():
        print("Музыка возобновлена")
        voice.resume()
        await ctx.send("Продолжаем петь")
    else:
        print("музыка не на паузе")
        await ctx.send("Музыка не на паузе")

# Стоп
@client.command(aliases=['остановить', 's'])
async def stop(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_playing():
        print("Музыка остановлена")
        voice.stop()
        await ctx.send("Музыка остановлена")
    else:
        print("Нет проигрывающейся музыки")
        await ctx.send("Нет проигрывающейся музыки.")

# Громкость
@client.command(aliases=['громкость', 'v'])
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Я не подключен к голосу")
    print(volume/100)
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Громкость изменена на {volume}%")

# Акинатор
@client.command(name = "ball")
async def ball(ctx, *, arg):

    message = ['Нет','Да','Возможно','Опредленно нет'] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: Знаки говорят:** {s}', color=0xbbd3e0))
    return

# Роли за реакцию
@client.event
async def on_raw_reaction_add(payload):
    msgID = int(payload.message_id)
    if msgID == int(config.message_id):
        emoji = str(payload.emoji)
        member = payload.member 
        role = discord.utils.get(member.guild.roles, id=config.roles[emoji])
        await member.add_roles(role)
    else:
        pass

@client.event
async def on_raw_reaction_remove(payload):
    msgID = int(payload.message_id)
    if msgID == int(config.message_id):
        channelID = payload.channel_id
        channel = client.get_channel(channelID)
        messageID = payload.message_id
        message = await channel.fetch_message(messageID)
        userID = payload.user_id
        member = discord.utils.get(message.guild.members, id= userID)
        emoji = str(payload.emoji)
        role = discord.utils.get(member.guild.roles, id=config.roles[emoji])
        await member.remove_roles(role)
    else:
        pass

# Время
@client.command()
async def time(ctx):
    emb = discord.Embed(colour= discord.Color.green(), url= 'https://www.timeserver.ru')
    
    emb.set_author(name= client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text= 'Если у вас время по МСК, то к этому добавляйте +1 час', icon_url=ctx.author.avatar_url)
    emb.set_thumbnail(url='https://www.worldtimeserver.com/img/dst/dst-2-3.png')

    now_date = datetime.datetime.now()
    emb.add_field(name='Time', value='{}'.format(now_date))

    await ctx.send( embed = emb )

# Класс
class Messages:

    def __init__(self, client):
        self.client = client

    async def number_messages(self, member):
        n_messages = 0
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit = None):
                        if message.author == member:
                            n_messages += 1
                except (discord.Forbidden, discord.HTTPException):
                    continue
        return n_messages


# Карточка
@client.command(aliases = ['карта', 'карточка', 'card'])
async def card_user(ctx):

        url = str(ctx.author.avatar_url)[:-10]

        r = requests.get(url, stream = True)
        r = Image.open(io.BytesIO(r.content))
        r = r.convert('RGBA')
        r = r.resize((227, 227), Image.ANTIALIAS)

        image = Image.new("RGBA", (917, 374), (0, 0, 0, 0))
        image.paste(r, (29, 22, 256, 249))

        banner = Image.open('banner.png') #место куда мы сохранили баннер
        banner = banner.convert('RGBA')

        image.paste(banner, (0, 0, 917, 374), banner)

        idraw = ImageDraw.Draw(image)
        name = ctx.author.name
        tag = ctx.author.discriminator
 
        font_50 = ImageFont.truetype("bahnschrift.ttf", size = 50)
        font_25 = ImageFont.truetype("bahnschrift.ttf", size = 25)

        idraw.text((294, 72), f'Имя: {name}#{tag}', font = font_50)
        idraw.text((294, 137), f'Айди: {ctx.author.id}', font = font_25)
        idraw.text((294, 165), f'Онлайн: {ctx.author.status}', font = font_25)

        image.save('userimg.png') #место, куда сохраняем картинку

        await ctx.send(file = discord.File(fp = 'userimg.png')) #прикрепляем картинку

# Создать приглашение
@client.command()
async def inv(ctx):
    channel = client.get_channel(685115736602968101)
    log = client.get_channel(684856831322882089)
    await ctx.message.delete()
    invitelink = await channel.create_invite(max_uses=100, max_age=0, unique=True)
    await ctx.author.send(f'Вы запросили ссылку-приглашение на сервер. Здорово! Теперь отправь eё другу:\n{invitelink}')
    emb = discord.Embed(title= 'Создано приглашение на сервер', color=discord.Color.blue())
    emb.add_field(name= 'Приглашение создано участником:', value = ctx.author.mention)
    await log.send(embed=emb)


# Курс/Валюта
class Currensy_rub:
    #Ссылка на сам ссайт
    DOLAR_RU = 'https://www.google.com/search?sxsrf=ALeKk01jZWoCi7DPRT-l4VJfCTYqs4DhtA%3A1584913719655&ei=N913XuzLJ4nurgSg27rgCA&q=доллара+к+рублю&oq=долара+к+ру&gs_l=psy-ab.3.0.0i10l4j0i22i10i30l6.9772.12721..13473...1.1..0.101.1022.11j1......0....1..gws-wiz.......0i71j35i39j0i131j0j0i131i67j0i10i67j0i67j0i203j35i305i39.mwJK-h5dzto'
    #Для таго чтоб сайт понял что вы не бот
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.87'}

    def get_currency_price(self):
        #делаем запрос на самом сайте
        full_page = requests.get(self.DOLAR_RU, headers=self.headers)
        
        #Делаю так чтоб мы парсели через библиотеку бютифулл суп
        soup = BeautifulSoup(full_page.content, 'html.parser')
        
        #Нахожу все нужные елементы 
        convert = soup.findAll('span', {'class': 'DFlfde', 
                                        'class': 'SwHCTb',
                                        'data-precision': 2})
        global odin 
        odin = convert[0].text

@client.command()
async def dollar_rub(ctx):
    cgrn =Currensy_rub()
    cgrn.get_currency_price()
    emb = discord.Embed(title = 'Курс рубля к доллару', color = (0xbbd3e0))
    emb.add_field(name = 'Валюта', value = f'1$ = {odin}руб.')
    await ctx.send(embed = emb)


# к евро
class Currensy_eu:
    #Ссылка на сам ссайт
    DOLAR_EU = 'https://www.google.com/search?sxsrf=ALeKk02M9ss0sb5d9N9PJap2LIJS5-X0sA%3A1584952472366&ei=mHR4Xoi9FY-OrwTC7p9I&q=евро+к+рублю&oq=евро+к+рублю&gs_l=psy-ab.3..0i131i67j0i7i30j0i67j0i7i30l5j0j0i7i30.3163.6946..7164...7.2..0.96.1092.13......0....1..gws-wiz.......0i71j0i7i10i30j0i13j0i13i5i30j0i7i5i30j0i10.B8E2jQH9kr4&ved=0ahUKEwiI6eaImLDoAhUPx4sKHUL3BwkQ4dUDCAo&uact=5'
    #Для таго чтоб сайт понял что вы не бот
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.87'}

    def get_currency_price(self):
        #делаем запрос на самом сайте
        full_page = requests.get(self.DOLAR_EU, headers=self.headers)
        
        #Делаю так чтоб мы парсели через библиотеку бютифулл суп
        soup = BeautifulSoup(full_page.content, 'html.parser')
        
        #Нахожу все нужные елементы 
        convert = soup.findAll('span', {'class': 'DFlfde', 
                                        'class': 'SwHCTb',
                                        'data-precision': 2})
        global odin 
        odin = convert[0].text

@client.command()
async def euro_rub(ctx):
    cgrn =Currensy_eu()
    cgrn.get_currency_price()
    emb = discord.Embed(title = 'Курс рубля к евро', color = (0xbbd3e0))
    emb.add_field(name = 'Валюта', value = f'1€ = {odin}руб.')
    await ctx.send(embed = emb)

@client.command()
async def h(ctx, category: str = None):
	if category == None:
		await ctx.send('Укажите категорию!')
	else:
		possible = [
        'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
        'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
        'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
        'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
        'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
        'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
        'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
        'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
        'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof'
        ]
	if category.lower() not in possible:
        	await ctx.send('Нет такой категории!')
	else:
		embed = discord.Embed(title = 'Ручки на стол!', color = 0xbbd3e0)
		embed.set_image(url = nekos.img(category))
		await ctx.send(embed = embed)

# Создать комнату
voiceID = 685384067398500352
categoryID = 685197606439354413
@client.event
async def on_voice_state_update(member, before, after):
    if(member.bot):return
    if(after.channel and after.channel.category.id == categoryID and after.channel.id == voiceID):

        voiceChannel = await member.guild.create_voice_channel(f"👥 ┇ {member.name}", overwrites={
            member: discord.PermissionOverwrite(
                connect=True, speak=True, move_members=True, manage_channels=True, manage_roles=True, use_voice_activation=True)
        }, category=after.channel.category, reason="Голосовая комната.")

        await member.edit(voice_channel=voiceChannel, reason="Перенос участника в его голосовую комнату.")
    for channel in client.get_channel(voiceID).category.voice_channels:
        if(channel.id == voiceID or len(channel.members) != 0): continue
        await channel.delete(reason="В голосовой комнате 0 людей!")

@client.command(aliases = ['помощь', 'хелп', 'команды', 'рудз'])
async def help(ctx):
	await ctx.author.send(embed = discord.Embed(title = 'Чат-бот💬', description = 'На сервере присутствует чат-бот. Для общения с ботом используйте обычные слова: Привет, как дела и т.д. Новые команды будут добавляться с просьбами пользователей (канал #ℹ┇помощь-просьбы-улучшения ). Общаться можно в канале #💬┇чат .', color = 0xbbd3e0))
	await ctx.author.send(embed = discord.Embed(title = 'Команды📋', description = '**!time** - узнать текущее время\n\n**!ping** - узнать ваш текущий пинг\n\n**!ball** - команда с рандомом (пример: !ball я крутой? (бот отвечает: да или нет и т.д.))\n\n**!report** - оставить жалобу в канале #📕┇подача-жалобы \n\n**!coin** - мини игра "Орел и Решка"\n\n**!math** - калькулятор (использовать так: !math 1 + 1 . ПЕРЕД и ПОСЛЕ аргумента(+,-,/,*) ставить пробел)\n\n**!say** - сказать от имени бота (пример: !say всем привет)\n\n**!inv** - создать уникальное приглашение на сервер для вашего друга.\n\n**!h [категория]** - nsfw команда, использовать только в #🔞┇nsfw-18 (там же и инструкция)\n\n**!dollar_rub** - позволяет узнать курс рубля к доллару.\n\n**!euro_rub** - позволяет узнать курс рубля к евро.\n\n**!card** - ваша персональная карточка с некоторой информацией о вас. (в разработке)', color = 0xbbd3e0))
	await ctx.author.send(embed = discord.Embed(title = 'Музыкальный бот🎶', description = 'На сервере присутствует музыкальный бот.\n\n**!join** - команда чтобы бот вошел в ваш канал\n\n**!play** [url] - проигрывание музыки (url - ссылка на ютуб видео с музыкой(ПОЛНАЯ ССЫЛКА))\n\n**!queue** - добавить еще оду (или более) музыку в очередь\n\n**!pause** - поставить музыку на паузу\n\n**!resume** - продолжить воспроизведение музыки\n\n**!stop** - закончить проигрывать текущую музыку\n\n**!leave** - команда чтобы бот вышел из вашего канала\n\n**!volume [value]** - изменение громкости в процентах (пример: !volume 10)', color = 0xbbd3e0))


# Connect
token = open('token.txt', 'r').readline()

client.run(token)