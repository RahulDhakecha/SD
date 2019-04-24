# using python 3
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from data import ACTORS, COMPANIES

app = Flask(__name__)
# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Please enter company name or select from drop down list', validators=[Required()])
    # submit = SubmitField('Submit')

# define functions to be used by the routes (just one here)

# retrieve all the names from the dataset and put them into a list
def get_names(source):
    names = []
    for row in source:
        name = row["name"]
        names.append(name)
    return sorted(names)

# all Flask routes below

# @app.route('/', methods=['GET'])
# def dropdown():
#     colours = ['Red', 'Blue', 'Black', 'Orange']
#     return render_template('/test.html', colours=colours)

# two decorators using the same function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    names = get_names(COMPANIES)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name in names:
            message = "Yay! " + name + "!"
            # empty the form field
            form.name.data = ""
        else:
            message = "That actor is not in our database."
    # notice that we don't need to pass name or names to the template
    return render_template('index.html', form=form, message=message, names=names)

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
