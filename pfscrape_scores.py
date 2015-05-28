from bs4 import BeautifulSoup
import requests
import csv
import unicodedata
unicodedata.normalize('NFC', u'a\u0308').encode('mac-roman')


###
###get the scores and other data for pitchfork albums from CSV made in step 1
        
f=open("albums_step3.csv", newline="")
spamreader = csv.DictReader(f, delimiter=",")

f2=open("real_scores3.csv", 'w', newline='')
spamwriter=csv.writer(f2, delimiter=",")
spamwriter.writerow(["Link", "recordcomp", "score", "page", "order"])
           
for row in spamreader:
    print(row["Link"])
    r  = requests.get("http://pitchfork.com"+row["Link"])
    data = r.text
    soup = BeautifulSoup(data)
    album_score = soup.find('div', attrs={'id': 'main'}).find('ul', attrs = {'class':'review-meta'}).li.find('div', attrs={'class': 'info'}).contents
    print (album_score[5](text=True))
    print (album_score[9](text=True))
    link=row["Link"]
    comp=album_score[5](text=True)
    score=album_score[9](text=True)
    page=row["page"]
    order=row["order"]
    ##at least one album doesn't have a score
    try:
        spamwriter.writerow([link, comp[0], score[0], page, order])
    except:
        spamwriter.writerow([link, "NONE", "NONE", page, order])
f2.close()
print("done scraping scores")
##for x in range(0, len(album_score)):
##    if (int(x/2)!=x/2):
##        print(album_score[x](text=True))
##

##random one won't work
##Various Artists	/reviews/albums/1365-no-more-shall-we-part/	No More Shall We Part	by Brad Pritchett	1-Apr-01

