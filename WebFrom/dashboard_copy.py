# using python 3
import time
start_time = time.time()
import sys, os
sys.path.append(os.path.join(sys.path[0], 'DashLayouts'))
from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField, FileField, HiddenField
from wtforms.validators import Required, InputRequired, Email, Length
from flask_login import LoginManager
from wtforms.fields.html5 import DateField
from functools import wraps
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from Connections.AWSMySQL import AWSMySQLConn
from fixedVariables import sow, lead_status, raj_group_office, follow_up_person, fields_enquiry_list, fields_followup_log, \
    fields_client_list, fields_client_rep_list, sow_code, raj_group_office_code, fields_rj_orders_list, master_users
from dashLayout import service_wise_pie_data, pending_offers_pie_data, submitted_offers_pie_data, lead_stages_bar_data, \
    weekly_leads_line_data, main_layout, new_offer_entry_layout, new_contact_entry_layout, order_layout, dn_order_layout

from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime
from plotly import tools
import plotly.graph_objs as go
import json
import pprint
import pandas as pd
import numpy as np
import multiprocessing


import dash
from dash.dependencies import Input, Output, State
import dash_table
# import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

login = LoginManager(app)

connection = AWSMySQLConn()
# data_upcoming_projects = connection.execute_query("select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
#                                                   "client_location, lead_status, follow_up_person from RajGroupEnquiryList;")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# Check if user logged in
def is_master_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'master_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


def call_dash_app(href):
    d_app = dash.Dash(__name__,
                         server=app,
                         routes_pathname_prefix=href,
                         external_stylesheets=external_stylesheets
                         )
    return d_app



dash_app3 = call_dash_app('/dash3/')

dash_app3.layout = dn_order_layout

@dash_app3.callback([Output('tabs', 'value'),
                     Output('order_key', 'value'),
                     Output('order_date', 'date'),
                     Output('order_po_no', 'value'),
                     Output('order_project_description', 'value'),
                     Output('order_scope_of_work', 'value'),
                     Output('order_client_name', 'value'),
                     Output('order_client_location', 'value'),
                     Output('order_existing_client', 'value'),
                     Output('order_order_no', 'value'),
                     Output('order_file_no', 'value'),
                     Output('order_status', 'value'),
                     Output('order_project_incharge', 'value'),
                     Output('order_raj_group_office', 'value'),
                     Output('order_project_value', 'value'),
                     Output('order_remarks', 'value'),
                     Output('order_comp_location', 'value'),
                     Output('order_modal_display', 'displayed'),
                     Output('orders_table', 'data')],
                    [Input('order_submit_button', 'submit_n_clicks'),
                     Input('order_close_button', 'submit_n_clicks'),
                     Input('order_enquiry_key', 'value'),
                     Input('order_client_dropdown', 'value'),
                     Input('orders_table', 'selected_rows'),
                     Input('orders_scope_pie_chart', 'clickData'),
                     Input('orders_status_pie_chart', 'clickData'), ],
                    [State('orders_table', 'data')]
                  )
def update_order_values(submit_clicks, close_clicks, order_enquiry_key, client_dropdown, row_id, clickData_scope, clickData_status, rows):
    print("Coming Here for trigger1")
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 1: "+str(triggered_input))

        if triggered_input == 'order_client_dropdown' and client_dropdown:
            if client_dropdown != 'Other':
                client_nm = str(client_dropdown).split(" -- ")[0]
                client_loc = str(client_dropdown).split(" -- ")[1]
                # client_loc = connection.execute_query("select * from RajGroupClientList where "
                #                                                                "client_name='{}';".format(client_dropdown)).iloc[0]['client_location']
                existing_client = "YES"
            else:
                client_nm = ''
                client_loc = ''
                existing_client = "NO"
            print("Client"+str(client_nm))
            print("Client Location" + str(client_loc))
            return 'tab-2', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   None
        else:
            return 'tab-2', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   None
    return 'tab-2', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   None


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class SelectFirmForm(FlaskForm):
    firm = SelectField('Please select the firm',
                                    choices=[('Raj Electricals', 'Raj Electricals'),
                                             ('Raj VijTech', 'Raj VijTech'),
                                             ('D.N. Syndicate', 'D.N. Syndicate'),
                                             ('Raj Enterprise', 'Raj Enterprise'),
                                             ('Raj Brookite', 'Raj Brookite')])
    submit = SubmitField('Submit')


# define functions to be used by the routes (just one here)

# all Flask routes below

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # connection = AWSMySQLConn()
        existing_users = connection.get_unique_values("users", "user_name")
        user_email = connection.execute_query("select email from users where user_name='{}'".format(form.username.data)).iloc[0]['email']
        if form.username.data in existing_users:
            password = connection.execute_query("select user_password from users where user_name='{}'".format(form.username.data)).iloc[0,0]

            if sha256_crypt.verify(form.password.data, password):
                session['logged_in'] = True
                session['username'] = form.username.data
                if user_email in master_users:
                    session['master_logged_in'] = True
                return redirect(url_for('base'))
            else:
                flash('Invalid Username or Password!', 'danger')
                # return '<h1> Invalid Username or Password! </h1>'
        else:
            flash('Invalid Username or Password!', 'danger')
            # return '<h1> Invalid Username or Password! </h1>'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        # connection = AWSMySQLConn()
        unique_emails = connection.get_unique_values("unique_users", "email")
        existing_emails = connection.get_unique_values("users", "email")
        existing_users = connection.get_unique_values("users", "user_name")
        if form.email.data in existing_emails or form.username.data in existing_users:
            flash('Cannot create Username.', 'danger')
            flash('Either Username or User Email already exists. Please log in.', 'danger')
            return redirect(url_for('signup'))
        if form.email.data in unique_emails:
            fields = "(user_name, email, user_password)"
            password = sha256_crypt.encrypt(str(form.password.data))
            values = [form.username.data, form.email.data, password]
            connection.insert_query("users", fields=fields, values=values)
            flash('User name successfully created!!', 'success')
            return redirect(url_for('signup'))
        else:
            flash('User email not identified.', 'danger')
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    # flash('You are now logged out', 'success')
    return redirect(url_for('base'))


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    return redirect('/dash')
    # return redirect(url_for('base'))


@app.route('/select_firm', methods=['GET', 'POST'])
@is_logged_in
@is_master_logged_in
def select_firm():
    form = SelectFirmForm()
    if form.validate_on_submit():
        if form.firm.data == 'Raj Electricals':
            return redirect('/dash2')
        elif form.firm.data == 'Raj VijTech':
            return redirect('/dash2')
        elif form.firm.data == 'D.N. Syndicate':
            return redirect('/dash3')
        elif form.firm.data == 'Raj Enterprise':
            return redirect('/dash2')
        elif form.firm.data == 'Raj Brookite':
            return redirect('/dash2')
    return render_template('select_firm.html', form=form)


# @app.route('/order_entry', methods=['GET', 'POST'])
# @is_logged_in
# def order_entry():
#     return redirect('/dash2')
# #     # return redirect(url_for('base'))



# @app.route('/order_entry', methods=['GET', 'POST'])
# @is_logged_in
# def home():
#     flash('You are now logged in', 'success')
#     form = HomeForm()
#     if form.validate_on_submit():
#         return redirect(url_for('/dash2'))
#     return render_template('home.html', form=form)


# keep this as is
if __name__ == '__main__':
    # print("Hello World")
    app.run(port=8000)
    # dash_app.run_server(debug=True)
