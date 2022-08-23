import requests
from bs4 import BeautifulSoup
import pandas as pd
def process_comman(string):
        split = string.split(",")
        return split[0],split[1].replace(" ", "")

def row_coverted(row):
        cells = row.find_all("td")
        result_dict = {}
        result_dict["vod"] = cells[-1].string
        result_dict["rr5"] = cells[-3].string.lower().strip()
        result_dict["rr4"] = cells[-4].string.lower().strip()
        result_dict["rr3"] = cells[-5].string.lower().strip()
        result_dict["rr2"] = cells[-6].string.lower().strip()
        result_dict["rr1"] = cells[-7].string.lower().strip()
        result_dict["br5"] = cells[-8].string.lower().strip()
        result_dict["br4"] = cells[-9].string.lower().strip()
        result_dict["br3"] = cells[-10].string.lower().strip()
        result_dict["br2"] = cells[-11].string.lower().strip()
        result_dict["br1"] = cells[-12].string.lower().strip()
        result_dict["rp5"] = cells[-13].string.lower().strip()
        result_dict["bp4"], result_dict["bp5"] = process_comman(cells[-14].string.lower().strip())
        result_dict["rp4"] = cells[-15].string.lower().strip()
        result_dict["bb5"] = cells[-16].string.lower().strip()
        result_dict["rb5"] = cells[-17].string.lower().strip()
        result_dict["bb4"] = cells[-18].string.lower().strip()
        result_dict["rb4"] = cells[-19].string.lower().strip()
        result_dict["rp3"] = cells[-20].string.lower().strip()
        result_dict["bp2"], result_dict["bp3"] = process_comman(cells[-21].string.lower().strip())
        result_dict["rp1"], result_dict["rp2"] = process_comman(cells[-22].string.lower().strip())
        result_dict["bp1"] = cells[-23].string.lower().strip()
        result_dict["rb3"] = cells[-24].string.lower().strip()
        result_dict["bb3"] = cells[-25].string.lower().strip()
        result_dict["rb2"] = cells[-26].string.lower().strip()
        result_dict["bb2"] = cells[-27].string.lower().strip()
        result_dict["rb1"] = cells[-28].string.lower().strip()
        result_dict["bb1"] = cells[-29].string.lower().strip()
        result_dict["patch"] = cells[-30].string
        result_dict["winner"] = cells[-31].string
        result_dict["score"] = cells[-32].string
        result_dict["red"] = cells[-33].string
        result_dict["blue"] = cells[-34].string
        result_dict["phase"] = cells[-35].string
        result_dict["region"] = to_crawl_key
        return result_dict
def filter_rows(row):
    cells = row.find_all("td")
    return len(cells)==35



def main():
        region_dict = {
                "CN": "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LPL+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run=",
                "KR": "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCK+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run=",
                # "LEC":"https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LEC+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run=",
                # "NA":"https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCS+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run=",
                "PCS": "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=PCS+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run="
        }

        all_rows = []
        for to_crawl_key in region_dict:
                url = region_dict[to_crawl_key]
                x = requests.get(url)

                soup = BeautifulSoup(x.content, 'html.parser')
                rows = soup.find("table", {"id": "pbh-table"}).find("tbody").find_all("tr")

                rows = list(filter(filter_rows, rows))
                rows = list(map(row_coverted, rows))
                all_rows += rows

        df = pd.DataFrame(all_rows)
        df.to_csv("out.csv", index=False)


