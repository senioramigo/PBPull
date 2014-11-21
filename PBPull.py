#1 origional size images, limited to 100 images per page
#1.1 Added links to the bottom of the page to progress through the galleries
#1.2 Resized the images to 200x200 and increased the images to 400 per page
#2 Added logic to chew through the XML files. The program will now go through all the g.sitemap.xxx.xml files. 
#   This makes it so it searches the entire server of xml filesfor images.


import urllib
import urllib2
runP = "true"
numPix = 0
fileNum = 0
response = urllib2.urlopen("http://s1236.photobucket.com/g.sitemap.001.xml")
http = response.read()
place1 = 0
place2 = 0
place3 = 1

myOutputFile = open("PBThumb.html", "wb")
#This writes the file as a recognizable HTML file. Load the files in your web browser to view the thumbs.
openingLines = ['\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"', '\n        "http://www.w3.org/TR/html4/loose.dtd">', '\n<html lang="en">', '\n', '\n<head>', '\n<meta http-equiv="content-type" content="text/html; charset=utf-8">', '\n<title>Photobucket Thumbs</title>', '\n</head>', '\n', '\n<body>']
closingLines =['\n</body>', '\n</html>']
myOutputFile.writelines(openingLines)

#The system will continue running until a blank XML file is found or a server error is encountered. No error handling has been included in this to prevent a perpetual loop/
while http != "":
    while runP == "true":
        numPix = numPix + 1
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
        PBLink = '\n<a href="'+hName+'"><img src="'+hName+'" height="200" width="200"></a>'
        myOutputFile.writelines(PBLink)
        http = http[endP+12:]
    #The following logic increments the XML files.
    if place3 == 9:
        place3 = 0
        if place2 == 9:
            place2 = 0
            place1 = place1 + 1
        else:
            place2 = place2 + 1
    else:
        place3 = place3 + 1
    #This loads the next XML file and lets the user know what file is being loaded.
    response = urllib2.urlopen("http://s1236.photobucket.com/g.sitemap."+str(place1)+str(place2)+str(place3)+".xml")
    http = response.read()
    print "Moving to " + "http://s1236.photobucket.com/g.sitemap."+str(place1)+str(place2)+str(place3)+".xml"
    #Resetting the runP variable so the system will processall the files.
    runP = "true"




myOutputFile.writelines(closingLines)
myOutputFile.close()


print "Done"
