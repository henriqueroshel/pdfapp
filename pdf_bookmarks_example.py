import random
from pdf_bookmarks import Bookmark, addBookmarks

random_string = lambda length : "".join([chr(65+random.randint(0,25)) for _ in range(length)])
random_hexcolor = lambda length : "#"+"".join([random.choice('0123456789abcdef') for _ in range(6)])

bookmarks_name_length = 6
number_of_bookmarks = 50

bookmarks_titles = [ f'{_+1}. {random_string(bookmarks_name_length)}' for _ in range(number_of_bookmarks) ]

bookmarks_pages = set()
page_skips = [random.randint(1,5) for _ in range(number_of_bookmarks-1)]
bookmarks_pages = [0]
for page_skip in page_skips:
    last_page = bookmarks_pages[-1]
    bookmarks_pages.append( last_page+page_skip )
bookmarks_colors = [ random_hexcolor(bookmarks_name_length) for _ in range(number_of_bookmarks) ]

bookmarks_list = []
for title,page_number,color in zip(bookmarks_titles, bookmarks_pages, bookmarks_colors):
    bookmark = Bookmark(title, page_number, color=color)
    bookmarks_list.append(bookmark)

path = 'C:/Users/henri/Documents/ProjectsProgramming/Python/pdf_app/test/MERGED_FILE.pdf'

pdf_reader = pypdf.PdfReader(path)
pdf_writer = pypdf.PdfWriter()
for page in pdf_reader.pages:
    pdf_writer.add_page(page)

addBookmarks(pdf_writer, *bookmarks_list)

output_filepath = path.replace('.pdf', '_bm.pdf')
with open(output_filepath, 'wb') as out:
    pdf_writer.write(out)
    print(f'Merged file saved as: {output_filepath}')