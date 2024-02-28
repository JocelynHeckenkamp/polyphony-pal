import time
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

#Currently Prints the File sent to this route
@app.route('/upload', methods=['PUT'])
def music_upload():
    content = request.get_data(False, True, False)
    print(content)
    return jsonify(200)

if __name__ == '__main__':
    app.run(debug=True)