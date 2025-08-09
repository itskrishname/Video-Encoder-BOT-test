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

async def safe_start_bot():
    """Safely start bot with connection state check"""
    try:
        # Check if already connected
        if app.is_connected:
            print("⚠️ Client already connected, disconnecting first...")
            await app.stop()
            await asyncio.sleep(2)
        
        print("🚀 Starting bot...")
        await app.start()
        
        # Success message भेजें
        try:
            bot_info = await app.get_me()
            success_msg = f'<b>✅ Bot Started Successfully! @{bot_info.username}</b>'
            await app.send_message(chat_id=log, text=success_msg)
        except Exception as e:
            print(f"Could not send start message: {e}")
        
        print("✅ Bot started successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return False

async def main():
    """Main function with proper connection handling"""
    try:
        print("🎯 Initializing Video Encoder Bot...")
        
        # Start bot safely
        if await safe_start_bot():
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
            if app.is_connected:
                await app.stop()
                print("✅ Bot stopped cleanly!")
        except:
            pass

if __name__ == "__main__":
    app.loop.run_until_complete(main())
