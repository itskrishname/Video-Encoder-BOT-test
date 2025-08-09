import dns.resolver
import asyncio
import time
from pyrogram import idle
from pyrogram.errors import BadMsgNotification, FloodWait

from . import app, log

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

async def main():
    max_attempts = 1  # Only ONE attempt to avoid flood
    
    for attempt in range(max_attempts):
        try:
            print(f"🚀 Starting bot (attempt {attempt + 1})...")
            
            # Small delay before start
            await asyncio.sleep(2)
            
            await app.start()
            await app.send_message(chat_id=log, text='<b>✅ Video Encoder Bot Started!</b>')
            print("✅ Bot started successfully!")
            
            await idle()
            break
            
        except BadMsgNotification as e:
            print(f"❌ Time sync error: {e}")
            print("💡 Stopping to avoid flood. Please try again in 5-10 minutes.")
            break
            
        except FloodWait as e:
            print(f"❌ Flood wait: {e.x} seconds required")
            break
            
        except Exception as e:
            print(f"❌ Error: {e}")
            break
            
    try:
        if app.is_connected:
            await app.stop()
    except:
        pass

app.loop.run_until_complete(main())
