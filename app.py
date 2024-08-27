# app.py
from flask import Flask, request, jsonify, send_from_directory, send_file
from PIL import Image
from io import BytesIO
import os
import tempfile
import cairosvg

app = Flask(__name__)
Image.MAX_IMAGE_PIXELS = 2000 * 1000 * 1000  
#os.environ['PIL_MAX_IMAGE_PIXELS'] = '2000 * 1000 * 1000'

@app.route('/convert', methods=['POST'])
def convert_to_rgb():
    array_buffer = request.data
    image = Image.open(BytesIO(array_buffer))
    # 制作缩略图以减少处理时间和复杂度
    image.thumbnail((1024, 1024)) # 1min to deal with 500M test_055.tif

    # 转换为 RGB
    rgb_image = image.convert('RGB')

    # 使用通用的后缀创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
        temp_path = temp.name
        rgb_image.save(temp_path)

    # 返回图片 URL
    return jsonify({'url': f'/display/{os.path.basename(temp_path)}'})

@app.route('/display/<filename>')
def display_image(filename):
    temp_folder = tempfile.gettempdir()
    return send_from_directory(temp_folder, filename) 
    #这里要是写成send_from_directory(directory=temp_folder, filename=filename)就失败了，要写path=filename
    #会报错TypeError: send_from_directory() missing 1 required positional argument: 'path'

@app.route('/')
def index():
    return send_file('transform.html')

if __name__ == '__main__':
    app.run(debug=True)
