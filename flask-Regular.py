from flask import Flask, render_template, request, current_app, g
from flask.views import View
from adminpage import admin
from werkzeug.routing import BaseConverter
app = Flask(__name__)

#--------------------here-----------------------------
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'hello %s' % user_id
#---------------------here-------------------------------

@app.template_filter()
def reverse(s):
    return s[::-1]


app.add_template_filter(reverse, name="test")


app.app_ctx_globals_class()

class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self,context):

        return render_template(self.get_template_name(),**context)

    def dispatch_request(self):
        print '4'
        if request.method != 'GET':
            return 'UNSUPPORTED!'

        context = {'users':self.get_users()}
        return self.render_template(context)


class UserView(BaseView):
    def get_template_name(self):
        print '1'
        return 'test.html'

    def get_users(self):
        print '2'
        return [{
            'username': 'fake',
            'avatar': 'http://lorempixel.com/100/100/nature/'
        }]

app.register_blueprint(admin)
app.add_url_rule('/users', view_func=UserView.as_view('userview'))
if __name__ == '__main__':

    app.run()
