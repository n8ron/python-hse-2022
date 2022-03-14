import argparse
import asyncio
import os

import aiohttp
import aiofiles

URL = "https://picsum.photos/400"


async def load_img(filename, session):
    async with session.get(URL) as response:
        if response.status == 200:
            async with aiofiles.open(filename, mode='wb') as f:
                await f.write(await response.read())


async def main(n_images: int, path_to_dir: str):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(load_img(f"{path_to_dir}/image_number_{i + 1}.png", session) for i in range(n_images)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('n_images', type=int)
    parser.add_argument('path_to_dir')
    args = parser.parse_args()
    if not os.path.exists(args.path_to_dir):
        os.makedirs(args.path_to_dir)
    asyncio.run(main(args.n_images, args.path_to_dir))
