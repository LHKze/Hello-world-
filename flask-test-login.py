from flask import Flask, request, render_template, redirect, url_for, make_response
from datetime import datetime, timedelta


app = Flask(__name__)


class UserLogin(object):
    @classmethod
    def check_cookie(cls):
        tmp = request.cookies.get('login')
        if tmp == 'you are login in!':
            return True


    @classmethod
    def login_in(cls, username, password):
        response = make_response(render_template('homepage.html'))
        if check_info(username, password):
            response.set_cookie('login', 'you are login in!', expires=datetime.today() + timedelta(days=30))
            return response
        else:
            return render_template('login.html')

    @classmethod
    def login_out(cls):
        tmp = request.cookies.get('login')
        if tmp == 'you are login in!':
            response = make_response(redirect(url_for('index')))
            response.delete_cookie('login')
            return response

        return redirect(url_for('index'))

def check_info(name, pas):
    return True
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('p')
        password = request.form.get('q')

        response = UserLogin.login_in(username, password)
        return response
    elif request.method == 'GET':
            if UserLogin.check_cookie():
                return render_template('homepage.html')
    else:
        return render_template('login.html')

    """
    response = make_response(render_template('homepage.html'))
    if request.method == 'POST':
        name = request.form.get('p')
        password = request.form.get('q')

        response.set_cookie('login', 'you are login in!', expires=datetime.today()+timedelta(days=30))

        return response

    if request.method == 'GET':
        tmp = request.cookies.get('login')
        if tmp == 'you are login in!':
            return response

    return render_template('login.html')"""


@app.route('/loginout', methods=['POST'])
def login_out():
    if request.method == 'POST':
        response = UserLogin.login_out()
        return response

    """
    if request.method == 'POST':
        tmp = request.cookies.get('login')
        if tmp == 'you are login in!':
            response = make_response(redirect(url_for('index')))
            response.delete_cookie('login')
            return response

    return redirect(url_for('index'))"""
if __name__ == '__main__':
    app.run()

    
