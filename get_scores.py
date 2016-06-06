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

# Extract the team names and com
team1 = [x.string.strip() for x in soup.find_all("div", class_='ply tright name')]
team2 = [x.string.strip() for x in soup.find_all("div", class_='ply name')]

# Combine the data into a list
data = [ team1, team2, list(X), list(Y)]

# Create and decorate a dataframe
df = pd.DataFrame(data).T
df.columns = ("team1", "team2", "score1", "score2")
df = df.set_index(["team1", "team2"]).sort_index()
print(df)
