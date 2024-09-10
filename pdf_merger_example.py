from pdf_merger import merge_pdf_files
import os, random, time

pdf_filepaths = [
    "C:/Users/henri/Documents/ProjectsProgramming/Python/pdf_app/example/0.pdf",
    "C:/Users/henri/Documents/ProjectsProgramming/Python/pdf_app/example/1.pdf",
    "C:/Users/henri/Documents/ProjectsProgramming/Python/pdf_app/example/2.pdf",
    "C:/Users/henri/Documents/ProjectsProgramming/Python/pdf_app/example/3.pdf",
    "C:/Users/henri/Documents/ProjectsProgramming/Python/pdf_app/example/4.pdf",
    "C:/Users/henri/Documents/ProjectsProgramming/Python/pdf_app/example/5.pdf",
]
n_filepaths = len(pdf_filepaths)
wkdir = os.path.commonpath(pdf_filepaths)

number_of_files = 10

print('\nGenerating different files by merging multiple individual pages')
for i in range(number_of_files):
    number_of_pages = random.randint(2,8)
    merged_filename = f'new_merged/test_{i}.pdf'
    print(f'\nNumber of pages on file {merged_filename}: {number_of_pages}')
    pages_filepaths = [ pdf_filepaths[ i % n_filepaths ] for j in range(number_of_pages) ]
    
    save_filepath = os.path.join(wkdir, merged_filename)
    merge_pdf_files(pages_filepaths, save_filepath, open_when_done=False, add_bookmarks=False)
    time.sleep(1)

print('\nMerging the generated files and adding bookmarks')
wkdir = os.path.commonpath(pdf_filepaths)
new_merged = [os.path.join(wkdir, f'new_merged/test_{i}.pdf') for i in range(number_of_files)]
save_filename = 'MergedFileWithBookmarks'
merge_pdf_files(new_merged, save_filename, open_when_done=True, add_bookmarks=True)