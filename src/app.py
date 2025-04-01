from flask import Flask, request
import logging
from models.plate_reader import PlateReader
from image_provider import ImageClient, ImageClientError

app = Flask(__name__)
model = PlateReader.load_from_file("/app/model_weights/plate_reader_model.pth")
img_client = ImageClient()


@app.route('/')
def hello():
    return '<h1><center>Hello!</center></h1>'


@app.route('/predict')
def prediction():
    """GET request with multiple or one id wuery param"""

    img_ids = request.args.getlist('img_id')
    logging.info({"input": img_ids})

    try:
        img_ids = set([int(img_id) for img_id in img_ids])
    except ValueError:
        return {"msg": "invalid format"}, 400

    if any([
        not img_client.check_if_img_acceptable(img_id)
        for img_id in img_ids
    ]):
        return {"msg": "One or more images not found"}, 404

    try:
        imgs = [img_client.request_image(img_id) for img_id in img_ids]
    except ImageClientError:
        return {"msg": "try again later plz"}, 504
    except OSError:
        return {"msg": "too much load"}, 503

    contents = {
        img_id: model.read_text(imgs[i])
        for i, img_id in enumerate(img_ids)
    }
    logging.info({"output": contents})
    return {"results": contents}


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )
    app.run(host='0.0.0.0', port=8080, debug=True)
