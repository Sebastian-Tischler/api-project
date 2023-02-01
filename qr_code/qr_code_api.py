from flask import Flask, request, make_response
from qrcode import make
from io import BytesIO

app = Flask(__name__)

@app.route("/qr", methods=["GET"])
def qr():
    # get url
    url = request.args.get("url")

    # create qr-code Image
    img = make(url)

    # save qr-code Image
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    # create the response
    response = make_response(img_io.getvalue())
    response.mimetype = 'image/png'
    response.headers['Content-Disposition'] = 'attachment; filename=qr.png'
    
    # return response
    return response

if __name__ == "__main__":
    app.run(debug=True)
