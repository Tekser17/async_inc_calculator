import time
import coinmarketcapapi
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def get_site(session, url):
    async with session.get(url) as resp:
        s = await resp.text()
        return s


async def main() -> None:
    income = 0.0
    async with aiohttp.ClientSession() as session:
        accounts = [
            "mamont.near",
        ]
        tasks = []
        for acc in accounts:
            url = f"https://explorer.mainnet.near.org/accounts/{acc}"
            tasks.append(asyncio.ensure_future(get_site(session, url)))
        sites = await asyncio.gather(*tasks)
        for site in sites:
            soup = BeautifulSoup(site, features="html.parser")
            mydivs = soup.find_all("div",
                                   {"class": "c-CardCellText-eLcwWo ml-auto align-self-center col-md-12 col-auto"})
            span = mydivs[2].find("span")
            pre_text = span.text
            sum = ""
            for i in range(len(pre_text) - 2):
                sum += pre_text[i]
            income += float(sum)
    cmc = coinmarketcapapi.CoinMarketCapAPI('35c3c462-1a9e-4e73-8aae-9f4ee4a90072')
    data = cmc.cryptocurrency_quotes_latest(symbol='NEAR', convert='USD')
    course = data.data['NEAR'][0]['quote']['USD']['price']
    total_near = str(round(income, 2)) + ' Near'
    total_income = str(round(income * course, 2)) + '$'
    print(total_near)
    print(total_income)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))