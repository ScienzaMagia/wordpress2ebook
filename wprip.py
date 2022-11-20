import requests
import re
from requests.auth import HTTPBasicAuth 
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


class Wprip:

    def main(self):

        stories = open("wpstories.txt", "r")
        
        
        for line in stories:
            
            story = line.strip()
            titleIndex = story.find(",")
 
            title = story[0:titleIndex]
            url = story[titleIndex+1:len(story)]
            tagIndex = url.find("/tag/") #Determines if the story is a direct link to a single chapter or a tagged list of chapters.
            i = 1
            
            
            if tagIndex == -1:
                doc = open("Rips/"+title +".html", "w") 
                print(title)            
                doc.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>"+title+"</h1>")
                chapterRaw = requests.get(url)
                chapterSoup = BeautifulSoup(chapterRaw.content, 'html.parser')
                chapterTitle = chapterSoup.find("h1", class_ = "entry-title").string
                doc.write("\n<h2>" + chapterTitle + "</h2>\n")
                entryContent = chapterSoup.find("div", class_ = "entry-content")
                chapterText = entryContent.find_all("p")
                for s in chapterText:
                    doc.write(str(s)+"\n")
                #print(chapterText)
                doc.write("\n</body>\n</html>")
                doc.close()           
                print ("\nFinished " + title)

            
            else:
                baseUrl = url.replace("?order=asc", "")
                chapters = list()
                pageNum = 1
                url = baseUrl + "page" + str(pageNum)
               
                while url != None:
                
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    is404 = soup.find("section", class_="error-404 not-found")
           
                    if is404 != None:
                        url = None
                    else:
                        ch = soup.find_all("h1", class_="entry-title")
                        for c in ch:
                            chapters.insert(0,c.a["href"])
                        pageNum = pageNum + 1
                        url = baseUrl + "page"+str(pageNum)

                doc = open("Rips/"+title +".html", "w") 
                print(title)            
                doc.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>"+title+"</h1>")
             
                for c in chapters:
                    chapterRaw = requests.get(c)
                    chapterSoup = BeautifulSoup(chapterRaw.content, 'html.parser')
                    chapterTitle = chapterSoup.find("h1", class_ = "entry-title").string
                    doc.write("\n<h2>" + chapterTitle + "</h2>\n")
                    entryContent = chapterSoup.find("div", class_ = "entry-content")
                    chapterText = entryContent.find_all("p")
                    for s in chapterText:
                        doc.write(str(s)+"\n")
                    #print(chapterText)
                doc.write("\n</body>\n</html>")
                doc.close()           
                print ("\nFinished " + title)
        stories.close()





if __name__ == '__main__':
    Wprip().main()
    