from flask import Flask, request, render_template, redirect, url_for, make_response, session, escape

app = Flask(__name__)
app.config['SECRET_KEY'] = 'strong'


@app.route('/login/', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        response = make_response(redirect(url_for('home')))
        username = request.form.get('username')
        # password = request.form.get('password')
        session['username'] = username
        session.permanent = True
        key = request.cookies.get('session')
        return response

    else:
        return render_template('test1.html')



@app.route('/logout/')
def logout():
    if 'username' in session:
        session.pop('username', None)

    return redirect(url_for('home'))


@app.route('/home/')
def home():

    if 'username' in session:
        print session
        return 'hello %s!' % escape(session['username'])
    return 'You are not logged in'

if __name__ == '__main__':
    app.run()
