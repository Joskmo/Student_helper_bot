import json
import os
import yadisk
import aiofiles
import asyncio
import logging
import json
import datetime

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('YA_TOKEN')

BOT_FOLDER = "/bot"

client = yadisk.AsyncClient(token=TOKEN)


async def main():
    async with client:
        # Проверяет, валиден ли токен
        print(await client.check_token())


def object_to_dict(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if hasattr(obj, '__dict__'):
        data = {}
        for key, value in obj.__dict__.items():
            data[key] = object_to_dict(value)
        return data
    elif isinstance(obj, list):
        return [object_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: object_to_dict(value) for key, value in obj.items()}
    else:
        return obj


async def get_files():
    files = []
    folders = []
    async with yadisk.AsyncClient(token=TOKEN, session="aiohttp") as client:
        result = [i async for i in await client.listdir(BOT_FOLDER)]
        for item in result:
            if item['type'] == 'dir':
                folders.append(item['name'])
            elif item['type'] == 'file':
                files.append(item['name'])
            res = {'dir': folders, 'file': files}
        print(f'Папки: {folders}')
        print(f'Файлы: {files}')
        print(res)
        return res

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  #Только на дебаг
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
