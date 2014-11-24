#1 origional size images, limited to 100 images per page
#1.1 Added links to the bottom of the page to progress through the galleries
#1.2 Resized the images to 200x200 and increased the images to 400 per page
#2 Added logic to chew through the XML files. The program will now go through all the g.sitemap.xxx.xml files. 
#   This makes it so it searches the entire server of xml filesfor images.
#2.1 Added additional logic so the system will read through all the files on each server. Application starts with 001 on s0001
#   continues through to 999 on s9999


import urllib
import urllib2
runP = "true"
moreS = "true"
moreF = "true"
numPix = 1
fileNum = 0
xplace1 = 0
xplace2 = 0
xplace3 = 1
sPlace1 = 0
sPlace2 = 0
sPlace3 = 0
sPlace4 = 1
response = urllib2.urlopen("http://s"+str(sPlace1)+str(sPlace2)+str(sPlace3)+str(sPlace4)+".photobucket.com/g.sitemap."+str(xplace1)+str(xplace2)+str(xplace3)+".xml")
http = response.read()
print "Starting at " + "http://s"+str(sPlace1)+str(sPlace2)+str(sPlace3)+str(sPlace4)+".photobucket.com/g.sitemap."+str(xplace1)+str(xplace2)+str(xplace3)+".xml"

myOutputFile = open("PBThumb.html", "wb")
#This writes the file as a recognizable HTML file. Load the files in your web browser to view the thumbs.
openingLines = ['\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"', '\n        "http://www.w3.org/TR/html4/loose.dtd">', '\n<html lang="en">', '\n', '\n<head>', '\n<meta http-equiv="content-type" content="text/html; charset=utf-8">', '\n<title>Photobucket Thumbs</title>', '\n</head>', '\n', '\n<body>']
closingLines =['\n</body>', '\n</html>']
myOutputFile.writelines(openingLines)
sPix = 1
#The system will continue running until a blank XML file is found or a server error is encountered. No error handling has been included in this to prevent a perpetual loop/
while moreS == "true":
    while moreF == "true":
        while runP == "true":
            if numPix >= 400:
                numPix = 0
                fileNum = fileNum + 1
                myOutputFile.writelines('\n<a href="PBThumb'+str(fileNum)+'.html">Next Page</a>')
                myOutputFile.writelines(closingLines)
                myOutputFile.close()
                myOutputFile = open("PBThumb"+str(fileNum)+".html", "wb")
                myOutputFile.writelines(openingLines)
            if http.find('image:loc') <= 0:
                runP = "false"
            startP = http.find('image:loc') + 10
            http = http[startP:]
            endP = http.find('image:loc') - 2
            hName = http[:endP]
            if hName != "":
                PBLink = '\n<a href="'+hName+'"><img src="'+hName+'" height="200" width="200"></a>' 
                myOutputFile.writelines(PBLink)
                sPix = sPix + 1
                numPix = numPix + 1
            http = http[endP+12:]
        #The following logic increments the XML files.
        if xplace3 == 9:
            xplace3 = 0
            if xplace2 == 9:
                xplace2 = 0
                if xplace1 == 9:
                    moreF = "false"
                else:
                    xplace1 = xplace1 + 1
            else:
                xplace2 = xplace2 + 1
        else:
            xplace3 = xplace3 + 1
        #This loads the next XML file and lets the user know what file is being loaded.
        response = urllib2.urlopen("http://s"+str(sPlace1)+str(sPlace2)+str(sPlace3)+str(sPlace4)+".photobucket.com/g.sitemap."+str(xplace1)+str(xplace2)+str(xplace3)+".xml")
        http = response.read()
        print sPix
        sPix = 0
        print "Moving to " + "http://s"+str(sPlace1)+str(sPlace2)+str(sPlace3)+str(sPlace4)+".photobucket.com/g.sitemap."+str(xplace1)+str(xplace2)+str(xplace3)+".xml"
        #Resetting the runP variable so the system will processall the files.
        runP = "true"
    if sPlace4 == 9:
        sPlace4 = 0
        if sPlace3 == 9:
            sPlace3 = 0
            if sPlace2 == 9:
                sPlace2 = 0
                if sPlace1 == 9:
                    moreS = "false"
                else:
                    sPlace1 = sPlace1 + 1
            else:
                sPlace2 = sPlace2 + 1
        else:
            sPlace3 = sPlace3 + 1
    else:
        sPlace4 = sPlace4 + 1
    xplace1 = 0
    xplace2 = 0
    xplace3 = 1
    moreF = "true"
    print "Moving to " + "http://s"+str(sPlace1)+str(sPlace2)+str(sPlace3)+str(sPlace4)+".photobucket.com/g.sitemap."+str(xplace1)+str(xplace2)+str(xplace3)+".xml"
    response = urllib2.urlopen("http://s"+str(sPlace1)+str(sPlace2)+str(sPlace3)+str(sPlace4)+".photobucket.com/g.sitemap."+str(xplace1)+str(xplace2)+str(xplace3)+".xml")
    http = response.read()
    

myOutputFile.writelines(closingLines)
myOutputFile.close()


print "Done"
