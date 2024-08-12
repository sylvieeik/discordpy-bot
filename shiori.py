# This example requires the 'message_content' privileged intents

import os
import discord
import datetime
import re
import locale
from discord.ext import commands
import random


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


# 発言したチャンネルのカテゴリ内にチャンネルを作成する非同期関数
async def rename_channel(message, yoteibi):
    category_id = message.channel.id
    category = message.guild.get_channel(category_id)
    edit_channel = await category.edit(name=yoteibi)
    return edit_channel

@client.event
async def on_message(message):
    if message.author.bot: # 送信者がbotである場合は弾く
        return

    if client.user in message.mentions: # 話しかけられたかの判定

# 次の活動日設定
        def daydelta(x):
            return datetime.timedelta(days=x)
        def weekdelta(x):
            return datetime.timedelta(weeks=x)

    # UCTから時差を調整
        d_now_jp = datetime.datetime.now() + datetime.timedelta(hours=9)
        d_today = d_now_jp.date()
        tomorrow = d_today + daydelta(1)
        afmorrow = d_today + daydelta(2)
        dfmorrow = d_today + daydelta(3)
        year = tomorrow.year

        def datesearch(moji):
            return re.search('(\d{1,2})\D(\d{1,2})\s',moji)

        def timesearch(moji):
                return re.search('\s(\d{1,2})\D?(\d{2})',moji)

        def slice_date(d):
            date = datesearch(d)
            kyou = re.match('(きょう|今日)\s\S+',d)
            ashita = re.match('(あした|あす|明日)\s\S+',d)
            asatte = re.match('(あさって|明後日)\s\S+',d)
            shiasatte = re.match('(しあさって|明々後日)\s\S+',d)
            if date:
                return date.group(1, 2)
            elif kyou:
                return datesearch(d_today.strftime('%m/%d ')).group(1, 2)
            elif ashita:
                return datesearch(tomorrow.strftime('%m/%d ')).group(1, 2)
            elif asatte:
                return datesearch(afmorrow.strftime('%m/%d ')).group(1, 2)
            elif shiasatte:
                return datesearch(dfmorrow.strftime('%m/%d ')).group(1, 2)
            else:
                return [-1] * 2

        def slice_time(s):
            time = timesearch(s)
            if time:
                return time.group(1, 2)
            else:
                return [-1] * 2

        def get_weekday(yyyy,mm,dd):
            wey = datetime.datetime(yyyy,mm,dd)
            w_list = ['〈月〉', '〈火〉', '〈水〉', '〈木〉', '〈金〉', '〈土〉', '〈日〉']
            return(w_list[wey.weekday()])


        naiyou = message.clean_content.replace("@シオリ","").strip()
        aruyou = [naiyou]
        for t in aruyou:
            month, day = slice_date(t)
            hour, minute = slice_time(t)
            weekday = get_weekday(int(year), int(month), int(day))
            yoteibi = month + "月" + day + "日" + weekday + hour + ":" + minute

            await rename_channel(message, yoteibi)

            text = '次の活動日は ' + yoteibi + ' ですね。'
            await message.channel.send(text)

# ランダムダイス
    if message.content.startswith("/dice"):
        if client.user != message.author:
            num_random = random.randrange(1,99)
            dice_num = str(num_random)
            await message.reply(dice_num)

client.run(os.environ["DISCORD_TOKEN"])
