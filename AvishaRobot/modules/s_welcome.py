import os
import random
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger

from AvishaRobot import pbot as app

from AvishaRobot.database.wel_db import *

COMMAND_HANDLER = ". /".split() # COMMAND HANDLER

LOGGER = getLogger(__name__)

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

CUTE = """**
@app.on_message(filters.command("zwelcome", COMMAND_HANDLER) & ~filters.private)
async def auto_state(_, message):
    usage = "**❅ ᴜsᴀɢᴇ ➥ **/zwelcome [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ]"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
      A = await wlcm.find_one({"chat_id" : chat_id})
      state = message.text.split(None, 1)[1].strip()
      state = state.lower()
      if state == "enable":
        if A:
           return await message.reply_text("๏ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ")
        elif not A:
           await add_wlcm(chat_id)
           await message.reply_text(f"๏ ᴇɴᴀʙʟᴇᴅ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ɪɴ ➥ {message.chat.title}")
      elif state == "disable":
        if not A:
           return await message.reply_text("๏ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ")
        elif A:
           await rm_wlcm(chat_id)
           await message.reply_text(f"๏ ᴅɪsᴀʙʟᴇᴅ sᴘᴇᴄɪᴀʟ ᴡᴇʟᴄᴏᴍᴇ ɪɴ ➥ {message.chat.title}")
      else:
        await message.reply_text(usage)
    else:
        await message.reply("๏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ")
** """


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    #A = await wlcm.find_one({"chat_id" : chat_id})
    #if not A:
      # return
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"restricted"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "HuTao/resources/profilepic.jpg"
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption= f"""
**Hᴇʏ ᴅᴇᴀʀ 🌺 {user.mention}, Wᴇʟᴄᴏᴍᴇ ᴛᴏ {member.chat.title} Gʀᴏᴜᴘ

┏━━━━»»❀
♛ ɴᴀᴍᴇ : {user.mention}
⍟ I'ᴅ : {user.id}
⍟ ᴜꜱᴇʀɴᴀᴍᴇ : @{user.username}
⍟ ᴇɴᴊᴏʏ ʏᴏᴜʀ ꜱᴛᴀʏ
┕━━━━━━━━━━━━»»❀
""",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton (f"ᴠɪᴇᴡ ᴜsᴇʀ", url=f"https://t.me/{user.username}")]])

            )
    except Exception as e:
        LOGGER.error(e)
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        return 


#####
