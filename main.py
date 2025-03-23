import eel 
import io, base64

from pdf_merger import merge_pdf_files

eel.init("web") 

@eel.expose
def store_file_content(file_id, base64_string, file_name):
    global files_base64, files_name
    files_base64[file_id] = base64_string
    files_name[file_id] = file_name

@eel.expose
def reset_files():
    global files_base64, files_name
    files_base64 = {}
    files_name = {}

@eel.expose
def remove_file_content(file_id):
    global files_base64
    file_id = int(file_id)
    files_base64.pop(file_id)

@eel.expose
def merge_pdf_files_py(files_id_list, add_bookmarks):
    global files_base64, files_name

    pdf_stream_list = []
    pdf_filename_list = []
    for file_id in files_id_list:
        base64_string = files_base64[int(file_id)]
        base64_bytes = base64_string.encode("ascii")
        stream = base64.b64decode(base64_bytes)
        stream = io.BytesIO(stream)
        pdf_stream_list.append(stream)

        filename = files_name[int(file_id)]
        pdf_filename_list.append(filename)

    try: 
        stream = merge_pdf_files(pdf_stream_list, pdf_filename_list, add_bookmarks)
        base64_bytes = base64.b64encode(stream)
        base64_string = base64_bytes.decode("ascii")
        return 200, base64_string
    except ValueError:
        return 400, "Select at least two files to merge."

if __name__ == '__main__':
    files_base64, files_name = {}, {}
    eel.start("index.html", mode='default', start_fullscreen=True)