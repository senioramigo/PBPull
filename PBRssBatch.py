import urllib
import urllib2
import os
import datetime
from easygui import *
import re
import json


        
        
#This value currently never changes so that it can run indefinitly.
rRepeat = True
#This is the opening and closing for the link HTML file.
jsonFile = os.path.join(os.getcwd(), "saved feeds.txt")
if os.path.isfile(jsonFile) == False:
    newRssName = raw_input("Bucket Name? ")
    hold = {u'feeds':[
        {u'link': u'http://feed856.photobucket.com/albums/f1348/'+newRssName+'/account.rss', u'bucketName':u''+newRssName+''}
    ]}
    jsonRead = open(jsonFile, 'w')
    jsonRead.write('{"feeds":[')
    jsonRead.write('\n    {"link":"http://feed856.photobucket.com/albums/f1348/'+newRssName+'/account.rss","bucketName":"'+newRssName+'"}')
    jsonRead.write('\n]}')
    jsonRead.close()
    jsonRead = open(jsonFile, 'rb')
    hold = jsonRead.read()
    jsonRead.close()
else:
    jsonRead = open(jsonFile, 'rb')
    hold = jsonRead.read()
    jsonRead.close()
jSon = json.loads(hold)
newRss = raw_input("New Feed? ")
if newRss[0] == "Y" or newRss[0] == "y":
    repeat = "Yes"
    while repeat == "Yes":
        newRssName = raw_input("Bucket Name: ")
        if newRssName[0] == "n" or newRssName[0] == "N":
            if len(newRssName) >= 2:
                repeat = "No"
        nfNum = 0
        hold = jSon['feeds']
        rssValid = True
        for i in hold:
            if hold[nfNum]['bucketName'] == newRssName:
                rssValid = False
        if rssValid == True:
            newRssItem = {u'link': u'http://feed856.photobucket.com/albums/f1348/'+newRssName+'/account.rss', u'bucketName':u''+newRssName+''}
            jSon['feeds'].append(newRssItem)
            moreRss = raw_input("More? ")
            if moreRss[0] == "N" or moreRss[0] == "n":
                repeat = "No"
                jsonRead = open(jsonFile, 'w')
                hold = jSon['feeds']
                jsonRead.write('{"feeds":[')
                nfNum = 0
                for i in hold:
                    wrHold = str(hold[nfNum])
                    wrHold = wrHold.replace(" ", "")
                    wrHold = wrHold.replace("u'", '"')
                    wrHold = wrHold.replace("'", '"')
                    if nfNum < len(hold) and nfNum != 0:
                        jsonRead.write(",")
                    jsonRead.write("\n    "+wrHold)
                    nfNum = nfNum+1
                jsonRead.write('\n]}')
                jsonRead.close()
        else:
            print "Bucket already exists."

hold = jSon['feeds']
while rRepeat == True:
    jLink = 0
    for i in hold:
        try:
            #This is the URL for the recents page. In theory you can use any page from recents but it doesnt matter that much.
            response = urllib2.urlopen(hold[jLink]['link'])
            http = response.read()
            results = re.findall('" url="(.*)" />', http)
            #This segment searches through the HTML we have read from Photobucket looking for images. If it doesnt find any more then it will
            #reread the page.
            Zero = 0
            for i in results:
                hName = results[Zero]
                if hName != "":
                    #This starts the parsing of the image url so we can give it an origional descriptive name so we know if a duplicate
                    #has been found.
                    startA = hName.find('albums') 
                    fName = hName[startA+7:]
                    fName = fName.replace('/', '')
                    folderN1 = hName[7:hName.find(".")]
                    folderN2 = hName[hName.find("albums")+7:]
                    folderN2 = folderN2[:folderN2.find('/')]
                    folderN3 = hName[hName.find("albums")+8+len(folderN2):]
                    folderN3 = folderN3[:folderN3.find('/')]
                    fName = folderN1+"--"+folderN3+"--"+fName
                    fPath = os.path.join(os.getcwd(), hold[jLink]['bucketName'])
                    if os.path.exists(fPath) == False:
                        os.makedirs(fPath)
                    fNameB = fName
                    fName = os.path.join(fPath, fName)
                    if hName[:4] == "http":
                        try:
                            if os.path.isfile(fName) != True:
                                imgData = urllib2.urlopen(hName).read()
                                rName = fName.lower()
                                output = open(fName, 'wb')
                                output.write(imgData)
                                output.close()
                                print fName
                            else:
                                print "Duplicate Image"
                                print fName
                        except:
                            #This exception occurs when the file has been found in the folder. This prevents a flooding of duplicate images
                            #or wasted time downloading one you already have.
                            print "Duplicate Image"
                Zero = Zero+1
        except Exception as e:
            #This is a simple restart in case of any issues. I have come in to find it not running and when checking the log I got errors
            #from HTTP access to simple timeout errors. This catches them all and restarts the application.
            print "Fatal Error, Restarting"
            print e
        jLink = jLink + 1
            
    
