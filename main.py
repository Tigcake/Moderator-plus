import nextcord
from nextcord.ext import commands
import datetime
import asyncio
import json
import os
import random

with open(file='setting.json', mode='r', encoding='utf-8') as file:
    config = json.load(fp=file)

intents = nextcord.Intents.all()

bot = commands.Bot(intents=intents)

runtime = int(datetime.datetime.timestamp(datetime.datetime.now()))

class dev:
    async def developers():
            
        allDevelopers = []

        for user in config['bot-developer']:
            try:
                allDevelopers.append(await bot.fetch_user(user))
            except Exception:
                allDevelopers.append('user not found')

        return allDevelopers
    
    async def testers():

        allTesters = []

        for user in config['bot-tester']:
            try:
                allTesters.append(await bot.fetch_user(user))
            except Exception:
                allTesters.append('user not found')

        return allTesters

    def getIntro(developers, testers):
        return '''
version - {}

developers - {}

testers - {}

runtime - {}s

github - {}
'''.format('.'.join('%s' %id for id in config['version']), ', '.join('%s' %id for id in developers), ', '.join('%s' %id for id in testers), (format(int(datetime.datetime.timestamp(datetime.datetime.now())) - runtime, ',d')), config['github'])

@bot.event
async def on_ready():
    print('{} is online\n\n{}'.format(bot.user.name, dev.getIntro(await dev.developers(), await dev.testers())))

# commands [start]

@bot.slash_command(name='dev', description='Obtain the development materials of the bot', description_localizations={'zh-TW': '獲取機器人的開發資料', 'zh-CN': '获取机器人的开发资料'}, dm_permission=True, force_global=True)
async def devCommand(interaction: nextcord.Interaction):
    
    devEmbed = nextcord.Embed(colour=nextcord.Colour.dark_theme(), title='開發者內容', description='```{}```'.format(dev.getIntro(await dev.developers(), await dev.testers())), timestamp=datetime.datetime.now())
    devEmbed.set_footer(text='{}ms'.format(round(bot.latency*1000)))

    await interaction.send(embed = devEmbed, ephemeral=True)

@bot.slash_command(name='purge', description='Purge the channel message(s)', description_localizations={'zh-TW': '清除頻道內的訊息', 'zh-CN': '清除频道内的讯息'}, dm_permission=False, default_member_permissions=8, force_global=True)
async def purgeCommand(interaction: nextcord.Interaction, limit: int = nextcord.SlashOption(name='limit', description='Amount of message(s) to clear', name_localizations={'zh-TW': '數量', 'zh-CN': '数量'}, description_localizations={'zh-TW': '欲清除的訊息數量', 'zh-CN': '欲清除的讯息数量'}, min_value=1, max_value=100), ephemeral: bool = nextcord.SlashOption(name='ephemeral', description='Make messages visible only to you', name_localizations={'zh-TW': '隱藏', 'zh-CN': '隐藏'}, description_localizations={'zh-TW': '使訊息只有你能看見', 'zh-CN': '使讯息只有你能看见'}, required=False, default=False)):
    try:
        messages = await interaction.channel.purge(limit=limit)
        sucessEmbed = nextcord.Embed(color=nextcord.Color.green(), title='✅ 成功運行！', description='您已成功刪除 {} 則訊息。'.format(len(messages)), timestamp=datetime.datetime.now())
        sucessEmbed.set_footer(text='訊息已成功刪除，顯示需要點時間')
        await interaction.send(embed=sucessEmbed, ephemeral=ephemeral)
    except Exception as error:
        errorEmbed = nextcord.Embed(color=nextcord.Color.red, title='❌ 運行失敗', description='指令出現錯誤，無法運行。', timestamp=datetime.datetime.now())
        errorEmbed.add_field(name='詳細錯誤訊息', value='```py\n{}\n```'.format(error))
        
        reportChannel: nextcord.TextChannel = await bot.get_channel(1081205215254028318)
        await reportChannel.send(content='Guild - {} | User - {} | Time - <t:{}> | Command - /purge\n```py\n{}\n```'.format(interaction.guild.name, interaction.user, interaction.created_at.timestamp(), error))
        
        errorEmbed.set_footer(text='錯誤已回報至開發團隊！')
        await interaction.send(embed=errorEmbed, ephemeral=True)

@bot.user_command(name='user-Info', force_global=True)
async def userInfoCommand(interaction: nextcord.Interaction, member: nextcord.Member):

    if member.color == nextcord.Color.default():
        memberColor = nextcord.Color.dark_theme()
    else:
        memberColor = member.color

    memberRoles = []

    userEmbed = nextcord.Embed(color=memberColor, title='成員資料', description='以下是 {} 在 {} 裡的個人資料。'.format(member.mention, interaction.guild.name))

    userEmbed.set_author(name=member, icon_url=member.display_avatar.url)
    userEmbed.add_field(name='顯示名稱', value=member.display_name, inline=False)
    userEmbed.add_field(name='伺服器加入日期', value='<t:{}> ( <t:{}:R> )'.format(int(member.joined_at.timestamp()), int(member.joined_at.timestamp())), inline=False)
    userEmbed.add_field(name='帳號創建日期', value='<t:{}> ( <t:{}:R> )'.format(int(member.created_at.timestamp()), int(member.created_at.timestamp())), inline=False)
    
    for role in member.roles:
        if role.mention != '@everyone':
            memberRoles.append(role.mention)
    if len(memberRoles) != 0:    
        userEmbed.add_field(name='身分組', value=', '.join(memberRoles), inline=False)
    
    userEmbed.add_field(name='帳號 ID', value='`{}`'.format(member.id), inline=False)

    await interaction.send(embed=userEmbed)

# commands [end]

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension('cogs.{}'.format(filename[:-3]))

if __name__ == '__main__':
    bot.run(config['token'])