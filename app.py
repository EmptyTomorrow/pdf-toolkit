from distutils.log import debug
import io, os
from flask import Flask, request, send_file
import fitz

flask_app = Flask("PDF Toolkit")

@flask_app.route('/addstamp', methods = ["POST"])
def add_stamp():

    pagenum = int(request.args.get('pageNum'))
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    inputFile = request.files['inputFile']
    stampFile = request.files['stampFile']

    file_handle = fitz.open(stream=inputFile.stream.read())
    page_handle = file_handle[pagenum]

    stamp_rectangle = fitz.Rect(0, 0, x, y)

    if not page_handle.is_wrapped: 
        page_handle.wrap_contents()

    page_handle.insert_image(stamp_rectangle, stream=stampFile.stream.read())

    file_bytes = file_handle.tobytes()
    return send_file(io.BytesIO(file_bytes), mimetype="application/pdf", as_attachment=False)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    flask_app.run(debug=True, host='0.0.0.0', port=port)