import dns.resolver
import asyncio
from pyrogram import idle
from pyrogram.errors import BadMsgNotification, FloodWait

from . import app, log

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

async def main():
    try:
        print("🚀 Starting bot (single attempt, flood safe)...")
        await asyncio.sleep(2)  # Delay avoids conflicts

        await app.start()
        await app.send_message(chat_id=log, text='<b>✅ Video Encoder Bot Started!</b>')
        print("✅ Bot started successfully!")
        await idle()
    except BadMsgNotification as e:
        print(f"❌ Time sync error: {e}")
        print("💡 This is usually a Heroku issue. Try again after a few minutes or consider migrating to Railway or VPS for reliable time sync.")
    except FloodWait as e:
        print(f"❌ Flood wait: You must wait {e.x} seconds ({e.x//60} min) before trying again.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            if app.is_connected:
                await app.stop()
        except:
            pass

app.loop.run_until_complete(main())
