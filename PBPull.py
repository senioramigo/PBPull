import urllib
import urllib2
runP = "true"
numPix = 0
fileNum = 0
#This is the URL of the XML page. Replace it with the URL you need.
response = urllib2.urlopen("http://s1236.photobucket.com/g.sitemap.001.xml")
http = response.read()

myOutputFile = open("PBThumb.html", "wb")
openingLines = ['\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"', '\n        "http://www.w3.org/TR/html4/loose.dtd">', '\n<html lang="en">', '\n', '\n<head>', '\n<meta http-equiv="content-type" content="text/html; charset=utf-8">', '\n<title>Photobucket Thumbs</title>', '\n</head>', '\n', '\n<body>']
closingLines =['\n</body>', '\n</html>']
myOutputFile.writelines(openingLines)

while runP == "true":
    numPix = numPix + 1
    if numPix >= 200:
        numPix = 0
        fileNum = fileNum + 1
        myOutputFile.writelines('\n<a href="PBThumb"'+str(fileNum)+'".html">Next Page</a>')
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
    PBLink = '\n<a href="'+hName+'"><img src="'+hName+'" style="width:100;height:100"></a>'
    myOutputFile.writelines(PBLink)
    http = http[endP+12:]

myOutputFile.writelines(closingLines)
myOutputFile.close()


print "Done"
