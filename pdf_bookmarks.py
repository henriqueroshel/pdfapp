import os
import pypdf

class Bookmark(object):
    def __init__( self, title: str, page_number: int, parent: object = None, 
                  color: str = None, bold: bool = False, italic: bool = False ):
        self.title = title
        self.page_number = page_number
        self.parent = parent
        self.color = color
        self.bold = bold
        self.italic = italic
    
    def add_to_pdf(self, pdf_writer):
        pdf_writer.add_outline_item(
            title=self.title,
            page_number=self.page_number,
            parent=self.parent,
            color=self.color,
            bold=self.bold,
            italic=self.italic
        )

    def __repr__(self):
        return self.title

def addBookmarks(pdf_writer, *bookmarks, output_filepath=None):
    for bookmark in bookmarks:
        bookmark.add_to_pdf(pdf_writer)