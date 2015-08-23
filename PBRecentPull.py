import urllib
import urllib2
import os
import datetime
import sys



class Photopull():
    def __init__(self, update_comm, parent_running):

        #This is the opening and closing for the link HTML file.
        self.running = False
        self.last_file = None
        self.update_parent = update_comm
        self.parent_running = parent_running

        self.working_path = os.path.join(os.getcwd(), 'Working')
        self.completed_path = os.path.join(os.getcwd(), 'Completed')

        if not os.path.exists(self.completed_path):
            os.mkdir(self.completed_path)
        if not os.path.exists(self.working_path):
            os.mkdir(self.working_path)

    def mHtmLink(self, HtmLink):
        openingLines = ['\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"', '\n        "http://www.w3.org/TR/html4/loose.dtd">', '\n<html lang="en">', '\n', '\n<head>']
        closingLines = ['\n<title>Photobucket Thumbs</title>', '\n</head>', '\n', '\n<body>', '\nLoading your Library','\n</body>', '\n</html>']
        if os.path.isfile(HtmLink)== False:
            myOutputFile = open(HtmLink, 'wb')
            myOutputFile.writelines(openingLines)
            myOutputFile.writelines('\n<meta HTTP-EQUIV="REFRESH" content="0; url='+self.LibFull+'">')
            myOutputFile.writelines(closingLines)
            myOutputFile.close()

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        hTime = str(datetime.datetime.utcnow())
        hTime = hTime[:hTime.find(':')]
        rRepeat = True

        while self.running:
            # try:
                    response = urllib2.urlopen("http://photobucket.com/recentuploads?page=1")
                    http = response.read()
                    http = http.replace("\/", "/")
                    #This segment searches through the HTML we have read from Photobucket looking for images. If it doesnt find any more then it will
                    #reread the page.
                    while http.find("fullsizeUrl") >= 0 and self.running:
                        http = http[http.find("fullsizeUrl")+14:]
                        end = http.find('","')
                        hName = http[:end]
                        http = http[end+3:]
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
                            htmlName = folderN1+"--"+folderN3+".html"

                            self.LibFull = "http://"+folderN1+".photobucket.com/user/"+folderN3+"/library/?view=recent&page=1"
                            #This checks the current time to verify if we need to move over to a different folder
                            nTime = str(datetime.datetime.now())
                            nTime = nTime[:nTime.find(':')]
                            if nTime != hTime:
                                hTime = nTime
                                try:
                                    for file in os.listdir(self.working_path):
                                        os.rename(os.path.join(self.working_path, file), os.path.join(self.completed_path, file))
                                except:
                                    pass
                            fNameB = fName
                            fName = os.path.join(self.working_path, fName)

                            filters = ['ebay', 'facebook', 'snapesave', 'screenshot', 'snapchat']
                            if hName[:4] == "http":
                                # try:
                                    if not os.path.isfile(fName):
                                        imgData = urllib2.urlopen(hName).read()
                                        rName = fName.lower()
                                        #I added this name filter to help weed out spammy ebay listing pics. This catches a lot but not all.
                                        #To avoid accidentally deleting a win, they are sent to a specific Ebay folder)

                                        image_location = None
                                        html_name = None
                                        for spam in filters:
                                            if spam in rName:
                                                spam_folder = os.path.join(os.getcwd(), spam)
                                                if not os.path.exists(spam_folder):
                                                    os.makedirs(spam_folder)
                                                image_location = os.path.join(spam_folder, fNameB)
                                                html_name = os.path.join(spam_folder, htmlName)
                                                # print spam + ": " + fName

                                            elif len(imgData) == 7883:
                                                tos = os.path.join(os.getcwd(), "TOS")
                                                if os.path.exists(tos) == False:
                                                    os.makedirs(tos)
                                                image_location = os.path.join(tos, fNameB)
                                                html_name = os.path.join(tos, htmlName)
                                                # print "TOS: "+ fName
                                            else:
                                                image_location = os.path.join(self.working_path, fNameB)
                                                html_name = os.path.join(self.working_path, htmlName)
                                                # print fName
                                            with open(image_location, 'wb') as output:
                                                output.write(imgData)
                                            self.mHtmLink(html_name)
                                            if self.parent_running():
                                                print self.LibFull
                                                self.update_parent(image_location, self.LibFull)


                                # except:
                                    #This exception occurs when the file has been found in the folder. This prevents a flooding of duplicate images
                                    #or wasted time downloading one you already have.
                                    # print "Error"
            # except:
                    #This is a simple restart in case of any issues. I have come in to find it not running and when checking the log I got errors
                    #from HTTP access to simple timeout errors. This catches them all and restarts the application.
                    # print "Fatal Error, Restarting"



if __name__ == '__main__':
    app = Photopull()
    app.run()
