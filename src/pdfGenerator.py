from io import StringIO
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.tables import Table
from typing import List
from pdfUtils import MultiFontParagraph, getSampleStyleSheet, ParagraphStyle, TA_JUSTIFY, Spacer
from pdfUtils import PageBreak, SimpleDocTemplate, A4, A6
from pdfUtils import Canvas, mm, TableOfContents

from PyPDF2 import PdfFileMerger, PdfFileReader
import os

# Usage:
# setMainContents(receivedContents, sentContents)
# generatePDF(fileHashInput: str, userName: str)

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="Justify",
        alignment=TA_JUSTIFY
    )
)
styles.add(
    ParagraphStyle(
        "main",
        fontName="SS",
        fontSize=8,
        firstLineIndent=16
    )
)

styles.add(
    ParagraphStyle(
        "main-no-indent",
        fontName="SS",
        fontSize=8,
        firstLineIndent=0
    )
)

styles.add(
    ParagraphStyle(
        "main-no-indent-bold",
        fontName="SS-Bold",
        fontSize=8,
        firstLineIndent=0
    )
)


def DefaultParaGraph(content: str, style=styles["main"]):
    return MultiFontParagraph(
        content,
        style,
        [
            ('SS', 'ttf/NotoSansHans-Regular.ttf'),
            ("Segoe", "ttf/Segoe UI.ttf"),
            ("Emoji", "ttf/Symbola_hint.ttf")
        ]
    )


def fromTextToParaGraph(text: str, style=styles["main"]):
    return DefaultParaGraph(text, style)


L_MARGIN = 10*mm
T_MARGIN = 10*mm
contentPageCnt = 0
mainCounter = 0

# Format of received and sent contents
mainReceivedContents = [{
    "name": "Tester",
    "content": "步现走力院但育总圆周加十角，说就空火效机没度件任和世，广办花隶动号不油放引派。而平么现这极府但万酸华，一真及说消团再日议，现改极什就学上想实。第马革图集特金一，半结际力两转年，解医利吼清传。红大一代音合长在，干且据月以第音矿，极两事内林场。素照自明情反世，每几整老系热，年O名白米。",
    "date": "2021.07.01",
    "sent": False
}]
mainSentContents = [{
    "name": "Tester",
    "content": "步现走力院但育总圆周加十角，说就空火效机没度件任和世，广办花隶动号不油放引派。而平么现这极府但万酸华，一真及说消团再日议，现改极什就学上想实。第马革图集特金一，半结际力两转年，解医利吼清传。红大一代音合长在，干且据月以第音矿，极两事内林场。素照自明情反世，每几整老系热，年O名白米。",
    "date": "2021.07.01",
    "sent": True
}]

mainContents = mainReceivedContents + mainSentContents
fileHash = "01"


def setMainContents(receivedContents, sentContents):
    global mainReceivedContents, mainSentContents, mainContents, mainCounter
    mainReceivedContents = list(receivedContents)
    mainSentContents = list(sentContents)
    mainContents = mainReceivedContents + mainSentContents
    mainCounter = 0


def mainPageHandler(canvas: Canvas, doc):
    global mainCounter
    """
    Add the page number
    """
    canvas.setFillColorRGB(234/256, 228/256, 255/256)
    canvas.rect(0, 0, A6[0], A6[1],
                stroke=0,
                fill=1)

    canvas.setFillColorRGB(255/256, 255/256, 255/256)
    canvas.rect(L_MARGIN, 1*T_MARGIN, A6[0] -
                2*L_MARGIN, A6[1] - 2*T_MARGIN,
                stroke=0,
                fill=1)

    page_num = canvas.getPageNumber()
    canvas.setFont("SS", 8)
    canvas.setFillColor("black")
    text = "%s" % page_num
    canvas.drawRightString(A6[0]-5*mm, 5*mm, text)

    # Draw date
    date = mainContents[mainCounter]["date"]
    canvas.drawString(16*mm, 12*mm, str(date))

    mainCounter += 1


def frontPage(canvas: Canvas, userName: str):
    canvas.setFillColorRGB(234/256, 228/256, 255/256)
    canvas.rect(0, 0, A4[0], A4[1],
                stroke=0,
                fill=1)

    canvas.setFillColor("black")
    canvas.setFont("SS", 10)
    canvas.drawString(16*mm, 24*mm, "姓名：{}".format(userName))
    canvas.drawString(16*mm, 20*mm, "年份：2021")

    canvas.setFont("SS-Bold", 24, 50)
    SPACING = 10*mm
    text = "毕业纪念册"
    for i in range(len(text)):
        canvas.drawString(A6[0]-15*mm, 120*mm-i*SPACING, text[i])

    # canvas.setFont("SS", 8)
    # canvas.drawString(A6[0]-40*mm, 5*mm, "APARTSA 毕业纪念册项目组")


def mainPage(name: str, content: str, dateStr: str, sent: bool):
    nameParagraph = None
    if sent:
        nameParagraph = fromTextToParaGraph(
            "致 {}：".format(name), style=styles["main-no-indent-bold"])
    else:
        nameParagraph = fromTextToParaGraph(
            "来自 {} 的赠言：".format(name), style=styles["main-no-indent-bold"])

    contentParagraphs = []
    for paragraph in content.split("\n"):
        contentParagraphs.append(fromTextToParaGraph(paragraph))

    # contentParagraph = fromTextToParaGraph(content)

    dateParagraph = fromTextToParaGraph(
        dateStr, style=styles["main-no-indent"])
    paragraphs = [
        nameParagraph,
        Spacer(1, 8)] + contentParagraphs + [
        PageBreak()
    ]

    return paragraphs


def getContentSize(numOfNotes: int):
    return (numOfNotes-1) // 15 + 1


def mainDoc():
    mainDocs = SimpleDocTemplate("/tmp/main-{}.pdf".format(fileHash),
                                 pagesize=A6,
                                 rightMargin=12*mm,
                                 leftMargin=12*mm,
                                 topMargin=12*mm,
                                 bottomMargin=12*mm,
                                 )
    pages = []
    for page in mainReceivedContents:
        pages = pages + mainPage(page["name"],
                                 page["content"],
                                 page["date"],
                                 False
                                 )
    for page in mainSentContents:
        pages = pages + mainPage(page["name"],
                                 page["content"],
                                 page["date"],
                                 True
                                 )
    mainDocs.build(pages, onFirstPage=mainPageHandler,
                   onLaterPages=mainPageHandler)


def contentPage(canvas: Canvas, nameList, sent: bool, baseIndex=1):
    page = []
    title = "我收到的赠言" if not sent else "我写的赠言"
    line = "来自 {} 的赠言" if not sent else "致 {}"

    canvas.setFont("SS", 9)
    for i, name in enumerate(nameList):
        if i % 15 == 0:
            canvas.setFillColorRGB(234/256, 228/256, 255/256)
            canvas.rect(0, A6[1]-30*mm, A6[0], 30*mm,
                        stroke=0,
                        fill=1)
            canvas.setFillColor("black")
            canvas.setFont("SS-Bold", 16)
            canvas.drawString(10*mm, A6[1] - 20*mm, title)
            canvas.setFont("SS", 9)

        SPACING = 7*mm
        height = A6[1] - (36*mm + (i % 15)*SPACING)
        canvas.drawString(10*mm, height, line.format(name))
        canvas.drawRightString(A6[0] - 10*mm, height, str(i+baseIndex))
        # canvas.linkURL('#page={}'.format(contentPageCnt+i+baseIndex), (10*mm, 10*mm, 100*mm,
                    #    100*mm), relative=1, thickness=1)

        if (i+1) % 15 == 0:
            canvas.showPage()
    return page


def firstAndContents(receivedNames, sentNames, userName):
    global contentPageCnt
    canvas = Canvas("/tmp/first-{}.pdf".format(fileHash), pagesize=A6)
    frontPage(canvas, userName)
    canvas.showPage()


    contentPageCnt = (len(receivedNames)-1)/15 + (len(sentNames)-1)/15 + 2
    contentPage(canvas, receivedNames, False)
    canvas.showPage()
    contentPage(canvas, sentNames, True, len(receivedNames) + 1)
    canvas.save()


def merge(firstFileName, secondFileName, lastPageFileName):
    merger = PdfFileMerger()
    merger.append(PdfFileReader(open(firstFileName, "rb")))
    merger.append(PdfFileReader(open(secondFileName, "rb")))
    merger.append(PdfFileReader(open(lastPageFileName, "rb")))

    merger.write("out/classmates-{}.pdf".format(fileHash))


def generatePDF(fileHashInput: str, userName: str):
    global fileHash
    fileHash = str(fileHashInput)

    firstAndContents([
        content["name"] for content in mainReceivedContents
    ], [
        content["name"] for content in mainSentContents
    ], userName)
    mainDoc()
    merge("/tmp/first-{}.pdf".format(fileHash), "/tmp/main-{}.pdf".format(fileHash), "src/lastPage.pdf")
    os.remove("/tmp/first-{}.pdf".format(fileHash))
    os.remove("/tmp/main-{}.pdf".format(fileHash))