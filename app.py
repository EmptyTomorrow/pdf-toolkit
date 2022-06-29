from distutils.log import debug
import io, os
from flask import Flask, request, send_file
import fitz

flask_app = Flask("PDF Toolkit")

@flask_app.route('/pdftoolkit/health', methods = ["GET"])
def health_check():
    return "1"

@flask_app.route('/pdftoolkit/addstamp', methods = ["POST"])
def add_stamp():

    pagenum = request.args.get('pagenum')
    
    if not pagenum:
        pagenum = 1
    pagenum = int(pagenum)

    x0 = request.args.get('x0')
    if not x0:
        return "Не передана координата x0", 400 
    x0 = int(x0)

    y0 = request.args.get('y0')
    if not y0:
        return "Не передана координата y0", 400 
    y0 = int(y0)

    x1 = request.args.get('x1')
    if not x1:
        return "Не передана координата x1", 400
    x1 = int(x1)

    y1 = request.args.get('y1')
    if not y1:
        return "Не передана координата y1", 400
    y1 = int(y1)

    inputFile = request.files['inputFile']
    stampFile = request.files['stampFile']

    # Открываем файл из стрима и страницы
    # TODO проверки
    file_handle = fitz.open(stream=inputFile.stream.read())
    page_handle = file_handle[pagenum - 1]

    if ((x0 > x1) or (y0 > y1)):
        return "Координаты штампа заданы неверно.", 400

    stamp_rectangle = fitz.Rect(x0, y0, x1, y1)

    # Перед вставкой картинки нормализуем страницу
    if not page_handle.is_wrapped: 
        page_handle.wrap_contents()

    page_handle.insert_image(stamp_rectangle, stream=stampFile.stream.read())
    # Возвращаем в виде байт, можно файлы и в base64 передавать вместо бинарей
    file_bytes = file_handle.tobytes()
    return send_file(io.BytesIO(file_bytes), mimetype="application/pdf", as_attachment=False)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    flask_app.run(debug=True, host='0.0.0.0', port=port)