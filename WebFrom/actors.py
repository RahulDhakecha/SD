# using python 3
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField, BooleanField, SelectMultipleField, SelectField, IntegerField, FileField
from wtforms.validators import Required, InputRequired, Email, Length
from flask_login import LoginManager
from wtforms import validators
from data import ACTORS, COMPANIES
from wtforms.fields.html5 import DateField
from Connections.AWSMySQL import AWSMySQLConn
import sys

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

login = LoginManager(app)

fields = "(order_no, po_no, po_date, company, location, project_description, po_value, file_no, project_status, " \
             "project_incharge, special_design, telecom, eht, turnkey, liaison, solar, lighting, cable_earthing, " \
             "maintenance_testing, bbt, sitc_panel, retrofitting)"


# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class POForm(FlaskForm):
    # connection = AWSMySQLConn()
    # default_val = int(connection.get_max_value("RajPO", "order_no")) if connection.get_max_value("RajPO", "order_no") else 0
    order_no = IntegerField('Order number')
    po_no = StringField('PO number')
    date = DateField('PO Date', format='%Y-%m-%d')
    # company_dropdown = SelectField(label='Please select company from drop down', choices = [('Voltas', 'Voltas'),
    #                                                                                 ('Hikal', 'Hikal'),
    #                                                                                 ('Glenmark', 'Glenmark'),
    #                                                                                 ('SMC', 'SMC')])

    company_dropdown = SelectField(label='Please select company from drop down', default=None)
    company_name = StringField('Please enter company name if not found in drop down')
    location = StringField('Location')
    project_description = StringField('Please enter project description')
    po_value = IntegerField('PO Value')
    file_no = StringField('File number')
    project_status = SelectField(label='Project Status',
                                   choices=[('Complete', 'Complete'),
                                            ('On Hand', 'On Hand')])
    project_incharge = StringField("Project Incharge")
    # po_file = FileField('Please upload PO file')

    special_design = BooleanField('Special/Design')
    telecom = BooleanField('Telecom')
    eht = BooleanField('66KV')
    turnkey = BooleanField('Turnkey')
    liaison = BooleanField('Liaison')
    solar = BooleanField('Solar')
    lighting = BooleanField('Lighting')
    cable_earthing = BooleanField('Cable and Earthing')
    maintenance_testing = BooleanField('Maintenance and Testing')
    bbt = BooleanField('BBT')
    sitc_panel = BooleanField('SITC Panels')
    retrofitting = BooleanField('Retrofitting')
    submit = SubmitField('Submit')


class HomeForm(FlaskForm):
    firm = SelectField('Please select the firm',
                                    choices=[('Raj Electricals', 'Raj Electricals'),
                                             ('Raj VijTech', 'Raj VijTech'),
                                             ('D.N. Syndicate', 'D.N. Syndicate'),
                                             ('Raj Enterprise', 'Raj Enterprise')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


# define functions to be used by the routes (just one here)

# all Flask routes below

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        connection = AWSMySQLConn()
        existing_users = connection.get_unique_values("users", "user_name")
        if form.username.data in existing_users:
            password = connection.execute_query("select user_password from users where user_name='{}'".format(form.username.data)).iloc[0,0]
            print(password == form.password.data)
            if password == form.password.data:
                return redirect(url_for('home'))
            else:
                return '<h1> Invalid Username or Password! </h1>'
        else:
            return '<h1> Invalid Username or Password! </h1>'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        connection = AWSMySQLConn()
        unique_emails = connection.get_unique_values("unique_users", "email")
        existing_emails = connection.get_unique_values("users", "email")
        existing_users = connection.get_unique_values("users", "user_name")
        if form.email.data in existing_emails or form.username.data in existing_users:
            return '<h1> Either Username or User Email already exists. Please log in. </h1>'
        if form.email.data in unique_emails:
            fields = "(user_name, email, user_password)"
            values = [form.username.data, form.email.data, form.password.data]
            connection.insert_query("users", fields=fields, values=values)
            return '<h1> User name' + form.username.data + ' successfully created for email ' + form.email.data + '</h1>'
        else:
            return '<h1> User email not identified </h1>'
    return render_template('signup.html', form=form)


# two decorators using the same function
# @app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():

    form = POForm()
    connection = AWSMySQLConn()
    default_val = int(connection.get_max_value("RajPO", "order_no")) if connection.get_max_value("RajPO",
                                                                                                 "order_no") else 0
    companies = connection.get_unique_values("RajPO", "Company")
    companies += ['None']

    message = ""

    # form.company_dropdown.choices += [("Rio", "Rio")]
    form.company_dropdown.choices = [(x,x) for x in companies]

    if request.method == 'GET':
        form.order_no.data = default_val + 1

    if form.validate_on_submit():
        # flash("Validation in process")
        raw_values = [form.order_no.data,
                  form.po_no.data,
                  str(form.date.data),
                  form.company_name.data if form.company_dropdown.data == "None" else form.company_dropdown.data,
                  form.location.data,
                  form.project_description.data,
                  form.po_value.data,
                  form.file_no.data,
                  form.project_status.data,
                  form.project_incharge.data,
                  form.special_design.data,
                  form.telecom.data,
                  form.eht.data,
                  form.turnkey.data,
                  form.liaison.data,
                  form.solar.data,
                  form.lighting.data,
                  form.cable_earthing.data,
                  form.maintenance_testing.data,
                  form.bbt.data,
                  form.sitc_panel.data,
                  form.retrofitting.data]

        values = [1 if x is True else 0 if x is False else x for x in raw_values]
        print(values)
        connection = AWSMySQLConn()
        connection.insert_query("RajPO", fields=fields, values=values)
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)


# @app.route('/', methods=['GET', 'POST'])
@app.route('/home.html', methods=['GET', 'POST'])
def home():
    # print("home method")
    form = HomeForm()
    if form.validate_on_submit():
        print(form.firm.data)
        return redirect(url_for('index'))
    return render_template('home.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/dashboard_table.html', methods=['GET', 'POST'])
def dashboard():
    # print("dashboard method")
    connection = AWSMySQLConn()
    # cursor.execute("select * from table_name")
    # data = cursor.fetchall() #data from database
    data = connection.execute_query("select * from RajPO;")
    return render_template('dashboard_table.html', tables=[data.to_html(classes='data',index=False)], titles=data.columns.values)


@app.route('/download.html', methods=['GET', 'POST'])
def download():
    return redirect(url_for('dashboard'))


# keep this as is
if __name__ == '__main__':
    # print("main method")
    # connection = AWSMySQLConn()
    # print(connection.get_max_value("RajPO", "Order_no"))
    app.run(port=8000)

