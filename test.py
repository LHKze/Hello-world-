from flask import Flask,jsonify,g


app = Flask(__name__)
count = []


@app.before_request
def before_request():
    print count


@app.route('/')
def hello_world():
    count.append(1)
    g.count = count
    return 'Hello World!'


@app.route('/get')
def get():
    return jsonify(count=g.count)


if __name__ == '__main__':
    app.run()
