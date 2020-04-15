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
    fields_client_list, fields_client_rep_list
from dashLayout import service_wise_pie_data, pending_offers_pie_data, submitted_offers_pie_data, lead_stages_bar_data, \
    weekly_leads_line_data, main_layout, new_offer_entry_layout, new_contact_entry_layout

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


def call_dash_app(href):
    d_app = dash.Dash(__name__,
                         server=app,
                         routes_pathname_prefix=href,
                         external_stylesheets=external_stylesheets
                         )
    return d_app


dash_app = call_dash_app('/dash/')

dash_app.layout = main_layout

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
                  [State('upcoming_projects_table', 'data'),
                   State('enquiry_key', 'value'),
                   State('entry_date', 'date'),
                   State('project_description', 'value'),
                   State('scope_of_work', 'value'),
                   State('client_name', 'value'),
                   State('client_location', 'value'),
                   State('existing_client', 'value'),
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
                   State('add_offer_div', 'children'),
                   State('add_contact_div', 'children')])
def update_output(submit_clicks, close_clicks, row_id, hoverData_lead_status, hoverData_service, hoverData_followup, hoverData_offers,
                  rows, enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client,
                  internal_lead, external_lead, lead_status,
                  contact_date, visit_date, enquiry_date, offer_date, raj_group_office, follow_up_person, tentative_project_value,
                  quotation_number, remarks, add_offer_div_value, add_contact_div_value):
    upcoming_projects_data_modified = connection.execute_query("select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
                                                  "client_location, lead_status, follow_up_person from RajGroupEnquiryList;").to_dict('records')
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
        if triggered_input == 'submit_button' and submit_clicks:
            if not enquiry_key:
                prev_enquiry_key = connection.execute_query("select count(enquiry_key) as cnt from RajGroupEnquiryList "
                                                            "where substr(enquiry_key, 9, 2) = '{}'".format(str(dt.now().month).zfill(2))).iloc[0]['cnt']
                enquiry_key = "EN_"+str(dt.now().year)+"_"+str(dt.now().month).zfill(2)+"_"+str(prev_enquiry_key+1).zfill(4)
                print("en_key:" + str(enquiry_key))
                enquiry_values = [enquiry_key, entry_date, project_description, str(scope_of_work).replace("[", '').replace("]", '').replace("'", ''),
                                  client_name,
                                  client_location, existing_client,
                                  '', '', '', internal_lead,
                                  external_lead,
                                  str(lead_status).replace("[", '').replace("]", '').replace("'", ''),
                                  contact_date, visit_date, enquiry_date, offer_date,
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
                        dispatch_no = i['props']['children'][0]['props']['children'][1]['props']['children'][1]['props'][
                            'value']
                        offer_location = i['props']['children'][0]['props']['children'][2]['props']['children'][1]['props'][
                            'value']
                        submitted_by = i['props']['children'][1]['props']['children'][0]['props']['children'][1]['props'][
                            'value']
                        remarks = i['props']['children'][1]['props']['children'][1]['props']['children'][1]['props'][
                            'value']
                        followup_log_values = [enquiry_key, dispatch_no, offer_location, submitted_by, remarks]
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
                                  contact_date, visit_date, enquiry_date, offer_date,
                                  str(raj_group_office).replace("[", '').replace("]", '').replace("'", ''),
                                  str(follow_up_person).replace("[", '').replace("]", '').replace("'", ''),
                                  tentative_project_value, quotation_number, remarks, enquiry_key))

                ## update RajGroupFollowUpLog
                if add_offer_div_value:
                    dispatch_no = add_offer_div_value[-1]['props']['children'][0]['props']['children'][1]['props']['children'][1]['props'][
                        'value']
                    offer_location = add_offer_div_value[-1]['props']['children'][0]['props']['children'][2]['props']['children'][1]['props'][
                        'value']
                    submitted_by = add_offer_div_value[-1]['props']['children'][1]['props']['children'][0]['props']['children'][1]['props'][
                        'value']
                    remarks = add_offer_div_value[-1]['props']['children'][1]['props']['children'][1]['props']['children'][1]['props']['value']
                    followup_log_values = [enquiry_key, dispatch_no, offer_location, submitted_by, remarks]
                    followup_log_mod_values = ['' if i is None else i for i in followup_log_values]

                    count = connection.execute_query("select enquiry_key, count(*) as cnt from "
                                                     "RajGroupFollowUpLog where enquiry_key='{}'"
                                                     "group by 1;".format(enquiry_key)).iloc[0]['cnt']

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

            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified
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
                   row_data.iloc[0]['contact_date'] if str(row_data.iloc[0]['contact_date']) != '0000-00-00' else None, \
                   row_data.iloc[0]['visit_date'] if str(row_data.iloc[0]['visit_date']) != '0000-00-00' else None, \
                   row_data.iloc[0]['enquiry_date'] if str(row_data.iloc[0]['enquiry_date']) != '0000-00-00' else None, \
                   row_data.iloc[0]['offer_date'] if str(row_data.iloc[0]['offer_date']) != '0000-00-00' else None, \
                   row_data.iloc[0]['raj_group_office'], row_data.iloc[0][
                       'follow_up_person'], row_data.iloc[0]['tentative_project_value'], row_data.iloc[0]['quotation_number'], \
                   row_data.iloc[0]['remarks'], upcoming_projects_data_modified

        elif triggered_input == 'graph_lead_stages' and hoverData_lead_status:
            status_var = hoverData_lead_status['points'][0]['x']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'service_wise_pie_chart' and hoverData_service:
            # connection = AWSMySQLConn()
            status_var = hoverData_service['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "scope_of_work='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'pending_offers_pie_chart' and hoverData_followup:
            status_var = hoverData_followup['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='ENQUIRY' and "
                                                                       "follow_up_person='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'submitted_offers_pie_chart' and hoverData_offers:
            status_var = hoverData_offers['points'][0]['label']
            upcoming_projects_data_modified = connection.execute_query("select * from RajGroupEnquiryList where "
                                                                           "lead_status='OFFER' and "
                                                                       "follow_up_person='{}';".format(status_var)).to_dict('records')
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified

        elif triggered_input == 'close_button' and close_clicks:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified
        else:
            return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
                   upcoming_projects_data_modified
    else:
        return 'tab-1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, \
               upcoming_projects_data_modified


@dash_app.callback(Output('add_offer_hide', 'style'),
                   [Input('lead_status', 'value')],
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


@dash_app.callback(Output('add_offer_div', 'children'),
                   [Input('add_another_offer', 'submit_n_clicks'),
                    Input('upcoming_projects_table', 'selected_rows'),
                    Input('submit_button', 'submit_n_clicks'),
                    Input('close_button', 'submit_n_clicks')],
                   [State('enquiry_key', 'value'),
                    State('upcoming_projects_table', 'data'),
                    State('add_offer_div', 'children')])
def add_new_offer_entry(offer_click, row_id, submit_button, click_button, enquiry_key, rows, add_offer_div_value):
    # connection = AWSMySQLConn()
    ctx = dash.callback_context
    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)
    if ctx.triggered:
        triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
        print("Triggered Input 3: "+str(triggered_input))
        if triggered_input == 'add_another_offer' and offer_click:
            existing_offer_entries = []
            if row_id:
                row_id = row_id[0]
                offer_data = connection.execute_query(
                    "select * from RajGroupFollowUpLog where enquiry_key='{}'".format(rows[row_id]['enquiry_key']))
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
                                                                  row['remarks']
                                                                  ))
                if index > 0:
                    existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_{}".format(index+1),
                                                                  '',
                                                                  "dispatch_id_{}".format(index+1),
                                                                  '',
                                                                  "offer_location_id_{}".format(index+1),
                                                                  '',
                                                                  "offer_submitted_id_{}".format(index+1),
                                                                  '',
                                                                  "offer_remarks_id_{}".format(index+1),
                                                                  ''
                                                                  ))
                else:
                    existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_0", '',
                                                                         "dispatch_id_0", '',
                                                                         "offer_location_id_0", '',
                                                                         "offer_submitted_id_0", '',
                                                                         "offer_remarks_id_0", ''))
            else:
                existing_offer_entries.append(new_offer_entry_layout("offer_timestamp_id_0", '',
                                                                     "dispatch_id_0", '',
                                                                     "offer_location_id_0", '',
                                                                     "offer_submitted_id_0", '',
                                                                     "offer_remarks_id_0", ''))
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
                                                              row['remarks']
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
                    Input('close_button', 'submit_n_clicks')],
                   [State('enquiry_key', 'value'),
                    State('upcoming_projects_table', 'data'),
                    State('add_contact_div', 'children'),
                    State('client_name', 'value'),
                    State('client_location', 'value')])
def add_new_contact_entry(contact_click, row_id, submit_button, close_button, enquiry_key, rows, add_contact_div_value, client_name, client_location):
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
                                                              row['contact_person_designation']
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


# @dash_app.callback(
#     [
#         Output("response_time_val", "children"),
#         Output("lead_to_enquiry_val", "children"),
#         Output("enquiry_to_offer_val", "children"),
#         Output("offer_to_won_val", "children"),
#     ],
#     [Input("submit_button", "submit_n_clicks")],
# )
# def update_text(data):
#     response_time_val = connection.execute_query("select (sum(time_diff)/count(time_diff)) as response_time from "
#                                                  "( select A.enquiry_key, A.time_stamp as A_time_stamp, B.lead_status, "
#                                                  "B.time_stamp as B_time_stamp, TIMESTAMPDIFF(HOUR, B.time_stamp, "
#                                                  "A.time_stamp) as time_diff from  (select enquiry_key, min(time_stamp) "
#                                                  "as time_stamp from RajGroupFollowUpLog group by 1) A inner join "
#                                                  "RajGroupLeadStatus B on A.enquiry_key=B.enquiry_key where B.lead_"
#                                                  "status='ENQUIRY') T1;").iloc[0]['response_time']
#     lead_to_enquiry_val = connection.execute_query("select  (select count(*) as total_enquiries from RajGroupEnquiryList"
#                                                    " where lead_status in ('ENQUIRY' , 'OFFER', 'WON', 'CLOSE', 'HOLD'))"
#                                                    " / (select count(*) as total_leads from RajGroupEnquiryList) as "
#                                                    "lead_to_enquiry;").iloc[0]['lead_to_enquiry']
#     enquiry_to_offer_val = connection.execute_query("select  "
#                                                     "(select count(*) as total_enquiries from "
#                                                     "RajGroupEnquiryList "
#                                                     "where lead_status in ('OFFER', 'WON', 'CLOSE', 'HOLD')) / "
#                                                     "(select count(*) as total_enquiries from "
#                                                     "RajGroupEnquiryList "
#                                                     "where lead_status in ('ENQUIRY' , 'OFFER', 'WON', 'CLOSE', 'HOLD'))"
#                                                     " as enquiry_to_offer ;").iloc[0]['enquiry_to_offer']
#     offer_to_won_val = connection.execute_query("select  "
#                                                 "(select count(*) as total_enquiries from "
#                                                 "RajGroupEnquiryList "
#                                                 "where lead_status in ('WON')) / "
#                                                 "(select count(*) as total_enquiries from "
#                                                 "RajGroupEnquiryList "
#                                                 "where lead_status in ('WON', 'CLOSE', 'HOLD')) as offer_to_won;").iloc[0]['offer_to_won']
#     return response_time_val, lead_to_enquiry_val, enquiry_to_offer_val, offer_to_won_val


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
        # connection = AWSMySQLConn()
        existing_users = connection.get_unique_values("users", "user_name")
        if form.username.data in existing_users:
            password = connection.execute_query("select user_password from users where user_name='{}'".format(form.username.data)).iloc[0,0]

            if sha256_crypt.verify(form.password.data, password):
                session['logged_in'] = True
                session['username'] = form.username.data
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


# keep this as is
if __name__ == '__main__':
    app.run(port=8000)
    # # dash_app.run_server(debug=True)

print("--- %s seconds ---" % (time.time() - start_time))