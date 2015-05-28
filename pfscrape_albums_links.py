from bs4 import BeautifulSoup
import requests
import csv
import unicodedata
unicodedata.normalize('NFC', u'a\u0308').encode('mac-roman')


###
###get all links and albums reviewed by pitchfork
###will exit when no more albums exist on scrape
###use links to scrape individual album websites



f=open("albums.csv", 'w', newline='')
spamwriter=csv.writer(f, delimiter=",")
spamwriter.writerow(["h1", "Link", "h2", "h3", "h4", "bestnew", "page", "order"])

for page in range (0, 1000) :
    order=0
    page1=str(page)
    r  = requests.get("http://pitchfork.com/reviews/albums/"+page1)
    data = r.text
    soup = BeautifulSoup(data)      
    print("Currently scraping: http://pitchfork.com/reviews/albums/"+page1)

    ##Find if page is not found and exit
    findpage = soup.head.meta.title(text=True)[0]
    print(findpage)
    ##Exit if no more albums
    if findpage=="Page Not Found":
        print('scrape is over, exiting at page '+page1)
        break
    ##Grab albums 
    if findpage!="Page Not Found":
        albums2 = soup.find('div', attrs={'id': 'main'}).find('ul', attrs = {'class':'object-grid'}).contents
        for x in range(0, len(albums2)):
            #prints alternative rows, so do the following
            if (int(x/2)!=x/2):
                albums = soup.find('div', attrs={'id': 'main'}).find('ul', attrs = {'class':'object-grid'}).contents[x].ul.contents
                for y in range(0, len(albums)):
                   if (int(y/2)!=y/2):
                        h1=albums[y].find('a').h1(text=True)[0]
                        Link=albums[y].find('a', href=True)['href']
                        h3=albums[y].find('a').h3(text=True)[0]
                        h2=albums[y].find('a').h2(text=True)[0]
                        h4=albums[y].find('a').h4(text=True)[0]
                        bestnew=albums[y].find('a').find('span', attrs={'class': 'p4ktag'})
                        order=order+1
                        ##Try and except is used because some albums have weird characters and I can't figure out how to export them to csv
                        try:
                            spamwriter.writerow([h1, Link, h2, h3, h4, bestnew, page1, order])
                        except:
                            print("Currently scraping: http://pitchfork.com/reviews/albums/"+page1 + "Is currently not exporting")
                            spamwriter.writerow(["NONE", Link, "NONE", "NONE", "NONE", "NONE", page1, order])
    f.close()
print("Done")
#
