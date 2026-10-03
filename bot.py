#!/usr/bin/env python3

# ============================================================
# 📞 NUMINFO TELEGRAM BOT
# 🔐 Safe Phone Number Metadata Bot
# ============================================================

import os
import re

import phonenumbers
from phonenumbers import carrier, geocoder, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ============================================================
# 🔐 CONFIGURATION
# ============================================================

# Hosting platform (Railway) में variable का नाम:
# BOT_TOKEN
BOT_TOKEN = os.getenv("8967548495:AAGt5iQEjHhidU8uBroFGJ_dT9J7r6L2Bws")
https://number-info-bot-omega.vercel.app/

# ============================================================
# 🎨 STYLISH BOX
# ============================================================

def stylish_box(title: str, icon: str = "🔍") -> str:
    return (
        "╔══════════════════════════════════════╗\n"
        f"║  {icon}  {title}\n"
        "╚══════════════════════════════════════╝"
    )


# ============================================================
# 📞 PHONE INFORMATION
# ============================================================

def get_phone_info(phone: str) -> str:

    try:
        parsed = phonenumbers.parse(phone, None)

        if not phonenumbers.is_valid_number(parsed):
            return "❌ Invalid phone number."

        formatted = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )

        country = (
            geocoder.country_name_for_number(parsed, "en")
            or "Unknown"
        )

        region = (
            geocoder.description_for_number(parsed, "en")
            or "Unknown"
        )

        carrier_name = (
            carrier.name_for_number(parsed, "en")
            or "Unknown"
        )

        zones = timezone.time_zones_for_number(parsed)

        timezone_text = (
            ", ".join(zones)
            if zones
            else "Unknown"
        )

        return (
            f"{stylish_box('PHONE INFORMATION', '📞')}\n"
            "║\n"
            f"├─ 📱 Number   : `{formatted}`\n"
            f"├─ 🌍 Country  : `{country}`\n"
            f"├─ 📍 Region   : `{region}`\n"
            f"├─ 📶 Carrier  : `{carrier_name}`\n"
            f"├─ ⏰ Timezone : `{timezone_text}`\n"
            "├─ ✅ Valid    : `Yes`\n"
            "║\n"
            "╚══════════════════════════════════════╝\n"
            "🔐 Basic phone metadata only."
        )

    except Exception:
        return (
            "❌ *Unable to process this number.*\n\n"
            "Please check the number and try again."
        )


# ============================================================
# 🚀 /START
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    welcome = (
        f"{stylish_box('WELCOME', '🚀')}\n"
        "║\n"
        "├─ 🤖 *NumInfo Bot*\n"
        "├─ 📞 Phone Number Information\n"
        "├─ 🔐 Privacy-Friendly Lookup\n"
        "║\n"
        "├─ 📌 *Command:*\n"
        "│  `/numinfo +919876543210`\n"
        "║\n"
        "└─ ⚡ Ready to use!"
    )

    await update.message.reply_text(
        welcome,
        parse_mode="Markdown"
    )


# ============================================================
# 📱 /NUMINFO
# ============================================================

async def numinfo_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.args:
        await update.message.reply_text(
            "❌ *Phone number missing!*\n\n"
            "📱 Example:\n"
            "`/numinfo +919876543210`",
            parse_mode="Markdown"
        )
        return

    phone = context.args[0].strip()

    # 10–15 digits, optionally beginning with +
    if not re.fullmatch(r"\+?[0-9]{10,15}", phone):
        await update.message.reply_text(
            "⚠️ *Invalid number!*\n\n"
            "Please enter 10–15 digits.\n\n"
            "Example:\n"
            "`+919876543210`",
            parse_mode="Markdown"
        )
        return

    # Add India country code for a normal 10-digit number
    if not phone.startswith("+") and len(phone) == 10:
        phone = "+91" + phone

    processing = await update.message.reply_text(
        f"🔎 *Checking number...*\n\n"
        f"📱 `{phone}`\n\n"
        "⏳ Please wait...",
        parse_mode="Markdown"
    )

    result = get_phone_info(phone)

    await processing.edit_text(
        result,
        parse_mode="Markdown"
    )


# ============================================================
# 🚀 MAIN
# ============================================================

def main():

    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN is not configured.")
        print("➡️ Add BOT_TOKEN in your hosting Environment Variables.")
        return

    print("==========================================")
    print("📞 NUMINFO TELEGRAM BOT")
    print("==========================================")
    print("✅ Configuration loaded")
    print("🤖 Starting bot...")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("numinfo", numinfo_cmd)
    )

    print("🟢 BOT IS ONLINE!")
    print("==========================================")

    application.run_polling()


# ============================================================
# ▶️ START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()