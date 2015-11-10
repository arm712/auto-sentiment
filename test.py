from ingestion.database import twitterDB
from wrangling.wrangler import Wrangler
from collections import Counter
from nltk import bigrams
import pandas as pd
import xlwt

db = twitterDB()
w = Wrangler()
count_all = Counter()

db.load_coll('103115 01:09:07')
tweets = db.load_tweets()
df = pd.DataFrame(tweets)
df_unique = df[-df.duplicated('text')]

tweets = df_unique['text']
print(tweets.size)

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Text")
sheet1.write(0, 1, "Positive/Negative")

i = 1
for t in tweets:
    sheet1.write(i, 0, t)
    i += 1


book.save("trial.xls")