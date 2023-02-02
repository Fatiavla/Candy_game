from aiogram.types import Message
from aiogram import types
from loader import dp
import random




max_count = 150
total = 0
new_game = False
duel = []
first = 0
current = 0

@dp.message_handler(commands=['start', 'старт'])
async def mes_start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'{name}, привет! Сегодня играем с тобой в конфеты! Для начала игры введи команду /new_game. '
                        'Для настройки конфет введи команду /set и укажи количество конфет.'
                        'Для того, что бы узнать свой ID введи /my_id' )
    print(message)


# Добавил отображение ID для игроков, так же добавил некую "очередь"

@dp.message_handler(commands=['my_id'])
async def my_id(message: Message):
    global duel
    name = message.from_user.first_name
    if message.from_id not in duel:
        duel.append(int(message.from_user.id))
        while len(duel) == 2:
                await dp.bot.send_message (duel[1], f' Твой id {duel[1]}, а противника {duel[0]}.'
                                        f'Теперь для начала дуели, введи /duel {duel[0]}')
                await dp.bot.send_message (duel[0], f' Твой id {duel[0]}, а противника {duel[1]}.'
                                        f'Теперь для начала дуели, введи /duel {duel[1]}')
                break
        else:
                await message.answer('Подожди, пока твой противник узнает свой ID') 
    else:
        await message.answer(f'{name} твой ID уже добавлен :)')

@dp.message_handler(commands=['new_game'])
async def mes_new_game(message: types.Message):
    global new_game
    global total
    global max_count
    global first
    new_game = True
    total = max_count
    first = random.randint(0,1)
    if first:
        await message.answer(f'Игра началась. По жребию первым ходит {message.from_user.first_name}! Бери конфеты')
    else:
        await message.answer(f'Игра началась. По жребию первым ходит Бот')
        await bot_turn(message)


@dp.message_handler(commands=['duel'])
async def mes_duel(message: types.Message):
    global new_game
    global total
    global max_count
    global duel
    global first
    global current
    name = message.from_user.first_name
    duel.append(int(message.from_user.id))
    while True:
        try:
            duel.append(int(message.text.split()[1]))
            player = int(message.from_user.id)
            enemy = int(message.text.split()[1])
            total = max_count
            first = random.randint(0,1)
            if first:
                await dp.bot.send_message(duel[0], 'Первый ход за тобой, бери конфеты')
                await dp.bot.send_message(duel[1], 'Первый ход за твоим противником! Жди своего хода')
                    
            else:
                await dp.bot.send_message(duel[1], 'Первый ход за тобой, бери конфеты')
                await dp.bot.send_message(duel[0], 'Первый ход за твоим противником! Жди своего хода')
            current = duel[0] if first else duel[1]
            new_game = True
            break
        except IndexError:
            await message.answer(f'{name} я же не маг, введи ID оппонента :)') # исключил вылет бота при невводе id 
            break


@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global max_count
    global new_game
    name = message.from_user.first_name
    count = message.text.split()[1]
    if not new_game:
        if count.isdigit():
            max_count = int(count)
            await message.answer(f'Конфет теперь будет {max_count}')
        else:
            await message.answer(f'{name}, напишите цифрами')
    else:
        await message.answer(f'{name}, нельзя менять правила во время игры')



@dp.message_handler()
async def mes_take_candy(message: types.Message):
    global total
    global new_game
    global max_count
    global duel
    global first
    
    name = message.from_user.first_name
    count = message.text
    if len(duel) == 0:
            if new_game:   
                if message.text.isdigit() and 0 < int(message.text) < 29:
                    total -= int(message.text)    
                    if total <= 0:
                        await message.answer(f'Ура!{name} ты победил')
                        new_game = False
                        
                    else: 
                        await message.answer(f'{name} взял {message.text} конфет. '
                                    f'На столе осталось {total}')
                        await bot_turn(message)
                else:
                    await message.answer(f'{name}, надо указать ЧИСЛО от 1 до 28!')
    else:
                if current == int(message.from_user.id):
                    name = message.from_user.first_name
                    count = message.text
                    if new_game:   
                        if message.text.isdigit() and 0 < int(message.text) < 29:
                            total -= int(message.text)    
                            if total <= 0:
                                await message.answer(f'Ура! {name} ты победил')
                                await dp.bot.send_message(enemy_id(), 'К сожалению ты проиграл! Твой оппонент оказался умнее! :)')
                                new_game = False
                                
                            else: 
                                await message.answer(f'{name} взял {message.text} конфет. '
                                            f'На столе осталось {total}')
                                await dp.bot.send_message(enemy_id(), f'Теперь твой ход, бери конфеты! На столе осталось ровно {total} ')           
                                switch_players()
                        else:
                            await message.answer(f'{name}, надо указать ЧИСЛО от 1 до 28!')
        



#ход бота
async def bot_turn(message: types.Message):
    global total
    global new_game
    bot_take = 0
    if 0 < total < 29:
        bot_take = total
        total -= bot_take
        await message.answer(f'Бот взял {bot_take} конфет. '
                            f'на столе осталось {total} и Бот одержал победу')
        new_game = False
        
    else:
        remainder = total%29
        bot_take = remainder if remainder != 0 else 28
        total -= bot_take
        await message.answer(f'Бот взял {bot_take} конфет. '
                            f'на столе осталось {total}')

def switch_players():
    global duel
    global current
    if current == duel[0]:
        current = duel[1]
    else:
        current = duel[0]

def enemy_id():
    global duel
    global current
    if current == duel[0]:
        return duel[1]
    else:
        return duel[0]


