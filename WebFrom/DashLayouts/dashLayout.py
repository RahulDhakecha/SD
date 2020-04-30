import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
from datetime import datetime as dt
from datetime import date, timedelta
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from fixedVariables import sow, lead_status, raj_group_office, follow_up_person, fields_enquiry_list, fields_followup_log
from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd


def service_wise_pie_data(data):
    # connection = AWSMySQLConn()
    # services = list(connection.execute_query("select scope_of_work, count(*) as cnt from RajGroupEnquiryList group by 1")['scope_of_work'])
    # service_wise_data = list(connection.execute_query("select scope_of_work, count(*) as cnt from RajGroupEnquiryList group by 1")['cnt'])
    data_mod = data[['enquiry_key', 'scope_of_work']].groupby('scope_of_work',
                                            as_index=False).count().rename(columns={'enquiry_key':'cnt'})
    services = list(data_mod['scope_of_work'])
    service_wise_data = list(data_mod['cnt'])

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


def pending_offers_pie_data(data):
    # connection = AWSMySQLConn()
    # pending_offers = connection.execute_query("select follow_up_person, count(*) as cnt from RajGroupEnquiryList where "
    #                                           "lead_status='ENQUIRY' group by 1")
    data = data[data['lead_status'] == 'ENQUIRY']
    pending_offers = data[['enquiry_key', 'follow_up_person']].groupby('follow_up_person',
                                                                 as_index=False).count().rename(
        columns={'enquiry_key': 'cnt'})
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


def submitted_offers_pie_data(data):
    # connection = AWSMySQLConn()
    # submitted_offers = connection.execute_query("select follow_up_person, count(*) as cnt from RajGroupEnquiryList where "
    #                                           "lead_status='OFFER' group by 1")

    data = data[data['lead_status'] == 'OFFER']
    submitted_offers = data[['enquiry_key', 'follow_up_person']].groupby('follow_up_person',
                                                                 as_index=False).count().rename(
        columns={'enquiry_key': 'cnt'})

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


def lead_stages_bar_data(data):
    # connection = AWSMySQLConn()
    # lead_status_data = connection.execute_query("select lead_status, count(*) as cnt from RajGroupEnquiryList group by 1")
    lead_status_data = data[['enquiry_key', 'lead_status']].groupby('lead_status',
                                                            as_index=False).count().rename(
        columns={'enquiry_key': 'cnt'})
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


def weekly_leads_line_data(data):
    # connection = AWSMySQLConn()
    # weekly_leads_data = connection.execute_query("select years, weeks, count(*) as leads_cnt "
    #                                              "from (select time_stamp, entry_date, year(entry_date) as years, week(entry_date, 5) as weeks "
    #                                              "from RajGroupEnquiryList) as temp where years=2020 group by 1,2;")
    data1 = data.copy()
    data1['years'] = pd.DatetimeIndex(data1['entry_date']).year
    data1['weeks'] = pd.DatetimeIndex(data1['entry_date']).week
    weekly = data1[['enquiry_key', 'years', 'weeks']].groupby(['years', 'weeks'],
                                                                               as_index=False).count().rename(
        columns={'enquiry_key': 'leads_cnt'})
    weekly_leads_data = weekly[weekly['years'] == 2020]

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


def new_offer_entry_layout(offer_timestamp_id=None,
                           offer_timestamp=None,
                           dispatch_id=None,
                           dispatch_value=None,
                           offer_location_id=None,
                           offer_location_value=None,
                           offer_submitted_id=None,
                           offer_submitted_by=None,
                           offer_remarks_id=None,
                           offer_remarks=None,
                           offer_submitted_to_id=None,
                           offer_submitted_to=None):
    return html.Div([
                html.Div([
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
                ], className="row"),
                html.Div([
                    html.Div([
                        html.Header("Offer Submitted By"),
                        dcc.Input(
                            id=offer_submitted_id,
                            type='text',
                            placeholder='Offer Submitted By',
                            size=50,
                            value=offer_submitted_by
                        ),
                    ], className="four columns"),
                    html.Div([
                        html.Header("Offer Remarks"),
                        dcc.Input(
                            id=offer_remarks_id,
                            type='text',
                            placeholder='Offer Remakrs',
                            size=50,
                            value=offer_remarks
                        ),
                    ], className="four columns"),
                    html.Div([
                        html.Header("Submitted To"),
                        dcc.Input(
                            id=offer_submitted_to_id,
                            type='text',
                            placeholder='Offer Submitted To',
                            size=50,
                            value=offer_submitted_to
                        ),
                    ], className="four columns"),
                ], className="row")
            ])


def new_contact_entry_layout(contact_person_name_id=None,
                             contact_person_name=None,
                             contact_person_mobile_id=None,
                             contact_person_mobile=None,
                             contact_person_email_id=None,
                             contact_person_email=None,
                             contact_person_designation_id=None,
                             contact_person_designation=None):
    return html.Div([
                html.Div([
                    html.Header("Contact Person Name"),
                    dcc.Input(
                        id=contact_person_name_id,
                        type='text',
                        placeholder='Enter Contact Person Name',
                        size=30,
                        value=contact_person_name
                    ),
                ], className="three columns"),
                html.Div([
                    html.Header("Contact Person Mobile"),
                    dcc.Input(
                        id=contact_person_mobile_id,
                        type='text',
                        placeholder='Enter Contact Person Mobile',
                        size=30,
                        value=contact_person_mobile
                    ),
                ], className="three columns"),
                html.Div([
                    html.Header("Contact Person Email"),
                    dcc.Input(
                        id=contact_person_email_id,
                        type='text',
                        placeholder='Enter Contact Person Email',
                        size=30,
                        value=contact_person_email
                    ),
                ], className="three columns"),
                html.Div([
                    html.Header("Contact Person Designation"),
                    dcc.Input(
                        id=contact_person_designation_id,
                        type='text',
                        placeholder='Enter Contact Person Designation',
                        size=30,
                        value=contact_person_designation
                    ),
                ], className="three columns"),
            ], className="row")


def main_layout():
    connection = AWSMySQLConn()
    data_upcoming_projects = connection.execute_query(
        "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
        "client_location, lead_status, follow_up_person from RajGroupEnquiryList;")

    raj_group_followup = connection.execute_query("select * from RajGroupFollowUpLog;")
    raj_group_lead_status = connection.execute_query("select * from RajGroupLeadStatus;")

    raj_followup_min = raj_group_followup[['enquiry_key', 'time_stamp']].groupby('enquiry_key', as_index=False).min()
    lead_follow_join = raj_followup_min.merge(raj_group_lead_status, on='enquiry_key')
    lead_follow_join = lead_follow_join[lead_follow_join['lead_status'] == 'ENQUIRY']

    def calc_diff(v1, v2):
        time_diff = v1 - v2
        return time_diff.total_seconds() / 3600

    response_time_val = round(lead_follow_join.apply(lambda row: calc_diff(row['time_stamp_x'], row['time_stamp_y']), axis=1).mean(), 0)

    lead_to_enquiry_val = round(sum(data_upcoming_projects['lead_status'].isin(['ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD'])) / len(
        list(data_upcoming_projects['enquiry_key'])), 2)

    enquiry_to_offer_val = round(sum(data_upcoming_projects['lead_status'].isin(['OFFER', 'WON', 'CLOSE', 'HOLD'])) / sum(
        data_upcoming_projects['lead_status'].isin(['ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD'])), 2)

    offer_to_won_val = round(sum(data_upcoming_projects['lead_status'] == 'WON') / sum(
        data_upcoming_projects['lead_status'].isin(['WON', 'CLOSE', 'HOLD'])), 2)


    # client_data = list(
    #     connection.execute_query("select client_name from RajGroupClientList group by 1;")['client_name'])

    return html.Div([
    html.Div([
        html.Div([
            dcc.Link('HOME', href='/', refresh=True),
        ], className="one columns"),
        html.Div([
            dcc.Link('REFRESH', href='/dash/', refresh=True),
        ], className="one columns"),
    ], className="row"),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tab1', value='tab-1', label='Raj Group Marketing Dashboard', children=[
            html.Div([
                html.Div([
                    # GRAPH - Lead Stages
                    dcc.Graph(
                        id='weekly_leads',
                        figure=weekly_leads_line_data(data_upcoming_projects)
                    ),
                ]),
            ], className="row"),
            html.Div(
                [
                    html.Div(
                        [html.H6(id="response_time_val", children=response_time_val), html.P("Response Time(in hours)")],
                        id="response_time",
                        className="mini_container three columns",
                    ),
                    html.Div(
                        [html.H6(id="lead_to_enquiry_val", children=lead_to_enquiry_val), html.P("Leads to Enquiries")],
                        id="lead_to_enquiry",
                        className="mini_container three columns",
                    ),
                    html.Div(
                        [html.H6(id="enquiry_to_offer_val", children=enquiry_to_offer_val), html.P("Enquiries to Offer")],
                        id="enquiry_to_offer",
                        className="mini_container three columns",
                    ),
                    html.Div(
                        [html.H6(id="offer_to_won_val", children=offer_to_won_val), html.P("Offer to Won")],
                        id="offer_to_won",
                        className="mini_container three columns",
                    ),
                ],
                id="info-container",
                className="row",
            ),
            html.Div([
                html.Div([
                    # Pie-chart reflecting submitted offer
                    dcc.Graph(
                        id='submitted_offers_pie_chart',
                        figure=submitted_offers_pie_data(data_upcoming_projects)
                    ),
                ], className="six columns"),

                html.Div([
                    # Pie-chart reflecting pending offers
                    dcc.Graph(
                        id='pending_offers_pie_chart',
                        figure=pending_offers_pie_data(data_upcoming_projects)
                    ),
                ], className="pretty_container six columns")

            ], className="row"),
            html.Div([
                html.Div([
                # GRAPH - Lead Stages
                dcc.Graph(
                    id='graph_lead_stages',
                    figure=lead_stages_bar_data(data_upcoming_projects)
                ),
                ], className="six columns"),
                html.Div([
                    # Pie-chart reflecting service wise enquiries
                    dcc.Graph(
                        id='service_wise_pie_chart',
                        figure=service_wise_pie_data(data_upcoming_projects)
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
                editable=False,
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
                    html.Header("Entry Date", className="required"),
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
                    html.Header("Scope of Work", className="required"),
                    dcc.Dropdown(
                        id='scope_of_work',
                        options=[{'value': i, 'label': i} for i in sow],
                    ),
                ], className="four columns"),
                html.Div([
                    html.H3("Client Details"),
                    html.Header("Client Name", className="required"),
                    dcc.Input(
                        id='client_name',
                        type='text',
                        placeholder='Enter Client Name',
                        size=50,
                    ),
                    # html.Header("Client Dropdown"),
                    # dcc.Dropdown(
                    #     id='client_dropdown',
                    #     options=[{'value': i, 'label': i} for i in client_data]
                    # ),
                    html.Header("Client Location", className="required"),
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
                ], className="four columns"),
            ], className="row"),

            html.H3("Contact Details"),
            html.Div([
                html.Div(id="add_contact_div"),
                html.Header("Add Another Contact"),
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Add Contact',
                    ),
                    id='add_another_contact',
                    message='Are you sure you want to continue?'
                ),
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
                    html.Header("Status", className="required"),
                    dcc.Dropdown(
                        id='lead_status',
                        options=[{'value': i, 'label': i} for i in lead_status]
                    ),
                ], className="four columns"),
                # html.Div([
                #     html.Header("Contact Date"),
                #     dcc.DatePickerSingle(
                #         id='contact_date',
                #         placeholder='Contact Date',
                #         with_portal=True,
                #         display_format="YYYY-MM-DD",
                #     ),
                #     html.Header("Visit Date"),
                #     dcc.DatePickerSingle(
                #         id='visit_date',
                #         placeholder='Visit Date',
                #         with_portal=True,
                #         display_format="YYYY-MM-DD",
                #     ),
                #     html.Header("Enquiry Date"),
                #     dcc.DatePickerSingle(
                #         id='enquiry_date',
                #         placeholder='Enquiry Date',
                #         with_portal=True,
                #         display_format="YYYY-MM-DD",
                #     ),
                #     html.Header("Offer Date"),
                #     dcc.DatePickerSingle(
                #         id='offer_date',
                #         placeholder='Offer Date',
                #         with_portal=True,
                #         display_format="YYYY-MM-DD"
                #     ),
                # ], className="four columns"),
                html.Div([
                    html.Header("Raj Group Office", className="required"),
                    dcc.Dropdown(
                        id='raj_group_office',
                        options=[{'value': i, 'label': i} for i in raj_group_office]
                    ),
                    html.Header("Follow Up Person", className="required"),
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
            html.Div(id="add_offer_hide", children=[
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
                dcc.ConfirmDialog(
                    id='modal_display',
                    message='Please fill all required values marked in RED!!',
                ),
            ], className="row"),
        ])
    ]),
    html.Div(id='tabs-content')
], className="page")


if __name__ == '__main__':
    print(service_wise_pie_data())


