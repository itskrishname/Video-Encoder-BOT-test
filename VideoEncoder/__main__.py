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

async def force_time_sync_start():
    """Time sync issue के लिए advanced retry logic"""
    max_retries = 8
    base_delay = 5
    
    for attempt in range(max_retries):
        try:
            print(f"🚀 Starting bot... (Attempt {attempt + 1}/{max_retries})")
            
            # Advanced time sync check
            current_time = datetime.now(timezone.utc)
            print(f"🕐 Current UTC: {current_time}")
            print(f"🕐 Timestamp: {int(current_time.timestamp())}")
            
            # Try different approaches for each attempt
            if attempt == 0:
                # Normal start
                await app.start()
            elif attempt == 1:
                # Wait a bit and try
                await asyncio.sleep(3)
                await app.start()
            elif attempt == 2:
                # Force disconnect and reconnect
                try:
                    if app.is_connected:
                        await app.stop()
                    await asyncio.sleep(5)
                except:
                    pass
                await app.start()
            else:
                # Progressive delay increase
                delay = base_delay * (attempt - 2)
                print(f"⏳ Waiting {delay} seconds for time sync...")
                await asyncio.sleep(delay)
                await app.start()
            
            # Success message
            try:
                bot_info = await app.get_me()
                success_msg = f'<b>✅ Bot Started Successfully! @{bot_info.username}</b>\n<b>🕐 Attempt:</b> {attempt + 1}\n<b>🕐 Time:</b> {datetime.now(timezone.utc)}'
                await app.send_message(chat_id=log, text=success_msg)
            except Exception as e:
                print(f"Could not send start message: {e}")
            
            print("✅ Bot started successfully!")
            return True
            
        except BadMsgNotification as e:
            print(f"⚠️ Time sync error (Attempt {attempt + 1}): {e}")
            
            # Clean up session files on time sync error
            if attempt > 2:  # After 3rd attempt
                try:
                    import os
                    import glob
                    session_files = glob.glob("VideoEncoder/*.session*")
                    for file in session_files:
                        try:
                            os.remove(file)
                            print(f"🗑️ Cleaned session file: {file}")
                        except:
                            pass
                except:
                    pass
            
            if attempt < max_retries - 1:
                delay = base_delay + (attempt * 2)  # Progressive delay
                print(f"⏳ Waiting {delay} seconds before retry...")
                await asyncio.sleep(delay)
            else:
                print("❌ Failed to start after all retries!")
                return False
                
        except Exception as e:
            print(f"❌ Unexpected error (Attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(base_delay)
            else:
                return False
    
    return False

async def main():
    """Main function with advanced time sync handling"""
    try:
        print("🎯 Initializing Video Encoder Bot with Time Sync Fix...")
        
        # Start bot with time sync retry logic
        if await force_time_sync_start():
            print("🎯 Bot is running... Press Ctrl+C to stop")
            await idle()
        else:
            print("❌ Bot failed to start after all attempts!")
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
