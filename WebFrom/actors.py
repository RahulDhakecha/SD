# using python 3
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, DecimalField, BooleanField, SelectMultipleField, SelectField, IntegerField
from wtforms.validators import Required
from data import ACTORS, COMPANIES
from wtforms.fields.html5 import DateField

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
class POForm(FlaskForm):
    firm = SelectMultipleField('Please select the firm',
                                    choices=[('Raj Electricals', 'Raj Electricals'),
                                             ('Raj VijTech', 'Raj VijTech'),
                                             ('D.N. Syndicate', 'D.N. Syndicate'),
                                             ('Raj Enterprise', 'Raj Enterprise')])
    date = DateField('PO Date', format='%Y-%m-%d')
    company_dropdown = SelectField(label='Please select company from drop down',
                                   choices=[('Voltas', 'Voltas'),
                                            ('Hikal', 'Hikal'),
                                            ('Glenmark', 'Glenmark'),
                                            ('SMC', 'SMC')])
    company_name = StringField('Please enter company name if not found in drop down', validators=[Required()])
    location = StringField('Location')
    project_description = StringField('Please enter project description')
    total_cost = DecimalField('Total Cost')
    order_no = IntegerField('Order number', default=121)
    special_design = BooleanField('Special/Design')
    telecom = BooleanField('Telecom')
    eht = BooleanField('66KV')
    turnkey = BooleanField('Turnkey')
    liaison = BooleanField('Liaison')
    ligthing = BooleanField('Lighting')
    cable_earthing = BooleanField('Cable and Earthing')
    maintenace_testing = BooleanField('Maintenance and Testing')
    bbt = BooleanField('BBT')
    sitc = BooleanField('SITC Panels')
    retrofitting = BooleanField('Retrofitting')
    submit = SubmitField('Submit')


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
    form = POForm()
    message = ""

    if form.validate_on_submit():
        # flash("Validation in process")
        company_name = form.company_name.data
        project_description = form.project_description.data
        date = form.date.data
        print(form.firm.data)
        print(date)
        print(company_name)
        print(project_description)
        # if name in names:
        #     message = "Yay! " + name + "!"
        #     # empty the form field
        #     form.name.data = ""
        # else:
        #     message = "That company is not in our database."
    # notice that we don't need to pass name or names to the template
    return render_template('index.html', form=form, message=message, names=names)


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
