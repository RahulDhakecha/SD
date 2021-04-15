# using python 3
import time
start_time = time.time()
import sys, os
sys.path.append(os.path.join(sys.path[0], 'DashLayouts'))
import flask
import io
import socket
from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify, make_response, url_for
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
    fields_client_list, fields_client_rep_list, sow_code, raj_group_office_code, fields_rj_orders_list, master_users, \
    fields_feedback, data_access_rights
from dashLayout import service_wise_pie_data, pending_offers_pie_data, submitted_offers_pie_data, lead_stages_bar_data, \
    weekly_leads_line_data, main_layout, new_offer_entry_layout, new_contact_entry_layout, order_layout, dn_order_layout, rv_order_layout

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
# from flask_caching.backends import FileSystemCache
# from dash_extensions.callback import CallbackCache, Trigger
from flask_caching import Cache
import dash_table
# import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


app = Flask('app')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10

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
                         external_stylesheets=external_stylesheets,
                         suppress_callback_exceptions = True
                         )
    return d_app


dash_app = call_dash_app('/dash/')
dash_app2 = call_dash_app('/dash2/')
dash_app3 = call_dash_app('/dash3/')
# dash_app4 = call_dash_app('/dash4/')
dash_app5 = call_dash_app('/dash5/')

cache = Cache(dash_app.server, config={
    'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 200
})

def get_enquiry_table(session_id, row_value):
    @cache.memoize()
    def query_and_serialize_data(session_id):
        # expensive or user/session-unique data processing step goes here

        if row_value:
            rows = row_value
        else:
            rows = connection.execute_query(
            "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
            "client_location, lead_status, follow_up_person, tentative_project_value  from RajGroupEnquiryList where"
            " follow_up_person like '{}' order by 1 desc;".format("%")).to_dict('records')

        return rows

    return query_and_serialize_data(session_id)


@app.route('/d')
def select_layout():
    username = "%"
    return main_layout
    # return main_layout(data_access_rights[username])


# dash_app.layout = main_layout(data_access_rights['rahul.dhakecha'])
# dash_app.layout = select_layout("%")
dash_app.layout = main_layout
dash_app2.layout = order_layout
dash_app3.layout = dn_order_layout
# dash_app4.layout = re_order_layout
dash_app5.layout = rv_order_layout


@dash_app.callback([Output('tabs', 'value'),
                    Output('enquiry_key', 'value'),
                    Output('entry_date', 'date'),
                    Output('project_description', 'value'),
                    Output('scope_of_work', 'value'),
                    Output('client_name', 'value'),
                    Output('client_location', 'value'),
                    Output('existing_client', 'value'),
                    # Output('contact_person_name', 'value'),
                    # Output('contact_person_mobile', 'value'),
                    # Output('contact_person_email', 'value'),
                    Output('internal_lead', 'value'),
                    Output('external_lead', 'value'),
                    Output('lead_status', 'value'),
                    # Output('contact_date', 'date'),
                    # Output('visit_date', 'date'),
                    # Output('enquiry_date', 'date'),
                    # Output('offer_date', 'date'),
                    Output('raj_group_office', 'value'),
                    Output('follow_up_person', 'value'),
                    Output('tentative_project_value', 'value'),
                    Output('quotation_number', 'value'),
                    Output('remarks', 'value'),
                    Output('modal_display', 'displayed'),
                    Output('upcoming_projects_table', 'data')],
                  [Input('submit_button', 'submit_n_clicks'),
                   Input('close_button', 'submit_n_clicks'),
                   Input('upcoming_projects_table', 'selected_rows'),
                   Input('graph_lead_stages', 'clickData'),
                   Input('service_wise_pie_chart', 'clickData'),
                   Input('pending_offers_pie_chart', 'clickData'),
                   Input('submitted_offers_pie_chart', 'clickData'),
                   Input('client_dropdown', 'value'),
                   Input('session-id', 'children')],
                  # [State('upcoming_projects_table', 'data'),
                  [State('enquiry_key', 'value'),
                   State('entry_date', 'date'),
                   State('project_description', 'value'),
                   State('scope_of_work', 'value'),
                   State('client_name', 'value'),
                   State('client_location', 'value'),
                   State('existing_client', 'value'),
                   State('internal_lead', 'value'),
                   State('external_lead', 'value'),
                   State('lead_status', 'value'),
                   # State('contact_date', 'date'),
                   # State('visit_date', 'date'),
                   # State('enquiry_date', 'date'),
                   # State('offer_date', 'date'),
                   State('raj_group_office', 'value'),
                   State('follow_up_person', 'value'),
                   State('tentative_project_value', 'value'),
                   State('quotation_number', 'value'),
                   State('remarks', 'value'),
                   # State('dispatch_number', 'value'),
                   # State('offer_location', 'value'),
                   State('add_offer_div', 'children'),
                   State('add_contact_div', 'children')])
def update_output(submit_clicks, close_clicks, row_id, hoverData_lead_status, hoverData_service, hoverData_followup, hoverData_offers,
                  client_dropdown, session_id,
                  enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client,
                  internal_lead, external_lead, lead_status,
                  raj_group_office, follow_up_person, tentative_project_value,
                  quotation_number, remarks, add_offer_div_value, add_contact_div_value):
    # upcoming_projects_data_modified = connection.execute_query("select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
    #                                               "client_location, lead_status, follow_up_person from RajGroupEnquiryList;").to_dict('records')
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    # try:
    #     username = session['username']
    # except:
    username = '%'
    print("Session ID: "+str(session_id))
    rows = get_enquiry_table(session_id, None)
    # rows = connection.execute_query(
    #     "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
    #     "client_location, lead_status, follow_up_person, tentative_project_value  from RajGroupEnquiryList where"
    #     " follow_up_person like '{}' order by 1 desc;".format(username)).to_dict('records')
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 1: "+str(triggered_input))
        print("Enquiry Key: "+str(enquiry_key))
        if triggered_input == 'submit_button' and submit_clicks:
            # if any of the required field is None, return to the same page
            if entry_date is None or entry_date == '' or scope_of_work is None or scope_of_work == '' or client_name is None or client_name == '' or client_location is None or client_location == '' or lead_status is None or lead_status == '' or raj_group_office is None or raj_group_office == '' or follow_up_person is None or follow_up_person == '':
                print("Return same page")
                return 'tab-2',enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client, \
                       internal_lead, external_lead, lead_status, \
                       raj_group_office, follow_up_person, tentative_project_value, \
                       quotation_number, remarks, True, rows
            if not enquiry_key:
                prev_enquiry_key = connection.execute_query("select count(enquiry_key) as cnt from RajGroupEnquiryList "
                                                            "where substr(enquiry_key, 4, 4) = '{}' and "
                                                            "substr(enquiry_key, 9, 2) = '{}'".format(
                    str(dt.now().year).zfill(4), str(dt.now().month).zfill(2))).iloc[0]['cnt']
                enquiry_key = "EN_"+str(dt.now().year)+"_"+str(dt.now().month).zfill(2)+"_"+str(prev_enquiry_key+1).zfill(4)
                print("en_key:" + str(enquiry_key))
                enquiry_values = [enquiry_key, entry_date, project_description, str(scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  client_name,
                                  client_location, existing_client,
                                  '', '', '', internal_lead,
                                  external_lead,
                                  str(lead_status).replace("[", '').replace("]", '').replace("'", ''),
                                  '', '', '', '',
                                  str(raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
                                  str(follow_up_person).replace("[", '').replace("]", '').replace("'", ''),
                                  tentative_project_value, quotation_number, remarks]
                enquiry_values = [i if i else '' for i in enquiry_values]
                client_values = [client_name, client_location, enquiry_key]
                client_values = [i if i else '' for i in client_values]
                connection.insert_query('RajGroupClientList', "(client_name, client_location, enquiry_key)", client_values)
                connection.insert_query('RajGroupEnquiryList', fields_enquiry_list, enquiry_values)
                ## update RajGroupFollowUpLog
                if add_offer_div_value:
                    for i in add_offer_div_value:
                        # dispatch_no = i['props']['children'][0]['props']['children'][1]['props']['children'][1]['props'][
                        #     'value']
                        # offer_location = i['props']['children'][0]['props']['children'][2]['props']['children'][1]['props'][
                        #     'value']
                        # submitted_by = i['props']['children'][1]['props']['children'][0]['props']['children'][1]['props'][
                        #     'value']
                        # remarks = i['props']['children'][1]['props']['children'][1]['props']['children'][1]['props'][
                        #     'value']
                        # submitted_to = i['props']['children'][1]['props']['children'][2]['props']['children'][1]['props'][
                        #     'value']
                        dispatch_no = i['props']['children'][1]['props']['children'][1]['props']['value']
                        offer_location = i['props']['children'][2]['props']['children'][1]['props']['value']
                        submitted_by = i['props']['children'][3]['props']['children'][1]['props']['value']
                        remarks = i['props']['children'][4]['props']['children'][1]['props']['value']
                        submitted_to = i['props']['children'][5]['props']['children'][1]['props']['value']
                        followup_log_values = [enquiry_key, dispatch_no, offer_location, submitted_by, remarks, submitted_to]
                        followup_log_mod_values = ['' if i is None else i for i in followup_log_values]
                        connection.insert_query('RajGroupFollowUpLog', fields_followup_log, followup_log_mod_values)
                ## update RajGroupClientRepresentativeList
                try:
                    connection.execute(
                        "delete from RajGroupClientRepresentativeList where enquiry_key='{}'".format(enquiry_key))
                except:
                    pass
                if add_contact_div_value:
                    for i in add_contact_div_value:
                        contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                        contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                        contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                        contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                        client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
                                             contact_person_designation, client_name, client_location, enquiry_key]
                        client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
                        connection.insert_query('RajGroupClientRepresentativeList',
                                                "(contact_person_name, contact_person_mobile, "
                                                "contact_person_email, contact_person_designation, "
                                                "client_name, client_location, enquiry_key)",
                                                client_rep_mod_values)

            else:
                connection.execute("UPDATE RajGroupClientList SET client_name='{}', client_location='{}' where "
                                   "enquiry_key='{}'".format(client_name, client_location, enquiry_key))
                connection.execute("UPDATE RajGroupEnquiryList "
                                         "SET entry_date='{}', "
                                         "project_description='{}', "
                                         "scope_of_work='{}', "
                                         "client_name='{}', "
                                         "client_location='{}', "
                                         "existing_client='{}', "
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
                                  client_location, existing_client, internal_lead,
                                  external_lead,
                                  str(lead_status).replace("[", '').replace("]", '').replace("'", ''),
                                  '', '', '', '',
                                  str(raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
                                  str(follow_up_person).replace("[", '').replace("]", '').replace("'", ''),
                                  tentative_project_value, quotation_number, remarks, enquiry_key))

                ## update RajGroupFollowUpLog
                if add_offer_div_value:
                    # dispatch_no = add_offer_div_value[-1]['props']['children'][0]['props']['children'][1]['props']['children'][1]['props'][
                    #     'value']
                    # offer_location = add_offer_div_value[-1]['props']['children'][0]['props']['children'][2]['props']['children'][1]['props'][
                    #     'value']
                    # submitted_by = add_offer_div_value[-1]['props']['children'][1]['props']['children'][0]['props']['children'][1]['props'][
                    #     'value']
                    # remarks = add_offer_div_value[-1]['props']['children'][1]['props']['children'][1]['props']['children'][1]['props']['value']
                    # submitted_to = add_offer_div_value[-1]['props']['children'][1]['props']['children'][2]['props']['children'][1]['props'][
                    #     'value']
                    dispatch_no = add_offer_div_value[-1]['props']['children'][1]['props']['children'][1]['props']['value']
                    offer_location = add_offer_div_value[-1]['props']['children'][2]['props']['children'][1]['props']['value']
                    submitted_by = add_offer_div_value[-1]['props']['children'][3]['props']['children'][1]['props']['value']
                    remarks = add_offer_div_value[-1]['props']['children'][4]['props']['children'][1]['props']['value']
                    submitted_to = add_offer_div_value[-1]['props']['children'][5]['props']['children'][1]['props']['value']
                    followup_log_values = [enquiry_key, dispatch_no, offer_location, submitted_by, remarks, submitted_to]
                    followup_log_mod_values = ['' if i is None else i for i in followup_log_values]

                    try:
                        count = connection.execute_query("select enquiry_key, count(*) as cnt from "
                                                     "RajGroupFollowUpLog where enquiry_key='{}'"
                                                     "group by 1;".format(enquiry_key)).iloc[0]['cnt']
                    except:
                        count = 0

                    if len(add_offer_div_value) > count:
                        connection.insert_query('RajGroupFollowUpLog', fields_followup_log, followup_log_mod_values)

                ## update RajGroupClientRepresentativeList
                try:
                    connection.execute(
                        "delete from RajGroupClientRepresentativeList where enquiry_key='{}'".format(enquiry_key))
                except:
                    pass
                if add_contact_div_value:
                    for i in add_contact_div_value:
                        contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                        contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                        contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                        contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                        client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
                                             contact_person_designation, client_name, client_location, enquiry_key]
                        client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
                        connection.insert_query('RajGroupClientRepresentativeList',
                                                "(contact_person_name, contact_person_mobile, "
                                                "contact_person_email, contact_person_designation, "
                                                "client_name, client_location, enquiry_key)",
                                                client_rep_mod_values)

            lead_data = connection.execute_query("select lead_status from RajGroupLeadStatus where enquiry_key='{}'".format(enquiry_key))
            if str(lead_status).replace("[", '').replace("]", '').replace("'", '') != "OFFER" and \
                    str(lead_status).replace("[", '').replace("]", '').replace("'", '') not in list(lead_data['lead_status']):
                connection.insert_query("RajGroupLeadStatus", "(enquiry_key, lead_status)", [enquiry_key,
                                                                                                   str(
                                                                                                       lead_status).replace(
                                                                                                       "[", '').replace(
                                                                                                       "]", '').replace(
                                                                                                       "'", '')])

            # upcoming_projects_data_modified = connection.execute_query("select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
            #                                       "client_location, lead_status, follow_up_person from RajGroupEnquiryList;").to_dict('records')

            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   rows
        # elif row_id and rows:
        elif triggered_input == 'upcoming_projects_table' and row_id:
            row_id = row_id[0]
            row_data = connection.execute_query("select * from RajGroupEnquiryList where enquiry_key='{}';".format(rows[row_id]['enquiry_key']))
            return 'tab-2', row_data.iloc[0]['enquiry_key'], \
                   row_data.iloc[0]['entry_date'] if str(row_data.iloc[0]['entry_date']) != '0000-00-00' else None, \
                   row_data.iloc[0]['project_description'], row_data.iloc[0]['scope_of_work'], \
                   row_data.iloc[0]['client_name'], row_data.iloc[0]['client_location'], row_data.iloc[0]['existing_client'], \
                   row_data.iloc[0]['internal_lead'], row_data.iloc[0]['external_lead'], \
                   row_data.iloc[0][
                       'lead_status'], \
                   row_data.iloc[0]['raj_group_office'], row_data.iloc[0][
                       'follow_up_person'], row_data.iloc[0]['tentative_project_value'], row_data.iloc[0]['quotation_number'], \
                   row_data.iloc[0]['remarks'], False, rows

        elif triggered_input == 'client_dropdown' and client_dropdown:
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
            return 'tab-2', enquiry_key, entry_date, project_description, scope_of_work, client_nm, client_loc, existing_client, \
                   internal_lead, external_lead, lead_status, raj_group_office, follow_up_person, tentative_project_value, quotation_number, remarks, \
                   False, rows

        elif triggered_input == 'graph_lead_stages' and hoverData_lead_status:
            status_var = hoverData_lead_status['points'][0]['x']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='{}' and follow_up_person like "
                                                                       "'{}' order by enquiry_key desc;".format(status_var,
                                                                                                               data_access_rights[username])).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   upcoming_projects_data_modified

        elif triggered_input == 'service_wise_pie_chart' and hoverData_service:
            # connection = AWSMySQLConn()
            status_var = hoverData_service['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "scope_of_work='{}' and follow_up_person like "
                                                                       "'{}' order by enquiry_key desc;".format(status_var,
                                                                                                                data_access_rights[username])).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   upcoming_projects_data_modified

        elif triggered_input == 'pending_offers_pie_chart' and hoverData_followup:
            status_var = hoverData_followup['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='ENQUIRY' and "
                                                                       "follow_up_person='{}' order by enquiry_key desc;".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   upcoming_projects_data_modified

        elif triggered_input == 'submitted_offers_pie_chart' and hoverData_offers:
            status_var = hoverData_offers['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='OFFER' and "
                                                                       "follow_up_person='{}' order by enquiry_key desc;".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   upcoming_projects_data_modified

        elif triggered_input == 'close_button' and close_clicks:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   rows
        else:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
                   rows
    else:
        return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
               rows


@dash_app.callback(Output('add_offer_hide', 'style'),
                   [Input('lead_status', 'value'),],
                   )
def offer_submission(lead_status):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggeredd Input 2: "+str(triggered_input))
        # followup_log_values = []
        if triggered_input == 'lead_status' and lead_status and \
                str(lead_status).replace("[", '').replace("]", '').replace("'", '') == "OFFER":
            return {'display': 'block'}
    return {'display': 'none'}


@dash_app.callback(Output('client_dropdown', 'value'),
                   [Input('close_button', 'submit_n_clicks')],
                   [State('upcoming_projects_table', 'selected_rows')],
                   )
def control_client_dropdwon(close_clicks, row_id):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggeredd Input 5: "+str(triggered_input))
        if triggered_input == 'close_button' and close_clicks:
            return None
        if row_id:
            return None
    return None


@dash_app.callback(Output('add_offer_div', 'children'),
                   [Input('add_another_offer', 'submit_n_clicks'),
                    Input('upcoming_projects_table', 'selected_rows'),
                    Input('submit_button', 'submit_n_clicks'),
                    Input('close_button', 'submit_n_clicks'),
                    Input('session-id', 'children')],
                   [State('enquiry_key', 'value'),
                    # State('upcoming_projects_table', 'data'),
                    State('add_offer_div', 'children'),
                    State('scope_of_work', 'value'),
                    State('client_name', 'value'),
                    State('client_location', 'value'),
                    State('raj_group_office', 'value')])
def add_new_offer_entry(offer_click, row_id, submit_button, click_button, session_id, enquiry_key, add_offer_div_value,
                        scope_of_work, client_name, client_location, raj_group_office):
    # connection = AWSMySQLConn()
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    rows = get_enquiry_table(session_id, None)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 3: "+str(triggered_input))
        if triggered_input == 'add_another_offer' and offer_click:
            try:
                prev_sr_no = connection.execute_query("select B.raj_group_office, count(*) as cnt  "
                                                      "from "
                                                      "(select enquiry_key "
                                                      "from RajGroupFollowUpLog "
                                                      "where substr(offer_key, 8, 4) = '{}' "
                                                      "group by 1) as A "
                                                      "left join "
                                                      "RajGroupEnquiryList as B "
                                                      "on A.enquiry_key=B.enquiry_key "
                                                      "where raj_group_office='{}' "
                                                      "group by 1;".format(str(dt.now().year).zfill(4),
                                                                           str(raj_group_office))).iloc[0]['cnt']
            except IndexError:
                prev_sr_no = 0
            rev_no = 1
            existing_offer_entries = []
            if row_id:
                row_id = row_id[0]
                offer_data = connection.execute_query(
                    "select * from RajGroupFollowUpLog where enquiry_key='{}';".format(rows[row_id]['enquiry_key']))
                index = 0
                for index, row in offer_data.iterrows():
                    existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_{}".format(index),
                                                                  row['time_stamp'],
                                                                  "dispatch_id_{}".format(index),
                                                                  row['offer_key'],
                                                                  "offer_location_id_{}".format(index),
                                                                  row['offer_location'],
                                                                  "offer_submitted_id_{}".format(index),
                                                                  row['submitted_by'],
                                                                  "offer_remarks_id_{}".format(index),
                                                                  row['remarks'],
                                                                  "offer_submitted_to_id_{}".format(index),
                                                                  row['submitted_to']
                                                                  ))

                if not offer_data.empty:
                    prev_rev_no = len(offer_data.index)
                    prev_dispatch_no = connection.execute_query(
                        "select offer_key from RajGroupFollowUpLog where enquiry_key='{}' "
                        "order by time_stamp desc limit 1;".format(rows[row_id]['enquiry_key'])).iloc[0]['offer_key']
                    try:
                        new_dispatch_no = prev_dispatch_no.replace(prev_dispatch_no.strip().split("-")[-1],
                                                                   "rev{}".format(prev_rev_no + 1))
                    except:
                        new_dispatch_no = str(prev_dispatch_no) + "-rev{}".format(prev_rev_no + 1)
                    existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_{}".format(index+1),
                                                                  '',
                                                                  "dispatch_id_{}".format(index+1),
                                                                  new_dispatch_no,
                                                                  "offer_location_id_{}".format(index+1),
                                                                  '',
                                                                  "offer_submitted_id_{}".format(index+1),
                                                                  '',
                                                                  "offer_remarks_id_{}".format(index+1),
                                                                  '',
                                                                  "offer_submitted_to_id_{}".format(index + 1),
                                                                  ''
                                                                  ))
                else:
                    new_dispatch_no = "{}-QTN-{}-{}-rev{}".format(raj_group_office_code[raj_group_office],
                                                                         str(dt.now().year),
                                                                         str(prev_sr_no + 1).zfill(4),
                                                                         rev_no)
                    existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_0", '',
                                                                         "dispatch_id_0", new_dispatch_no,
                                                                         "offer_location_id_0", '',
                                                                         "offer_submitted_id_0", '',
                                                                         "offer_remarks_id_0", '',
                                                                         "offer_submitted_to_id_0", ''))
            else:
                new_dispatch_no = "{}-QTN-{}-{}-rev{}".format(raj_group_office_code[raj_group_office],
                                                              str(dt.now().year),
                                                              str(prev_sr_no + 1).zfill(4),
                                                              rev_no)
                existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_0", '',
                                                                     "dispatch_id_0", new_dispatch_no,
                                                                     "offer_location_id_0", '',
                                                                     "offer_submitted_id_0", '',
                                                                     "offer_remarks_id_0", '',
                                                                     "offer_submitted_to_id_0", ''))
            return existing_offer_entries

        elif triggered_input == 'upcoming_projects_table' and row_id:
            existing_offer_entries = []
            row_id = row_id[0]
            offer_data = connection.execute_query(
                "select * from RajGroupFollowUpLog where enquiry_key='{}'".format(rows[row_id]['enquiry_key']))
            for index, row in offer_data.iterrows():
                existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_{}".format(index),
                                                              row['time_stamp'],
                                                              "dispatch_id_{}".format(index),
                                                              row['offer_key'],
                                                              "offer_location_id_{}".format(index),
                                                              row['offer_location'],
                                                              "offer_submitted_id_{}".format(index),
                                                              row['submitted_by'],
                                                              "offer_remarks_id_{}".format(index),
                                                              row['remarks'],
                                                              "offer_submitted_to_id_{}".format(index),
                                                              row['submitted_to']
                ))
            return existing_offer_entries
        # elif triggered_input == 'submit_button' and submit_button:
        #     # pprint.pprint(add_offer_div_value, indent=8)
        #     if not enquiry_key:
        #         if add_offer_div_value:
        #             for i in add_offer_div_value:
        #                 dispatch_no = i['props']['children'][0]['props']['children'][1]['props']['children'][1]['props'][
        #                     'value']
        #                 offer_location = i['props']['children'][0]['props']['children'][2]['props']['children'][1]['props'][
        #                     'value']
        #                 submitted_by = i['props']['children'][1]['props']['children'][0]['props']['children'][1]['props'][
        #                     'value']
        #                 remarks = i['props']['children'][1]['props']['children'][1]['props']['children'][1]['props'][
        #                     'value']
        #                 followup_log_values = [enquiry_key, dispatch_no, offer_location, submitted_by, remarks]
        #                 followup_log_mod_values = ['' if i is None else i for i in followup_log_values]
        #                 connection.insert_query('RajGroupFollowUpLog', fields_followup_log, followup_log_mod_values)
        #     else:
        #         if add_offer_div_value:
        #             dispatch_no = add_offer_div_value[-1]['props']['children'][0]['props']['children'][1]['props']['children'][1]['props'][
        #                 'value']
        #             offer_location = add_offer_div_value[-1]['props']['children'][0]['props']['children'][2]['props']['children'][1]['props'][
        #                 'value']
        #             submitted_by = add_offer_div_value[-1]['props']['children'][1]['props']['children'][0]['props']['children'][1]['props'][
        #                 'value']
        #             remarks = add_offer_div_value[-1]['props']['children'][1]['props']['children'][1]['props']['children'][1]['props']['value']
        #             followup_log_values = [enquiry_key, dispatch_no, offer_location, submitted_by, remarks]
        #             followup_log_mod_values = ['' if i is None else i for i in followup_log_values]
        #             connection.insert_query('RajGroupFollowUpLog', fields_followup_log, followup_log_mod_values)
        #
        #     return None
        elif triggered_input == 'close_button':
            return None
        else:
            return None


@dash_app.callback(Output('add_contact_div', 'children'),
                   [Input('add_another_contact', 'submit_n_clicks'),
                    Input('upcoming_projects_table', 'selected_rows'),
                    Input('submit_button', 'submit_n_clicks'),
                    Input('close_button', 'submit_n_clicks'),
                    Input('client_dropdown', 'value'),
                    Input('delete_contact_button', 'submit_n_clicks'),
                    Input('session-id', 'children')],
                   [State('enquiry_key', 'value'),
                    # State('upcoming_projects_table', 'data'),
                    State('add_contact_div', 'children'),
                    State('client_name', 'value'),
                    State('client_location', 'value')])
def add_new_contact_entry(contact_click, row_id, submit_button, close_button, client_dropdown, delete_contact, session_id,
                          enquiry_key, add_contact_div_value, client_name, client_location):
    # connection = AWSMySQLConn()
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    rows = get_enquiry_table(session_id, None)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 4: " + str(triggered_input))
        if triggered_input == 'add_another_contact' and contact_click:
            existing_contact_entries = []
            index = 0
            if add_contact_div_value:
                for index, i in enumerate(add_contact_div_value):
                    contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                    contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                    contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                    contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                    existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                                             contact_person_name,
                                                                             "contact_person_mobile_id_{}".format(
                                                                                 index),
                                                                             contact_person_mobile,
                                                                             "contact_person_email_id_{}".format(index),
                                                                             contact_person_email,
                                                                             "contact_person_designation_id_{}".format(
                                                                                 index),
                                                                             contact_person_designation,
                                                                             "contact_person_id_{}".format(index)
                                                                             ))
            existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_mobile_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_email_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_designation_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_id_{}".format(index+1)
                                                                  ))
            return existing_contact_entries

        elif triggered_input == 'upcoming_projects_table' and row_id:
            existing_contact_entries = []
            row_id = row_id[0]
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where enquiry_key='{}'".format(rows[row_id]['enquiry_key']))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                              row['contact_person_name'],
                                                              "contact_person_mobile_id_{}".format(index),
                                                              row['contact_person_mobile'],
                                                              "contact_person_email_id_{}".format(index),
                                                              row['contact_person_email'],
                                                              "contact_person_designation_id_{}".format(index),
                                                              row['contact_person_designation'],
                                                              "contact_person_id_{}".format(index)
                                                              ))
            return existing_contact_entries

        elif triggered_input == 'client_dropdown' and client_dropdown and client_dropdown != 'Other':
            cl_nm = str(client_dropdown).split(" -- ")[0]
            cl_lc = str(client_dropdown).split(" -- ")[1]
            existing_contact_entries = []
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where client_name='{}' and client_location='{}' group by 1,2,3,4;".format(cl_nm, cl_lc))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                              row['contact_person_name'],
                                                              "contact_person_mobile_id_{}".format(index),
                                                              row['contact_person_mobile'],
                                                              "contact_person_email_id_{}".format(index),
                                                              row['contact_person_email'],
                                                              "contact_person_designation_id_{}".format(index),
                                                              row['contact_person_designation'],
                                                              "contact_person_id_{}".format(index)
                                                              ))
                # if index>2:
                #     break
            return existing_contact_entries
        elif triggered_input == 'delete_contact_button' and delete_contact:
            print(add_contact_div_value)
            existing_contact_entries = []
            index = 0
            if add_contact_div_value:
                for index, i in enumerate(add_contact_div_value):
                    contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                    contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                    contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                    contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                    contact_person_delete_value = i['props']['children'][4]['props']['children'][0]['props']['value']
                    print(contact_person_delete_value)
                    if contact_person_delete_value != 'Delete':
                        existing_contact_entries.append(
                            new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                     contact_person_name,
                                                     "contact_person_mobile_id_{}".format(
                                                         index),
                                                     contact_person_mobile,
                                                     "contact_person_email_id_{}".format(index),
                                                     contact_person_email,
                                                     "contact_person_designation_id_{}".format(
                                                         index),
                                                     contact_person_designation,
                                                     "contact_person_id_{}".format(index)
                                                     ))
                return existing_contact_entries
        # elif triggered_input == 'submit_button' and submit_button:
        #     # pprint.pprint(add_contact_div_value, indent=8)
        #     try:
        #         connection.execute("delete from RajGroupClientRepresentativeList where enquiry_key='{}'".format(enquiry_key))
        #     except:
        #         pass
        #     if add_contact_div_value:
        #         for i in add_contact_div_value:
        #             contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
        #             contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
        #             contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
        #             contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
        #             client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
        #                                  contact_person_designation, client_name, client_location, enquiry_key]
        #             client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
        #             connection.insert_query('RajGroupClientRepresentativeList', "(contact_person_name, contact_person_mobile, "
        #                                                            "contact_person_email, contact_person_designation, "
        #                                                            "client_name, client_location, enquiry_key)",
        #                                     client_rep_mod_values)
        #     return None
        elif triggered_input == 'close_button':
            return None
        else:
            return None


@dash_app.callback(Output('my_link', 'href'),
                   [Input('file_options', 'value')],
                  )
def download_file(file_options):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 5: " + str(triggered_input))
        if triggered_input == 'file_options' and file_options:
            return '/dash/urlToDownload/RGEnq/'
        return None


@dash_app2.callback(Output('feedback_link', 'children'),
                    [Input('order_status', 'value')],
                    [State('order_key', 'value')])
def add_feedback_entry(order_status, order_key):
    # connection = AWSMySQLConn()
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        print("Triggered Input Feedback Link: "+str(IPAddr))
        if triggered_input == 'order_status' and order_status == 'FEEDBACK':
            url = url_for("feedback", order_key=order_key)
            return "http://18.237.178.54"+url
        else:
            return None


@dash_app2.callback(Output('my_link', 'href'),
                   [Input('file_options', 'value')],
                  )
def download_file(file_options):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 5: " + str(triggered_input))
        if triggered_input == 'file_options' and file_options:
            return '/dash/urlToDownload/'
        return None


@dash_app2.callback([Output('tabs', 'value'),
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
                     Output('order_project_technical', 'value'),
                     Output('order_project_management', 'value'),
                     Output('order_project_supervisor', 'value'),
                     Output('order_modal_display', 'displayed'),
                     Output('orders_table', 'data')],
                  [Input('order_submit_button', 'submit_n_clicks'),
                   Input('order_close_button', 'submit_n_clicks'),
                   Input('order_enquiry_key', 'value'),
                   Input('order_client_dropdown', 'value'),
                   Input('orders_table', 'selected_rows'),
                   Input('orders_scope_pie_chart', 'clickData'),
                   Input('orders_status_pie_chart', 'clickData'),
                   Input('order_key_load_button', 'submit_n_clicks')],
                    [State('orders_table', 'data'),
                     State('order_key', 'value'),
                     State('order_date', 'date'),
                     State('order_po_no', 'value'),
                     State('order_project_description', 'value'),
                     State('order_scope_of_work', 'value'),
                     State('order_client_name', 'value'),
                     State('order_client_location', 'value'),
                     State('order_existing_client', 'value'),
                     State('order_order_no', 'value'),
                     State('order_file_no', 'value'),
                     State('order_status', 'value'),
                     State('order_project_incharge', 'value'),
                     State('order_raj_group_office', 'value'),
                     State('order_project_value', 'value'),
                     State('order_remarks', 'value'),
                     State('order_comp_location', 'value'),
                     State('order_project_technical', 'value'),
                     State('order_project_management', 'value'),
                     State('order_project_supervisor', 'value'),
                     State('order_add_contact_div', 'children')]
                  )
def update_order_values(submit_clicks, close_clicks, order_enquiry_key, client_dropdown, row_id, clickData_scope, clickData_status,
                        order_key_load_button, rows, order_key, order_date, order_po_no,
                        order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client,
                        order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office,
                        order_project_value, order_remarks, order_comp_location, order_project_technical,
                        order_project_management, order_project_supervisor, add_contact_div_value):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 1: "+str(triggered_input))
        print("Enquiry Key: "+str(order_enquiry_key))
        if triggered_input == 'order_enquiry_key' and order_enquiry_key:
            # if any of the required field is None, return to the same page
            existing_enquiry_data = connection.execute_query(
                "select * from RajGroupEnquiryList where enquiry_key='{}';".format(order_enquiry_key))
            return 'tab-2', '', None, '', \
                   existing_enquiry_data.iloc[0]['project_description'], existing_enquiry_data.iloc[0]['scope_of_work'], \
                   existing_enquiry_data.iloc[0]['client_name'], existing_enquiry_data.iloc[0]['client_location'], existing_enquiry_data.iloc[0][
                       'existing_client'], '', '', '', '', \
                   existing_enquiry_data.iloc[0]['raj_group_office'], existing_enquiry_data.iloc[0]['tentative_project_value'], \
                   existing_enquiry_data.iloc[0]['remarks'], '', '', '', '', False, rows
        elif triggered_input == 'order_key_load_button' and order_key_load_button:
            prev_order_key = connection.execute_query("select order_key from RajElectricalsOrdersNew "
                                                      "where substr(order_key, 8, 4) = '{}';".format(str(dt.now().year)))['order_key']
            try:
                prev_order_key_no = max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)])
            except:
                prev_order_key_no = 0
            # if prev_order_key_no <= 2000:
            #     prev_order_key_no = 2000
            new_order_key_no = str(int(prev_order_key_no) + 1).zfill(4)
            # order_key = "{}-{}-{}-ORD-{}-{}-{}".format(raj_group_office_code[order_raj_group_office],
            #                                            str(order_client_name).strip().split(" ")[0],
            #                                            str(order_client_location).strip().split(" ")[0],
            #                                            sow_code[order_scope_of_work],
            #                                            str(dt.now().year),
            #                                            new_order_key_no)
            order_key = "{}-ODR-{}-{}".format('RJ',
                                              str(dt.now().year),
                                              new_order_key_no)

            return 'tab-2', order_key, None, None, \
                   None, None, None, None, None, \
                   None, None, None, None, None, \
                   None, None, None, None, None, None, False, rows

        elif triggered_input == 'order_submit_button' and submit_clicks:
            # if any of the required field is None, return to the same page
            if order_date is None or order_date == '' or order_scope_of_work is None or order_scope_of_work == '' or order_client_name is None or order_client_name == '' or order_client_location is None or order_client_location == '' or order_status is None or order_status == '' or order_raj_group_office is None or order_raj_group_office == '' or order_project_incharge is None or order_project_incharge == '':
                print("Return same page")
                print(order_raj_group_office)
                return 'tab-2', order_key, order_date, order_po_no, \
                       order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client, \
                       order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
                       order_project_value, order_remarks, order_comp_location, order_project_technical, \
                       order_project_management, order_project_supervisor, True, rows
            if not order_order_no:
                prev_order_key = connection.execute_query("select order_key from RajElectricalsOrdersNew "
                                                          "where substr(order_key, 8, 4) = '{}';".format(str(dt.now().year)))['order_key']
                try:
                    prev_order_key_no = max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)])
                except:
                    prev_order_key_no = 0
                # if prev_order_key_no <= 2000:
                #     prev_order_key_no = 2000
                new_order_key_no = str(int(prev_order_key_no)+1).zfill(4)
                # order_key = "{}-{}-{}-ORD-{}-{}-{}".format(raj_group_office_code[order_raj_group_office],
                #                                            str(order_client_name).strip().split(" ")[0],
                #                                            str(order_client_location).strip().split(" ")[0],
                #                                            sow_code[order_scope_of_work],
                #                                            str(dt.now().year),
                #                                            new_order_key_no)
                order_key = "{}-ODR-{}-{}".format(raj_group_office_code[order_raj_group_office],
                                                           str(dt.now().year),
                                                           new_order_key_no)

                order_order_no = new_order_key_no
                print("order_key:" + str(order_key))
                order_values = [order_enquiry_key, order_key, order_date, order_po_no, order_project_description,
                                str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  order_client_name,
                                  order_client_location, order_existing_client, order_order_no, order_file_no,
                                  str(order_status).replace("[", '').replace("]", '').replace("'", '') ,
                                  order_project_incharge, str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
                                order_project_value, order_remarks, "{}".format(order_comp_location).replace('\\', '\\\\'),
                                order_project_technical, order_project_management, order_project_supervisor]
                # "{}".format(str(order_comp_location).replace('"',''))]
                # r'{}'.format(order_comp_location).replace('\\', '\\\\')

                order_values = [i if i else '' for i in order_values]
                client_values = [order_client_name, order_client_location, order_key]
                client_values = [i if i else '' for i in client_values]
                connection.insert_query('RajGroupClientList', "(client_name, client_location, po_key)", client_values)
                connection.insert_query('RajElectricalsOrdersNew', fields_rj_orders_list, order_values)

                ## update RajGroupClientRepresentativeList
                try:
                    connection.execute(
                        "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
                except:
                    pass
                if add_contact_div_value:
                    for i in add_contact_div_value:
                        contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                        contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                        contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                        contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                        client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
                                             contact_person_designation, order_client_name, order_client_location, order_key]
                        client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
                        connection.insert_query('RajGroupClientRepresentativeList',
                                                "(contact_person_name, contact_person_mobile, "
                                                "contact_person_email, contact_person_designation, "
                                                "client_name, client_location, po_key)",
                                                client_rep_mod_values)

            else:
                connection.execute("UPDATE RajGroupClientList SET client_name='{}', client_location='{}' where "
                                   "po_key='{}'".format(order_client_name, order_client_location, order_key))
                connection.execute("UPDATE RajElectricalsOrdersNew "
                                         "SET order_date='{}', "
                                   "po_no='{}', "
                                   "project_description='{}', "
                                         "scope_of_work='{}', "
                                         "client_name='{}', "
                                         "client_location='{}', "
                                         "existing_client='{}', "
                                         "order_no='{}', "
                                         "file_no ='{}', "
                                         "order_status='{}', "
                                         "project_incharge='{}', "
                                         "raj_group_office='{}', "
                                         "project_value='{}', "
                                         "remarks='{}',"
                                         "comp_location='{}',"
                                         "project_technical='{}',"
                                         "project_management='{}',"
                                         "project_supervisor='{}' "
                                         "where  order_key='{}';".format(order_date, order_po_no, order_project_description,
                                  str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  order_client_name,
                                  order_client_location, order_existing_client, order_order_no,
                                  order_file_no,
                                  str(order_status).replace("[", '').replace("]", '').replace("'", ''),
                                                                         str(order_project_incharge).replace("[", '').replace(
                                                                             "]", '').replace("'", ''),
                                  str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),

                                  order_project_value, order_remarks, r'{}'.format(order_comp_location).replace('\\', '\\\\'),
                                                                         order_project_technical, order_project_management,
                                                                         order_project_supervisor, order_key))


                ## update RajGroupClientRepresentativeList
                try:
                    connection.execute(
                        "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
                except:
                    pass
                if add_contact_div_value:
                    for i in add_contact_div_value:
                        contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                        contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                        contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                        contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                        client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
                                             contact_person_designation, order_client_name, order_client_location, order_key]
                        client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
                        connection.insert_query('RajGroupClientRepresentativeList',
                                                "(contact_person_name, contact_person_mobile, "
                                                "contact_person_email, contact_person_designation, "
                                                "client_name, client_location, po_key)",
                                                client_rep_mod_values)


            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, None, False, \
                   rows

        elif triggered_input == 'orders_table' and row_id:
            row_id = row_id[0]
            row_data = connection.execute_query("select * from RajElectricalsOrdersNew where order_key='{}';".format(rows[row_id]['order_key']))
            return 'tab-2', row_data.iloc[0]['order_key'], \
                   row_data.iloc[0]['order_date'] if str(row_data.iloc[0]['order_date']) != '0000-00-00' else None, \
                   row_data.iloc[0]['po_no'], \
                   row_data.iloc[0]['project_description'], row_data.iloc[0]['scope_of_work'], \
                   row_data.iloc[0]['client_name'], row_data.iloc[0]['client_location'], row_data.iloc[0]['existing_client'], \
                   row_data.iloc[0]['order_no'], row_data.iloc[0]['file_no'], \
                   row_data.iloc[0]['order_status'], \
                   row_data.iloc[0]['project_incharge'], row_data.iloc[0]['raj_group_office'], row_data.iloc[0]['project_value'], \
                   row_data.iloc[0]['remarks'], row_data.iloc[0]['comp_location'], row_data.iloc[0]['project_technical'], \
                   row_data.iloc[0]['project_management'], row_data.iloc[0]['project_supervisor'], False, rows

        elif triggered_input == 'order_client_dropdown' and client_dropdown:
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
            return 'tab-2', order_key, order_date, order_po_no, \
                   order_project_description, order_scope_of_work, client_nm, client_loc, existing_client, \
                   order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
                   order_project_value, order_remarks, order_comp_location, order_project_technical, \
                   order_project_management, order_project_supervisor, False, rows

        elif triggered_input == 'orders_scope_pie_chart' and clickData_scope:
            status_var = clickData_scope['points'][0]['label']
            orders_data_modified = connection.execute_query("select * from RajElectricalsOrdersNew where "
                                                                       "scope_of_work='{}' order by order_key desc;".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, None, None, False, \
                   orders_data_modified

        elif triggered_input == 'orders_status_pie_chart' and clickData_status:
            status_var = clickData_status['points'][0]['label']
            orders_data_modified = connection.execute_query("select * from RajElectricalsOrdersNew where "
                                                                       "order_status='{}' order by order_key desc;".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, None, False, \
                   orders_data_modified

        else:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, None, False, \
                   rows
    return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
           None, None, None, False, \
               rows


@dash_app2.callback(Output('order_add_contact_div', 'children'),
                   [Input('order_add_another_contact', 'submit_n_clicks'),
                    Input('orders_table', 'selected_rows'),
                    Input('order_submit_button', 'submit_n_clicks'),
                    Input('order_close_button', 'submit_n_clicks'),
                    Input('order_client_dropdown', 'value'),
                    Input('order_enquiry_key', 'value')],
                   [State('order_key', 'value'),
                    State('orders_table', 'data'),
                    State('order_add_contact_div', 'children'),
                    State('order_client_name', 'value'),
                    State('order_client_location', 'value')])
def order_add_new_contact_entry(contact_click, row_id, submit_button, close_button, client_dropdown, order_enquiry_key, enquiry_key, rows, add_contact_div_value, client_name, client_location):
    # connection = AWSMySQLConn()
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 4: " + str(triggered_input))
        if triggered_input == 'order_add_another_contact' and contact_click:
            existing_contact_entries = []
            index = 0
            if add_contact_div_value:
                for index, i in enumerate(add_contact_div_value):
                    contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                    contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                    contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                    contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                    existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                                             contact_person_name,
                                                                             "contact_person_mobile_id_{}".format(
                                                                                 index),
                                                                             contact_person_mobile,
                                                                             "contact_person_email_id_{}".format(index),
                                                                             contact_person_email,
                                                                             "contact_person_designation_id_{}".format(
                                                                                 index),
                                                                             contact_person_designation
                                                                             ))
            existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_mobile_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_email_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_designation_id_{}".format(index+1),
                                                                  None
                                                                  ))

            return existing_contact_entries

        elif triggered_input == 'orders_table' and row_id:
            existing_contact_entries = []
            row_id = row_id[0]
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where po_key='{}';".format(rows[row_id]['order_key']))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                              row['contact_person_name'],
                                                              "contact_person_mobile_id_{}".format(index),
                                                              row['contact_person_mobile'],
                                                              "contact_person_email_id_{}".format(index),
                                                              row['contact_person_email'],
                                                              "contact_person_designation_id_{}".format(index),
                                                              row['contact_person_designation']
                                                              ))
            return existing_contact_entries

        elif triggered_input == 'order_enquiry_key' and order_enquiry_key:
            existing_contact_entries = []
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where enquiry_key='{}';".format(order_enquiry_key))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                                         row['contact_person_name'],
                                                                         "contact_person_mobile_id_{}".format(index),
                                                                         row['contact_person_mobile'],
                                                                         "contact_person_email_id_{}".format(index),
                                                                         row['contact_person_email'],
                                                                         "contact_person_designation_id_{}".format(
                                                                             index),
                                                                         row['contact_person_designation']
                                                                         ))
            return existing_contact_entries

        elif triggered_input == 'order_client_dropdown' and client_dropdown and client_dropdown != 'Other':
            cl_nm = str(client_dropdown).split(" -- ")[0]
            cl_lc = str(client_dropdown).split(" -- ")[1]
            existing_contact_entries = []
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where client_name='{}' and client_location='{}' group by 1,2,3,4;".format(cl_nm, cl_lc))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                              row['contact_person_name'],
                                                              "contact_person_mobile_id_{}".format(index),
                                                              row['contact_person_mobile'],
                                                              "contact_person_email_id_{}".format(index),
                                                              row['contact_person_email'],
                                                              "contact_person_designation_id_{}".format(index),
                                                              row['contact_person_designation']
                                                              ))
            return existing_contact_entries

        elif triggered_input == 'order_close_button':
            return None
        else:
            return None


# @dash_app3.callback([Output('tabs', 'value'),
#                      Output('order_key', 'value'),
#                      Output('order_date', 'date'),
#                      Output('order_po_no', 'value'),
#                      Output('order_project_description', 'value'),
#                      Output('order_scope_of_work', 'value'),
#                      Output('order_client_name', 'value'),
#                      Output('order_client_location', 'value'),
#                      Output('order_existing_client', 'value'),
#                      Output('order_order_no', 'value'),
#                      Output('order_file_no', 'value'),
#                      Output('order_status', 'value'),
#                      Output('order_project_incharge', 'value'),
#                      Output('order_raj_group_office', 'value'),
#                      Output('order_project_value', 'value'),
#                      Output('order_remarks', 'value'),
#                      Output('order_comp_location', 'value'),
#                      Output('order_modal_display', 'displayed'),
#                      Output('orders_table', 'data')],
#                   [Input('order_submit_button', 'submit_n_clicks'),
#                    Input('order_close_button', 'submit_n_clicks'),
#                    Input('order_enquiry_key', 'value'),
#                    Input('order_client_dropdown', 'value'),
#                    Input('orders_table', 'selected_rows'),
#                    Input('orders_scope_pie_chart', 'clickData'),
#                    Input('orders_status_pie_chart', 'clickData'),
#                    Input('order_key_load_button', 'submit_n_clicks')],
#                     [State('order_key', 'value'),
#                      State('order_date', 'date'),
#                      State('order_po_no', 'value'),
#                      State('order_project_description', 'value'),
#                      State('order_scope_of_work', 'value'),
#                      State('order_client_name', 'value'),
#                      State('order_client_location', 'value'),
#                      State('order_existing_client', 'value'),
#                      State('order_order_no', 'value'),
#                      State('order_file_no', 'value'),
#                      State('order_status', 'value'),
#                      State('order_project_incharge', 'value'),
#                      State('order_raj_group_office', 'value'),
#                      State('order_project_value', 'value'),
#                      State('order_remarks', 'value'),
#                      State('order_comp_location', 'value'),
#                      State('order_add_contact_div', 'children')]
#                   )
# def update_order_values(submit_clicks, close_clicks, order_enquiry_key, client_dropdown, row_id, clickData_scope, clickData_status,
#                         order_key_load_button, order_key, order_date, order_po_no,
#                         order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client,
#                         order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office,
#                         order_project_value, order_remarks, order_comp_location, add_contact_div_value):
#     ctx = dash.callback_context
#     ctx_msg = json.dumps({
#         'states': ctx.states,
#         'triggered': ctx.triggered,
#         'inputs': ctx.inputs
#     }, indent=2)
#     temp_data = connection.execute_query(
#         "select order_key, order_date, project_description, client_name,"
#         "client_location, project_value, scope_of_work, order_status, project_incharge from DNSyndicateOrdersNew order by order_key desc;")
#     rows = temp_data.to_dict('records')
#     if ctx.triggered:
#         triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
#         print("Triggered Input 1: "+str(triggered_input))
#         print("Enquiry Key: "+str(order_enquiry_key))
#         if triggered_input == 'order_enquiry_key' and order_enquiry_key:
#             # if any of the required field is None, return to the same page
#             existing_enquiry_data = connection.execute_query(
#                 "select * from RajGroupEnquiryList where enquiry_key='{}';".format(order_enquiry_key))
#             return 'tab-2', '', None, '', \
#                    existing_enquiry_data.iloc[0]['project_description'], existing_enquiry_data.iloc[0]['scope_of_work'], \
#                    existing_enquiry_data.iloc[0]['client_name'], existing_enquiry_data.iloc[0]['client_location'], existing_enquiry_data.iloc[0][
#                        'existing_client'], '', '', '', '', \
#                    existing_enquiry_data.iloc[0]['raj_group_office'], existing_enquiry_data.iloc[0]['tentative_project_value'], \
#                    existing_enquiry_data.iloc[0]['remarks'], '', False, rows
#
#         elif triggered_input == 'order_key_load_button' and order_key_load_button:
#             prev_order_key = connection.execute_query("select order_key from DNSyndicateOrdersNew;")['order_key']
#             prev_order_key_no = max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)])
#             # if prev_order_key_no <= 2000:
#             #     prev_order_key_no = 2000
#             new_order_key_no = str(int(prev_order_key_no) + 1).zfill(4)
#             # order_key = "{}-{}-{}-ORD-{}-{}-{}".format(raj_group_office_code[order_raj_group_office],
#             #                                            str(order_client_name).strip().split(" ")[0],
#             #                                            str(order_client_location).strip().split(" ")[0],
#             #                                            sow_code[order_scope_of_work],
#             #                                            str(dt.now().year),
#             #                                            new_order_key_no)
#             order_key = "{}-ODR-{}-{}".format('DN',
#                                               str(dt.now().year),
#                                               new_order_key_no)
#
#             return 'tab-2', order_key, None, None, \
#                    None, None, None, None, None, \
#                    None, None, None, None, None, \
#                    None, None, None, False, rows
#
#         elif triggered_input == 'order_submit_button' and submit_clicks:
#             # if any of the required field is None, return to the same page
#             if order_date is None or order_date == '' or order_scope_of_work is None or order_scope_of_work == '' or order_client_name is None or order_client_name == '' or order_client_location is None or order_client_location == '' or order_status is None or order_status == '' or order_raj_group_office is None or order_raj_group_office == '' or order_project_incharge is None or order_project_incharge == '':
#                 print("Return same page")
#                 return 'tab-2', order_key, order_date, order_po_no, \
#                        order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client, \
#                        order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
#                        order_project_value, order_remarks, order_comp_location, True, rows
#             if not order_key:
#                 prev_order_key = connection.execute_query("select order_key from DNSyndicateOrdersNew;")['order_key']
#                 prev_order_key_no = max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)])
#                 new_order_key_no = str(int(prev_order_key_no)+1).zfill(4)
#                 order_key = "{}-ODR-{}-{}".format(raj_group_office_code[order_raj_group_office],
#                                                   str(dt.now().year),
#                                                   new_order_key_no)
#
#                 order_order_no = new_order_key_no
#
#                 # order_key = 1
#                 print("order_key:" + str(order_key))
#                 order_values = [order_enquiry_key, order_key, order_date, order_po_no, order_project_description,
#                                 str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
#                                   order_client_name,
#                                   order_client_location, order_existing_client, order_order_no, order_file_no,
#                                   str(order_status).replace("[", '').replace("]", '').replace("'", '') ,
#                                   order_project_incharge, str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
#                                 order_project_value, order_remarks, "{}".format(str(order_comp_location).replace('"',''))]
#                 order_values = [i if i else '' for i in order_values]
#                 client_values = [order_client_name, order_client_location, order_key]
#                 client_values = [i if i else '' for i in client_values]
#                 connection.insert_query('RajGroupClientList', "(client_name, client_location, po_key)", client_values)
#                 connection.insert_query('DNSyndicateOrdersNew', fields_rj_orders_list, order_values)
#
#                 ## update RajGroupClientRepresentativeList
#                 try:
#                     connection.execute(
#                         "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
#                 except:
#                     pass
#                 if add_contact_div_value:
#                     for i in add_contact_div_value:
#                         contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
#                         contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
#                         contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
#                         contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
#                         client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
#                                              contact_person_designation, order_client_name, order_client_location, order_key]
#                         client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
#                         connection.insert_query('RajGroupClientRepresentativeList',
#                                                 "(contact_person_name, contact_person_mobile, "
#                                                 "contact_person_email, contact_person_designation, "
#                                                 "client_name, client_location, po_key)",
#                                                 client_rep_mod_values)
#
#             else:
#                 connection.execute("UPDATE RajGroupClientList SET client_name='{}', client_location='{}' where "
#                                    "po_key='{}'".format(order_client_name, order_client_location, order_key))
#                 connection.execute("UPDATE DNSyndicateOrdersNew "
#                                          "SET order_date='{}', "
#                                    "po_no='{}', "
#                                    "project_description='{}', "
#                                          "scope_of_work='{}', "
#                                          "client_name='{}', "
#                                          "client_location='{}', "
#                                          "existing_client='{}', "
#                                          "order_no='{}', "
#                                          "file_no ='{}', "
#                                          "order_status='{}', "
#                                          "project_incharge='{}', "
#                                          "raj_group_office='{}', "
#                                          "project_value='{}', "
#                                          "remarks='{}',"
#                                          "comp_location='{}' "
#                                          "where  order_key='{}';".format(order_date, order_po_no, order_project_description,
#                                   str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
#                                   order_client_name,
#                                   order_client_location, order_existing_client, order_order_no,
#                                   order_file_no,
#                                   str(order_status).replace("[", '').replace("]", '').replace("'", ''),
#                                                                          str(order_project_incharge).replace("[", '').replace(
#                                                                              "]", '').replace("'", ''),
#                                   str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
#
#                                   order_project_value, order_remarks, "{}".format(str(order_comp_location).replace('"','')), order_key))
#
#
#                 ## update RajGroupClientRepresentativeList
#                 try:
#                     connection.execute(
#                         "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
#                 except:
#                     pass
#                 if add_contact_div_value:
#                     for i in add_contact_div_value:
#                         contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
#                         contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
#                         contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
#                         contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
#                         client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
#                                              contact_person_designation, order_client_name, order_client_location, order_key]
#                         client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
#                         connection.insert_query('RajGroupClientRepresentativeList',
#                                                 "(contact_person_name, contact_person_mobile, "
#                                                 "contact_person_email, contact_person_designation, "
#                                                 "client_name, client_location, po_key)",
#                                                 client_rep_mod_values)
#
#
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    rows
#
#         elif triggered_input == 'orders_table' and row_id:
#             row_id = row_id[0]
#             row_data = connection.execute_query("select * from DNSyndicateOrdersNew where order_key='{}';".format(rows[row_id]['order_key']))
#             return 'tab-2', row_data.iloc[0]['order_key'], \
#                    row_data.iloc[0]['order_date'] if str(row_data.iloc[0]['order_date']) != '0000-00-00' else None, \
#                    row_data.iloc[0]['po_no'], \
#                    row_data.iloc[0]['project_description'], row_data.iloc[0]['scope_of_work'], \
#                    row_data.iloc[0]['client_name'], row_data.iloc[0]['client_location'], row_data.iloc[0]['existing_client'], \
#                    row_data.iloc[0]['order_no'], row_data.iloc[0]['file_no'], \
#                    row_data.iloc[0]['order_status'], \
#                    row_data.iloc[0]['project_incharge'], row_data.iloc[0]['raj_group_office'], row_data.iloc[0]['project_value'], \
#                    row_data.iloc[0]['remarks'], row_data.iloc[0]['comp_location'], False, rows
#
#         elif triggered_input == 'order_client_dropdown' and client_dropdown:
#             if client_dropdown != 'Other':
#                 client_nm = str(client_dropdown).split(" -- ")[0]
#                 client_loc = str(client_dropdown).split(" -- ")[1]
#                 # client_loc = connection.execute_query("select * from RajGroupClientList where "
#                 #                                                                "client_name='{}';".format(client_dropdown)).iloc[0]['client_location']
#                 existing_client = "YES"
#             else:
#                 client_nm = ''
#                 client_loc = ''
#                 existing_client = "NO"
#             return 'tab-2', order_key, order_date, order_po_no, \
#                    order_project_description, order_scope_of_work, client_nm, client_loc, existing_client, \
#                    order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
#                    order_project_value, order_remarks, order_comp_location, False, rows
#
#         elif triggered_input == 'orders_scope_pie_chart' and clickData_scope:
#             status_var = clickData_scope['points'][0]['label']
#             orders_data_modified = connection.execute_query("select * from DNSyndicateOrdersNew where "
#                                                                        "scope_of_work='{}' order by order_key desc;".format(status_var)).to_dict('records')
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    orders_data_modified
#
#         elif triggered_input == 'orders_status_pie_chart' and clickData_status:
#             status_var = clickData_status['points'][0]['label']
#             orders_data_modified = connection.execute_query("select * from DNSyndicateOrdersNew where "
#                                                                        "order_status='{}' order by order_key desc;".format(status_var)).to_dict('records')
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    orders_data_modified
#
#         else:
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    rows
#     return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                rows
#
#
# @dash_app3.callback(Output('order_add_contact_div', 'children'),
#                    [Input('order_add_another_contact', 'submit_n_clicks'),
#                     Input('orders_table', 'selected_rows'),
#                     Input('order_submit_button', 'submit_n_clicks'),
#                     Input('order_close_button', 'submit_n_clicks'),
#                     Input('order_client_dropdown', 'value'),
#                     Input('order_enquiry_key', 'value')],
#                    [State('order_key', 'value'),
#                     State('order_add_contact_div', 'children'),
#                     State('order_client_name', 'value'),
#                     State('order_client_location', 'value')])
# def order_add_new_contact_entry(contact_click, row_id, submit_button, close_button, client_dropdown, order_enquiry_key, enquiry_key, add_contact_div_value, client_name, client_location):
#     # connection = AWSMySQLConn()
#     ctx = dash.callback_context
#     ctx_msg = json.dumps({
#         'states': ctx.states,
#         'triggered': ctx.triggered,
#         'inputs': ctx.inputs
#     }, indent=2)
#     temp_data = connection.execute_query(
#         "select order_key, order_date, project_description, client_name,"
#         "client_location, project_value, scope_of_work, order_status, project_incharge from DNSyndicateOrdersNew order by order_key desc;")
#     rows = temp_data.to_dict('records')
#     if ctx.triggered:
#         triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
#         print("Triggered Input 4: " + str(triggered_input))
#         if triggered_input == 'order_add_another_contact' and contact_click:
#             existing_contact_entries = []
#             index = 0
#             if add_contact_div_value:
#                 for index, i in enumerate(add_contact_div_value):
#                     contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
#                     contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
#                     contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
#                     contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
#                     existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                                              contact_person_name,
#                                                                              "contact_person_mobile_id_{}".format(
#                                                                                  index),
#                                                                              contact_person_mobile,
#                                                                              "contact_person_email_id_{}".format(index),
#                                                                              contact_person_email,
#                                                                              "contact_person_designation_id_{}".format(
#                                                                                  index),
#                                                                              contact_person_designation
#                                                                              ))
#             existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index+1),
#                                                                   None,
#                                                                   "contact_person_mobile_id_{}".format(index+1),
#                                                                   None,
#                                                                   "contact_person_email_id_{}".format(index+1),
#                                                                   None,
#                                                                   "contact_person_designation_id_{}".format(index+1),
#                                                                   None
#                                                                   ))
#
#             return existing_contact_entries
#
#         elif triggered_input == 'orders_table' and row_id:
#             existing_contact_entries = []
#             row_id = row_id[0]
#             contact_data = connection.execute_query(
#                 "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
#                 " from RajGroupClientRepresentativeList where po_key='{}'".format(rows[row_id]['order_key']))
#             for index, row in contact_data.iterrows():
#                 existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                               row['contact_person_name'],
#                                                               "contact_person_mobile_id_{}".format(index),
#                                                               row['contact_person_mobile'],
#                                                               "contact_person_email_id_{}".format(index),
#                                                               row['contact_person_email'],
#                                                               "contact_person_designation_id_{}".format(index),
#                                                               row['contact_person_designation']
#                                                               ))
#             return existing_contact_entries
#
#         elif triggered_input == 'order_enquiry_key' and order_enquiry_key:
#             existing_contact_entries = []
#             contact_data = connection.execute_query(
#                 "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
#                 " from RajGroupClientRepresentativeList where enquiry_key='{}';".format(order_enquiry_key))
#             for index, row in contact_data.iterrows():
#                 existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                                          row['contact_person_name'],
#                                                                          "contact_person_mobile_id_{}".format(index),
#                                                                          row['contact_person_mobile'],
#                                                                          "contact_person_email_id_{}".format(index),
#                                                                          row['contact_person_email'],
#                                                                          "contact_person_designation_id_{}".format(
#                                                                              index),
#                                                                          row['contact_person_designation']
#                                                                          ))
#             return existing_contact_entries
#
#
#         elif triggered_input == 'order_client_dropdown' and client_dropdown and client_dropdown != 'Other':
#             cl_nm = str(client_dropdown).split(" -- ")[0]
#             cl_lc = str(client_dropdown).split(" -- ")[1]
#             existing_contact_entries = []
#             contact_data = connection.execute_query(
#                 "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
#                 " from RajGroupClientRepresentativeList where client_name='{}' and client_location='{}' group by 1,2,3,4;".format(cl_nm, cl_lc))
#             for index, row in contact_data.iterrows():
#                 existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                               row['contact_person_name'],
#                                                               "contact_person_mobile_id_{}".format(index),
#                                                               row['contact_person_mobile'],
#                                                               "contact_person_email_id_{}".format(index),
#                                                               row['contact_person_email'],
#                                                               "contact_person_designation_id_{}".format(index),
#                                                               row['contact_person_designation']
#                                                               ))
#             return existing_contact_entries
#
#         elif triggered_input == 'order_close_button':
#             return None
#         else:
#             return None


# @dash_app4.callback([Output('tabs', 'value'),
#                      Output('order_key', 'value'),
#                      Output('order_date', 'date'),
#                      Output('order_po_no', 'value'),
#                      Output('order_project_description', 'value'),
#                      Output('order_scope_of_work', 'value'),
#                      Output('order_client_name', 'value'),
#                      Output('order_client_location', 'value'),
#                      Output('order_existing_client', 'value'),
#                      Output('order_order_no', 'value'),
#                      Output('order_file_no', 'value'),
#                      Output('order_status', 'value'),
#                      Output('order_project_incharge', 'value'),
#                      Output('order_raj_group_office', 'value'),
#                      Output('order_project_value', 'value'),
#                      Output('order_remarks', 'value'),
#                      Output('order_comp_location', 'value'),
#                      Output('order_modal_display', 'displayed'),
#                      Output('orders_table', 'data')],
#                   [Input('order_submit_button', 'submit_n_clicks'),
#                    Input('order_close_button', 'submit_n_clicks'),
#                    Input('order_enquiry_key', 'value'),
#                    Input('order_client_dropdown', 'value'),
#                    Input('orders_table', 'selected_rows'),
#                    Input('orders_scope_pie_chart', 'clickData'),
#                    Input('orders_status_pie_chart', 'clickData'),],
#                     [State('orders_table', 'data'),
#                      State('order_key', 'value'),
#                      State('order_date', 'date'),
#                      State('order_po_no', 'value'),
#                      State('order_project_description', 'value'),
#                      State('order_scope_of_work', 'value'),
#                      State('order_client_name', 'value'),
#                      State('order_client_location', 'value'),
#                      State('order_existing_client', 'value'),
#                      State('order_order_no', 'value'),
#                      State('order_file_no', 'value'),
#                      State('order_status', 'value'),
#                      State('order_project_incharge', 'value'),
#                      State('order_raj_group_office', 'value'),
#                      State('order_project_value', 'value'),
#                      State('order_remarks', 'value'),
#                      State('order_comp_location', 'value'),
#                      State('order_add_contact_div', 'children')]
#                   )
# def update_order_values(submit_clicks, close_clicks, order_enquiry_key, client_dropdown, row_id, clickData_scope, clickData_status, rows, order_key, order_date, order_po_no,
#                         order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client,
#                         order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office,
#                         order_project_value, order_remarks, order_comp_location, add_contact_div_value):
#     ctx = dash.callback_context
#     ctx_msg = json.dumps({
#         'states': ctx.states,
#         'triggered': ctx.triggered,
#         'inputs': ctx.inputs
#     }, indent=2)
#     if ctx.triggered:
#         triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
#         print("Triggered Input 1: "+str(triggered_input))
#         print("Enquiry Key: "+str(order_enquiry_key))
#         if triggered_input == 'order_enquiry_key' and order_enquiry_key:
#             # if any of the required field is None, return to the same page
#             existing_enquiry_data = connection.execute_query(
#                 "select * from RajGroupEnquiryList where enquiry_key='{}';".format(order_enquiry_key))
#             return 'tab-2', '', None, '', \
#                    existing_enquiry_data.iloc[0]['project_description'], existing_enquiry_data.iloc[0]['scope_of_work'], \
#                    existing_enquiry_data.iloc[0]['client_name'], existing_enquiry_data.iloc[0]['client_location'], existing_enquiry_data.iloc[0][
#                        'existing_client'], '', '', '', '', \
#                    existing_enquiry_data.iloc[0]['raj_group_office'], existing_enquiry_data.iloc[0]['tentative_project_value'], \
#                    existing_enquiry_data.iloc[0]['remarks'], '', False, rows
#
#         elif triggered_input == 'order_submit_button' and submit_clicks:
#             # if any of the required field is None, return to the same page
#             if order_date is None or order_date == '' or order_scope_of_work is None or order_scope_of_work == '' or order_client_name is None or order_client_name == '' or order_client_location is None or order_client_location == '' or order_status is None or order_status == '' or order_raj_group_office is None or order_raj_group_office == '' or order_project_incharge is None or order_project_incharge == '':
#                 print("Return same page")
#                 return 'tab-2', order_key, order_date, order_po_no, \
#                        order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client, \
#                        order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
#                        order_project_value, order_remarks, order_comp_location, True, rows
#             if not order_key:
#                 prev_order_key = connection.execute_query("select order_key from RajEnterpriseOrdersNew order by order_date "
#                                                           "desc limit 1;").iloc[0]['order_key']
#                 prev_order_key_no = prev_order_key.strip().split("-")[-1]
#                 new_order_key_no = str(int(prev_order_key_no)+1).zfill(4)
#                 order_key = "{}-{}-{}-ORD-{}-{}-{}".format(raj_group_office_code[order_raj_group_office],
#                                                            str(order_client_name).strip().split(" ")[0],
#                                                            str(order_client_location).strip().split(" ")[0],
#                                                            sow_code[order_scope_of_work],
#                                                            str(dt.now().year),
#                                                            new_order_key_no)
#
#                 # order_key = 1
#                 print("order_key:" + str(order_key))
#                 order_values = [order_enquiry_key, order_key, order_date, order_po_no, order_project_description,
#                                 str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
#                                   order_client_name,
#                                   order_client_location, order_existing_client, order_order_no, order_file_no,
#                                   str(order_status).replace("[", '').replace("]", '').replace("'", '') ,
#                                   order_project_incharge, str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
#                                 order_project_value, order_remarks, order_comp_location]
#                 order_values = [i if i else '' for i in order_values]
#                 client_values = [order_client_name, order_client_location, order_key]
#                 client_values = [i if i else '' for i in client_values]
#                 connection.insert_query('RajGroupClientList', "(client_name, client_location, po_key)", client_values)
#                 connection.insert_query('RajEnterpriseOrdersNew', fields_rj_orders_list, order_values)
#
#                 ## update RajGroupClientRepresentativeList
#                 try:
#                     connection.execute(
#                         "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
#                 except:
#                     pass
#                 if add_contact_div_value:
#                     for i in add_contact_div_value:
#                         contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
#                         contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
#                         contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
#                         contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
#                         client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
#                                              contact_person_designation, order_client_name, order_client_location, order_key]
#                         client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
#                         connection.insert_query('RajGroupClientRepresentativeList',
#                                                 "(contact_person_name, contact_person_mobile, "
#                                                 "contact_person_email, contact_person_designation, "
#                                                 "client_name, client_location, po_key)",
#                                                 client_rep_mod_values)
#
#             else:
#                 connection.execute("UPDATE RajGroupClientList SET client_name='{}', client_location='{}' where "
#                                    "po_key='{}'".format(order_client_name, order_client_location, order_key))
#                 connection.execute("UPDATE RajEnterpriseOrdersNew "
#                                          "SET order_date='{}', "
#                                    "po_no='{}', "
#                                    "project_description='{}', "
#                                          "scope_of_work='{}', "
#                                          "client_name='{}', "
#                                          "client_location='{}', "
#                                          "existing_client='{}', "
#                                          "order_no='{}', "
#                                          "file_no ='{}', "
#                                          "order_status='{}', "
#                                          "project_incharge='{}', "
#                                          "raj_group_office='{}', "
#                                          "project_value='{}', "
#                                          "remarks='{}',"
#                                          "comp_location='{}' "
#                                          "where  order_key='{}';".format(order_date, order_po_no, order_project_description,
#                                   str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
#                                   order_client_name,
#                                   order_client_location, order_existing_client, order_order_no,
#                                   order_file_no,
#                                   str(order_status).replace("[", '').replace("]", '').replace("'", ''),
#                                                                          str(order_project_incharge).replace("[", '').replace(
#                                                                              "]", '').replace("'", ''),
#                                   str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
#
#                                   order_project_value, order_remarks, order_comp_location, order_key))
#
#
#                 ## update RajGroupClientRepresentativeList
#                 try:
#                     connection.execute(
#                         "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
#                 except:
#                     pass
#                 if add_contact_div_value:
#                     for i in add_contact_div_value:
#                         contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
#                         contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
#                         contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
#                         contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
#                         client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
#                                              contact_person_designation, order_client_name, order_client_location, order_key]
#                         client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
#                         connection.insert_query('RajGroupClientRepresentativeList',
#                                                 "(contact_person_name, contact_person_mobile, "
#                                                 "contact_person_email, contact_person_designation, "
#                                                 "client_name, client_location, po_key)",
#                                                 client_rep_mod_values)
#
#
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    rows
#
#         elif triggered_input == 'orders_table' and row_id:
#             row_id = row_id[0]
#             row_data = connection.execute_query("select * from RajEnterpriseOrdersNew where order_key='{}';".format(rows[row_id]['order_key']))
#             return 'tab-2', row_data.iloc[0]['order_key'], \
#                    row_data.iloc[0]['order_date'] if str(row_data.iloc[0]['order_date']) != '0000-00-00' else None, \
#                    row_data.iloc[0]['po_no'], \
#                    row_data.iloc[0]['project_description'], row_data.iloc[0]['scope_of_work'], \
#                    row_data.iloc[0]['client_name'], row_data.iloc[0]['client_location'], row_data.iloc[0]['existing_client'], \
#                    row_data.iloc[0]['order_no'], row_data.iloc[0]['file_no'], \
#                    row_data.iloc[0]['order_status'], \
#                    row_data.iloc[0]['project_incharge'], row_data.iloc[0]['raj_group_office'], row_data.iloc[0]['project_value'], \
#                    row_data.iloc[0]['remarks'], row_data.iloc[0]['comp_location'], False, rows
#
#         elif triggered_input == 'order_client_dropdown' and client_dropdown:
#             if client_dropdown != 'Other':
#                 client_nm = str(client_dropdown).split(" -- ")[0]
#                 client_loc = str(client_dropdown).split(" -- ")[1]
#                 # client_loc = connection.execute_query("select * from RajGroupClientList where "
#                 #                                                                "client_name='{}';".format(client_dropdown)).iloc[0]['client_location']
#                 existing_client = "YES"
#             else:
#                 client_nm = ''
#                 client_loc = ''
#                 existing_client = "NO"
#             return 'tab-2', order_key, order_date, order_po_no, \
#                    order_project_description, order_scope_of_work, client_nm, client_loc, existing_client, \
#                    order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
#                    order_project_value, order_remarks, order_comp_location, False, rows
#
#         elif triggered_input == 'orders_scope_pie_chart' and clickData_scope:
#             status_var = clickData_scope['points'][0]['label']
#             orders_data_modified = connection.execute_query("select * from RajEnterpriseOrdersNew where "
#                                                                        "scope_of_work='{}';".format(status_var)).to_dict('records')
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    orders_data_modified
#
#         elif triggered_input == 'orders_status_pie_chart' and clickData_status:
#             status_var = clickData_status['points'][0]['label']
#             orders_data_modified = connection.execute_query("select * from RajEnterpriseOrdersNew where "
#                                                                        "order_status='{}';".format(status_var)).to_dict('records')
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    orders_data_modified
#
#         else:
#             return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                    rows
#     return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, False, \
#                rows
#
#
# @dash_app2.callback(Output('order_add_contact_div', 'children'),
#                    [Input('order_add_another_contact', 'submit_n_clicks'),
#                     Input('orders_table', 'selected_rows'),
#                     Input('order_submit_button', 'submit_n_clicks'),
#                     Input('order_close_button', 'submit_n_clicks'),
#                     Input('order_client_dropdown', 'value'),
#                     Input('order_enquiry_key', 'value')],
#                    [State('order_key', 'value'),
#                     State('orders_table', 'data'),
#                     State('order_add_contact_div', 'children'),
#                     State('order_client_name', 'value'),
#                     State('order_client_location', 'value')])
# def order_add_new_contact_entry(contact_click, row_id, submit_button, close_button, client_dropdown, order_enquiry_key, enquiry_key, rows, add_contact_div_value, client_name, client_location):
#     # connection = AWSMySQLConn()
#     ctx = dash.callback_context
#     ctx_msg = json.dumps({
#         'states': ctx.states,
#         'triggered': ctx.triggered,
#         'inputs': ctx.inputs
#     }, indent=2)
#     if ctx.triggered:
#         triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
#         print("Triggered Input 4: " + str(triggered_input))
#         if triggered_input == 'order_add_another_contact' and contact_click:
#             existing_contact_entries = []
#             index = 0
#             if add_contact_div_value:
#                 for index, i in enumerate(add_contact_div_value):
#                     contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
#                     contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
#                     contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
#                     contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
#                     existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                                              contact_person_name,
#                                                                              "contact_person_mobile_id_{}".format(
#                                                                                  index),
#                                                                              contact_person_mobile,
#                                                                              "contact_person_email_id_{}".format(index),
#                                                                              contact_person_email,
#                                                                              "contact_person_designation_id_{}".format(
#                                                                                  index),
#                                                                              contact_person_designation
#                                                                              ))
#             existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index+1),
#                                                                   None,
#                                                                   "contact_person_mobile_id_{}".format(index+1),
#                                                                   None,
#                                                                   "contact_person_email_id_{}".format(index+1),
#                                                                   None,
#                                                                   "contact_person_designation_id_{}".format(index+1),
#                                                                   None
#                                                                   ))
#
#             return existing_contact_entries
#
#         elif triggered_input == 'orders_table' and row_id:
#             existing_contact_entries = []
#             row_id = row_id[0]
#             contact_data = connection.execute_query(
#                 "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
#                 " from RajGroupClientRepresentativeList where po_key='{}';".format(rows[row_id]['order_key']))
#             for index, row in contact_data.iterrows():
#                 existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                               row['contact_person_name'],
#                                                               "contact_person_mobile_id_{}".format(index),
#                                                               row['contact_person_mobile'],
#                                                               "contact_person_email_id_{}".format(index),
#                                                               row['contact_person_email'],
#                                                               "contact_person_designation_id_{}".format(index),
#                                                               row['contact_person_designation']
#                                                               ))
#             return existing_contact_entries
#
#         elif triggered_input == 'order_enquiry_key' and order_enquiry_key:
#             existing_contact_entries = []
#             contact_data = connection.execute_query(
#                 "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
#                 " from RajGroupClientRepresentativeList where enquiry_key='{}';".format(order_enquiry_key))
#             for index, row in contact_data.iterrows():
#                 existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                                          row['contact_person_name'],
#                                                                          "contact_person_mobile_id_{}".format(index),
#                                                                          row['contact_person_mobile'],
#                                                                          "contact_person_email_id_{}".format(index),
#                                                                          row['contact_person_email'],
#                                                                          "contact_person_designation_id_{}".format(
#                                                                              index),
#                                                                          row['contact_person_designation']
#                                                                          ))
#             return existing_contact_entries
#
#         elif triggered_input == 'order_client_dropdown' and client_dropdown and client_dropdown != 'Other':
#             cl_nm = str(client_dropdown).split(" -- ")[0]
#             cl_lc = str(client_dropdown).split(" -- ")[1]
#             existing_contact_entries = []
#             contact_data = connection.execute_query(
#                 "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
#                 " from RajGroupClientRepresentativeList where client_name='{}' and client_location='{}' group by 1,2,3,4;".format(cl_nm, cl_lc))
#             for index, row in contact_data.iterrows():
#                 existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
#                                                               row['contact_person_name'],
#                                                               "contact_person_mobile_id_{}".format(index),
#                                                               row['contact_person_mobile'],
#                                                               "contact_person_email_id_{}".format(index),
#                                                               row['contact_person_email'],
#                                                               "contact_person_designation_id_{}".format(index),
#                                                               row['contact_person_designation']
#                                                               ))
#             return existing_contact_entries
#
#         elif triggered_input == 'order_close_button':
#             return None
#         else:
#             return None

@dash_app5.callback([Output('tabs', 'value'),
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
                     Output('order_project_technical', 'value'),
                     Output('order_project_management', 'value'),
                     Output('order_project_supervisor', 'value'),
                     Output('order_modal_display', 'displayed'),
                     Output('orders_table', 'data')],
                  [Input('order_submit_button', 'submit_n_clicks'),
                   Input('order_close_button', 'submit_n_clicks'),
                   Input('order_enquiry_key', 'value'),
                   Input('order_client_dropdown', 'value'),
                   Input('orders_table', 'selected_rows'),
                   Input('orders_scope_pie_chart', 'clickData'),
                   Input('orders_status_pie_chart', 'clickData'),
                   Input('order_key_load_button', 'submit_n_clicks')],
                    [State('orders_table', 'data'),
                     State('order_key', 'value'),
                     State('order_date', 'date'),
                     State('order_po_no', 'value'),
                     State('order_project_description', 'value'),
                     State('order_scope_of_work', 'value'),
                     State('order_client_name', 'value'),
                     State('order_client_location', 'value'),
                     State('order_existing_client', 'value'),
                     State('order_order_no', 'value'),
                     State('order_file_no', 'value'),
                     State('order_status', 'value'),
                     State('order_project_incharge', 'value'),
                     State('order_raj_group_office', 'value'),
                     State('order_project_value', 'value'),
                     State('order_remarks', 'value'),
                     State('order_comp_location', 'value'),
                     State('order_project_technical', 'value'),
                     State('order_project_management', 'value'),
                     State('order_project_supervisor', 'value'),
                     State('order_add_contact_div', 'children')]
                  )
def update_order_values(submit_clicks, close_clicks, order_enquiry_key, client_dropdown, row_id, clickData_scope, clickData_status,
                        order_key_load_button, rows, order_key, order_date, order_po_no,
                        order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client,
                        order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office,
                        order_project_value, order_remarks, order_comp_location, order_project_technical,
                        order_project_management, order_project_supervisor, add_contact_div_value):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 1: "+str(triggered_input))
        print("Enquiry Key: "+str(order_enquiry_key))
        if triggered_input == 'order_enquiry_key' and order_enquiry_key:
            # if any of the required field is None, return to the same page
            existing_enquiry_data = connection.execute_query(
                "select * from RajGroupEnquiryList where enquiry_key='{}';".format(order_enquiry_key))
            return 'tab-2', '', None, '', \
                   existing_enquiry_data.iloc[0]['project_description'], existing_enquiry_data.iloc[0]['scope_of_work'], \
                   existing_enquiry_data.iloc[0]['client_name'], existing_enquiry_data.iloc[0]['client_location'], existing_enquiry_data.iloc[0][
                       'existing_client'], '', '', '', '', \
                   existing_enquiry_data.iloc[0]['raj_group_office'], existing_enquiry_data.iloc[0]['tentative_project_value'], \
                   existing_enquiry_data.iloc[0]['remarks'], '', '', '', '', False, rows
        elif triggered_input == 'order_key_load_button' and order_key_load_button:
            prev_order_key = connection.execute_query("select order_key from RajVijtechOrdersNew;")['order_key']
            prev_order_key_no = max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)])
            new_order_key_no = str(int(prev_order_key_no) + 1).zfill(4)
            order_key = "{}-ODR-{}-{}".format('RV',
                                              str(dt.now().year),
                                              new_order_key_no)

            return 'tab-2', order_key, None, None, \
                   None, None, None, None, None, \
                   None, None, None, None, None, \
                   None, None, None, None, None, None, False, rows

        elif triggered_input == 'order_submit_button' and submit_clicks:
            # if any of the required field is None, return to the same page
            if order_date is None or order_date == '' or order_scope_of_work is None or order_scope_of_work == '' or order_client_name is None or order_client_name == '' or order_client_location is None or order_client_location == '' or order_status is None or order_status == '' or order_raj_group_office is None or order_raj_group_office == '' or order_project_incharge is None or order_project_incharge == '':
                print("Return same page")
                return 'tab-2', order_key, order_date, order_po_no, \
                       order_project_description, order_scope_of_work, order_client_name, order_client_location, order_existing_client, \
                       order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
                       order_project_value, order_remarks, order_comp_location, order_project_technical, \
                       order_project_management, order_project_supervisor, True, rows
            if not order_order_no:
                prev_order_key = connection.execute_query("select order_key from RajVijtechOrdersNew;")['order_key']
                prev_order_key_no = max([int(s.strip().split("-")[-1]) for s in list(prev_order_key)])
                new_order_key_no = str(int(prev_order_key_no)+1).zfill(4)
                order_key = "{}-ODR-{}-{}".format(raj_group_office_code[order_raj_group_office],
                                                           str(dt.now().year),
                                                           new_order_key_no)

                order_order_no = new_order_key_no
                print("order_key:" + str(order_key))
                order_values = [order_enquiry_key, order_key, order_date, order_po_no, order_project_description,
                                str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  order_client_name,
                                  order_client_location, order_existing_client, order_order_no, order_file_no,
                                  str(order_status).replace("[", '').replace("]", '').replace("'", '') ,
                                  order_project_incharge, str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
                                order_project_value, order_remarks, r'{}'.format(order_comp_location).replace('\\', '\\\\'),
                                order_project_technical, order_project_management, order_project_supervisor]
                order_values = [i if i else '' for i in order_values]
                client_values = [order_client_name, order_client_location, order_key]
                client_values = [i if i else '' for i in client_values]
                connection.insert_query('RajGroupClientList', "(client_name, client_location, po_key)", client_values)
                connection.insert_query('RajVijtechOrdersNew', fields_rj_orders_list, order_values)

                ## update RajGroupClientRepresentativeList
                try:
                    connection.execute(
                        "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
                except:
                    pass
                if add_contact_div_value:
                    for i in add_contact_div_value:
                        contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                        contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                        contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                        contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                        client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
                                             contact_person_designation, order_client_name, order_client_location, order_key]
                        client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
                        connection.insert_query('RajGroupClientRepresentativeList',
                                                "(contact_person_name, contact_person_mobile, "
                                                "contact_person_email, contact_person_designation, "
                                                "client_name, client_location, po_key)",
                                                client_rep_mod_values)

            else:
                connection.execute("UPDATE RajGroupClientList SET client_name='{}', client_location='{}' where "
                                   "po_key='{}'".format(order_client_name, order_client_location, order_key))
                connection.execute("UPDATE RajVijtechOrdersNew "
                                         "SET order_date='{}', "
                                   "po_no='{}', "
                                   "project_description='{}', "
                                         "scope_of_work='{}', "
                                         "client_name='{}', "
                                         "client_location='{}', "
                                         "existing_client='{}', "
                                         "order_no='{}', "
                                         "file_no ='{}', "
                                         "order_status='{}', "
                                         "project_incharge='{}', "
                                         "raj_group_office='{}', "
                                         "project_value='{}', "
                                         "remarks='{}',"
                                         "comp_location='{}', "
                                         "project_technical='{}',"
                                         "project_management='{}',"
                                         "project_supervisor='{}' "
                                         "where  order_key='{}';".format(order_date, order_po_no, order_project_description,
                                  str(order_scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  order_client_name,
                                  order_client_location, order_existing_client, order_order_no,
                                  order_file_no,
                                  str(order_status).replace("[", '').replace("]", '').replace("'", ''),
                                                                         str(order_project_incharge).replace("[", '').replace(
                                                                             "]", '').replace("'", ''),
                                  str(order_raj_group_office).replace("[", '').replace("]", '').replace("'", ''),

                                  order_project_value, order_remarks, r'{}'.format(order_comp_location).replace('\\', '\\\\'),
                                                                         order_project_technical,
                                                                         order_project_management,
                                                                         order_project_supervisor, order_key))


                ## update RajGroupClientRepresentativeList
                try:
                    connection.execute(
                        "delete from RajGroupClientRepresentativeList where po_key='{}'".format(order_key))
                except:
                    pass
                if add_contact_div_value:
                    for i in add_contact_div_value:
                        contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                        contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                        contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                        contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                        client_rep_values = [contact_person_name, contact_person_mobile, contact_person_email,
                                             contact_person_designation, order_client_name, order_client_location, order_key]
                        client_rep_mod_values = ['' if i is None else i for i in client_rep_values]
                        connection.insert_query('RajGroupClientRepresentativeList',
                                                "(contact_person_name, contact_person_mobile, "
                                                "contact_person_email, contact_person_designation, "
                                                "client_name, client_location, po_key)",
                                                client_rep_mod_values)


            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, False, \
                   rows

        elif triggered_input == 'orders_table' and row_id:
            row_id = row_id[0]
            row_data = connection.execute_query("select * from RajVijtechOrdersNew where order_key='{}';".format(rows[row_id]['order_key']))
            return 'tab-2', row_data.iloc[0]['order_key'], \
                   row_data.iloc[0]['order_date'] if str(row_data.iloc[0]['order_date']) != '0000-00-00' else None, \
                   row_data.iloc[0]['po_no'], \
                   row_data.iloc[0]['project_description'], row_data.iloc[0]['scope_of_work'], \
                   row_data.iloc[0]['client_name'], row_data.iloc[0]['client_location'], row_data.iloc[0]['existing_client'], \
                   row_data.iloc[0]['order_no'], row_data.iloc[0]['file_no'], \
                   row_data.iloc[0]['order_status'], \
                   row_data.iloc[0]['project_incharge'], row_data.iloc[0]['raj_group_office'], row_data.iloc[0]['project_value'], \
                   row_data.iloc[0]['remarks'], row_data.iloc[0]['comp_location'], row_data.iloc[0]['project_technical'], \
                   row_data.iloc[0]['project_management'], row_data.iloc[0]['project_supervisor'], False, rows

        elif triggered_input == 'order_client_dropdown' and client_dropdown:
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
            return 'tab-2', order_key, order_date, order_po_no, \
                   order_project_description, order_scope_of_work, client_nm, client_loc, existing_client, \
                   order_order_no, order_file_no, order_status, order_project_incharge, order_raj_group_office, \
                   order_project_value, order_remarks, order_comp_location, order_project_technical, order_project_management,\
                   order_project_supervisor, False, rows

        elif triggered_input == 'orders_scope_pie_chart' and clickData_scope:
            status_var = clickData_scope['points'][0]['label']
            orders_data_modified = connection.execute_query("select * from RajVijtechOrdersNew where "
                                                                       "scope_of_work='{}' order by order_key desc;".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, None, False, \
                   orders_data_modified

        elif triggered_input == 'orders_status_pie_chart' and clickData_status:
            status_var = clickData_status['points'][0]['label']
            orders_data_modified = connection.execute_query("select * from RajVijtechOrdersNew where "
                                                                       "order_status='{}' order by order_key desc;".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, None, False, \
                   orders_data_modified

        else:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   None, None, None, None, False, \
                   rows
    return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
           None, None, None, False, \
               rows


@dash_app5.callback(Output('order_add_contact_div', 'children'),
                   [Input('order_add_another_contact', 'submit_n_clicks'),
                    Input('orders_table', 'selected_rows'),
                    Input('order_submit_button', 'submit_n_clicks'),
                    Input('order_close_button', 'submit_n_clicks'),
                    Input('order_client_dropdown', 'value'),
                    Input('order_enquiry_key', 'value')],
                   [State('order_key', 'value'),
                    State('orders_table', 'data'),
                    State('order_add_contact_div', 'children'),
                    State('order_client_name', 'value'),
                    State('order_client_location', 'value')])
def order_add_new_contact_entry(contact_click, row_id, submit_button, close_button, client_dropdown, order_enquiry_key, enquiry_key, rows, add_contact_div_value, client_name, client_location):
    # connection = AWSMySQLConn()
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 4: " + str(triggered_input))
        if triggered_input == 'order_add_another_contact' and contact_click:
            existing_contact_entries = []
            index = 0
            if add_contact_div_value:
                for index, i in enumerate(add_contact_div_value):
                    contact_person_name = i['props']['children'][0]['props']['children'][1]['props']['value']
                    contact_person_mobile = i['props']['children'][1]['props']['children'][1]['props']['value']
                    contact_person_email = i['props']['children'][2]['props']['children'][1]['props']['value']
                    contact_person_designation = i['props']['children'][3]['props']['children'][1]['props']['value']
                    existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                                             contact_person_name,
                                                                             "contact_person_mobile_id_{}".format(
                                                                                 index),
                                                                             contact_person_mobile,
                                                                             "contact_person_email_id_{}".format(index),
                                                                             contact_person_email,
                                                                             "contact_person_designation_id_{}".format(
                                                                                 index),
                                                                             contact_person_designation
                                                                             ))
            existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_mobile_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_email_id_{}".format(index+1),
                                                                  None,
                                                                  "contact_person_designation_id_{}".format(index+1),
                                                                  None
                                                                  ))

            return existing_contact_entries

        elif triggered_input == 'orders_table' and row_id:
            existing_contact_entries = []
            row_id = row_id[0]
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where po_key='{}';".format(rows[row_id]['order_key']))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                              row['contact_person_name'],
                                                              "contact_person_mobile_id_{}".format(index),
                                                              row['contact_person_mobile'],
                                                              "contact_person_email_id_{}".format(index),
                                                              row['contact_person_email'],
                                                              "contact_person_designation_id_{}".format(index),
                                                              row['contact_person_designation']
                                                              ))
            return existing_contact_entries

        elif triggered_input == 'order_enquiry_key' and order_enquiry_key:
            existing_contact_entries = []
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where enquiry_key='{}';".format(order_enquiry_key))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                                         row['contact_person_name'],
                                                                         "contact_person_mobile_id_{}".format(index),
                                                                         row['contact_person_mobile'],
                                                                         "contact_person_email_id_{}".format(index),
                                                                         row['contact_person_email'],
                                                                         "contact_person_designation_id_{}".format(
                                                                             index),
                                                                         row['contact_person_designation']
                                                                         ))
            return existing_contact_entries

        elif triggered_input == 'order_client_dropdown' and client_dropdown and client_dropdown != 'Other':
            cl_nm = str(client_dropdown).split(" -- ")[0]
            cl_lc = str(client_dropdown).split(" -- ")[1]
            existing_contact_entries = []
            contact_data = connection.execute_query(
                "select contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation"
                " from RajGroupClientRepresentativeList where client_name='{}' and client_location='{}' group by 1,2,3,4;".format(cl_nm, cl_lc))
            for index, row in contact_data.iterrows():
                existing_contact_entries.append(new_contact_entry_layout("contact_person_name_id_{}".format(index),
                                                              row['contact_person_name'],
                                                              "contact_person_mobile_id_{}".format(index),
                                                              row['contact_person_mobile'],
                                                              "contact_person_email_id_{}".format(index),
                                                              row['contact_person_email'],
                                                              "contact_person_designation_id_{}".format(index),
                                                              row['contact_person_designation']
                                                              ))
            return existing_contact_entries

        elif triggered_input == 'order_close_button':
            return None
        else:
            return None


@dash_app5.callback(Output('my_link', 'href'),
                   [Input('file_options', 'value')],
                  )
def download_file(file_options):
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 5: " + str(triggered_input))
        if triggered_input == 'file_options' and file_options:
            return '/dash/urlToDownload/RV/'
        return None



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15,message="Username must be 4-15 char long")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80,message="Password must be 8-80 char long")])
    submit= SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15,message="Username must be 4-15 char long")])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80,message="Password must be 8-80 char long")])
    submit= SubmitField('Sign Up')


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
    # print(str(session['username']))
    # dash_app.layout = select_layout(str(session['username']))
    # dash_app.layout = select_layout
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
            return redirect('/dash5')
        elif form.firm.data == 'D.N. Syndicate':
            return redirect('/dash3')
        elif form.firm.data == 'Raj Enterprise':
            return redirect('/dash4')
        elif form.firm.data == 'Raj Brookite':
            return redirect('/dash2')
    return render_template('select_firm.html', form=form)


def add_hyperlink(comp_location, order_key):
    comp_location = comp_location.replace('"','')
    return '=HYPERLINK("{}","{}")'.format(comp_location, order_key)


@app.route('/dash/urlToDownload/RGEnq/')
def download_rg_enq_list():
    value = connection.execute_query("select enquiry_key, entry_date, project_description, scope_of_work, client_name, "
                                     "client_location, lead_status, follow_up_person, tentative_project_value  "
                                     "from RajGroupEnquiryList order by 1 desc;")
    # value['order_key'] = value.apply(lambda row: add_hyperlink(row['comp_location'], row['order_key']), axis=1)
    # str_io = io.StringIO()
    # value.to_csv(str_io)
    # mem = io.BytesIO()
    # mem.write(str_io.getvalue().encode('utf-8'))
    # mem.seek(0)
    # str_io.close()
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine='xlsxwriter')
    value.to_excel(excel_writer, sheet_name='sheet1')
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)
    return flask.send_file(strIO,
                           # mimetype='excel',
                           # mimetype='text/csv',
                           attachment_filename='Raj_Group_Enquiry_List.xlsx',
                           as_attachment=True,
                           cache_timeout=0)


@app.route('/dash/urlToDownload/')
def download_csv():
    value = connection.execute_query("select order_key, order_date, po_no, project_description, scope_of_work, client_name, "
                                     "client_location, order_no, file_no, order_status, project_technical, project_management, "
                                     "project_supervisor, cast(REPLACE(project_value,',','') as unsigned) as project_value, "
                                     "remarks, comp_location from RajElectricalsOrdersNew;")
    value['order_key'] = value.apply(lambda row: add_hyperlink(row['comp_location'], row['order_key']), axis=1)
    # str_io = io.StringIO()
    # value.to_csv(str_io)
    # mem = io.BytesIO()
    # mem.write(str_io.getvalue().encode('utf-8'))
    # mem.seek(0)
    # str_io.close()
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine='xlsxwriter')
    value.to_excel(excel_writer, sheet_name='sheet1')
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)
    return flask.send_file(strIO,
                           # mimetype='excel',
                           # mimetype='text/csv',
                           attachment_filename='Raj_Electricals_Order_List.xlsx',
                           as_attachment=True,
                           cache_timeout=0)


@app.route('/dash/urlToDownload/RV/')
def download_rv_excel():
    value = connection.execute_query(
        "select order_key, order_date, po_no, project_description, scope_of_work, client_name, "
        "client_location, order_no, file_no, order_status, project_technical, project_management, "
        "project_supervisor, cast(REPLACE(project_value,',','') as unsigned) as project_value, "
        "remarks, comp_location from RajVijtechOrdersNew;")
    value['order_key'] = value.apply(lambda row: add_hyperlink(row['comp_location'], row['order_key']), axis=1)
    # str_io = io.StringIO()
    # value.to_csv(str_io)
    #
    # mem = io.BytesIO()
    # mem.write(str_io.getvalue().encode('utf-8'))
    # mem.seek(0)
    # str_io.close()

    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine='xlsxwriter')
    value.to_excel(excel_writer, sheet_name='sheet1')
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)

    return flask.send_file(strIO,
                           # mimetype='excel',
                           # mimetype='text/csv',
                           attachment_filename='Raj_Vijtech_Order_List.xlsx',
                           as_attachment=True,
                           cache_timeout=0)



@app.route('/feedback/<order_key>', methods=['GET', 'POST'])
def feedback(order_key):
    try:
        order_status = connection.execute_query("select order_status from RajElectricalsOrdersNew where order_key='{}';"
                                            .format(order_key))['order_status'][0]
    except:
        order_status = ''
    if order_status == 'FEEDBACK':
        if request.method == 'POST':
            feedback_data = request.get_json()
            recommend_score = feedback_data['data_list'][0]
            satisfaction_score = feedback_data['data_list'][1]
            technical_score = feedback_data['data_list'][2]
            behavorial_score = feedback_data['data_list'][3]
            future_services = ', '.join(feedback_data['allVals'])
            lesser_time = feedback_data['data_list'][4]
            suggestion = feedback_data['data_list'][5]
            feedback_table_values = [order_key, recommend_score, satisfaction_score, technical_score, behavorial_score, future_services,
                                     lesser_time, suggestion]
            connection.insert_query('RajGroupFeedback', fields_feedback, feedback_table_values)
            connection.execute("UPDATE RajElectricalsOrdersNew SET order_status='COMPLETE' where "
                               "order_key='{}'".format(order_key))
        return render_template('feedback.html')
    else:
        return render_template('feedback_error.html')

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
