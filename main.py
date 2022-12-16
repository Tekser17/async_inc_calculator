import time
import coinmarketcapapi
import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from pymongo import MongoClient


async def get_site(session, url):
    async with session.get(url) as resp:
        s = await resp.text()
        return s


async def main() -> None:
    income = 0.0
    async with aiohttp.ClientSession() as session:
        accounts = [
            "tgritsaev.crowdforces.near",  # 1й
            "dyominov.crowdforces.near",  #2й
            "god_of_code.crowdforces.near",  #3й
            "tintin122.crowdforces.near",  #4й
            "vyshniak_ivan.crowdforces.near",  # 5й
            "tekser15.near",
            "60e4d771034dadae8a754aadfd9ad0dfd6e94774360b549a502302a0000b8f49",
            "ba8ec64b357e447523b34383f037e390683df567025a0da231af39b105bcc10f",
        ]
        tasks = []
        for acc in accounts:
            url = f"https://explorer.mainnet.near.org/accounts/{acc}"
            tasks.append(asyncio.ensure_future(get_site(session, url)))
        sites = await asyncio.gather(*tasks)
        ac = 0
        for site in sites:
            soup = BeautifulSoup(site, features="html.parser")
            #mydivs = soup.find_all("div",
            #                       {"class": "c-CardCellText-eLcwWo ml-auto align-self-center col-md-12 col-auto"})
            mydivs = soup.select("#__next > div.c-AppWrapper-eIdCBM > div:nth-child(4) > div.container > div > div:nth-child(2) > div.col-md-4.col-12 > div > div > div > div.c-CardCellText-eLcwWo.ml-auto.align-self-center.col-md-12.col-auto > span")
            try:
                pre_text = mydivs[0].text
                print(accounts[ac], pre_text)
                sum = ""
                for i in range(len(pre_text) - 2):
                    sum += pre_text[i]
                income += float(sum)
            except Exception as ex:
                print("Ошибка в аккаунте", accounts[ac])
            ac += 1
    cluster = MongoClient("mongodb+srv://Tekser15:<pass>@cluster0.tc9nrxs.mongodb.net/Inventory?retryWrites=true&w=majority")
    mongo = cluster["Nikis-train"]
    db = mongo["Income"]
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    cmc = coinmarketcapapi.CoinMarketCapAPI('35c3c462-1a9e-4e73-8aae-9f4ee4a90072')
    data = cmc.cryptocurrency_quotes_latest(symbol='NEAR', convert='USD')
    course = data.data['NEAR'][0]['quote']['USD']['price']
    total_near = str(round(income, 2)) + ' Near'
    total_income = str(round(income * course, 2)) + '$'
    print(total_near, round(course, 2), '$')
    print(total_income)
    f = [total_near, total_income]
    dates = [str(day) + '.' + str(month) + '.' + str(year)]
    data = {'data': dates, 'name': 'Tekser15', 'income': f}
    db.find_one_and_delete({'data': dates})
    db.insert_one(data)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
