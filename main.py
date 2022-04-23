from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if 'create_account' in request.form:
            print('create acount')
        elif 'enter' in request.form:
            print('enter')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
