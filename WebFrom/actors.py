# using python 3
from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify
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

fields = "(po_date \
        ,po_key \
        ,order_no \
        ,po_no \
        ,client \
        ,sector \
        ,location \
        ,po_description \
        ,po_value \
        ,file_no \
        ,tender_file_no \
        ,project_status \
        ,project_incharge \
        ,po_file \
        ,innovative_design \
        ,electrical_turnkey \
        ,maintenance_and_testing \
        ,retrofiting \
        ,sitc \
        ,supply \
        ,itc \
        ,bbt \
        ,lighting \
        ,cable_and_earthing \
        ,liaison \
        ,eht \
        ,telecom_construction \
        ,solar)"


fields_up = "(up_key,client,sector,location,existing_work,project_description,work_scope,project_value,start_month, \
             internal_lead,external_lead,competition,enquiry,final_verdict)"

fields_call = "(reference, call_date)"
fields_visit = "(reference, visit_date)"
fields_followup = "(reference, followup_comment)"
fields_company_rep = "(up_reference,name,mobile,email)"


connection = AWSMySQLConn()
data1 = connection.execute_query("select * from Raj_PO;")
data_upcoming_projects = connection.execute_query("select A.* , B.call_date, C.visit_date, D.followup_comment, E.name \
from Upcoming_Projects as A \
left join \
(select reference, max(call_date) as call_date \
from Call_Log group by 1) as B \
on A.up_key=B.reference \
left join \
(select reference, max(visit_date) as visit_date \
from Visit_Log group by 1) as C \
on A.up_key=C.reference \
left join \
Followup_Log as D \
on A.up_key=D.reference \
left join \
Company_Rep as E \
on A.up_key=E.up_reference;")

lost_opportunities = data_upcoming_projects['Final_Verdict']=='CLOSE'
open_opportunities = data_upcoming_projects['Final_Verdict']=='OPEN'
not_contacted = data_upcoming_projects['call_date'].isnull()
contacted = data_upcoming_projects['call_date'].notnull()
visited = data_upcoming_projects['visit_date'].notnull()
enquiries = data_upcoming_projects['Enquiry']=='YES'
x_crm_stages = ['Lost Opportunities', 'Not contacted', 'Contacted', 'Visited', 'Enquiries']
y_crm_stages = [sum(lost_opportunities), sum(not_contacted), sum(contacted), sum(visited), sum(enquiries)]

internal_leads = data_upcoming_projects.Internal_Lead.unique()




# data_upcoming_projects['id'] = data_upcoming_projects['UP_Key']
# data_upcoming_projects.set_index('id', inplace=True, drop=False)

dash_app = dash.Dash(__name__,
                     server=app,
                     routes_pathname_prefix='/dash/',
                     )


date_col_converted = pd.to_datetime(data1['PO_Date'])
filtered_df = data1[date_col_converted >= '2018-04-01']
cols = list(filtered_df)[-14:-1]
values = []
for c in cols:
    values.append(filtered_df[c].sum(axis=0, skipna=True))



######################## Layout ########################
dash_app.layout = html.Div([

    html.Div([
        # # Refresh Button
        # html.Button('Refresh', id='button'),
        #
        # # First Data Table
        # html.Div([
        #     dash_table.DataTable(id='table',
        #                         style_data={'whiteSpace': 'normal',
        #                                     'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
        #                         style_table={
        #                             'maxHeight': '30',
        #                             'overflowY': 'scroll'
        #                         },
        #                         style_header={
        #                             'backgroundColor': 'rgb(230, 230, 230)',
        #                             'fontWeight': 'bold'
        #                         },
        #                         style_cell={
        #                             'textAlign': 'center'
        #                         },
        #                         style_data_conditional=[
        #                             {
        #                                 'if': {'row_index': 'odd'},
        #                                 'backgroundColor': 'rgb(248, 248, 248)'
        #                             }
        #                         ],
        #                         fixed_rows={'headers': True, 'data': 0},
        #                         css=[{
        #                             'selector': '.dash-cell div.dash-cell-value',
        #                             'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        #                         }],
        #                         filter_action="native",
        #                         sort_action="native",
        #                         sort_mode="multi",
        #                         columns=[{"name": i, "id": i} for i in data1.columns],
        #                         data=data1.to_dict('records')
        #         ),
        # ], className=" twelve columns"),

        # GRAPH - CRM Stages
        html.Div([
            html.Div(
                id='graph_crm'
            ),
            html.Div([
                dcc.Graph(
                    id='graph_crm_stages',
                    figure={
                        'data': [
                            {'x': x_crm_stages, 'y': y_crm_stages, 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Raj Electrical - CRM stages'
                        }
                    }
                ),
            ], className=" twelve columns"
            ), ], className="row "
        ),


        # # Dropdown - employees
        # html.Div([
        #     dcc.Dropdown(
        #         id='crm_internal_lead_dropdown',
        #         options=[{'label': i, 'value': i} for i in internal_leads],
        #         value=''
        #     ),
        # ], style={'width': '49%', 'display': 'inline-block'}),


        # Data Table - Upcoming Projects
        html.Div([
            dash_table.DataTable(id='upcoming_projects_table',
                                style_data={'whiteSpace': 'normal',
                                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
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
                html.Div(id='upcoming_projects_table_container')
        ], className=" twelve columns"),


        # # Date Picker
        # html.Div([
        #     dcc.DatePickerRange(
        #         id='my-date-picker',
        #         # with_portal=True,
        #         min_date_allowed=dt(2004, 1, 1),
        #         max_date_allowed=date_col_converted.max().to_pydatetime(),
        #         initial_visible_month=dt(date_col_converted.max().to_pydatetime().year, date_col_converted.max().to_pydatetime().month, 1),
        #         start_date=(date_col_converted.max() - timedelta(6)).date(),
        #         end_date=date_col_converted.max().date(),
        #     ),
        #     html.Div(id='output-container-date-picker')
        # ], className="row ", style={'marginTop': 30, 'marginBottom': 15}),
        #
        # # GRAPH - Sector Wise Orders
        # html.Div([
        #     html.Div(
        #     id='graph_1'
        #     ),
        #     html.Div([
        #         dcc.Graph(
        #             id='graph_sector_wise_orders',
        #             figure={
        #                 'data': [
        #                     {'x': cols, 'y': values, 'type': 'bar', 'name': 'SF'},
        #                 ],
        #                 'layout': {
        #                     'title': 'Raj Electrical - Service wise Orders'
        #                 }
        #             }
        #         ),
        #     ], className=" twelve columns"
        #     ), ], className="row "
        # ),
        #
        # # GRAPH - Monthly Order Booking
        # html.Div([
        #     html.Div(
        #     id='graph_2'
        #     ),
        #     html.Div([
        #         dcc.Graph(
        #             id='graph_monthly_order_booking',
        #             figure={
        #                 'data': [
        #                     {'x': cols, 'y': values, 'type': 'bar', 'name': 'SF'},
        #                 ],
        #                 'layout': {
        #                     'title': 'Raj Electrical - Service wise Orders'
        #                 }
        #             }
        #         ),
        #     ], className=" twelve columns"
        #     ), ], className="row "
        # ),
        #
        # # GRAPH - Geographic Bubble Plot
        # html.Div([
        #     html.Div(
        #     id='graph_3'
        #     ),
        #     html.Div([
        #         dcc.Graph(
        #             id='graph_geographic_reach'
        #         ),
        #     ], className=" twelve columns"
        #     ), ], className="row "
        # ),

    ], className="subpage")
], className="page")

########################  Layout End ########################

@dash_app.callback(Output('upcoming_projects_table_container', 'children'),
                [Input('upcoming_projects_table', 'data_timestamp'),
                 Input('upcoming_projects_table', 'active_cell'),
                 # Input('upcoming_projects_table', 'selected_row_ids'),
                 Input('upcoming_projects_table', 'data')])
def get_active_cell_value(time_updated,cell_coordinates,table_data):
    # active_row_id = active_cell['row_id'] if active_cell else None
    # print(active_cell)
    # print(selected_row_ids)
    # print(time_updated)
    # print(table_data)
    if time_updated:
        if cell_coordinates['column_id']=='call_date' or cell_coordinates['column_id']=='visit_date' or cell_coordinates['column_id']=='followup_comment':
            print(time_updated)
            print(cell_coordinates)
            print(table_data)
            print(table_data[cell_coordinates['row']][cell_coordinates['column_id']])

            if table_data[cell_coordinates['row']][cell_coordinates['column_id']]!=data_upcoming_projects.ix[cell_coordinates['row_id'],cell_coordinates['column_id']]:
                print("Data needs to be updated")
    # print(time_updated)
    # time_now = round(time.time()) - 2
    # print(time_now)
    # if time_updated >= time_now:
    #     print("IF CONDITION")
    #     # print("Updated following values: "+str(data_upcoming_projects.ix[active_cell['row_id'],active_cell['column_id']]))
    # else:
    #     print("ELSE CONDITION")
        # print("Not Updated following values: " + str(data_upcoming_projects.ix[active_cell['row_id'],active_cell['column_id']]))
    # if active_cell['column_id']=='call_date':
    #     print(data_upcoming_projects.ix[active_cell['row_id'],active_cell['column_id']])
        # connection.insert_query("Call_Log", fields=fields_call, values=[active_cell['row_id'],])
    return cell_coordinates


@dash_app.callback(
    dash.dependencies.Output('upcoming_projects_table', 'data'),
    [dash.dependencies.Input('graph_crm_stages', 'hoverData')])
def update_upcoming_projects_table(hoverData):
    if hoverData:
        print(hoverData['points'][0]['x'])
        if hoverData['points'][0]['x']=='Lost Opportunities':
            data = data_upcoming_projects[lost_opportunities].to_dict('records')
        elif hoverData['points'][0]['x']=='Not contacted':
            data = data_upcoming_projects[np.logical_and(not_contacted,open_opportunities)].to_dict('records')
        elif hoverData['points'][0]['x']=='Contacted':
            data = data_upcoming_projects[np.logical_and(contacted,open_opportunities)].to_dict('records')
        elif hoverData['points'][0]['x']=='Visited':
            data = data_upcoming_projects[np.logical_and(visited,open_opportunities)].to_dict('records')
        elif hoverData['points'][0]['x']=='Enquiries':
            data = data_upcoming_projects[np.logical_and(enquiries,open_opportunities)].to_dict('records')
        else:
            data = data_upcoming_projects.to_dict('records')
    return data


# @dash_app.callback(
#     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
#     [dash.dependencies.Input('crm_internal_lead_dropdown', 'value')])

# # Refresh Button Callback
# @dash_app.callback(Output('upcoming_projects_table', 'data'),
#                    [Input('button', 'n_clicks')])
# def update_upcoming_projects_table(n_clicks):
#     if n_clicks is not None:
#         connection = AWSMySQLConn()
#         new_data_upcoming_projects = connection.execute_query("select A.* , B.call_date, C.visit_date, D.followup_comment, E.name \
#         from Upcoming_Projects as A \
#         left join \
#         Call_Log as B \
#         on A.up_key=B.reference \
#         left join \
#         Visit_Log as C \
#         on A.up_key=C.reference \
#         left join \
#         Followup_Log as D \
#         on A.up_key=D.reference \
#         left join \
#         Company_Rep as E \
#         on A.up_key=E.up_reference;")
#
#         data = new_data_upcoming_projects.to_dict('records')
#         print(data)
#         return data



# # Date Picker Callback
# @dash_app.callback(Output('output-container-date-picker', 'children'),
#               [Input('my-date-picker', 'start_date'),
#                Input('my-date-picker', 'end_date')])
# def update_output(start_date, end_date):
#     string_prefix = 'You have selected '
#     print(start_date)
#     print(end_date)
#     if start_date is not None:
#         start_date = dt.strptime(start_date, '%Y-%m-%d')
#         start_date_string = start_date.strftime('%B %d, %Y')
#         print(string_prefix + start_date_string)
#     #     string_prefix = string_prefix + 'a Start Date of ' + start_date_string + ' | '
#     # if end_date is not None:
#     #     end_date = dt.strptime(end_date, '%Y-%m-%d')
#     #     end_date_string = end_date.strftime('%B %d, %Y')
#     #     days_selected = (end_date - start_date).days
#     #     prior_start_date = start_date - timedelta(days_selected + 1)
#     #     prior_start_date_string = datetime.strftime(prior_start_date, '%B %d, %Y')
#     #     prior_end_date = end_date - timedelta(days_selected + 1)
#     #     prior_end_date_string = datetime.strftime(prior_end_date, '%B %d, %Y')
#     #     string_prefix = string_prefix + 'End Date of ' + end_date_string + ', for a total of ' + str(days_selected + 1) + ' Days. The prior period Start Date was ' + \
#     #     prior_start_date_string + ' | End Date: ' + prior_end_date_string + '.'
#     # if len(string_prefix) == len('You have selected: '):
#     #     return 'Select a date to see it displayed here'
#     # else:
#     #     return string_prefix


# # Callback for the Graph - Sector Wise
# @dash_app.callback(
#    Output('graph_sector_wise_orders', 'figure'),
#    [Input('my-date-picker', 'start_date'),
#     Input('my-date-picker', 'end_date')])
# def update_graph_1(start_date, end_date):
#     new_df = data1[np.logical_and(date_col_converted>=start_date, date_col_converted<=end_date)]
#     fig = update_graph(new_df)
#     return fig
#
#
# def update_graph(new_df):
#     cols = list(new_df)[-14:]
#     values = []
#     for c in cols:
#         values.append(new_df[c].sum(axis=0, skipna=True))
#
#     bar_total_order = go.Figure([go.Bar(
#       x=cols,
#       y=values,
#       text='Sessions YoY (%)', opacity=0.6
#     )])
#
#     return bar_total_order
#
#
# # Callback for the Graph - Month Wise Order Value
# @dash_app.callback(
#    Output('graph_monthly_order_booking', 'figure'),
#    [Input('my-date-picker', 'start_date'),
#     Input('my-date-picker', 'end_date')])
# def update_graph_2(start_date, end_date):
#     new_df = data1[np.logical_and(date_col_converted>=start_date, date_col_converted<=end_date)]
#     fig = update_graph_montly_order_value(new_df)
#     return fig
#
#
# def update_graph_montly_order_value(new_df):
#     cols = list(new_df)[-14:]
#     values = []
#     for c in cols:
#         values.append(new_df[c].sum(axis=0, skipna=True))
#
#     bar_total_order = go.Figure([go.Scatter(
#       x=cols,
#       y=values,
#       text='Sessions YoY (%)', opacity=0.6
#     )])
#     return bar_total_order
#
#
#
# # Callback for the Graph - Geographic Reach
# @dash_app.callback(
#    Output('graph_geographic_reach', 'figure'),
#    [Input('my-date-picker', 'start_date'),
#     Input('my-date-picker', 'end_date')])
# def update_graph_2(start_date, end_date):
#     new_df = data1[np.logical_and(date_col_converted>=start_date, date_col_converted<=end_date)]
#     fig = update_geographic_reach(new_df)
#     return fig
#
#
# def update_geographic_reach(new_df):
#     cols = list(new_df)[-14:]
#     values = []
#     for c in cols:
#         values.append(new_df[c].sum(axis=0, skipna=True))
#
#     # print(new_df.groupby(by=['Location','Client']).apply(list))
#     # print(dict(new_df.groupby(['Location','Client'])['Location','Client'].apply(list)))
#     geo_conn = GeoInfoConn()
#     # locs = ["Surat","Vadodara","Ankleshwar","Dahej","Jhagadia","Vapi","Ahmedabad","Bharuch","Daman","Silvassa",
#     #         "Jambusar","Gandhidham","Mumbai","Panoli","Ukai","Valia","Jamnagar","Rajpipla","Kosamba","Mangrol",
#     #         "Palsana","Navsari","Porbandar","Valsad"]
#     # values = [215,22,173,85,53,35,15,13,5,8,19,25,22,71,5,7,3,20,9,13,8,3,6]
#     locs = ["Surat"]
#     values = [215]
#     lats = []
#     lons = []
#     for loc in locs:
#         lats.append(geo_conn.find_latitude(location=loc))
#         lons.append(geo_conn.find_longitude(location=loc))
#
#
#     fig = go.Figure()
#
#     fig.add_trace(go.Scattergeo(
#         lat=lats,
#         lon=lons,
#         mode="markers+text",
#         # location=['Surat'],
#         text=locs,
#         # hoverinfo="text",
#         # hovertext=[['Dharmanandan','Ankit Gems']],
#         marker=dict(
#             size=values,
#             sizemode='area',
#             color='rgb(33,113,181)',
#             line_width=0
#         )
#         # geo='geo'
#     ))
#
#     fig.update_layout(
#         title=go.layout.Title(
#             text='Raj Group - Geographic Reach'),
#         width=1200,
#         height=1200,
#         geo=go.layout.Geo(
#             resolution=50,
#             scope='asia',
#             showframe=False,
#             showcoastlines=True,
#             showland=True,
#             landcolor="#F0DC82",
#             showocean=True,
#             oceancolor= "#89C5DA",
#             countrycolor="white",
#             coastlinecolor="blue",
#             projection_type='mercator',
#             lonaxis_range=[67.0, 75.0],
#             lataxis_range=[20.0, 25.0],
#             domain=dict(x=[0, 1], y=[0, 1])
#         ),
#         legend_traceorder='reversed'
#     )
#
#     return fig




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
    client_dropdown = SelectField(label='Please select client from drop down', default=None)
    client_name = StringField('Please enter client name if not found in drop down')
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
    result = connection.cursor.execute("select * from Raj_PO;")
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


