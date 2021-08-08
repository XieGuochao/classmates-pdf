import pdfGenerator
from time import time
import logging
from pdfGenerator import setMainContents, generatePDF
import json

# Format of received and sent contents
# mainReceivedContents = [{
#     "name": "Tester",
#     "content": "步现走力院但育总圆周加十角，说就空火效机没度件任和世，广办花隶动号不油放引派。而平么现这极府但万酸华，一真及说消团再日议，现改极什就学上想实。第马革图集特金一，半结际力两转年，解医利吼清传。红大一代音合长在，干且据月以第音矿，极两事内林场。素照自明情反世，每几整老系热，年O名白米。",
#     "date": "2021.07.01",
#     "sent": False
# }]
# mainSentContents = [{
#     "name": "Tester",
#     "content": "步现走力院但育总圆周加十角，说就空火效机没度件任和世，广办花隶动号不油放引派。而平么现这极府但万酸华，一真及说消团再日议，现改极什就学上想实。第马革图集特金一，半结际力两转年，解医利吼清传。红大一代音合长在，干且据月以第音矿，极两事内林场。素照自明情反世，每几整老系热，年O名白米。",
#     "date": "2021.07.01",
#     "sent": True
# }]

def loadContents(sentFileName, receivedFileName):
    return loadContentFromFile(sentFileName), loadContentFromFile(receivedFileName)

def loadContentFromFile(fileName):
    return json.loads(open(fileName, "r").read())

def loadUsername(fileName):
    return open(fileName, "r").read()

def main_handler(sentContents, receivedContents, username):
    hashString = hash(time())
    logging.debug(username)
    setMainContents(receivedContents, sentContents)
    logging.critical("Generating ...")
    generatePDF(hashString, username)

    logging.critical("Generate PDF: out/classmates-{}.pdf {}".format(hashString, username))

    return "classmates-{}.pdf".format(hashString), username

sentContents, receivedContents = loadContents("in/sent.json", "in/received.json")
username = loadUsername("in/username.txt")
print(main_handler(sentContents, receivedContents, username))
print("done")
