import os
import json
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.errors import SessionPasswordNeededError
import asyncio
from dotenv import load_dotenv
import pandas as pd

# ----------------------
# Instructions:
# 1. Register your app at https://my.telegram.org to get API_ID and API_HASH
# 2. Add your API credentials to a .env file (API_ID, API_HASH, PHONE)
# 3. Add your target channel usernames to the CHANNELS list
# ----------------------
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_NAME = 'amharic_ecommerce'
CHANNELS = [
    '@ZemenExpress',
    '@Leyueqa',
    '@Shewabrand',
    '@qnashcom',
    '@aradabrand2'
]  # Add at least 5 channels

OUTPUT_DIR = '../../data/raw/'
MEDIA_DIR = os.path.join(OUTPUT_DIR, 'media')
RAW_DATA_PATH = os.path.join(OUTPUT_DIR, 'raw_messages.jsonl')
CSV_DATA_PATH = os.path.join(OUTPUT_DIR, 'raw_messages.csv')

os.makedirs(MEDIA_DIR, exist_ok=True)

MAX_MESSAGES_PER_CHANNEL = 500  # Set your max limit here

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def download_media(message, media_dir):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            file_path = await message.download_media(file=media_dir)
            return file_path
        elif isinstance(message.media, MessageMediaDocument):
            file_path = await message.download_media(file=media_dir)
            return file_path
    return None

async def fetch_and_save_messages():
    await client.start()
    if await client.is_user_authorized() is False:
        try:
            await client.send_code_request(os.getenv('PHONE'))
            await client.sign_in(phone=input('Re-enter your phone number: '), code=input('Enter the code you received: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Two-step verification enabled. Enter your password: '))

    all_messages = []
    with open(RAW_DATA_PATH, 'w', encoding='utf-8') as outfile:
        for channel in CHANNELS:
            print(f'Fetching messages from {channel} (max {MAX_MESSAGES_PER_CHANNEL})...')
            count = 0
            async for message in client.iter_messages(channel, limit=MAX_MESSAGES_PER_CHANNEL):
                msg_data = {
                    'channel': channel,
                    'message_id': message.id,
                    'date': str(message.date),
                    'sender_id': message.sender_id,
                    'text': message.text,
                    'media_type': None,
                    'media_path': None,
                }
                if message.media:
                    media_path = await download_media(message, MEDIA_DIR)
                    msg_data['media_type'] = type(message.media).__name__
                    msg_data['media_path'] = media_path
                outfile.write(json.dumps(msg_data, ensure_ascii=False) + '\n')
                all_messages.append(msg_data)
                count += 1
                if count >= MAX_MESSAGES_PER_CHANNEL:
                    break
    print(f'All messages saved to {RAW_DATA_PATH}')

    # Save to CSV
    df = pd.DataFrame(all_messages)
    df.to_csv(CSV_DATA_PATH, index=False, encoding='utf-8-sig')
    print(f'All messages also saved to {CSV_DATA_PATH}')

if __name__ == '__main__':
    asyncio.run(fetch_and_save_messages())
