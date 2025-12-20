
from file_util.core.app import (
    get_mime_type,
    get_sheet_names,
    extract_excel_sheet,
    extract_text_from_file,
    extract_base64_to_text,
    export_to_excel,
    import_from_excel,
    extract_text_from_file,
    list_zip_contents,
    extract_zip,
    create_zip,
)
from fastapi import FastAPI
app = FastAPI()
# get_mime_type
app.add_api_route(path='/get_mime_type', endpoint=get_mime_type, methods=['GET'])
 
# get_sheet_names
app.add_api_route(path='/get_sheet_names', endpoint=get_sheet_names, methods=['GET'])

# extract_excel_sheet
app.add_api_route(path='/extract_excel_sheet', endpoint=extract_excel_sheet, methods=['POST'])

# extract_text_from_file
app.add_api_route(path='/extract_text_from_file', endpoint=extract_text_from_file, methods=['POST'])

# extract_base64_to_text
app.add_api_route(path='/extract_base64_to_text', endpoint=extract_base64_to_text, methods=['GET'])

# export_to_excel
app.add_api_route(path='/export_to_excel', endpoint=export_to_excel, methods=['GET'])

# import_from_excel
app.add_api_route(path='/import_from_excel', endpoint=import_from_excel, methods=['GET'])

# extract_text_from_file
app.add_api_route(path='/extract_text_from_file', endpoint=extract_text_from_file, methods=['POST'])

# ZIPファイルの内容をリストする関数
app.add_api_route(path='/list_zip_contents', endpoint=list_zip_contents, methods=['GET'])

# ZIPファイルを展開する関数
app.add_api_route(path='/extract_zip', endpoint=extract_zip, methods=['POST'])

# ZIPファイルを作成する関数
app.add_api_route(path='/create_zip', endpoint=create_zip, methods=['POST'])


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=8000)