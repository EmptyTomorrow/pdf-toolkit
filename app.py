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

    # Получаем параметры 
    # TODO дефолтные значения
    pagenum = int(request.args.get('pageNum'))
    x0 = int(request.args.get('x0'))
    y0 = int(request.args.get('y0'))
    x1 = int(request.args.get('x1'))
    y1 = int(request.args.get('y1'))
    inputFile = request.files['inputFile']
    stampFile = request.files['stampFile']

    # Открываем файл из стрима и страницы
    # TODO проверки
    file_handle = fitz.open(stream=inputFile.stream.read())
    page_handle = file_handle[pagenum - 1]
    
    if (x0 > x1) or (y0 > y1):
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