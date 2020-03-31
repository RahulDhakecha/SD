# using python 3
from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField, FileField, HiddenField
from wtforms.validators import Required, InputRequired, Email, Length
from flask_login import LoginManager
from wtforms.fields.html5 import DateField
from functools import wraps
from passlib.hash import sha256_crypt
from werkzeug import secure_filename
from Connections.AWSMySQL import AWSMySQLConn
from Connections.GeographicInfo import GeoInfoConn
from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime
from plotly import tools
import plotly.graph_objs as go
import sys
import time
import json
import pprint
import pandas as pd
import numpy as np
sys.path.append('~/RajGroup/SD/')


import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc
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


sow = ['Turnkey', '66KV Switchyard', 'BBT', 'Solar', 'Civil/Telecom', 'Liaison', 'Testing', 'Maintenance/Servicing',
       'Retrofitting', 'SITC', 'Supply only', 'ITC only']
lead_status = ['OPEN', 'CONTACTED', 'VISITED', 'ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD']
raj_group_office = ['Raj Vijtech Pvt Ltd', 'Raj Electricals', 'D.N. Syndicate', 'Raj Enterprise', 'Raj Brookite']
follow_up_person = ['Rahul Dhakecha',
                    'Rajesh Kunjadiya',
                    'Ashish Dhakecha',
                    'Dhiren Sankaliya',
                    'Umang Sharma',
                    'Unmil Naik',
                    'Purvik Mistry',
                    'Kanubhai Patel',
                    'Anil Kathiriya',
                    'Divyesh Patel',
                    'Kinjal Dhakecha',
                    'Hiren Paghdal',
                    'Praful Shyani',
                    'Sachin Patel',
                    'Chirag Patel',
                    'Jitendra Kotnala',
                    'Ninad',
                    'Samir']

fields_enquiry_list = "(enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client, " \
                      "contact_person_name, contact_person_mobile, contact_person_email, internal_lead, external_lead, " \
                      "lead_status, contact_date, visit_date, enquiry_date, offer_date, raj_group_office, " \
                      "follow_up_person, tentative_project_value, quotation_number, remarks)"

fields_followup_log = "(enquiry_key, offer_key, offer_location)"

connection = AWSMySQLConn()
data_upcoming_projects = connection.execute_query("select * from RajGroupEnquiryList;")


def service_wise_pie_data():
    services = list(connection.execute_query("select scope_of_work, count(*) as cnt from RajGroupEnquiryList group by 1")['scope_of_work'])
    service_wise_data = list(connection.execute_query("select scope_of_work, count(*) as cnt from RajGroupEnquiryList group by 1")['cnt'])
    service_wise_pie_data = [
            {
                'labels': services,
                'values': service_wise_data,
                'type': 'pie',
            },
        ]
    fig = {
        'data': service_wise_pie_data,
        'layout': {
            'title': 'Raj Group - Service Wise Enquiries',
            'autosize': True
        }
    }
    return fig


def pending_offers_pie_data():
    pending_offers = connection.execute_query("select follow_up_person, count(*) as cnt from RajGroupEnquiryList where "
                                              "lead_status='ENQUIRY' group by 1")
    pending_offers_data = []
    for i in follow_up_person:
        try:
            pending_offers_data.append(pending_offers[pending_offers['follow_up_person'] == i]['cnt'].iloc[0])
        except:
            pending_offers_data.append(0)
    pending_offers_pie_data_var = [
            {
                'labels': follow_up_person,
                'values': pending_offers_data,
                'type': 'pie',
                'hole': 0.5,
            },
        ]
    fig = {
        'data': pending_offers_pie_data_var,
        'layout': {
            'title': 'Raj Group - Pending Offers'
        }
    }
    return fig


def submitted_offers_pie_data():
    submitted_offers = connection.execute_query("select follow_up_person, count(*) as cnt from RajGroupEnquiryList where "
                                              "lead_status='OFFER' group by 1")
    submitted_offers_data = []
    for i in follow_up_person:
        try:
            submitted_offers_data.append(submitted_offers[submitted_offers['follow_up_person'] == i]['cnt'].iloc[0])
        except:
            submitted_offers_data.append(0)
    submitted_offers_pie_data = [
            {
                'labels': follow_up_person,
                'values': submitted_offers_data,
                'type': 'pie',
                'hole': 0.5,
            },
        ]
    fig = {
            'data': submitted_offers_pie_data,
            'layout': {
                'title': 'Raj Group - Submitted Offers',
                'autosize': True
            }
        }
    return fig


def lead_stages_bar_data():
    lead_status_data = connection.execute_query("select lead_status, count(*) as cnt from RajGroupEnquiryList group by 1")
    lead_stages_data = []
    for i in lead_status:
        try:
            lead_stages_data.append(lead_status_data[lead_status_data['lead_status'] == i]['cnt'].iloc[0])
        except:
            lead_stages_data.append(0)

    lead_stages_bar_data = [
            {
                'x': lead_status,
                'y': lead_stages_data,
                'type': 'bar',
            },
        ]
    fig = {
            'data': lead_stages_bar_data,
            'layout': {
                'title': 'Raj Group - Lead Status'
            }
        }
    return fig


def getDateRangeFromWeek(p_year,p_week):
    firstdayofweek = dt.strptime(f'{p_year}-W{int(p_week )}-1', "%Y-W%W-%w").date()
    # lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek.strftime("%Y-%m-%d")


def weekly_leads_line_data():
    weekly_leads_data = connection.execute_query("select years, weeks, count(*) as leads_cnt "
                                                 "from (select time_stamp, entry_date, year(entry_date) as years, week(entry_date, 5) as weeks "
                                                 "from RajGroupEnquiryList) as temp where years=2020 group by 1,2;")
    # print(weekly_leads_data)
    current_year, current_week, current_day = date.today().isocalendar()
    weeks = [getDateRangeFromWeek('2020', p_week) for p_week in range(1, current_week)]

    weekly_leads_cnt_data = []
    for i in range(1, current_week):
        # print(weekly_leads_data[weekly_leads_data['weeks'] == i]['leads_cnt'].iloc[0])
        try:
            weekly_leads_cnt_data.append(weekly_leads_data[weekly_leads_data['weeks'] == i]['leads_cnt'].iloc[0])
        except IndexError:
            weekly_leads_cnt_data.append(0)

    weekly_leads_line_data = [
            {
                'x': weeks,
                'y': weekly_leads_cnt_data,
                'type': 'line',
            },
        ]
    fig = {
            'data': weekly_leads_line_data,
            'layout': {
                'title': 'Raj Group - Weekly Leads',
                'xaxis': {
                    'title': 'Weeks',
                    'range': weeks,
                    'type': "category"
                }
            }
        }
    return fig


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


def call_dash_app(href):
    d_app = dash.Dash(__name__,
                         server=app,
                         routes_pathname_prefix=href,
                         external_stylesheets=external_stylesheets
                         )
    return d_app


dash_app = call_dash_app('/dash/')


######################## Layout ########################
def return_layout():
    return html.Div([
    dcc.Link('HOME', href='/', refresh=True),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tab1', value='tab-1', label='Raj Group Marketing Dashboard', children=[
            html.Div([
                html.Div([
                    # GRAPH - Lead Stages
                    dcc.Graph(
                        id='weekly_leads',
                        figure=weekly_leads_line_data()
                    ),
                ]),
            ], className="row"),
            html.Div([
                html.Div([
                    # Pie-chart reflecting submitted offer
                    dcc.Graph(
                        id='submitted_offers_pie_chart',
                        figure=submitted_offers_pie_data()
                    ),
                ], className="six columns"),

                html.Div([
                    # Pie-chart reflecting pending offers
                    dcc.Graph(
                        id='pending_offers_pie_chart',
                        figure=pending_offers_pie_data()
                    ),
                ], className="six columns")

            ], className="row"),
            html.Div([
                html.Div([
                # GRAPH - Lead Stages
                dcc.Graph(
                    id='graph_lead_stages',
                    figure=lead_stages_bar_data()
                ),
                ], className="six columns"),
                html.Div([
                    # Pie-chart reflecting service wise enquiries
                    dcc.Graph(
                        id='service_wise_pie_chart',
                        figure=service_wise_pie_data()
                    ),
                ], className="six columns"),
            ], className="row"),

            # Data Table - Upcoming Projects
            dash_table.DataTable(
                id='upcoming_projects_table',
                style_data={'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
                style_table={
                    'maxHeight': '30',
                    'overflowY': 'scroll'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_cell={
                    'textAlign': 'center'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                fixed_rows={'headers': True, 'data': 0},
                css=[{
                    'selector': '.dash-cell div.dash-cell-value',
                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                }],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="single",
                editable=True,
                columns=[{"name": i, "id": i} for i in data_upcoming_projects.columns],
                data=data_upcoming_projects.to_dict('records')
            ),
        ]),
        dcc.Tab(id='tab2', value='tab-2', label='Raj Group Marketing Form', children=[
            html.Div([
                html.Div([
                    html.H3("Project Details"),
                    html.Header("Enquiry Key"),
                    dcc.Input(
                        id='enquiry_key',
                        type='text',
                        placeholder='Enquiry Key is locked for User',
                        size=50,
                        disabled=True
                    ),
                    html.Header("Entry Date"),
                    dcc.DatePickerSingle(
                        id='entry_date',
                        placeholder='Select a Date',
                        with_portal=True,
                        display_format="YYYY-MM-DD",
                    ),
                    html.Header("Project Description"),
                    dcc.Input(
                        id='project_description',
                        type='text',
                        placeholder='Enter Project Description',
                        size=50
                    ),
                    html.Header("Scope of Work"),
                    dcc.Dropdown(
                        id='scope_of_work',
                        options=[{'value': i, 'label': i} for i in sow]
                    ),
                ], className="four columns"),
                html.Div([
                    html.H3("Client Details"),
                    html.Header("Client Name"),
                    dcc.Input(
                        id='client_name',
                        type='text',
                        placeholder='Enter Client Name',
                        size=50
                    ),
                    html.Header("Client Location"),
                    dcc.Input(
                        id='client_location',
                        type='text',
                        placeholder='Enter Client Location',
                        size=50
                    ),
                    html.Header("Existing Client"),
                    dcc.RadioItems(
                        id='existing_client',
                        options=[{'value': 'YES', 'label': 'YES'},
                                 {'value': 'NO', 'label': 'NO'}]
                    ),
                    html.Header("Contact Person Name"),
                    dcc.Input(
                        id='contact_person_name',
                        type='text',
                        placeholder='Enter Contact Person Name',
                        size=50
                    ),
                    html.Header("Contact Person Mobile"),
                    dcc.Input(
                        id='contact_person_mobile',
                        type='text',
                        placeholder='Enter Contact Person Mobile',
                        size=50
                    ),
                    html.Header("Contact Person Email"),
                    dcc.Input(
                        id='contact_person_email',
                        type='text',
                        placeholder='Enter Contact Person Email',
                        size=50
                    ),
                ], className="six columns"),
            ], className="row"),

            html.H3("Internal Follow Up"),

            html.Div([
                html.Div([
                    html.Header("Internal Lead"),
                    dcc.Input(
                        id='internal_lead',
                        type='text',
                        placeholder='Internal Lead',
                        size=50
                    ),
                    html.Header("External Lead"),
                    dcc.Input(
                        id='external_lead',
                        type='text',
                        placeholder='External Lead',
                        size=50
                    ),
                    html.Header("Status"),
                    dcc.Dropdown(
                        id='lead_status',
                        options=[{'value': i, 'label': i} for i in lead_status]
                    ),
                ], className="four columns"),
                html.Div([
                    html.Header("Contact Date"),
                    dcc.DatePickerSingle(
                        id='contact_date',
                        placeholder='Contact Date',
                        with_portal=True,
                        display_format="YYYY-MM-DD",
                    ),
                    html.Header("Visit Date"),
                    dcc.DatePickerSingle(
                        id='visit_date',
                        placeholder='Visit Date',
                        with_portal=True,
                        display_format="YYYY-MM-DD",
                    ),
                    html.Header("Enquiry Date"),
                    dcc.DatePickerSingle(
                        id='enquiry_date',
                        placeholder='Enquiry Date',
                        with_portal=True,
                        display_format="YYYY-MM-DD",
                    ),
                    html.Header("Offer Date"),
                    dcc.DatePickerSingle(
                        id='offer_date',
                        placeholder='Offer Date',
                        with_portal=True,
                        display_format="YYYY-MM-DD"
                    ),
                ], className="four columns"),
                html.Div([
                    html.Header("Raj Group Office"),
                    dcc.Dropdown(
                        id='raj_group_office',
                        options=[{'value': i, 'label': i} for i in raj_group_office]
                    ),
                    html.Header("Follow Up Person"),
                    dcc.Dropdown(
                        id='follow_up_person',
                        options=[{'value': i, 'label': i} for i in follow_up_person]
                    ),
                    html.Header("Tentative Project Value"),
                    dcc.Input(
                        id='tentative_project_value',
                        type='text',
                        placeholder='Tentative Project Value',
                        size=50
                    ),
                    html.Header("Quotation Number"),
                    dcc.Input(
                        id='quotation_number',
                        type='text',
                        placeholder='Quotation Number',
                        size=50
                    ),
                    html.Header("Remarks"),
                    dcc.Input(
                        id='remarks',
                        type='text',
                        placeholder='Remarks',
                        size=50
                    ),
                ], className="four columns"),
            ], className="row"),
            html.Div(id="temp", children=[
                html.H3("Offer Details"),
                html.Div([
                    html.Div([
                        html.Header("Add Another Offer"),
                        dcc.ConfirmDialogProvider(
                            children=html.Button(
                                'Add Offer',
                            ),
                            id='add_another_offer',
                            message='Are you sure you want to continue?'
                        ),
                    ], className="four columns")
                ], className="row"),
            ], style={'display': 'none'}),
            html.Div(id="add_offer_div"),
            html.Div([
                html.Div([
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                        'Submit',
                        ),
                        id='submit_button',
                        message='Are you sure you want to continue?'
                    ),
                ], className="six columns"),
                html.Div([
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                        'Close',
                        ),
                        id='close_button',
                        message='Are you sure you want to continue?'
                    )
                ], className="six columns"),
            ], className="row"),
        ])
    ]),
    html.Div(id='tabs-content')
], className="page")


dash_app.layout = return_layout
########################  Layout End ########################


@dash_app.callback([Output('tabs', 'value'),
                    Output('enquiry_key', 'value'),
                    Output('entry_date', 'date'),
                    Output('project_description', 'value'),
                    Output('scope_of_work', 'value'),
                    Output('client_name', 'value'),
                    Output('client_location', 'value'),
                    Output('existing_client', 'value'),
                    Output('contact_person_name', 'value'),
                    Output('contact_person_mobile', 'value'),
                    Output('contact_person_email', 'value'),
                    Output('internal_lead', 'value'),
                    Output('external_lead', 'value'),
                    Output('lead_status', 'value'),
                    Output('contact_date', 'date'),
                    Output('visit_date', 'date'),
                    Output('enquiry_date', 'date'),
                    Output('offer_date', 'date'),
                    Output('raj_group_office', 'value'),
                    Output('follow_up_person', 'value'),
                    Output('tentative_project_value', 'value'),
                    Output('quotation_number', 'value'),
                    Output('remarks', 'value'),
                    Output('upcoming_projects_table', 'data')],
                  [Input('submit_button', 'submit_n_clicks'),
                   Input('close_button', 'submit_n_clicks'),
                   Input('upcoming_projects_table', 'selected_rows'),
                   Input('graph_lead_stages', 'clickData'),
                   Input('service_wise_pie_chart', 'clickData'),
                   Input('pending_offers_pie_chart', 'clickData'),
                   Input('submitted_offers_pie_chart', 'clickData')],
                  [State('upcoming_projects_table', 'derived_virtual_data'),
                   State('enquiry_key', 'value'),
                   State('entry_date', 'date'),
                   State('project_description', 'value'),
                   State('scope_of_work', 'value'),
                   State('client_name', 'value'),
                   State('client_location', 'value'),
                   State('existing_client', 'value'),
                   State('contact_person_name', 'value'),
                   State('contact_person_mobile', 'value'),
                   State('contact_person_email', 'value'),
                   State('internal_lead', 'value'),
                   State('external_lead', 'value'),
                   State('lead_status', 'value'),
                   State('contact_date', 'date'),
                   State('visit_date', 'date'),
                   State('enquiry_date', 'date'),
                   State('offer_date', 'date'),
                   State('raj_group_office', 'value'),
                   State('follow_up_person', 'value'),
                   State('tentative_project_value', 'value'),
                   State('quotation_number', 'value'),
                   State('remarks', 'value'),
                   # State('dispatch_number', 'value'),
                   # State('offer_location', 'value'),
                   State('add_offer_div', 'children')])
def update_output(submit_clicks, close_clicks, row_id, hoverData_lead_status, hoverData_service, hoverData_followup, hoverData_offers,
                  rows, enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client,
                  contact_person_name, contact_person_mobile, contact_person_email, internal_lead, external_lead, lead_status,
                  contact_date, visit_date, enquiry_date, offer_date, raj_group_office, follow_up_person, tentative_project_value,
                  quotation_number, remarks, add_offer_div_value):
    connection = AWSMySQLConn()
    upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList;").to_dict('records')
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 1: "+str(triggered_input))
        print("Enquiry Key: "+str(enquiry_key))
        if triggered_input == 'submit_button' and triggered_input != 'graph_lead_stages' and triggered_input != 'service_wise_pie_chart'\
                and triggered_input != 'pending_offers_pie_chart' and triggered_input != 'submitted_offers_pie_chart':
            if not enquiry_key:
                prev_enquiry_key = connection.execute_query("select count(enquiry_key) as cnt from RajGroupEnquiryList").ix[0]['cnt']
                enquiry_key = "EN_"+str(dt.now().year)+"_"+str(dt.now().month).zfill(2)+"_"+str(prev_enquiry_key+1).zfill(4)
                enquiry_values = [enquiry_key, entry_date, project_description, str(scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  client_name,
                                  client_location, existing_client,
                                  contact_person_name, contact_person_mobile, contact_person_email, internal_lead,
                                  external_lead,
                                  str(lead_status).replace("[", '').replace("]", '').replace("'", ''),
                                  contact_date, visit_date, enquiry_date, offer_date,
                                  str(raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
                                  str(follow_up_person).replace("[", '').replace("]", '').replace("'", ''),
                                  tentative_project_value, quotation_number, remarks]
                enquiry_values = [i if i else '' for i in enquiry_values]

                connection.insert_query('RajGroupEnquiryList', fields_enquiry_list, enquiry_values)
            else:
                connection.execute("UPDATE RajGroupEnquiryList "
                                         "SET entry_date='{}', "
                                         "project_description='{}', "
                                         "scope_of_work='{}', "
                                         "client_name='{}', "
                                         "client_location='{}', "
                                         "existing_client='{}', "
                                         "contact_person_name='{}', "
                                         "contact_person_mobile='{}', "
                                         "contact_person_email='{}', "
                                         "internal_lead='{}', "
                                         "external_lead ='{}', "
                                         "lead_status='{}', "
                                         "contact_date='{}', "
                                         "visit_date='{}', "
                                         "enquiry_date='{}', "
                                         "offer_date='{}', "
                                         "raj_group_office='{}', "
                                         "follow_up_person='{}', "
                                         "tentative_project_value='{}', "
                                         "quotation_number='{}', "
                                         "remarks='{}' "
                                         "where  enquiry_key='{}';".format(entry_date, project_description,
                                  str(scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  client_name,
                                  client_location, existing_client,
                                  contact_person_name, contact_person_mobile, contact_person_email, internal_lead,
                                  external_lead,
                                  str(lead_status).replace("[", '').replace("]", '').replace("'", ''),
                                  contact_date, visit_date, enquiry_date, offer_date,
                                  str(raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
                                  str(follow_up_person).replace("[", '').replace("]", '').replace("'", ''),
                                  tentative_project_value, quotation_number, remarks, enquiry_key))

            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList;").to_dict('records')

            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified
        # elif row_id and rows:
        elif triggered_input == 'upcoming_projects_table' and row_id:
            row_id = row_id[0]
            return 'tab-2', rows[row_id]['enquiry_key'], \
                   rows[row_id]['entry_date'] if str(rows[row_id]['entry_date'])!='0000-00-00' else None, \
                   rows[row_id]['project_description'], rows[row_id]['scope_of_work'], \
                   rows[row_id]['client_name'], rows[row_id]['client_location'], rows[row_id]['existing_client'], \
                   rows[row_id]['contact_person_name'], rows[row_id]['contact_person_mobile'], rows[row_id][
                       'contact_person_email'], rows[row_id]['internal_lead'], rows[row_id]['external_lead'], rows[row_id][
                       'lead_status'], \
                   rows[row_id]['contact_date'] if str(rows[row_id]['contact_date'])!='0000-00-00' else None, \
                   rows[row_id]['visit_date'] if str(rows[row_id]['visit_date'])!='0000-00-00' else None, \
                   rows[row_id]['enquiry_date'] if str(rows[row_id]['enquiry_date'])!='0000-00-00' else None,\
                   rows[row_id]['offer_date'] if str(rows[row_id]['offer_date'])!='0000-00-00' else None, \
                   rows[row_id]['raj_group_office'], rows[row_id][
                       'follow_up_person'], rows[row_id]['tentative_project_value'], rows[row_id]['quotation_number'], \
                   rows[row_id]['remarks'], upcoming_projects_data_modified

        elif triggered_input == 'graph_lead_stages' and hoverData_lead_status:
            status_var = hoverData_lead_status['points'][0]['x']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'service_wise_pie_chart' and hoverData_service:
            # connection = AWSMySQLConn()
            status_var = hoverData_service['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "scope_of_work='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'pending_offers_pie_chart' and hoverData_followup:
            status_var = hoverData_followup['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='ENQUIRY' and "
                                                                       "follow_up_person='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'submitted_offers_pie_chart' and hoverData_offers:
            status_var = hoverData_offers['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='OFFER' and "
                                                                       "follow_up_person='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'close_button':
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified
        else:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified
    else:
        return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
               upcoming_projects_data_modified


@dash_app.callback(Output('temp', 'style'),
                   [Input('offer_date', 'date')],
                   )
def offer_submission(date):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print(triggered_input)
        # followup_log_values = []
        if triggered_input == 'offer_date' and date:
            return {'display': 'block'}
    return {'display': 'none'}


def new_offer_entry(offer_timestamp_id, offer_timestamp, dispatch_id, dispatch_value, offer_location_id, offer_location_value):
    return html.Div([
                    html.Div([
                        html.Header("Offer Date"),
                        dcc.Input(
                            id=offer_timestamp_id,
                            type='text',
                            placeholder='Offer Date is locked for User',
                            size=50,
                            disabled=True,
                            value=offer_timestamp
                        ),
                    ], className="four columns"),
                    html.Div([
                        html.Header("Dispatch Number"),
                        dcc.Input(
                            id=dispatch_id,
                            type='text',
                            placeholder='Dispatch Number',
                            size=50,
                            value=dispatch_value
                        ),
                    ], className="four columns"),
                    html.Div([
                        html.Header("Offer Location on Local Computer"),
                        dcc.Input(
                            id=offer_location_id,
                            type='text',
                            placeholder='Offer Location',
                            size=50,
                            value=offer_location_value
                        ),
                    ], className="four columns"),
                ], className="row")


def add_offer_entry(existing_offer_entries, new_offer_entry):
    existing_offer_entries.append(new_offer_entry)
    new_list = tuple(existing_offer_entries)
    return new_list


@dash_app.callback(Output('add_offer_div', 'children'),
                   [Input('add_another_offer', 'submit_n_clicks'),
                    Input('upcoming_projects_table', 'selected_rows'),
                    Input('submit_button', 'submit_n_clicks'),
                    Input('close_button', 'submit_n_clicks')],
                   [State('enquiry_key', 'value'),
                    State('upcoming_projects_table', 'derived_virtual_data'),
                    State('add_offer_div', 'children')])
def add_new_offer_entry(offer_click, row_id, submit_button, click_button, enquiry_key, rows, add_offer_div_value):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 2: "+str(triggered_input))
        if triggered_input == 'add_another_offer' and offer_click:
            existing_offer_entries = []
            row_id = row_id[0]
            offer_data = connection.execute_query(
                "select * from RajGroupFollowUpLog where enquiry_key='{}'".format(rows[row_id]['enquiry_key']))
            for index, row in offer_data.iterrows():
                existing_offer_entries.append(new_offer_entry("offer_timestamp_id_{}".format(index),
                                                              row['time_stamp'],
                                                              "dispatch_id_{}".format(index),
                                                              row['offer_key'],
                                                              "offer_location_id_{}".format(index),
                                                              row['offer_location']))
            try:
                existing_offer_entries.append(new_offer_entry("offer_timestamp_id_{}".format(index),
                                                              None,
                                                              "dispatch_id_{}".format(index+1),
                                                              None,
                                                              "offer_location_id_{}".format(index+1),
                                                              None))
            except UnboundLocalError:
                existing_offer_entries.append(new_offer_entry("offer_timestamp_id_0", None, "dispatch_id_0", None, "offer_location_id_0", None))
            return existing_offer_entries

        elif triggered_input == 'upcoming_projects_table' and row_id:
            existing_offer_entries = []
            row_id = row_id[0]
            offer_data = connection.execute_query(
                "select * from RajGroupFollowUpLog where enquiry_key='{}'".format(rows[row_id]['enquiry_key']))
            for index, row in offer_data.iterrows():
                existing_offer_entries.append(new_offer_entry("offer_timestamp_id_{}".format(index),
                                                              row['time_stamp'],
                                                              "dispatch_id_{}".format(index),
                                                              row['offer_key'],
                                                              "offer_location_id_{}".format(index),
                                                              row['offer_location']))
            return existing_offer_entries
        elif triggered_input == 'submit_button' and offer_click:
            # pprint.pprint(add_offer_div_value, indent=8)
            if not enquiry_key:
                for i in add_offer_div_value:
                    dispatch_no = i['props']['children'][1]['props']['children'][1]['props']['value']
                    offer_location = i['props']['children'][2]['props']['children'][1]['props']['value']
                    followup_log_values = [enquiry_key, dispatch_no, offer_location]
                    connection.insert_query('RajGroupFollowUpLog', fields_followup_log, followup_log_values)
            else:
                connection.execute("delete from RajGroupFollowUpLog where enquiry_key='{}'".format(enquiry_key))
                for i in add_offer_div_value:
                    dispatch_no = i['props']['children'][1]['props']['children'][1]['props']['value']
                    offer_location = i['props']['children'][2]['props']['children'][1]['props']['value']
                    followup_log_values = [enquiry_key, dispatch_no, offer_location]
                    connection.insert_query('RajGroupFollowUpLog', fields_followup_log, followup_log_values)

            return None
        elif triggered_input == 'close_button':
            return None
        else:
            return None


# @dash_app.callback(
#                     # Output('weekly_leads', 'figure'),
#                     # Output('submitted_offers_pie_chart', 'figure'),
#                     Output('pending_offers_pie_chart', 'figure')
#                     # Output('graph_lead_stages', 'figure'),
#                     # Output('service_wise_pie_chart', 'figure')
#                     ,
#                   [Input('submit_button', 'submit_n_clicks')])
# def update_graphs(submit_clicks):
#     ctx = dash.callback_context
#     ctx_msg = json.dumps({
#         'states': ctx.states,
#         'triggered': ctx.triggered,
#         'inputs': ctx.inputs
#     }, indent=2)
#     if ctx.triggered:
#         triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
#         print("Triggered Input: "+str(triggered_input))
#
#         if triggered_input == 'submit_button':
#             return pending_offers_pie_data()
#             # return weekly_leads_line_data(), submitted_offers_pie_data(), pending_offers_pie_data(), \
#             # lead_stages_bar_data(), service_wise_pie_data()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


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

            if sha256_crypt.verify(form.password.data, password):
                session['logged_in'] = True
                session['username'] = form.username.data
                return redirect(url_for('home'))
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
        connection = AWSMySQLConn()
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

@app.route('/dashboard.html', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    return redirect('/dash')


# keep this as is
if __name__ == '__main__':
    app.run(port=8000)
    # dash_app.run_server(debug=True)