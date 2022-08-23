import pandas as pd
import numpy as np
import main


import os
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
        return result_dict
def filter_rows(row):
    cells = row.find_all("td")
    return len(cells)==35



def get_patch():
        region_dict = {
                "CN": "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LPL+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run=",
                "KR": "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCK+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run=",
                # "LEC":"https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LEC+2022+Summer+Playoffs&PBH%5Btextonly%5D=Yes&_run=",
                "LCS":"https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCS+2022+Championship&PBH%5Btextonly%5D=Yes&_run=",
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
                for i in range(len(rows)):
                    rows[i]["region"] = to_crawl_key

                all_rows += rows

        df = pd.DataFrame(all_rows)
        df.to_csv("out.csv", index=False)




from jinja2 import Environment, FileSystemLoader
from flask import Flask


app = Flask(__name__)
@app.route('/patch/patch/patch')
def patch():
    get_patch()
    return "1"

@app.route('/<champion>')
def output_single(champion):
    df = pd.read_csv("out.csv")
    print(df.columns)
    patch = df
    games = len(patch)

    def ban_rate():
        frames = [patch["bb1"], patch["bb2"], patch["bb3"], patch["rb1"], patch["rb2"], patch["rb3"]]
        result = pd.concat(frames)
        return result

    def blue_bans():
        frames = [patch["bb1"], patch["bb2"], patch["bb3"]]
        result = pd.concat(frames)
        return result

    def red_bans():
        frames = [patch["rb1"], patch["rb2"], patch["rb3"]]
        result = pd.concat(frames)
        return result

    def pick_games():
        frames = [patch["bp1"], patch["bp2"], patch["bp3"], patch["bp4"], patch["bp5"], patch["rp1"], patch["rp2"],
                  patch["rp3"], patch["rp4"], patch["rp5"]]
        result = pd.concat(frames)
        return result

    def win_games():
        wins = patch[patch["winner"] == 1]
        frames = [wins["bp1"], wins["bp2"], wins["bp3"], wins["bp4"], wins["bp5"]]
        result1 = pd.concat(frames)
        wins = patch[patch["winner"] == 2]
        frames = [wins["rp1"], wins["rp2"], wins["rp3"], wins["rp4"], wins["rp5"]]
        result2 = pd.concat(frames)
        return (pd.concat(([result1, result2])))

    def blue_first_bans():
        frames = [patch["bb1"]]
        result = pd.concat(frames)
        return result

    def red_first_bans():
        frames = [patch["rb1"]]
        result = pd.concat(frames)
        return result

    def win_rate():
        frames = [patch["r1"]]
        result = pd.concat(frames)
        return result

    # print(red_first_ban_rate().value_counts().rename_axis('champion').reset_index(name=''))
    pick_games = pick_games().value_counts().rename_axis('champion').reset_index(name='picks')
    win_games = win_games().value_counts().rename_axis('champion').reset_index(name='wins')
    blue_bans = blue_bans().value_counts().rename_axis('champion').reset_index(name='blue_bans')
    red_bans = red_bans().value_counts().rename_axis('champion').reset_index(name='red_bans')
    bans = ban_rate().value_counts().rename_axis('champion').reset_index(name='bans')
    merge1 = pd.merge(pick_games, win_games, on='champion', how='left')
    print(merge1)
    merge1["pick_rate"] = merge1["picks"].map(lambda x: str(round(100 * (x / games))) + "%")
    merge1["wins"] = merge1["wins"].apply(lambda x: 0 if x != x else x)
    merge1["win_rate"] = merge1.apply(lambda x: str(round(100 * (x["wins"] / x["picks"]))) + "%", axis=1)
    merge2 = pd.merge(merge1, blue_bans, on='champion', how='left')
    merge2["blue_bans"] = merge2["blue_bans"].apply(lambda x: 0 if x != x else x)
    merge2["blue_ban_rate"] = merge2["blue_bans"].map(lambda x: str(round(100 * (x / games))) + "%")
    merge3 = pd.merge(merge2, red_bans, on='champion', how='left')
    merge3["red_bans"] = merge3["red_bans"].apply(lambda x: 0 if x != x else x)
    merge3["red_ban_rate"] = merge3["red_bans"].map(lambda x: str(round(100 * (x / games))) + "%")
    merge4 = pd.merge(merge3, bans, on='champion', how='left')
    merge4["bans"] = merge4["bans"].apply(lambda x: 0 if x != x else x)
    merge4["ban_rate"] = merge4["bans"].map(lambda x: str(round(100 * (x / games))) + "%")
    champion = champion.lower().strip()
    with open("champion.html") as f:
        template_str = f.read()
    template = Environment(loader=FileSystemLoader("")).from_string(template_str)

    dfs = [df[df.bp1.str.lower() == champion.lower()],
           df[df.bp2.str.lower() == champion.lower()],
           df[df.bp3.str.lower() == champion.lower()],
           df[df.bp4.str.lower() == champion.lower()],
           df[df.bp5.str.lower() == champion.lower()],
           df[df.rp1.str.lower() == champion.lower()],
           df[df.rp2.str.lower() == champion.lower()],
           df[df.rp3.str.lower() == champion.lower()],
           df[df.rp4.str.lower() == champion.lower()],
           df[df.rp5.str.lower() == champion.lower()]]
    result = pd.concat(dfs)
    result["winner"] = result["winner"].map(lambda x: "Blue" if x == 1 else "Red")
    context = {
        "champion_name": champion,
        "vod_df": result,
        "stat_row": merge4[merge4.champion.str.lower() == champion.lower()].to_dict('records')[0]
    }
    html_str = template.render(context)
    return  html_str

@app.route('/<champion1>/<champion2>')
def output_single2(champion1, champion2):
    df = pd.read_csv("out.csv")
    champion1 = champion1.lower().strip()
    champion2 = champion2.lower().strip()
    with open("champion_vs.html") as f:
        template_str = f.read()
    template = Environment(loader=FileSystemLoader("")).from_string(template_str)

    dfs = [df[df.bp1.str.lower() == champion1.lower()],
           df[df.bp2.str.lower() == champion1.lower()],
           df[df.bp3.str.lower() == champion1.lower()],
           df[df.bp4.str.lower() == champion1.lower()],
           df[df.bp5.str.lower() == champion1.lower()]]
    result = pd.concat(dfs)
    results = [
               result[result.rp1.str.lower() == champion2.lower()],
               result[result.rp2.str.lower() == champion2.lower()],
               result[result.rp3.str.lower() == champion2.lower()],
               result[result.rp4.str.lower() == champion2.lower()],
               result[result.rp5.str.lower() == champion2.lower()]]
    result2 = pd.concat(results)
    result2["bluechamp"] = champion1
    result2["redchamp"] = champion2
    blue_games = len(result2)
    blue_win_games = len(result2[result2["winner"] == 1])
    results3  = [df[df.rp1.str.lower() == champion1.lower()],
           df[df.rp2.str.lower() == champion1.lower()],
           df[df.rp3.str.lower() == champion1.lower()],
           df[df.rp4.str.lower() == champion1.lower()],
           df[df.rp5.str.lower() == champion1.lower()]]
    result3 = pd.concat(results3)

    results4 = [result3[result3.bp1.str.lower() == champion2.lower()],
    result3[result3.bp2.str.lower() == champion2.lower()],
    result3[result3.bp3.str.lower() == champion2.lower()],
    result3[result3.bp4.str.lower() == champion2.lower()],
    result3[result3.bp5.str.lower() == champion2.lower()]]

    result4 = pd.concat(results4)
    result4["bluechamp"] = champion2
    result4["redchamp"] = champion1
    red_games = len(result4)
    red_win_games = len(result4[result4["winner"] == 2])
    champ1_blue_win_rate = ((blue_win_games ) / (blue_games))
    champ2_blue_win_rate = 1 - champ1_blue_win_rate
    champ1_red_win_rate = ((red_win_games) / (red_games))
    champ2_red_win_rate = 1 - champ1_red_win_rate
    champ1_win_rate = ((blue_win_games+red_win_games)/(blue_games+red_games))
    champ2_win_rate = 1 - champ1_win_rate
    result = pd.concat([result2,result4])
    result["winner"] = result["winner"].map(lambda x: "Blue" if x == 1 else "Red")

    context = {
        "champion_name": champion1,
        "champion_name_2": champion2,
        "vod_df": result,
        "champ1_win_rate": champ1_win_rate,
        "champ2_win_rate": champ2_win_rate,
        "champ1_blue_win_rate": champ1_blue_win_rate,
        "champ2_blue_win_rate": champ2_blue_win_rate,
        "champ1_red_win_rate": champ1_red_win_rate,
        "champ2_red_win_rate": champ2_red_win_rate,
    }
    print(context)
    html_str = template.render(context)
    return  html_str

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
