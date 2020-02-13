from flask import Flask, render_template, request, json

app = Flask(__name__, template_folder="./templates", static_folder='static')


@app.route('/', methods=['GET'])
def index_page():
    info = {}
    # return render_template('index.html', **info)
    return "Hello World"


if __name__ == '__main__':
    # TODO comment the lines below
    # app.app_context().push()
    # db.drop_all()
    # db.create_all()
    app.run(debug=True, host='0.0.0.0', port=90)
