import bs4
import urllib
import pandas as pd

# Hope these good folks don't change the URL and the format!
URL = "http://www.livescore.com/soccer/copa-america/"
html = urllib.request.urlopen(URL).read()
soup = bs4.BeautifulSoup(html, 'html5lib')

# Extact the scores
X, _, Y = zip(*[(list(x.strings)[1].split() if len(list(x.strings)) > 1 
                 else 3 * [float("nan")]) for x 
                in list(soup.find_all("div", class_='sco'))])
X = pd.Series(X).replace("?", float("nan")).astype(float)
Y = pd.Series(Y).replace("?", float("nan")).astype(float)

# Extract the team names and com
team1 = pd.Series([x.string.strip() for x in 
                   soup.find_all("div", class_='ply tright name')])
team2 = pd.Series([x.string.strip() for x in 
                   soup.find_all("div", class_='ply name')])

# Create and decorate a dataframe
df = pd.DataFrame({"team1" : team1, "team2" : team2, 
                   "score1" : X, "score2" : Y})

df = df.set_index(["team1", "team2"]).sort_index()
df["diff"] = df["score1"] - df["score2"]

print(df.dropna().astype(int))
