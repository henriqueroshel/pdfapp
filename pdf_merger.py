import pypdf
from io import BytesIO

from random import randint

def merge_pdf_files(pdf_stream_list, pdf_filename_list, add_bookmarks=False):
    if len(pdf_stream_list) < 2:
        raise ValueError(f"Expected at least 2 file to merge, got {len(pdf_stream_list)}")
        
    # merge pdf files
    merged_pdf_writer = pypdf.PdfWriter()
    base_pagewidth = pypdf.PdfReader(pdf_stream_list[0]).pages[0].mediabox.width
    for (files_stream, file_name) in zip(pdf_stream_list, pdf_filename_list):
        pdf_reader = pypdf.PdfReader(files_stream)

        for page in pdf_reader.pages:
            merged_pdf_writer.add_page(page)
            if page.mediabox.width > base_pagewidth:
                base_pagewidth = page.mediabox.width
        if add_bookmarks:
            bookmark_title = file_name.replace('.pdf', '')
            page_number = len(merged_pdf_writer.pages) - len(pdf_reader.pages)
            merged_pdf_writer.add_outline_item(title=bookmark_title, page_number=page_number)

    for page in merged_pdf_writer.pages:
        if page.mediabox.width != base_pagewidth:
            scale_factor = base_pagewidth/page.mediabox.width 
            page.scale(sx=scale_factor, sy=scale_factor)

    with BytesIO() as bytes_stream:
        my_file, stream = merged_pdf_writer.write(bytes_stream)
        return stream.getvalue()