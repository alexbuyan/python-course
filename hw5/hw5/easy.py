import asyncio
from random import randint
from time import time

import aiohttp


async def download_one_image(image_url, session, out_dir, image_id):
    response = await session.get(image_url)
    data = await response.read()
    with open(f'{out_dir}/image_{image_id}.png', 'wb') as file:
        file.write(data)


async def download_images(image_urls, out_dir):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(download_one_image(url, session, out_dir, image_id) for url, image_id in image_urls))

def easy_solution(images_n, out_dir):
    web_url = 'https://picsum.photos/'
    image_urls = [(f'{web_url}/{str(randint(100, 500))}/{str(randint(100, 500))}', image_id) for image_id in
                  range(1, images_n + 1)]
    start_time = time()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(download_images(image_urls, out_dir))
    finally:
        loop.close()

    download_time = time() - start_time
    print(f'Download of {images_n} images to {out_dir} directory took {download_time}')
