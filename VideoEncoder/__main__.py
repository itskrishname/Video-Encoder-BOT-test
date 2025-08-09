# VideoEncoder - a telegram bot for compressing/encoding videos in h264/h265 format.
# Copyright (c) 2021 WeebTime/VideoEncoder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import dns.resolver
import asyncio
import sys
import logging
from pyrogram import idle
from pyrogram.errors import BadMsgNotification, FloodWait, AuthKeyUnregistered

from . import app, log

# DNS configuration
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

async def start_bot_with_retry():
    """Bot start करने के लिए retry logic के साथ"""
    max_retries = 5
    retry_delay = 10
    
    for attempt in range(max_retries):
        try:
            print(f"🚀 Starting bot... (Attempt {attempt + 1}/{max_retries})")
            await app.start()
            
            # Success message भेजें
            try:
                bot_info = await app.get_me()
                success_msg = f'<b>✅ Bot Started Successfully! @{bot_info.username}</b>\n<b>🕐 Attempt:</b> {attempt + 1}'
                await app.send_message(chat_id=log, text=success_msg)
            except Exception as e:
                print(f"Could not send start message: {e}")
            
            print("✅ Bot started successfully!")
            return True
            
        except BadMsgNotification as e:
            print(f"⚠️ Time synchronization error (Attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Waiting {retry_delay} seconds before retry...")
                await asyncio.sleep(retry_delay)
                retry_delay += 5  # Increase delay for next attempt
            else:
                print("❌ Failed to start after all retries!")
                return False
                
        except FloodWait as e:
            print(f"⏳ FloodWait: Waiting {e.x} seconds...")
            await asyncio.sleep(e.x)
            
        except AuthKeyUnregistered:
            print("❌ Session expired! Please delete session file and restart.")
            return False
            
        except Exception as e:
            print(f"❌ Unexpected error (Attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay += 5
            else:
                print("❌ Failed to start after all retries!")
                return False
    
    return False

async def main():
    """Main function with proper error handling"""
    try:
        # Bot start करें retry logic के साथ
        if await start_bot_with_retry():
            print("🎯 Bot is running... Press Ctrl+C to stop")
            await idle()
        else:
            print("❌ Bot failed to start!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user!")
    except Exception as e:
        print(f"❌ Fatal error in main: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)
    finally:
        try:
            await app.stop()
            print("✅ Bot stopped cleanly!")
        except:
            pass

if __name__ == "__main__":
    app.loop.run_until_complete(main())
