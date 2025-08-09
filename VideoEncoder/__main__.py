import dns.resolver
import asyncio
import sys
import logging
import time
from datetime import datetime, timezone
from pyrogram import idle
from pyrogram.errors import BadMsgNotification, FloodWait, AuthKeyUnregistered

from . import app, log

# DNS configuration
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

async def safe_start_with_flood_protection():
    """FLOOD_WAIT protection के साथ safe start"""
    try:
        print("🚀 Starting bot with flood protection...")
        
        # Simple start - no retries to avoid flood
        await app.start()
        
        # Success message
        try:
            bot_info = await app.get_me()
            success_msg = f'<b>✅ Bot Started Successfully! @{bot_info.username}</b>\n<b>🕐 Time:</b> {datetime.now(timezone.utc)}'
            await app.send_message(chat_id=log, text=success_msg)
        except Exception as e:
            print(f"Could not send start message: {e}")
        
        print("✅ Bot started successfully!")
        return True
        
    except FloodWait as e:
        print(f"🚨 FLOOD_WAIT: Need to wait {e.x} seconds ({e.x//60} minutes)")
        print(f"💡 Bot will auto-restart after {e.x//60} minutes. Please wait...")
        
        # Wait for the flood period
        await asyncio.sleep(e.x)
        
        # Try once more after waiting
        try:
            await app.start()
            print("✅ Bot started successfully after flood wait!")
            return True
        except Exception as retry_error:
            print(f"❌ Failed even after flood wait: {retry_error}")
            return False
            
    except BadMsgNotification as e:
        print(f"⚠️ Time sync error: {e}")
        print("🔄 Trying once more after 10 seconds...")
        await asyncio.sleep(10)
        try:
            await app.start()
            return True
        except:
            print("❌ Time sync issue persists")
            return False
            
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return False

async def main():
    """Main function with flood protection"""
    try:
        print("🎯 Initializing Video Encoder Bot...")
        
        # Start bot with flood protection
        if await safe_start_with_flood_protection():
            print("🎯 Bot is running... Press Ctrl+C to stop")
            await idle()
        else:
            print("❌ Bot failed to start!")
            print("💡 If you see FLOOD_WAIT, please wait and try again later")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user!")
    except Exception as e:
        print(f"❌ Fatal error in main: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)
    finally:
        try:
            if app.is_connected:
                await app.stop()
                print("✅ Bot stopped cleanly!")
        except:
            pass

if __name__ == "__main__":
    app.loop.run_until_complete(main())
