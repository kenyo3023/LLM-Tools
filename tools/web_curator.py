import json
import trafilatura
from concurrent.futures import ThreadPoolExecutor, as_completed

class WebCurator:

    # def __init__(self):
    prune_xpath = [
        '//div[contains(@class, "ad")]',  # 使用類名包含 "ad"
        '//div[contains(@class, "advertisement")]',  # 其他可能的類名
        '//aside',  # 側邊欄一般包含廣告
        '//footer',  # 頁腳中有時候也會有廣告
    ]

    @classmethod
    def _extract(cls, url:str, **kwargs) -> dict:
        downloaded = trafilatura.fetch_url(url)

        extracted_content =  trafilatura.extract(
            downloaded,
            output_format='json',
            include_tables=True,
            include_images=False,
            include_formatting=True,
            include_links=False,
            with_metadata=True,
            # only_with_metadata='title',
            prune_xpath=cls.prune_xpath,
        )
        if extracted_content:
            extracted_content = json.loads(extracted_content)
        return extracted_content


    # @classmethod
    # def extract(cls, urls:str | list[str], **kwargs) -> list[dict]:
    #     if isinstance(urls, str):
    #         urls = [urls]
    #     extracted_contents = [cls._extract(url, **kwargs) for url in urls]
    #     return extracted_contents


    @classmethod
    def extract(cls, urls: str | list[str], max_workers:int=5, **kwargs) -> list[dict]:
        if isinstance(urls, str):
            urls = [urls]

        extracted_contents = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(cls._extract, url, **kwargs): url for url in urls}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    extracted_contents.append(data)
                except Exception as exc:
                    print(f'Error occurred while extracting {url}: {exc}')

        return extracted_contents


import asyncio

class AysncWebCurator:

    # def __init__(self):
    prune_xpath = [
        '//div[contains(@class, "ad")]',  # 使用類名包含 "ad"
        '//div[contains(@class, "advertisement")]',  # 其他可能的類名
        '//aside',  # 側邊欄一般包含廣告
        '//footer',  # 頁腳中有時候也會有廣告
    ]

    @classmethod
    async def _extract(cls, url:str, **kwargs) -> dict:
        downloaded = trafilatura.fetch_url(url)

        extracted_content =  trafilatura.extract(
            downloaded,
            output_format='json',
            include_tables=True,
            include_images=False,
            include_formatting=True,
            include_links=False,
            with_metadata=True,
            # only_with_metadata='title',
            prune_xpath=cls.prune_xpath,
        )
        if extracted_content:
            extracted_content = json.loads(extracted_content)
        return extracted_content

    @classmethod
    async def extract(cls, urls:str | list[str], **kwargs) -> list[dict]:
        if isinstance(urls, str):
            urls = [urls]
        tasks = [cls._extract(url, **kwargs) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
