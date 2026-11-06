# Commands: !add | !prmt | !admin | !add1 | !prmt1 | !mixx
import asyncio
import os
import re
import random
import logging

from telethon import TelegramClient, events
from telethon.tl.types import ChatAdminRights
from telethon.tl.functions.channels import InviteToChannelRequest, EditAdminRequest

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("addbot")

# ==================== CONFIG ====================
API_ID   = int(os.environ.get("TG_API_ID",   "37837779"))
API_HASH = os.environ.get("TG_API_HASH",     "03b72efd37a98662270e83e815621257")
OWNER_ID = int(os.environ.get("TG_OWNER_ID", "8729846345"))
SESSION  = os.environ.get("TG_SESSION",      "8729846345")

# List 1 — !add / !prmt
BOT_USERNAMES = [
    "@Xkdjxjxdh_bot",
    "@Bsksdh_bot",
    "@Jshxshshbot",
    "@BSKSJDBOT",
    "@Jdosdhb_bot",
    "@Kdgdjzk_bot",
    "@Ududhhej_bot",
    "@Ejejegg_bot",
    "@Sjushs_bot",
    "@Hdkejzhsddbot",
]

# List 2 — !add1 / !prmt1
BOT_USERNAMES_1 = [
    "@Ilsmkk_bot",
    "@Iiptm_bot",
    "@Rey_fytr3_bot",
    "@Team_hh_bot",
    "@Rey_fytr1_bot",
    "@Rey_fytr_bot",
    "@mnnopp_bot",
    "@m14tfbot",
    "@Uhmmg_hh_bot",
    "@Rey_fytr2_bot",
]
# ================================================

bot = TelegramClient(SESSION, API_ID, API_HASH, auto_reconnect=True, connection_retries=10, retry_delay=3)

RIGHTS = ChatAdminRights(
    change_info=True,
    post_messages=True,
    edit_messages=True,
    delete_messages=True,
    ban_users=True,
    invite_users=True,
    pin_messages=True,
    add_admins=True,
    manage_call=True,
    anonymous=False,
)


async def _edit(status, text):
    try:
        await status.edit(text)
    except Exception:
        pass


def _owner_only(event):
    return event.out or event.sender_id == OWNER_ID


async def _add_bots(event, bots, label="Adding bots"):
    total = len(bots)
    if not total:
        return await event.reply("Bot list khali hai.")

    status = await event.reply(f"⏳ **{label}...** `0/{total}`")
    added = 0

    for i, b in enumerate(bots, 1):
        await _edit(status, f"⏳ **{label}...** `{i}/{total}`\n`{b}`")
        try:
            user = await bot.get_input_entity(b)
            await bot(InviteToChannelRequest(event.chat_id, [user]))
            added += 1
        except Exception as e:
            name = type(e).__name__
            if "UserAlreadyParticipant" in name or "already" in str(e).lower():
                added += 1
        await asyncio.sleep(0.2)

    if added == total:
        final = (
            f"✅ **Bots Added:** `{added}/{total}`\n"
            f"🎉 **Successfully Completed!**"
        )
    else:
        final = f"✅ **Bots Added:** `{added}/{total}`"
    await _edit(status, final)
    return added


async def _promote_bots(event, bots, label="Promoting bots"):
    total = len(bots)
    if not total:
        return await event.reply("Bot list khali hai.")

    status = await event.reply(f"👑 **{label}...** `0/{total}`")
    promoted = 0

    for i, b in enumerate(bots, 1):
        await _edit(status, f"👑 **{label}...** `{i}/{total}`\n`{b}`")
        try:
            user = await bot.get_input_entity(b)
            await bot(EditAdminRequest(event.chat_id, user, RIGHTS, rank="Admin"))
            promoted += 1
        except Exception:
            pass
        await asyncio.sleep(0.2)

    if promoted == total:
        final = (
            f"👑 **Bots Promoted:** `{promoted}/{total}`\n"
            f"🎉 **Successfully Completed!**"
        )
    else:
        final = f"👑 **Bots Promoted:** `{promoted}/{total}`"
    await _edit(status, final)
    return promoted


# ── !add  — List 1 add ─────────────────────────────────────────
@bot.on(events.NewMessage(pattern=re.compile(r"^!add(?:\s|$)", re.I)))
async def cmd_add(event):
    if not _owner_only(event):
        return
    await _add_bots(event, BOT_USERNAMES, "Adding bots")


# ── !prmt  — List 1 promote ────────────────────────────────────
@bot.on(events.NewMessage(pattern=re.compile(r"^!prmt(?:\s|$)", re.I)))
async def cmd_prmt(event):
    if not _owner_only(event):
        return
    await _promote_bots(event, BOT_USERNAMES, "Promoting bots")


# ── !add1  — List 2 add ────────────────────────────────────────
@bot.on(events.NewMessage(pattern=re.compile(r"^!add1(?:\s|$)", re.I)))
async def cmd_add1(event):
    if not _owner_only(event):
        return
    await _add_bots(event, BOT_USERNAMES_1, "Adding bots (set 1)")


# ── !prmt1  — List 2 promote ───────────────────────────────────
@bot.on(events.NewMessage(pattern=re.compile(r"^!prmt1(?:\s|$)", re.I)))
async def cmd_prmt1(event):
    if not _owner_only(event):
        return
    await _promote_bots(event, BOT_USERNAMES_1, "Promoting bots (set 1)")


# ── !mixx  — random 5 from each list → add + auto promote ──────
@bot.on(events.NewMessage(pattern=re.compile(r"^!mixx(?:\s|$)", re.I)))
async def cmd_mixx(event):
    if not _owner_only(event):
        return

    n1 = min(5, len(BOT_USERNAMES))
    n2 = min(5, len(BOT_USERNAMES_1))
    pick1 = random.sample(BOT_USERNAMES, n1) if n1 else []
    pick2 = random.sample(BOT_USERNAMES_1, n2) if n2 else []
    mixed = pick1 + pick2
    random.shuffle(mixed)

    total = len(mixed)
    if not total:
        return await event.reply("Bot lists khali hain.")

    status = await event.reply(
        f"🎲 **Mixx starting...** `0/{total}`\n"
        f"📦 SetA: `{n1}` | SetB: `{n2}`"
    )

    added = 0
    promoted = 0

    for i, b in enumerate(mixed, 1):
        await _edit(
            status,
            f"🎲 **Mixx...** `{i}/{total}`\n"
            f"`{b}`\n"
            f"✅ Add: `{added}` | 👑 Promo: `{promoted}`"
        )
        # Add
        try:
            user = await bot.get_input_entity(b)
            await bot(InviteToChannelRequest(event.chat_id, [user]))
            added += 1
        except Exception as e:
            name = type(e).__name__
            if "UserAlreadyParticipant" in name or "already" in str(e).lower():
                added += 1
        await asyncio.sleep(0.2)

        # Auto promote
        try:
            user = await bot.get_input_entity(b)
            await bot(EditAdminRequest(event.chat_id, user, RIGHTS, rank="Admin"))
            promoted += 1
        except Exception:
            pass
        await asyncio.sleep(0.2)

    names = "\n".join(f"• `{b}`" for b in mixed)
    final = (
        f"🎲 **Mixx Done**\n"
        f"✅ Added: `{added}/{total}`\n"
        f"👑 Promoted: `{promoted}/{total}`\n"
        f"\n"
        f"**This round:**\n{names}"
    )
    if added == total and promoted == total:
        final += "\n\n🎉 **Successfully Completed!**"
    await _edit(status, final)


# ── !admin  — single user/bot admin ────────────────────────────
@bot.on(events.NewMessage(pattern=re.compile(r"^!admin(?:\s+(.+))?$", re.I)))
async def cmd_admin(event):
    if not _owner_only(event):
        return

    target = None
    arg = (event.pattern_match.group(1) or "").strip()

    if event.is_reply:
        try:
            r = await event.get_reply_message()
            if r and r.sender_id:
                target = r.sender_id
        except Exception:
            pass

    if target is None and arg:
        part = arg.split()[0].strip()
        try:
            if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
                target = int(part)
            else:
                ent = await bot.get_entity(part)
                target = int(ent.id)
        except Exception:
            return await event.reply("❌ User nahi mila.\nUsage: `!admin @username` ya `!admin USER_ID`")

    if target is None:
        return await event.reply(
            "❌ Usage:\n"
            "`!admin @username`\n"
            "`!admin USER_ID`\n"
            "ya kisi ke message pe reply karke `!admin`"
        )

    status = await event.reply(f"👑 **Promoting...** `{target}`")

    try:
        user = await bot.get_input_entity(target)
        await bot(EditAdminRequest(event.chat_id, user, RIGHTS, rank="Admin"))
        await _edit(
            status,
            f"✅ **Admin done**\n"
            f"🆔 `{target}`"
        )
    except Exception as e:
        await _edit(status, f"❌ Failed: `{type(e).__name__}`")


if __name__ == "__main__":
    logger.info("Commands: !add | !prmt | !add1 | !prmt1 | !mixx | !admin")
    bot.start()
    me = bot.loop.run_until_complete(bot.get_me())
    logger.info(f"Logged in as {me.first_name} | {me.id}")
    logger.info(f"List1: {len(BOT_USERNAMES)} | List2: {len(BOT_USERNAMES_1)}")
    bot.run_until_disconnected()
