from flask import render_template, send_from_directory

from flask.views import MethodView

from . import app


class Index(MethodView):
    def get(self):
        return render_template("index.html")


app.add_url_rule('/', view_func=Index.as_view('index'))


@app.route("/favicon.ico")
def favicon():
    return send_from_directory('.', 'favicon.ico')
