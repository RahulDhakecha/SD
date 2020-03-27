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

connection = AWSMySQLConn()
data_upcoming_projects = connection.execute_query("select * from RajGroupEnquiryList;")

services = list(connection.execute_query("select scope_of_work, count(*) as cnt from RajGroupEnquiryList group by 1")['scope_of_work'])
service_wise_data = list(connection.execute_query("select scope_of_work, count(*) as cnt from RajGroupEnquiryList group by 1")['cnt'])
service_wise_pie_data = [
        {
            'labels': services,
            'values': service_wise_data,
            'type': 'pie',
        },
    ]

pending_offers = connection.execute_query("select follow_up_person, count(*) as cnt from RajGroupEnquiryList where "
                                          "lead_status='ENQUIRY' group by 1")
pending_offers_data = []
for i in follow_up_person:
    try:
        pending_offers_data.append(pending_offers[pending_offers['follow_up_person'] == i]['cnt'].iloc[0])
    except:
        pending_offers_data.append(0)
pending_offers_pie_data = [
        {
            'labels': follow_up_person,
            'values': pending_offers_data,
            'type': 'pie',
            'hole': 0.5,
        },
    ]


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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = dash.Dash(__name__,
                     server=app,
                     routes_pathname_prefix='/dash/',
                     external_stylesheets=external_stylesheets
                     )


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

######################## Layout ########################
dash_app.layout = html.Div([
    dcc.Link('HOME', href='/', refresh=True),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tab1', value='tab-1', label='Raj Group Marketing Dashboard', children=[
            html.Div([
                html.Div([
                    # Pie-chart reflecting submitted offer
                    dcc.Graph(
                        id='submitted_offers_pie_chart',
                        figure={
                            'data': submitted_offers_pie_data,
                            'layout': {
                                'title': 'Raj Group - Submitted Offers',
                                'autosize': True
                            }
                        }
                    ),
                ], className="six columns"),

                html.Div([
                    # Pie-chart reflecting pending offers
                    dcc.Graph(
                        id='pending_offers_pie_chart',
                        figure={
                            'data': pending_offers_pie_data,
                            'layout': {
                                'title': 'Raj Group - Pending Offers'
                            }
                        }
                    ),
                ], className="six columns")

            ], className="row"),
            html.Div([
                html.Div([
                # GRAPH - Lead Stages
                dcc.Graph(
                    id='graph_lead_stages',
                    figure={
                        'data': lead_stages_bar_data,
                        'layout': {
                            'title': 'Raj Group - Lead Status'
                        }
                    }
                ),
                ], className="six columns"),
                html.Div([
                    # Pie-chart reflecting service wise enquiries
                    dcc.Graph(
                        id='service_wise_pie_chart',
                        figure={
                            'data': service_wise_pie_data,
                            'layout': {
                                'title': 'Raj Group - Service Wise Enquiries',
                                'autosize': True
                            }
                        }
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
                        display_format="YYYY-MM-DD",
                        date='0000-00-00'
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

########################  Layout End ########################





# @app.route('/', methods=['GET', 'POST'])
# def base():
#     return render_template('base.html')


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
                  [State('upcoming_projects_table', 'derived_viewport_data'),
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
                   State('remarks', 'value')])
def update_output(submit_clicks, close_clicks, row_id, hoverData_lead_status, hoverData_service, hoverData_followup, hoverData_offers,
                  rows, enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client,
                  contact_person_name, contact_person_mobile, contact_person_email, internal_lead, external_lead, lead_status,
                  contact_date, visit_date, enquiry_date, offer_date, raj_group_office, follow_up_person, tentative_project_value,
                  quotation_number, remarks):
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
        print(triggered_input)

        if triggered_input == 'submit_button':
            print(offer_date)
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
                print(enquiry_values)

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

            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified
        # elif row_id and rows:
        elif triggered_input == 'upcoming_projects_table' and row_id:
            row_id = row_id[0]
            return 'tab-2', rows[row_id]['enquiry_key'], \
                   rows[row_id]['entry_date'] if str(rows[row_id]['entry_date'])!='0000-00-00' else None, \
                   rows[row_id]['project_description'], str(rows[row_id]['scope_of_work']).split(', '), \
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
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified

        elif triggered_input == 'service_wise_pie_chart' and hoverData_service:
            # connection = AWSMySQLConn()
            status_var = hoverData_service['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "scope_of_work='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified

        elif triggered_input == 'pending_offers_pie_chart' and hoverData_followup:
            status_var = hoverData_followup['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='ENQUIRY' and "
                                                                       "follow_up_person='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified

        elif triggered_input == 'submitted_offers_pie_chart' and hoverData_offers:
            status_var = hoverData_offers['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='OFFER' and "
                                                                       "follow_up_person='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified

        elif triggered_input == 'close_button':
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified
        else:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified

    else:
        return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, upcoming_projects_data_modified



# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class POForm(FlaskForm):
    # connection = AWSMySQLConn()
    # default_val = int(connection.get_max_value("RajPO", "order_no")) if connection.get_max_value("RajPO", "order_no") else 0
    po_date = DateField('PO Date', format='%Y-%m-%d')
    po_key = IntegerField('PO Key')
    order_no = IntegerField('Order number')
    po_no = StringField('PO number')
    client_dropdown = SelectField(label='Please select client from drop down', default=None)
    client_name = StringField('Please enter client name if not found in drop down')
    sector_dropdown = SelectField(label='Please select sector from drop down', default=None)
    sector = StringField('Client Sector')
    location_dropdown = SelectField(label='Please select location from drop down', default=None)
    location = StringField('Location')
    po_description = StringField('PO description')
    po_value = StringField('PO Value')
    file_no = StringField('File number')
    tender_file_no = StringField('Tender File number')
    project_status = SelectField(label='Project Status',
                                   choices=[('Complete', 'Complete'),
                                            ('On Hand', 'On Hand')])
    project_incharge = StringField("Project Incharge")
    po_file = FileField("PO file")
    innovative_design = BooleanField('Innovative/Design')
    turnkey = BooleanField('Turnkey')
    maintenance_testing = BooleanField('Maintenance and Testing')
    retrofitting = BooleanField('Retrofitting')
    sitc = BooleanField('SITC')
    supply = BooleanField('Supply')
    itc = BooleanField('ITC')
    bbt = BooleanField('BBT')
    lighting = BooleanField('Lighting')
    cable_earthing = BooleanField('Cable and Earthing')
    liaison = BooleanField('Liaison')
    eht = BooleanField('EHT-66KV')
    telecom_const = BooleanField('Telecom/Construction')
    solar = BooleanField('Solar')

    submit = SubmitField('Submit')


class UPForm(FlaskForm):
    up_key = StringField('UP Key')
    client_dropdown = SelectField(label='Please select client from drop down', default='Alstom')
    client_name = StringField(label='Please enter client name if not found in drop down')
    sector_dropdown = SelectField(label='Please select sector from drop down', default=None)
    sector = StringField('Client Sector')
    location_dropdown = SelectField(label='Please select location from drop down', default=None)
    location = StringField('Location')
    existing_work = SelectField(label='Exsiting Work', choices=[('YES','YES'),('NO','NO')])
    project_description = StringField('Project description')
    work_scope = StringField('Scope of Work')
    project_value = StringField('Project Value')
    start_month = StringField('Project Start Month')
    contact_person_name = StringField("Contact Person Name")
    contact_person_mobile = StringField("Contact Person Mobile")
    contact_person_email = StringField("Contact Person Email")
    internal_lead = StringField("Internal Lead")
    external_lead = StringField("External Lead")
    competition = StringField("Competition")
    last_call = DateField('Last Call', format='%Y-%m-%d')
    last_visit = DateField('Last Visit', format='%Y-%m-%d')
    last_followup = StringField('Last Follow Up')
    enquiry = SelectField(label='Enquiry', choices=[('NO', 'NO'), ('YES', 'YES')])
    final_verdict = SelectField(label='Final Verdict', choices=[('OPEN', 'OPEN'), ('CLOSE', 'CLOSE'), ('HOLD', 'HOLD')])

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


@app.route('/upcoming_projects.html', methods=['GET', 'POST'])
@is_logged_in
def upcoming_projects():

    up_form = UPForm()
    connection = AWSMySQLConn()
    cnt = connection.execute_query("select count(UP_Key) as cnt from Upcoming_Projects").ix[0]['cnt']

    companies = connection.get_unique_values("Raj_PO", "Client")
    companies += ['None']
    locations = connection.get_unique_values("Raj_PO", "Location")
    locations += ['None']
    sectors = connection.get_unique_values("Raj_PO", "Sector")
    sectors += ['None']

    up_form.client_dropdown.choices = [(x, x) for x in companies]
    up_form.location_dropdown.choices = [(x, x) for x in locations]
    up_form.sector_dropdown.choices = [(x, x) for x in sectors]

    if request.method == 'GET':
        default_val = "UP_" + str(dt.now().year) + "_" + str(cnt+1).zfill(4)
        up_form.up_key.data = default_val

    if up_form.validate_on_submit() or request.method == 'POST':
        # flash("Validation in process")
        # "=HYPERLINK(/Users/rahuldhakecha/fees/{},{})".format(form.upload_file.name, form.order_no.data)
        raw_values_up = [
                  up_form.up_key.data,
                  up_form.client_name.data if up_form.client_dropdown.data == "None" else up_form.client_dropdown.data,
                  up_form.sector.data if up_form.sector_dropdown.data == "None" else up_form.sector_dropdown.data,
                  up_form.location.data if up_form.location_dropdown.data == "None" else up_form.location_dropdown.data,
                  up_form.existing_work.data,
                  up_form.project_description.data,
                  up_form.work_scope.data,
                  up_form.project_value.data,
                  up_form.start_month.data,
                  up_form.internal_lead.data,
                  up_form.external_lead.data,
                  up_form.competition.data,
                  up_form.enquiry.data,
                  up_form.final_verdict.data]
        raw_values_company_rep=[
                  up_form.up_key.data,
                  up_form.contact_person_name.data,
                  up_form.contact_person_mobile.data,
                  up_form.contact_person_email.data]
        raw_values_call=[
                  up_form.up_key.data,
                  str(up_form.last_call.data)]
        raw_values_visit = [
                  up_form.up_key.data,
                  str(up_form.last_visit.data)]
        raw_values_followup = [
                  up_form.up_key.data,
                  up_form.last_followup.data]

        print(raw_values_up)
        print(raw_values_call)
        print(raw_values_visit)
        print(raw_values_followup)
        print(raw_values_company_rep)

        connection.insert_query("Upcoming_Projects", fields=fields_up, values=raw_values_up)
        if up_form.last_call.data is not None:
            connection.insert_query("Call_Log", fields=fields_call, values=raw_values_call)
        if up_form.last_visit.data is not None:
            connection.insert_query("Visit_Log", fields=fields_visit, values=raw_values_visit)
        if up_form.last_followup.data != '':
            connection.insert_query("Followup_Log", fields=fields_followup, values=raw_values_followup)
        if up_form.contact_person_name.data != '':
            connection.insert_query("Company_Rep", fields=fields_company_rep, values=raw_values_company_rep)

        return redirect(url_for('upcoming_projects'))
    return render_template('upcoming_projects.html', form=up_form)


# two decorators using the same function
# @app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
@is_logged_in
def index():

    po_form = POForm()
    connection = AWSMySQLConn()
    default_val = int(connection.get_max_value("Raj_PO", "PO_Key")) if connection.get_max_value("Raj_PO",
                                                                                                 "PO_Key") else 0
    companies = connection.get_unique_values("Raj_PO", "Client")
    companies += ['None']
    locations = connection.get_unique_values("Raj_PO", "Location")
    locations += ['None']
    sectors = connection.get_unique_values("Raj_PO", "Sector")
    sectors += ['None']

    po_form.client_dropdown.choices = [(x, x) for x in companies]
    po_form.location_dropdown.choices = [(x, x) for x in locations]
    po_form.sector_dropdown.choices = [(x, x) for x in sectors]

    if request.method == 'GET':
        po_form.po_key.data = default_val + 1

    if po_form.validate_on_submit():
        # flash("Validation in process")
        f = po_form.po_file.data
        f_name = secure_filename(f.filename)
        print(secure_filename(f.filename))

        # "=HYPERLINK(/Users/rahuldhakecha/fees/{},{})".format(form.upload_file.name, form.order_no.data)
        raw_values = [
                  str(po_form.po_date.data),
                  po_form.po_key.data,
                  po_form.order_no.data,
                  po_form.po_no.data,
                  po_form.client_name.data if po_form.client_dropdown.data == "None" else po_form.client_dropdown.data,
                  po_form.sector.data if po_form.sector_dropdown.data == "None" else po_form.sector_dropdown.data,
                  po_form.location.data if po_form.location_dropdown.data == "None" else po_form.location_dropdown.data,
                  po_form.po_description.data,
                  po_form.po_value.data,
                  po_form.file_no.data,
                  po_form.tender_file_no.data,
                  po_form.project_status.data,
                  po_form.project_incharge.data,
                  str('=HYPERLINK("/Users/rahuldhakecha/fees/{}","{}")'.format(f_name, po_form.order_no.data)),
                  po_form.innovative_design.data,
                  po_form.turnkey.data,
                  po_form.maintenance_testing.data,
                  po_form.retrofitting.data,
                  po_form.sitc.data,
                  po_form.supply.data,
                  po_form.itc.data,
                  po_form.bbt.data,
                  po_form.lighting.data,
                  po_form.cable_earthing.data,
                  po_form.liaison.data,
                  po_form.eht.data,
                  po_form.telecom_const.data,
                  po_form.solar.data]

        values = [1 if x is True else 0 if x is False else x for x in raw_values]
        print(values)
        connection = AWSMySQLConn()
        connection.insert_query("Raj_PO", fields=fields, values=values)
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=po_form)


@app.route('/location/<client>', methods=['GET', 'POST'])
@is_logged_in
def location(client):
    print("client: "+str(client))
    if client == "None":
        locations = connection.get_unique_values("Raj_PO", "Location")
        locations += ['None']
    else:
        locations = list(connection.execute_query("select location from Raj_PO where client='{}' group by 1".format(client))['location'])
        locations += ['None']

    if client == "None":
        sectors = connection.get_unique_values("Raj_PO", "Sector")
        sectors += ['None']
    else:
        sectors = list(connection.execute_query("select sector from Raj_PO where client='{}' group by 1".format(client))['sector'])
        sectors += ['None']

    locArray = []
    for loc in locations:
        locObj = {}
        locObj['name'] = loc
        locArray.append(locObj)

    secArray = []
    for sec in sectors:
        secObj = {}
        secObj['name'] = sec
        secArray.append(secObj)

    return jsonify({'locations':locArray, 'sectors':secArray})


@app.route('/sector/<client>', methods=['GET', 'POST'])
@is_logged_in
def sector(client):
    if client == "None":
        sectors = connection.get_unique_values("Raj_PO", "Sector")
        sectors += ['None']
    else:
        sectors = list(connection.execute_query("select sector from Raj_PO where client='{}'".format(client))['sector'])
        sectors += ['None']

    secArray = []
    for sec in sectors:
        secObj = {}
        secObj['name'] = sec
        secArray.append(secObj)

    return jsonify({'sectors': secArray})


# @app.route('/', methods=['GET', 'POST'])
@app.route('/home.html', methods=['GET', 'POST'])
@is_logged_in
def home():
    flash('You are now logged in', 'success')
    form = HomeForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('home.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/data_edit.html', methods=['GET', 'POST'])
@is_logged_in
def data_edit():
    # print("dashboard method")
    connection = AWSMySQLConn()
    # cursor.execute("select * from table_name")
    # data = cursor.fetchall() #data from database
    data = connection.execute_query("select * from Raj_PO;")
    # po_list = []
    result = connection.cursor.execute("select * from Raj_PO limit 5;")
    po_list = connection.cursor.fetchall()
    connection.cursor.close()
    return render_template('data_edit.html', po_list=po_list)
    # return render_template('dashboard_table.html', tables=[data.to_html(classes='data', index=False)], titles=data.columns.values)


@app.route('/dashboard.html', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    return redirect('/dash')


@app.route('/download.html', methods=['GET', 'POST'])
@is_logged_in
def download():
    connection = AWSMySQLConn()
    data = connection.execute_query("select * from Raj_PO;")
    print("Successfully fetched data from database")
    data.to_excel(r"/Users/rahuldhakecha/RajGroup/Raj_PO_list.xlsx", index=False)
    return redirect(url_for('data_edit'))


# Edit PO entry
@app.route('/edit_po/<string:po_key>', methods=['GET', 'POST'])
@is_logged_in
def edit_po(po_key):
    # Create cursor
    connection = AWSMySQLConn()
    # cur = connection.cursor()

    # Get article by id
    result = connection.cursor.execute("SELECT * FROM Raj_PO WHERE PO_Key = %s", [po_key])

    po = connection.cursor.fetchone()

    connection.cursor.close()
    # Get form
    form = POForm(request.form)

    # populate company drop down list
    companies = connection.get_unique_values("Raj_PO", "Client")
    companies += ['None']
    locations = connection.get_unique_values("Raj_PO", "Location")
    locations += ['None']
    sectors = connection.get_unique_values("Raj_PO", "Sector")
    sectors += ['None']

    form.client_dropdown.choices = [(x, x) for x in companies]
    form.location_dropdown.choices = [(x, x) for x in companies]
    form.sector_dropdown.choices = [(x, x) for x in sectors]

    # Populate PO form fields
    # form.order_no.data = po[0]
    # form.po_no.data = po[1]
    # form.date.data = po[2]
    # form.company_name.data = po[3]
    # form.location.data = po[4]
    # form.project_description.data = po[5]
    # form.po_value.data = po[6]
    # form.file_no.data = po[7]
    # form.project_status.data = po[8]
    # form.project_incharge.data = po[9]
    # form.special_design.data = True if po[10] is 1 else False
    # form.telecom.data = po[11]
    # form.eht.data = po[12]
    # form.turnkey.data = po[13]
    # form.liaison.data = po[14]
    # form.solar.data = po[15]
    # form.lighting.data = po[16]
    # form.cable_earthing.data = po[17]
    # form.maintenance_testing.data = po[18]
    # form.bbt.data = po[19]
    # form.sitc_panel.data = po[20]
    # form.retrofitting.data = po[21]

    form.po_date.data=po[1]
    form.po_key.data=po[2]
    form.order_no.data=po[3]
    form.po_no.data=po[4]
    form.client_name.data=po[5]
    form.sector.data=po[6]
    form.location.data=po[7]
    form.po_description.data=po[8]
    form.po_value.data=po[9]
    form.file_no.data=po[10]
    form.tender_file_no.data=po[11]
    form.project_status.data=po[12]
    form.project_incharge.data=po[13]
    form.po_file.data=po[14]
    form.innovative_design.data=po[15]
    form.turnkey.data=po[16]
    form.maintenance_testing.data=po[17]
    form.retrofitting.data=po[18]
    form.sitc.data=po[19]
    form.supply.data=po[20]
    form.itc.data=po[21]
    form.bbt.data=po[22]
    form.lighting.data=po[23]
    form.cable_earthing.data=po[24]
    form.liaison.data=po[25]
    form.eht.data=po[26]
    form.telecom_const.data=po[27]
    form.solar.data=po[28]

    if request.method == 'POST' and form.validate():
        # order_no = request.form['order_no']
        # po_no = request.form['po_no']
        # po_date = request.form['date']
        # company = request.form['company_name']
        # location = request.form['location']
        # project_description = request.form['project_description']
        # po_value = request.form['po_value']
        # file_no = request.form['file_no']
        # project_status = request.form['project_status']
        # project_incharge = request.form['project_incharge']
        # special_design = 1 if request.form.getlist('special_design') else 0
        # telecom = 1 if request.form.getlist('telecom') else 0
        # eht = 1 if request.form.getlist('eht') else 0
        # turnkey = 1 if request.form.getlist('turnkey') else 0
        # liaison = 1 if request.form.getlist('liaison') else 0
        # solar = 1 if request.form.getlist('solar') else 0
        # lighting = 1 if request.form.getlist('lighting') else 0
        # cable_earthing = 1 if request.form.getlist('cable_earthing') else 0
        # maintenance_testing = 1 if request.form.getlist('maintenance_testing') else 0
        # bbt = 1 if request.form.getlist('bbt') else 0
        # sitc_panel = 1 if request.form.getlist('sitc_panel') else 0
        # retrofitting = 1 if request.form.getlist('retrofitting') else 0


        po_date = request.form['po_date']
        po_key = request.form['po_key']
        order_no = request.form['order_no']
        po_no = request.form['po_no']
        client_name = request.form['client_name'] if request.form['client_dropdown'] == "None" else request.form['client_dropdown']
        sector = request.form['sector'] if request.form['sector_dropdown'] == "None" else request.form['sector_dropdown']
        location = request.form['location'] if request.form['location_dropdown'] == "None" else request.form['location_dropdown']
        po_description = request.form['po_description']
        po_value = request.form['po_value']
        file_no = request.form['file_no']
        tender_file_no = request.form['tender_file_no']
        project_status = request.form['project_status']
        project_incharge = request.form['project_incharge']
        file_no = request.form['file_no']
        innovative_design = 1 if request.form.getlist('innovative_design') else 0
        turnkey = 1 if request.form.getlist('turnkey') else 0
        maintenance_testing = 1 if request.form.getlist('maintenance_testing') else 0
        retrofitting = 1 if request.form.getlist('retrofitting') else 0
        sitc = 1 if request.form.getlist('sitc') else 0
        supply = 1 if request.form.getlist('supply') else 0
        itc = 1 if request.form.getlist('itc') else 0
        bbt = 1 if request.form.getlist('bbt') else 0
        lighting = 1 if request.form.getlist('lighting') else 0
        cable_earthing = 1 if request.form.getlist('cable_earthing') else 0
        liaison = 1 if request.form.getlist('liaison') else 0
        eht = 1 if request.form.getlist('eht') else 0
        telecom_const = 1 if request.form.getlist('telecom_const') else 0
        solar = 1 if request.form.getlist('solar') else 0





        # Create Cursor
        connection = AWSMySQLConn()
        # cur = connection.cursor()
        # Execute

        connection.cursor.execute("UPDATE Raj_PO SET \
        po_date=%s\
        ,po_key=%s \
        ,order_no=%s \
        ,po_no=%s \
        ,client=%s \
        ,sector=%s \
        ,location=%s \
        ,po_description=%s \
        ,po_value=%s \
        ,file_no=%s \
        ,tender_file_no=%s \
        ,project_status=%s \
        ,project_incharge=%s \
        ,po_file=%s \
        ,innovative_design=%s \
        ,electrical_turnkey=%s \
        ,maintenance_and_testing=%s \
        ,retrofiting=%s \
        ,sitc=%s \
        ,supply=%s \
        ,itc=%s \
        ,bbt=%s \
        ,lighting=%s \
        ,cable_and_earthing=%s \
        ,liaison=%s \
        ,eht=%s \
        ,telecom_construction=%s \
        ,solar=%s \
        where po_key=%s",
        (po_date
        ,po_key
        ,order_no
        ,po_no
        ,client_name
        ,sector
        ,location
        ,po_description
        ,po_value
        ,file_no
        ,tender_file_no
        ,project_status
        ,project_incharge
        ,file_no
        ,innovative_design
        ,turnkey
        ,maintenance_testing
        ,retrofitting
        ,sitc
        ,supply
        ,itc
        ,bbt
        ,lighting
        ,cable_earthing
        ,liaison
        ,eht
        ,telecom_const
        ,solar
        ,po_key))
        # po_date
        # po_key
        # order_no
        # po_no
        # client_name
        # sector
        # location
        # po_description
        # po_value
        # file_no
        # tender_file_no
        # project_status
        # project_incharge
        # file_no
        # innovative_design
        # turnkey
        # maintenance_testing
        # retrofitting
        # sitc
        # supply
        # itc
        # bbt
        # lighting
        # cable_earthing
        # liaison
        # eht
        # telecom_const
        # solar

        # Commit to DB
        connection.conn.commit()

        #Close connection
        connection.cursor.close()

        flash('PO Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_po.html', form=form)


@app.route('/temp', methods=['GET', 'POST'])
@is_logged_in
def temp():
    return render_template('temp.html')


# keep this as is
if __name__ == '__main__':
    app.run(port=8000)
    # dash_app.run_server(debug=True)


