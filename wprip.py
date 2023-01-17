import requests
import re
import os
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
            
            #Processes a single-chapter story
            if tagIndex == -1: 
                
                       
                
                chapterRaw = requests.get(url)
                chapterSoup = BeautifulSoup(chapterRaw.content, 'html.parser')
                chapterTitle = chapterSoup.find("h1", class_ = "entry-title").string
                author = chapterSoup.find("span", class_ = "author vcard").a.string
                print("\n"+title + " by " + author) 
                doc = open("Rips/"+title + " - " + author + ".html", "w") 
                doc.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>"+title+ " by " + author + "</h1>")
                doc.write("\n<h2>" + chapterTitle + "</h2>\n")
                entryContent = chapterSoup.find("div", class_ = "entry-content")
                chapterText = entryContent.find_all("p")
                for s in chapterText:
                    doc.write(str(s)+"\n")
                #print(chapterText)
                doc.write("\n</body>\n</html>")
                doc.close()           
                print ("Finished " + title)

            #Processes a multi-chapter story
            else:
                baseUrl = url.replace("?order=asc", "")
                if baseUrl[-1] != '/':
                    baseUrl = baseUrl + '/'
                chapters = list()
                pageNum = 1
                author = ""
                url = baseUrl + "page" + str(pageNum)
               
                while url != None:
                
                    page = requests.get(url)
                    #print (url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    is404 = soup.find("section", class_="error-404 not-found")
           
                    if is404 != None:
                        #print("404")
                        url = None
                    else:
                        ch = soup.find_all("h1", class_="entry-title")
                        for c in ch:
                            chapters.insert(0,c.a["href"])
                        pageNum = pageNum + 1
                        author = soup.find("span", class_ = "author vcard").a.string
                        url = baseUrl + "page"+str(pageNum)

                doc = open("Rips/"+title + " - " + author + ".html", "w") 
                print("\n"+title + " by " + author)            
                print (str(len(chapters)) + " chapters")
                doc.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>"+title+ " by " + author + "</h1>")
             
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
                print ("Finished " + title)
        stories.close()





if __name__ == '__main__':
    Wprip().main()
    