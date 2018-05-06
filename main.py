
import requests
from pprint import pprint
from bs4 import BeautifulSoup, Tag

class Hero(object):
    table_body = None
    matches = []
    def __init__(self, hero_name):
        self.name = hero_name
        self.table_body = self.fetch_hero_counter_table()
        self.table_body_to_list()

    def fetch_hero_counter_table(self):
        r = requests.get(
            'https://www.dotabuff.com/heroes/{0}/counters'.format(self.name), 
            headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
        )
        soup = BeautifulSoup(r.content, "html.parser")
        for s in soup.select("section > header"):
            if s.text.lower() == "matchups":
                el = s
                break

        return el.find_parent().find('tbody')


    def table_body_to_list(self):
        for row in self.table_body.find_all('tr'):
            columns = row.find_all('td')
            
            self.matches.append({
                    "hero_name": columns[0].attrs["data-value"].lower().replace(" ", "_", -1),
                    "disadvantage": columns[2].attrs["data-value"],
                    "win_percentage": columns[3].attrs["data-value"],
                    "matches_played": columns[4].attrs["data-value"],
            })
    
    def top_five_counter_heroes(self):
        return self.matches[0:5]

    def bottom_five_counter_heroes(self):
        return self.matches[-5:]



h = Hero("faceless-void")

print("TOP 5 COUNTERED BY:")
pprint(h.top_five_counter_heroes())
print("")

print("TOP 5 COUNTERS:")
pprint(h.bottom_five_counter_heroes())