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
    #run script then return
    return content

# @app.route('/results', methods=['GET', 'POST'])
# def music_return():
#     f = open(r'voice-leading-1.mxml', "r")
#     x = f.read()
#     return x


if __name__ == '__main__':
    app.run(debug=True)