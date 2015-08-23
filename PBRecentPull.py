import urllib
import urllib2
import os
import datetime
import sys


class Photopull():

    def __init__(self, update_comm, parent_running):

        # This is the opening and closing for the link HTML file.
        self.running = False
        self.last_file = None
        self.update_parent = update_comm
        self.parent_running = parent_running

        self.working_path = os.path.join(os.getcwd(), 'Working')
        self.completed_path = os.path.join(os.getcwd(), 'Completed')

        self.start_time = datetime.datetime.now()
        self.move_files(first_run=True)

        if not os.path.exists(self.completed_path):
            os.mkdir(self.completed_path)
        if not os.path.exists(self.working_path):
            os.mkdir(self.working_path)

    def mHtmLink(self, HtmLink):
        openingLines = ['\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"',
                        '\n        "http://www.w3.org/TR/html4/loose.dtd">', '\n<html lang="en">', '\n', '\n<head>']
        closingLines = ['\n<title>Photobucket Thumbs</title>', '\n</head>',
                        '\n', '\n<body>', '\nLoading your Library', '\n</body>', '\n</html>']
        if os.path.isfile(HtmLink) == False:
            myOutputFile = open(HtmLink, 'wb')
            myOutputFile.writelines(openingLines)
            myOutputFile.writelines(
                '\n<meta HTTP-EQUIV="REFRESH" content="0; url=' + self.bucket_link + '">')
            myOutputFile.writelines(closingLines)
            myOutputFile.close()

    def stop(self):
        self.running = False

    def move_files(self, timeout=60, first_run=False):
     # This checks the current time to verify if we need to
        # move over to a different folder
        now = datetime.datetime.now()
        if self.start_time + \
                datetime.timedelta(minutes=timeout) < now or first_run:
            self.start_time = now
            print "Moving files"

            # This will move the files from the working directory to the completed directory.
            # Duplicates throw an exception, and will be
            # deleted.
            for file in os.listdir(self.working_path):
                try:
                    os.rename(
                        os.path.join(self.working_path, file), os.path.join(self.completed_path, file))
                except:
                    os.remove(
                        os.path.join(self.working_path, file))

    def run(self):
        self.running = True

        while self.running:
            try:
                response = urllib2.urlopen(
                    "http://photobucket.com/recentuploads?page=1")
                http = response.read().replace("\/", "/")
                # This segment searches through the HTML we have read from Photobucket looking for images. If it doesnt find any more then it will
                # reread the page.
                while http.find("fullsizeUrl") >= 0 and self.running:
                    http = http[http.find("fullsizeUrl") + 14:]
                    end = http.find('","')
                    image_url = http[:end]
                    http = http[end + 3:]
                    if image_url != "":
                        # This starts the parsing of the image url so we can give it an origional descriptive name so we know if a duplicate
                        # has been found.
                        file_name = image_url[image_url.find('albums') + 7:].replace('/', '')
                        fold = []
                        fold.append(image_url[7:image_url.find(".")])
                        fold.append(image_url[image_url.find("albums") + 7:])
                        fold[1] = fold[1][:fold[1].find('/')]
                        fold.append(
                            image_url[image_url.find("albums") + 8 + len(fold[1]):])
                        fold[2] = fold[2][:fold[2].find('/')]
                        file_name = fold[0] + "--" + fold[2] + "--" + file_name
                        htmlName = fold[0] + "--" + fold[2] + ".html"

                        self.bucket_link = "http://" + \
                            fold[0] + ".photobucket.com/user/" + \
                            fold[2] + "/library/?view=recent&page=1"
                        self.move_files(timeout=20)
                        file_path = os.path.join(self.working_path, file_name)
                        filters = [
                            'ebay', 'facebook', 'snapesave', 'screenshot', 'snapchat']
                        if image_url[:4] == "http":
                            if not os.path.isfile(file_path):
                                image = urllib2.urlopen(image_url).read()
                                image_location = None
                                html_name = None
                                for spam in filters:
                                    if spam in file_path.lower():
                                        spam_folder = os.path.join(
                                            os.getcwd(), spam)
                                        if not os.path.exists(spam_folder):
                                            os.makedirs(spam_folder)
                                        image_location = os.path.join(
                                            spam_folder, file_name)
                                        html_name = os.path.join(
                                            spam_folder, htmlName)

                                    elif len(image) == 7883:
                                        tos = os.path.join(os.getcwd(), "TOS")
                                        if os.path.exists(tos) == False:
                                            os.makedirs(tos)
                                        image_location = os.path.join(
                                            tos, file_name)
                                        html_name = os.path.join(tos, htmlName)
                                    else:
                                        image_location = os.path.join(
                                            self.working_path, file_name)
                                        html_name = os.path.join(
                                            self.working_path, htmlName)
                                    try:
                                        with open(image_location, 'wb') as output:
                                            output.write(image)
                                        self.mHtmLink(html_name)
                                        if self.parent_running():
                                            self.update_parent(
                                                image_location, self.bucket_link)
                                    except IOError:
                                        print "IO Error"
            except urllib2.HTTPError:
                # This is a simple restart in case of any issues. I have come in to find it not running and when checking the log I got errors
                # from HTTP access to simple timeout errors. This catches them
                # all and restarts the application.
                print "404 Error encountered."


if __name__ == '__main__':
    app = Photopull()
    app.run()
