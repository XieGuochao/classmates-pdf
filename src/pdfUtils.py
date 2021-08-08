from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4, A6
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.platypus.tableofcontents import TableOfContents


class MultiFontParagraph(Paragraph):
    # Created by B8Vrede for http://stackoverflow.com/questions/35172207/
    def __init__(self, text, style, fonts_locations):

        font_list = []
        for font_name, font_location in fonts_locations:
            # Load the font
            font = TTFont(font_name, font_location)

            # Get the char width of all known symbols
            font_widths = font.face.charWidths

            # Register the font to able it use
            pdfmetrics.registerFont(font)

            # Store the font and info in a list for lookup
            font_list.append((font_name, font_widths))

        # Set up the string to hold the new text
        new_text = u''

        # Loop through the string
        for char in text:

            # Loop through the fonts
            for font_name, font_widths in font_list:

                # Check whether this font know the width of the character
                # If so it has a Glyph for it so use it
                if ord(char) in font_widths:

                    # Set the working font for the current character
                    new_text += u'<font name="{}">{}</font>'.format(
                        font_name, char)
                    break

        Paragraph.__init__(self, new_text, style)


pdfmetrics.registerFont(TTFont('FZ', 'ttf/FZKTJW.TTF'))
pdfmetrics.registerFont(TTFont('FZHT', 'ttf/FZHTJW.TTF'))
pdfmetrics.registerFont(TTFont('SY', 'ttf/NotoSerifCJKsc-Regular.ttf'))
pdfmetrics.registerFont(TTFont('SY-Bold', 'ttf/NotoSerifCJKsc-Bold.ttf'))

pdfmetrics.registerFont(TTFont('SS', 'ttf/NotoSansHans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('SS-Bold', 'ttf/NotoSansHans-Bold.ttf'))