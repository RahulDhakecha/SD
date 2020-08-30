import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
from datetime import datetime as dt
from datetime import date, timedelta
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from fixedVariables import sow, lead_status, raj_group_office, follow_up_person, fields_enquiry_list, fields_followup_log, order_status
from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import plotly.graph_objects as go


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
                'textfont': {
                    'family': 'Comfortaa',
                    'color': '#1034A6',
                    'size': 15
                },
                'hoverlabel': {
                    'bgcolor': '#1034A6',
                    'bordercolor': '#1034A6',
                    'font': {
                        'family': 'Comfortaa',
                        'color': '#F5F5F5',
                        'size': 15
                    }
                },
                'marker': {
                    'colors': ['#e41c59', '#003f5c', '#58508d', 'cyan',
                               '#bc5090',
                               '#ff6361',
                               '#ffa600',
                               '#63b179',
                               '#8fa351',
                               '#b58f40',
                               '#d2784e',
                               '#dc6272',
                               ],
                    'line': {
                        'color': '#F5F5F5',
                        'width': 3
                    }
                },
            },
        ]
    fig = {
        'data': service_wise_pie_data,
        'layout': {
            'title': 'Raj Group - Service Wise Enquiries',
            'autosize': True,
            'font': {
                'family': 'Comfortaa',
                'color': '#1034A6',
            },
            'paper_bgcolor': '#F5F5F5',
            'plot_bgcolor': '#F5F5F5',
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
            pending_offers_data.append(None)
    pending_offers_pie_data_var = [
        {
            'labels': follow_up_person,
            'values': pending_offers_data,
            'type': 'pie',
            'textfont': {
                'family': 'Comfortaa',
                'color': '#1034A6',
                'size': 15
            },
            'hoverlabel': {
                'bgcolor': '#1034A6',
                'bordercolor': '#1034A6',
                'font': {
                    'family': 'Comfortaa',
                    'color': '#F5F5F5',
                    'size': 15
                }
            },
            'marker': {
                'colors': ['#e41c59', '#003f5c', '#58508d', 'cyan',
                           '#bc5090',
                           '#ff6361',
                           '#ffa600',
                           '#ADD8E6',
                           '#63b179',
                           '#8fa351',
                           '#b58f40',

                           ],
                'line': {
                    'color': '#F5F5F5',
                    'width': 3
                }
            },
        },
    ]
    fig = {
        'data': pending_offers_pie_data_var,
        'layout': {
            'title': 'Raj Group - Pending Offers',
            'autosize': True,
            'font': {
                'family': 'Comfortaa',
                'color': '#1034A6',
            },
            'paper_bgcolor': '#F5F5F5',
            'plot_bgcolor': '#F5F5F5',
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
            submitted_offers_data.append(None)
    submitted_offers_pie_data = [
            {
                'labels': follow_up_person,
                'values': submitted_offers_data,
                'type': 'pie',
                'textfont': {
                    'family': 'Comfortaa',
                    'color': '#1034A6',
                    'size': 15
                },
                'hoverlabel': {
                    'bgcolor': '#1034A6',
                    'bordercolor': '#1034A6',
                    'font': {
                        'family': 'Comfortaa',
                        'color': '#F5F5F5',
                        'size': 15
                    }
                },
                'marker': {
                    'colors': ['#e41c59', '#003f5c', '#58508d', 'cyan',
                               '#bc5090',
                               '#ADD8E6',
                               '#ff6361',
                               '#ffa600',
                               '#63b179',
                               '#8fa351',
                               '#b58f40',
                               '#d2784e',
                               '#dc6272',

                               ],
                    'line': {
                        'color': '#F5F5F5',
                        'width': 3
                    }
                },
            },
        ]
    fig = {
        'data': submitted_offers_pie_data,
        'layout': {
            'title': 'Raj Group - Submitted Offers',
            'autosize': True,
            'font': {
                'family': 'Comfortaa',
                'color': '#1034A6',
            },
            'paper_bgcolor': '#F5F5F5',
            'plot_bgcolor': '#F5F5F5',
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
    display_lead_status = ['OPEN', 'CONTACTED', 'VISITED', 'ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD', 'REGRET']
    for i in display_lead_status:
        try:
            lead_stages_data.append(lead_status_data[lead_status_data['lead_status'] == i]['cnt'].iloc[0])
        except:
            lead_stages_data.append(None)

    lead_stages_bar_data = [
            {
                'x': display_lead_status,
                'y': lead_stages_data,
                'type': 'bar',
                'marker': {
                    'color': ['white', '#58508d', '#003f5c', 'cyan', 'green', 'yellow', 'red', 'pink'],
                },
            },
        ]
    fig = {
        'data': lead_stages_bar_data,
        'layout': {
            'title': 'Raj Group - Lead Status',

            'font': {
                'family': 'Comfortaa',
                'color': '#1034A6',
                'size': 15,
            },
            'paper_bgcolor': '#F5F5F5',
            'plot_bgcolor': '#F5F5F5',
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
                'line': {
                    'color': '#1034A6',
                },
                'textfont': {
                    'family': 'Comfortaa',
                    'color': '#F5F5F5',
                    'size': 15
                },
                'hoverlabel': {
                    'bgcolor': '#1034A6',
                    'bordercolor': '#1034A6',
                    'font': {
                        'family': 'Comfortaa',
                        'color': '#F5F5F5',
                        'size': 15
                    }
                },
            },
        ]

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=weekly_leads_line_data[0]['x'], y=weekly_leads_line_data[0]['y'], name='Leads'))
    # fig.add_trace(go.Scatter(x=weekly_offers_line_data()[0]['x'], y=weekly_offers_line_data()[0]['y'], name='Offers'))
    # fig.update_layout(title={
    #                         'text': "Weekly Leads and Offers",
    #                         'y': 0.9,
    #                         'x': 0.45,
    #                         'xanchor': 'center',
    #                         'yanchor': 'top'},
    #                   xaxis_title='Weeks',
    #                   yaxis_title='Leads and Offers')
    fig = {
            'data': weekly_leads_line_data,
            'layout': {
                'title': 'Raj Group - Weekly Leads',
                'xaxis': {
                    'title': 'Weeks',
                    'range': weeks,
                    'type': "category"
                },
                'font': {
                    'family': 'Comfortaa',
                    'color': '#1034A6',
                    'size': 15
                },
                'paper_bgcolor': '#F5F5F5',
                'plot_bgcolor': '#F5F5F5',

            }
        }

    return fig


def weekly_offers_line_data():
    connection = AWSMySQLConn()
    data = connection.execute_query("select * from RajGroupFollowUpLog;")
    data1 = data.copy()
    data1['years'] = pd.DatetimeIndex(data1['time_stamp']).year
    data1['weeks'] = pd.DatetimeIndex(data1['time_stamp']).week
    weekly = data1[['enquiry_key', 'years', 'weeks']].groupby(['years', 'weeks'],
                                                                               as_index=False).count().rename(
        columns={'enquiry_key': 'offers_cnt'})
    weekly_offers_data = weekly[weekly['years'] == 2020]

    # print(weekly_leads_data)
    current_year, current_week, current_day = date.today().isocalendar()
    weeks = [getDateRangeFromWeek('2020', p_week) for p_week in range(1, current_week)]

    weekly_offers_cnt_data = []
    for i in range(1, current_week):
        # print(weekly_leads_data[weekly_leads_data['weeks'] == i]['leads_cnt'].iloc[0])
        try:
            weekly_offers_cnt_data.append(weekly_offers_data[weekly_offers_data['weeks'] == i]['offers_cnt'].iloc[0])
        except IndexError:
            weekly_offers_cnt_data.append(0)

    weekly_offers_line_data = [
            {
                'x': weeks,
                'y': weekly_offers_cnt_data,
                'type': 'line',
            },
        ]
    # fig = {
    #         'data': weekly_offers_line_data,
    #         'layout': {
    #             'title': 'Raj Group - Weekly Offers',
    #             'xaxis': {
    #                 'title': 'Weeks',
    #                 'range': weeks,
    #                 'type': "category"
    #             }
    #         }
    #     }
    return weekly_offers_line_data


def orders_scope_pie_data(data):

    orders_scope = data[['order_key', 'scope_of_work']].groupby('scope_of_work',
                                                                 as_index=False).count().rename(
        columns={'order_key': 'cnt'})
    orders_scope_data = []
    for i in sow:
        try:
            orders_scope_data.append(orders_scope[orders_scope['scope_of_work'] == i]['cnt'].iloc[0])
        except:
            orders_scope_data.append(None)
    orders_scope_pie_data_var = [
            {
                'labels': sow,
                'values': orders_scope_data,
                'type': 'pie',
                'textfont': {
                    'family': 'Comfortaa',
                    'color': '#1034A6',
                    'size': 15
                },
                'hoverlabel': {
                    'bgcolor': '#1034A6',
                    'bordercolor': '#1034A6',
                    'font': {
                        'family': 'Comfortaa',
                        'color': '#F5F5F5',
                        'size': 15
                    }
                },
                'marker': {
                    'colors': ['#e41c59', '#003f5c', '#58508d', 'cyan',
                               '#bc5090',
                               '#ADD8E6',
                               '#ff6361',
                               '#ffa600',
                               '#63b179',
                               '#8fa351',
                               '#b58f40',
                               '#d2784e',
                               '#dc6272',

                               ],
                    'line': {
                        'color': '#F5F5F5',
                        'width': 3
                    }
                },
            },
        ]
    fig = {
        'data': orders_scope_pie_data_var,
        'layout': {
            'title': 'Work Order Scope',
            'autosize': True,
            'font': {
                'family': 'Comfortaa',
                'color': '#1034A6',
            },
            'paper_bgcolor': '#F5F5F5',
            'plot_bgcolor': '#F5F5F5',
        }
    }
    return fig


def orders_status_pie_data(data):
    orders_status = data[['order_key', 'order_status']].groupby('order_status',
                                                                as_index=False).count().rename(
        columns={'order_key': 'cnt'})
    orders_status_data = []
    for i in order_status:
        try:
            orders_status_data.append(orders_status[orders_status['order_status'] == i]['cnt'].iloc[0])
        except:
            orders_status_data.append(None)
    orders_status_pie_data_var = [
        {
            'labels': order_status,
            'values': orders_status_data,
            'type': 'pie',
            'textfont': {
                    'family': 'Comfortaa',
                    'color': '#1034A6',
                    'size': 15
                },
                'hoverlabel': {
                    'bgcolor': '#1034A6',
                    'bordercolor': '#1034A6',
                    'font': {
                        'family': 'Comfortaa',
                        'color': '#F5F5F5',
                        'size': 15
                    }
                },
                'marker': {
                    'colors': ['#e41c59', '#003f5c', '#58508d', 'cyan',
                               '#bc5090',
                               '#ff6361',
                               '#ffa600',
                               '#63b179',
                               '#8fa351',
                               '#b58f40',
                               '#d2784e',
                               '#dc6272',
                               ],
                    'line': {
                        'color': '#F5F5F5',
                        'width': 3
                    }
                },
        },
    ]
    fig = {
        'data': orders_status_pie_data_var,
        'layout': {
            'title': 'Work Order Status',
            'autosize': True,
            'font': {
                'family': 'Comfortaa',
                'color': '#1034A6',
            },
            'paper_bgcolor': '#F5F5F5',
            'plot_bgcolor': '#F5F5F5',
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
            html.Header("Date"),
            dcc.Input(
                id=offer_timestamp_id,
                type='text',
                style={'width': '100%'},
                disabled=True,
                value=offer_timestamp
            ),
        ], className="add_itm"),
        html.Div([
            html.Header("Dispatch Number"),
            dcc.Input(
                id=dispatch_id,
                type='text',
                style={'width': '100%'},
                value=dispatch_value
            ),
        ], className="add_itm"),
        html.Div([
            html.Header("Location"),
            dcc.Input(
                id=offer_location_id,
                type='text',
                style={'width': '100%'},
                value=offer_location_value
            ),
        ], className="add_itm"),

        html.Div([
            html.Header("Submitted By"),
            dcc.Input(
                id=offer_submitted_id,
                type='text',
                style={'width': '100%'},
                value=offer_submitted_by
            ),
        ], className="add_itm"),
        html.Div([
            html.Header("Remarks"),
            dcc.Input(
                id=offer_remarks_id,
                type='text',
                style={'width': '100%'},
                value=offer_remarks
            ),
        ], className="add_itm"),
        html.Div([
            html.Header("Submitted To"),
            dcc.Input(
                id=offer_submitted_to_id,
                type='text',
                style={'width': '100%'},
                value=offer_submitted_to
            ),
        ], className="add_itm"),

    ], className="new_offer")


def new_contact_entry_layout(contact_person_name_id=None,
                             contact_person_name=None,
                             contact_person_mobile_id=None,
                             contact_person_mobile=None,
                             contact_person_email_id=None,
                             contact_person_email=None,
                             contact_person_designation_id=None,
                             contact_person_designation=None,
                             contact_person_id=None):
    return html.Div([
        html.Div([
            html.P("Person Name"),
            dcc.Input(
                id=contact_person_name_id,
                type='text',
                style={'width': '100%'},
                value=contact_person_name
            ),
        ], className='add_itm'),
        html.Div([
            html.P("Person Mobile"),
            dcc.Input(
                id=contact_person_mobile_id,
                type='text',
                style={'width': '100%'},
                value=contact_person_mobile
            ),
        ], className='add_itm'),
        html.Div([
            html.P("Person Email"),
            dcc.Input(
                id=contact_person_email_id,
                type='text',
                style={'width': '100%'},
                value=contact_person_email
            ),
        ], className='add_itm'),
        html.Div([
            html.P("Designation"),
            dcc.Input(
                id=contact_person_designation_id,
                type='text',
                style={'width': '100%'},
                value=contact_person_designation
            ),
        ], className='add_itm'),
        html.Div([
            dcc.RadioItems(
                id='delete_contact',
                options=[{'label': 'Delete','value': 'Delete'}],
                value="",
                className="radiodelete",
                inputClassName='deleteinput',
                labelClassName='deletelabel'
            ),
        ], className='add_itm1'),
        # html.A(id="X", children=contact_person_id, style={'text-decoration':'none','padding-top':'7vh','font-weight':'bold','color':'#1034A6'}),
        # html.A("X",
        #        style={'text-decoration':'none','padding-top':'7vh','font-weight':'bold','color':'#1034A6'},
        #        href="javascript:delete1(this.document)"),
    ], className="new_contect")


def main_layout(username):
    connection = AWSMySQLConn()
    data_upcoming_projects = connection.execute_query(
        "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
        "client_location, lead_status, follow_up_person, tentative_project_value  from RajGroupEnquiryList where"
        " follow_up_person like '{}' order by 1 desc;".format(username))

    en_keys = list(data_upcoming_projects['enquiry_key'])

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

    client_data = ['Other']
    client_data_all = connection.execute_query("select client_name, client_location from RajGroupClientList group by 1,2;")
    for i, j in zip(list(client_data_all['client_name']), list(client_data_all['client_location'])):
        client_data.append(i+" -- "+j)


    return html.Div([
        html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        # html.Div([
        #     html.Div([
        #         dcc.Link('HOME', href='/', refresh=True),
        #     ], className="one columns"),
        #     html.Div([
        #         dcc.Link('REFRESH', href='/dash/', refresh=True),
        #     ], className="one columns"),
        #     # html.Div([
        #     #     html.A('Download Dispatch Register', href='/dash/urlToDownload', id='my_link'),
        #     # ], className="one columns"),
        # ], className="row"),

        html.Div([
            html.Div([
                html.A('Home', href="/", className='nav_item now', style={'border-left': 'none'}),
                html.A('REFRESH', href="/dash/", className='nav_item'),

            ], className='nav_bar_content'),
            html.A('Logout', href="/logout", className='nav_item last'),
        ], className='nav_bar'),
        html.Div([
            html.Div([
                html.A([
                    html.Img(src="assets/close.png", style={'width': '30px', 'height': '30px', 'padding': '5px'})
                ], href="javascript:closeNav()", className='closebtn'),
                html.A('HOME', href="/", className='menulink'),
                html.A('REFRESH', href="/dash/", className='menulink'),
                html.A('LOGOUT', href="/logout", className='menulink'),

            ], id='mySidenav', className='sidenav'),

            html.A([
                html.Img(src="assets/menu.png", style={'width': '30px', 'height': '30px', 'padding': '5px'})
            ], href='javascript:openNav()'),

        ], className='nav_bar2'),

    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tab1', value='tab-1', label='Raj Group Marketing Dashboard', children=[

            # Body1 start

            html.Div([

                html.Div([
                    html.H3('Welcome to Raj Group DashBoard', className='main_title')
                ]),

                html.Div([
                    # GRAPH - Lead Stages
                    dcc.Graph(
                        id='weekly_leads',
                        figure=weekly_leads_line_data(data_upcoming_projects),
                    ),
                ], className='weeklead'),

                html.Div([
                    html.Div(
                        [html.P("Response Time(/hours)"),
                         html.H4(id="response_time_val", children=response_time_val)],
                        id="response_time",
                        className="analysis_container",
                    ),
                    html.Div(
                        [html.P("Leads to Enquiries"),
                         html.H4(id="lead_to_enquiry_val", children=lead_to_enquiry_val)],
                        id="lead_to_enquiry",
                        className="analysis_container",
                    ),
                    html.Div(
                        [html.P("Enquiries to Offer"),
                         html.H4(id="enquiry_to_offer_val", children=enquiry_to_offer_val)],
                        id="enquiry_to_offer",
                        className="analysis_container",
                    ),
                    html.Div(
                        [html.P("Offer to Won"), html.H4(id="offer_to_won_val", children=offer_to_won_val)],
                        id="offer_to_won",
                        className="analysis_container",
                    ),
                ],
                    id="info-container",
                    className="analysis",
                ),

            ], className='body_data1'),

            # Body1 End

            # Body2 start
            html.Div([
                html.Div([
                    html.H1('Offer Details', className='main_title')
                ]),
                html.Div([
                    html.Div([
                        # Pie-chart reflecting submitted offer
                        dcc.Graph(
                            id='submitted_offers_pie_chart',
                            figure=submitted_offers_pie_data(data_upcoming_projects)
                        ),
                    ], className="pie_charts_container"),

                    html.Div([

                        # Pie-chart reflecting pending offers
                        dcc.Graph(
                            id='pending_offers_pie_chart',
                            figure=pending_offers_pie_data(data_upcoming_projects)
                        ),
                    ], className="pie_charts_container"),

                    html.Div([

                        # Pie-chart reflecting service wise enquiries
                        dcc.Graph(
                            id='service_wise_pie_chart',
                            figure=service_wise_pie_data(data_upcoming_projects)
                        ),
                    ], className="pie_charts_container"),

                    html.Div([

                        # GRAPH - Lead Stages
                        dcc.Graph(
                            id='graph_lead_stages',
                            figure=lead_stages_bar_data(data_upcoming_projects)
                        ),
                    ], className="pie_charts_container"),

                ], className='pie_charts'),
            ], className='body_data2'),
            # Body2 End

            # BOdy3 Start
            html.Div([


                html.Div([

                    # Data Table - Upcoming Projects
                    dash_table.DataTable(
                        id='upcoming_projects_table',
                        style_data={'minWidth': 'auto', 'width': 'auto', 'maxWidth': '8vw'},
                        style_table={

                            # 'border': '1px solid  #F5F5F5',
                            'overflowY': 'auto',
                            'minHeight': '90vh', 'height': '90vh', 'maxHeight': '90vh',

                        },

                        style_header={
                            'backgroundColor': '#1034A6',
                            'fontWeight': '500',
                            'color': '#F5F5F5',
                            'borderRadius': '10px',
                            # 'border': '1px solid  #F5F5F5',
                            'font-family': 'Comfortaa',
                            'font-size': '2',

                        },
                        style_cell={
                            'textAlign': 'center',
                            'whiteSpace': 'normal',
                            'minHeight': '30px',
                            'font-size': 'xx-small',
                            'font-family': 'Comfortaa',

                            # 'height': 'auto',

                        },
                        style_data_conditional=[
                            {'color': '#1034A6',
                             'backgroundColor': '#F5F5F5',
                             'border': '1px solid  #1034A6',

                             # 'if': {'row_index': 'odd'},
                             # 'backgroundColor': 'rgb(248, 248, 248)'
                             }
                        ],
                        fixed_rows={'headers': True, 'data': 0},
                        css=[{
                            'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; font-family: Comfortaa;white-space: inherit; overflow: inherit; text-overflow: inherit;',

                        }],

                        filter_action="native",
                        style_filter_conditional=[{
                            'backgroundColor': '#F5F5F5',
                            'color': '#1034A6',
                            'padding': '10px',
                            'height': '20px',
                            'border': '2px solid #433cde9',
                        }],
                        style_as_list_view=True,
                        sort_action="native",
                        sort_mode="multi",
                        row_selectable="single",
                        editable=False,
                        columns=[{"name": i, "id": i} for i in data_upcoming_projects.columns],
                        data=data_upcoming_projects.to_dict('records')
                    ),
                    # html.Div([
                    #     dcc.Dropdown(
                    #         id='file_options',
                    #         options=[{'value': i, 'label': i} for i in ['Raj Group Enquiry List']],
                    #         placeholder='Select File to Download',
                    #         className='downloadfile',
                    #
                    #     ),
                    #
                    #     html.A(children=[
                    #         html.Img(src='assets/images/download.png', className="logoimg", alt='home'),
                    #
                    #     ], id='my_link'),
                    #
                    # ], style={'display': 'inline'}),
                ], className='table_data')
            ], className='body_data3'),
            # BOdy3 end

        ]),
        dcc.Tab(id='tab2', value='tab-2', label='Raj Group Marketing Form', children=[

            # Body4 start

            html.Div([
                html.Div([
                    html.Div([

                        html.Div([

                            html.H5("Project Details", className='modeltitle'),

                            html.P("Enquiry Key"),
                            dcc.Input(
                                id='enquiry_key',
                                type='text',
                                disabled='True',
                                className='input1'
                            ),

                            html.P("Enquiry Date", className='date_1'),
                            dcc.DatePickerSingle(
                                id='entry_date',
                                placeholder='Select a Date',
                                with_portal=True,
                                display_format="YYYY-MM-DD",
                                className='input1',

                            ),
                            html.P("Project Description"),
                            dcc.Input(
                                id='project_description',
                                type='text',
                                className='input1'
                            ),
                            html.P("Scope of Work"),
                            dcc.Dropdown(
                                id='scope_of_work',
                                options=[{'value': i, 'label': i} for i in sow],
                                className='dropdownc',
                                placeholder="Select a Work",
                                style={'border': 'none', 'border-radius': '20px'}
                            ),
                        ], className='')
                    ], className='squreborder'),
                    html.Div([
                        html.H5("Client Details", className='modeltitle'),

                        html.P("Client Dropdown"),
                        dcc.Dropdown(
                            id='client_dropdown',
                            options=[{'value': i, 'label': i} for i in client_data],
                            className='dropdownc',
                            placeholder="Select a Client",
                            style={'border': 'none', 'border-radius': '20px'}

                        ),
                        dcc.Loading(
                            id="loading-1",
                            type="dot",
                            fullscreen='true',
                            style={'background-color': 'rgba(67, 60, 233,0.3)'},
                            children=html.Div(id="loading-output-1")
                        ),
                        html.P("Client Name"),
                        dcc.Input(
                            id='client_name',
                            type='text',
                            required='true',
                            className='input1'
                        ),
                        html.P("Client Location"),
                        dcc.Input(
                            id='client_location',
                            type='text',
                            required='true',
                            className='input1'
                        ),
                        html.P("Existing Client"),
                        dcc.RadioItems(
                            id='existing_client',
                            options=[{'value': 'YES', 'label': 'YES'},
                                     {'value': 'NO', 'label': 'NO'}]
                        ),
                    ], className='squreborder'),

                    html.Div([
                        html.Div([
                            html.H5("Internal Follow Up", className='modeltitle'),
                            html.P("Internal Lead"),
                            dcc.Input(
                                id='internal_lead',
                                type='text',
                                className='input1'
                            ),
                            html.P("External Lead"),
                            dcc.Input(
                                id='external_lead',
                                type='text',
                                className='input1'
                            ),
                            html.P("Status"),
                            dcc.Dropdown(
                                id='lead_status',
                                options=[{'value': i, 'label': i} for i in lead_status],
                                className='dropdownc',
                                placeholder="Select a lead status",
                                style={'border': 'none', 'border-radius': '20px'}
                            ),

                            html.P("Raj Group Office"),
                            dcc.Dropdown(
                                id='raj_group_office',
                                options=[{'value': i, 'label': i} for i in raj_group_office],
                                className='dropdownc',
                                placeholder="Select an office",
                                style={'border': 'none', 'border-radius': '20px'}
                            ),
                            html.P("Follow Up Person"),
                            dcc.Dropdown(
                                id='follow_up_person',
                                options=[{'value': i, 'label': i} for i in follow_up_person],
                                className='dropdownc',
                                placeholder="Select a Work",
                                style={'border': 'none', 'border-radius': '20px'}
                            ),
                            html.P("Tentative Project Value"),
                            dcc.Input(
                                id='tentative_project_value',
                                type='text',
                                className='input1'
                            ),
                            html.Div([
                                html.P("Quotation Number"),
                                dcc.Input(
                                    id='quotation_number',
                                    type='text',
                                    className='input1'
                                ),
                            ], style={'display': 'none'}),
                            html.P("Remarks"),
                            dcc.Input(
                                id='remarks',
                                type='text',
                                className='input1'
                            ),
                        ], className=''),

                    ], className='followup squreborder'),

                    html.Div([
                        html.H5("Contact Details", className='modeltitle'),
                        html.Div([
                            html.Div(id="add_contact_div", className='add_dynamic_details',
                                     style={'margin-bottom': '10px'}),
                            html.Div([
                                dcc.ConfirmDialogProvider(
                                    children=html.Button(
                                        'Add',
                                        className='allbutton alignbtn'
                                    ),
                                    id='add_another_contact',
                                    message='Are you sure you want to continue?'
                                ),

                                dcc.ConfirmDialogProvider(
                                    children=html.Button(
                                        'Delete',
                                        className='allbutton alignbtn'
                                    ),
                                    id='delete_contact_button',
                                    message='Are you sure you want to continue?'
                                ),
                            ], className='centerbtn'),
                        ]),

                    ], className='squreborder addcontect', style={'position': 'relative'}),

                    html.Div(id="add_offer_hide", children=[
                        html.H5("Offer Details", className='modeltitle'),
                        html.Div(id="add_offer_div", className='add_dynamic_details', style={'margin-bottom': '10px'}),
                        # html.P("Add Another Offer"),
                        html.Div([
                            dcc.ConfirmDialogProvider(
                                children=html.Button(
                                    'Add Offer',
                                    className='allbutton alignbtn'
                                ),
                                id='add_another_offer',
                                message='Are you sure you want to continue?'
                            ),
                        ], className='centerbtn'),
                    ], className='squreborder addoffer', style={'display': 'none'}),

                    html.Div([

                        dcc.ConfirmDialogProvider(
                            children=html.Button(
                                'Submit',
                                className='allbutton'
                            ),
                            id='submit_button',
                            message='Are you sure you want to continue?'
                        ),
                        dcc.Loading(
                            id="loading-2",
                            type="circle",
                            fullscreen='true',
                            style={'background-color': 'rgba(67, 60, 233,0.3)'},
                            children=html.Div(id="loading-output-2")
                        ),
                        dcc.ConfirmDialogProvider(
                            children=html.Button(
                                'Close',
                                id='close_dash',
                                className='allbutton'
                            ),
                            id='close_button',
                            message='Are you sure you want to continue?'
                        ),

                        dcc.ConfirmDialog(
                            id='modal_display',
                            message='Please fill all required values marked in RED!!',
                        ),

                    ], className='btnn btncls')
                ], className='form_container'),
            ], id='show_dashboard', className='body_data4'),

            # Body4 End

        ]),
    ]),
    html.Div(id='tabs-content')
], className="page")


def order_layout():
    connection = AWSMySQLConn()
    # if company == "DN":
    data_orders = connection.execute_query(
        "select order_key, order_date, project_description, client_name,"
        "client_location, project_value, scope_of_work, order_status, project_incharge from RajElectricalsOrdersNew "
        "order by 1 desc;")
    # elif company == "RJ":
    # data_orders = connection.execute_query(
    #     "select order_key, order_date, project_description, client_name,"
    #     "client_location, project_value, scope_of_work, order_status, project_incharge from DNSyndicateOrdersNew order by order_date desc;")

    data_upcoming_projects = connection.execute_query(
        "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
        "client_location, lead_status, follow_up_person from RajGroupEnquiryList order by 1 desc;")

    en_keys = list(data_upcoming_projects['enquiry_key'])


    client_data = ['Other']
    client_data_all = connection.execute_query("select client_name, client_location from RajGroupClientList group by 1,2;")
    for i, j in zip(list(client_data_all['client_name']), list(client_data_all['client_location'])):
        client_data.append(i+" -- "+j)


    return html.Div([
        html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        # html.Div([
        #     html.Div([
        #         dcc.Link('HOME', href='/', refresh=True),
        #     ], className="one columns"),
        #     html.Div([
        #         dcc.Link('REFRESH', href='/dash/', refresh=True),
        #     ], className="one columns"),
        #     # html.Div([
        #     #     html.A('Download Dispatch Register', href='/dash/urlToDownload', id='my_link'),
        #     # ], className="one columns"),
        # ], className="row"),

        html.Div([
            html.Div([
                html.A('Home', href="/", className='nav_item now', style={'border-left': 'none'}),
                html.A('REFRESH', href="/dash2/", className='nav_item'),

            ], className='nav_bar_content'),
            html.A('Logout', href="/logout", className='nav_item last'),
        ], className='nav_bar'),
        html.Div([
            html.Div([
                html.A([
                    html.Img(src="assets/close.png", style={'width': '30px', 'height': '30px', 'padding': '5px'})
                ], href="javascript:closeNav()", className='closebtn'),
                html.A('HOME', href="/", className='menulink'),
                html.A('REFRESH', href="/dash/", className='menulink'),
                html.A('LOGOUT', href="/logout", className='menulink'),

            ], id='mySidenav', className='sidenav'),

            html.A([
                html.Img(src="assets/menu.png", style={'width': '30px', 'height': '30px', 'padding': '5px'})
            ], href='javascript:openNav()'),

        ], className='nav_bar2'),

        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(id='tab1', value='tab-1', label='Work Order Dashboard', children=[
                # Body1 start
                html.Div([
                    html.Div([
                        html.H1('Offer Details', className='main_title')
                    ]),
                    html.Div([
                        html.Div([
                            # Pie-chart reflecting scope wise orders
                            dcc.Graph(
                                id='orders_scope_pie_chart',
                                figure=orders_scope_pie_data(data_orders)
                            ),
                        ], className="pie_charts_container"),

                        html.Div([

                            # Pie-chart reflecting status wise orders
                            dcc.Graph(
                                id='orders_status_pie_chart',
                                figure=orders_status_pie_data(data_orders)
                            ),
                        ], className="pie_charts_container"),

                    ], className='pie_charts'),
                ], className='body_data2'),
                # Body1 End

                # BOdy2 Start
                html.Div([

                    html.Div([
                        # Data Table - Work Orders
                        dash_table.DataTable(
                            id='orders_table',
                            style_data={'minWidth': 'auto', 'width': 'auto', 'maxWidth': '8vw'},
                            style_table={
                                'overflowY': 'auto',
                                'minHeight': '90vh', 'height': '90vh', 'maxHeight': '90vh',

                            },
                            style_header={
                                'backgroundColor': '#1034A6',
                                'fontWeight': '500',
                                'color': '#F5F5F5',
                                'borderRadius': '10px',
                                # 'border': '1px solid  #F5F5F5',
                                'font-family': 'Comfortaa',
                                'font-size': '2',
                                'height': '7vh'

                            },
                            style_cell={
                                'textAlign': 'center',
                                'whiteSpace': 'normal',
                                'minHeight': '30px',
                                'font-size': 'xx-small',
                                'font-family': 'Comfortaa',

                            },
                            style_data_conditional=[
                                {'color': '#1034A6',
                                 'backgroundColor': '#F5F5F5',
                                 'border': '1px solid  #1034A6',
                                 }
                            ],
                            fixed_rows={'headers': True, 'data': 0},
                            # tooltip_data=[
                            #     {
                            #         column: {'value': str(value), 'type': 'markdown'}
                            #         for column, value in row.items()
                            #     } for row in data_orders.to_dict('rows')
                            # ],
                            # tooltip_duration=None,
                            # css=[{
                            #     'selector': '.dash-cell div.dash-cell-value',
                            #     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                            # }],
                            css=[{
                                'selector': '.dash-cell div.dash-cell-value',
                                'rule': 'display: inline; font-family: Comfortaa;white-space: inherit; overflow: inherit; text-overflow: inherit;',

                            }],

                            style_filter_conditional=[{
                                'backgroundColor': '#F5F5F5',
                                'color': '#1034A6',
                                'padding': '10px',
                                'height': '20px',
                                'border': '2px solid #433cde9',
                            }],
                            style_as_list_view=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            row_selectable="single",
                            editable=False,
                            columns=[{"name": i, "id": i} for i in data_orders.columns],
                            data=data_orders.to_dict('records')
                        ),

                    ], className='table_data')
                ], className='body_data3'),
                # BOdy2 end
                html.Div([
                    dcc.Dropdown(
                        id='file_options',
                        options=[{'value': i, 'label': i} for i in ['Raj Electricals Orders']],
                        placeholder='Select File to Download'
                    ),
                ], className="two columns"),
                html.Div([
                    html.A('Download', id='my_link'),
                ], className="two columns"),
            ]),
            dcc.Tab(id='tab2', value='tab-2', label='Raj Group Order Form', children=[
                # Body3 start
                html.Div([
                    html.Div([
                        html.Div([

                            html.Div([

                                html.H5("Project Details", className='modeltitle'),

                                html.P("Enquiry Key"),
                                dcc.Dropdown(
                                    id='order_enquiry_key',
                                    options=[{'value': i, 'label': i} for i in en_keys],
                                    className='dropdownc',
                                    placeholder="Select a Enquiry Key",
                                    style={'border': 'none', 'border-radius': '20px'}
                                ),
                                html.Div([
                                    html.P("Order Key"),
                                    dcc.Input(
                                        id='order_key',
                                        type='text',
                                        className='input1 ',

                                    ),
                                    dcc.ConfirmDialogProvider(
                                        # children=html.Button(
                                        #     'Load Order Key',
                                        # ),
                                        [
                                            html.A([
                                                html.Img(src='assets/loadkey.png', className="logoimg", alt='home'),
                                            ], className="keyspan")
                                        ],
                                        id='order_key_load_button',
                                        message='Are you sure you want to continue?'
                                    ),

                                ], className='loadkey'),

                                html.P("Order Date", className='date_1'),
                                dcc.DatePickerSingle(
                                    id='order_date',
                                    placeholder='Select a Date',
                                    with_portal=True,
                                    display_format="YYYY-MM-DD",
                                    className='input1',

                                ),
                                html.P("PO No"),
                                dcc.Input(
                                    id='order_po_no',
                                    type='text',
                                    className='input1',

                                ),
                                html.P("Project Description"),
                                dcc.Input(
                                    id='order_project_description',
                                    type='text',
                                    className='input1'
                                ),
                                html.P("Scope of Work"),
                                dcc.Dropdown(
                                    id='order_scope_of_work',
                                    options=[{'value': i, 'label': i} for i in sow],
                                    className='dropdownc',
                                    placeholder="Select a Work",
                                    style={'border': 'none', 'border-radius': '20px'}
                                ),
                            ], className='')
                        ], className='squreborder'),
                        html.Div([
                            html.H5("Client Details", className='modeltitle'),

                            html.P("Client Dropdown"),
                            dcc.Dropdown(
                                id='order_client_dropdown',
                                options=[{'value': i, 'label': i} for i in client_data],
                                className='dropdownc',
                                placeholder="Select a Client",
                                style={'border': 'none', 'border-radius': '20px'}

                            ),

                            html.P("Client Name"),
                            dcc.Input(
                                id='order_client_name',
                                type='text',
                                required='true',
                                className='input1'
                            ),
                            html.P("Client Location"),
                            dcc.Input(
                                id='order_client_location',
                                type='text',
                                required='true',
                                className='input1'
                            ),
                            html.P("Existing Client"),
                            dcc.RadioItems(
                                id='order_existing_client',
                                options=[{'value': 'YES', 'label': 'YES'},
                                         {'value': 'NO', 'label': 'NO'}]
                            ),
                        ], className='squreborder'),

                        html.Div([
                            html.Div([
                                html.H5("Local Office Details", className='modeltitle'),
                                html.P("Order No/Tender File No"),
                                dcc.Input(
                                    id='order_order_no',
                                    type='text',
                                    className='input1'
                                ),
                                html.P("File No"),
                                dcc.Input(
                                    id='order_file_no',
                                    type='text',
                                    className='input1'
                                ),
                                html.P("Status"),
                                dcc.Dropdown(
                                    id='order_status',
                                    options=[{'value': i, 'label': i} for i in order_status],
                                    className='dropdownc',
                                    placeholder="Select a lead status",
                                    style={'border': 'none', 'border-radius': '20px'}
                                ),
                                html.P("Project incharge"),
                                dcc.Input(
                                    id='order_project_incharge',
                                    type='text',
                                    className='input1',
                                    required=True
                                ),
                                html.P("Raj Group Office"),
                                dcc.Dropdown(
                                    id='order_raj_group_office',
                                    options=[{'value': i, 'label': i} for i in raj_group_office],
                                    className='dropdownc',
                                    placeholder="Select an office",
                                    style={'border': 'none', 'border-radius': '20px'}
                                ),
                                html.P("Project value"),
                                dcc.Input(
                                    id='order_project_value',
                                    type='text',
                                    className='input1',

                                ),

                                html.P("Remarks"),
                                dcc.Input(
                                    id='order_remarks',
                                    type='text',
                                    className='input1'
                                ),

                                html.P("Computer Location"),
                                dcc.Input(
                                    id='order_comp_location',
                                    type='text',
                                    className='input1'
                                ),

                                html.Header("Feedback Link"),
                                dcc.Link(id="feedback_link", children=[
                                    None
                                ]),
                            ], className=''),

                        ], className='followup squreborder'),

                        html.Div([
                            html.H5("Contact Details", className='modeltitle'),
                            html.Div([
                                html.Div(id="order_add_contact_div", className='add_dynamic_details',
                                         style={'margin-bottom': '10px'}),
                                html.Div([
                                    dcc.ConfirmDialogProvider(
                                        children=html.Button(
                                            'Add',
                                            className='allbutton alignbtn'
                                        ),
                                        id='order_add_another_contact',
                                        message='Are you sure you want to continue?'
                                    ),

                                    dcc.ConfirmDialogProvider(
                                        children=html.Button(
                                            'Delete',
                                            className='allbutton alignbtn'
                                        ),
                                        id='delete_contact_button',
                                        message='Are you sure you want to continue?'
                                    ),
                                ], className='centerbtn'),
                            ]),

                        ], className='squreborder addcontect', style={'position': 'relative'}),

                        html.Div(id="add_offer_hide", children=[
                            html.H5("Offer Details", className='modeltitle'),
                            html.Div(id="add_offer_div", className='add_dynamic_details',
                                     style={'margin-bottom': '10px'}),
                            # html.P("Add Another Offer"),
                            html.Div([
                                dcc.ConfirmDialogProvider(
                                    children=html.Button(
                                        'Add Offer',
                                        className='allbutton alignbtn'
                                    ),
                                    id='add_another_offer',
                                    message='Are you sure you want to continue?'
                                ),
                            ], className='centerbtn'),
                        ], className='squreborder addoffer', style={'display': 'none'}),

                        html.Div([

                            dcc.ConfirmDialogProvider(
                                children=html.Button(
                                    'Submit',
                                    className='allbutton'
                                ),
                                id='order_submit_button',
                                message='Are you sure you want to continue?'
                            ),

                            dcc.ConfirmDialogProvider(
                                children=html.Button(
                                    'Close',
                                    id='close_dash',
                                    className='allbutton'
                                ),
                                id='order_close_button',
                                message='Are you sure you want to continue?'
                            ),

                            dcc.ConfirmDialog(
                                id='order_modal_display',
                                message='Please fill all required values marked in RED!!',
                            ),

                        ], className='btnn btncls')
                    ], className='form_container'),
                ], id='show_dashboard', className='body_data4'),
                # Body3 End
            ])
        ]),
        html.Div(id='tabs-content')
], className="page")



def rv_order_layout():
    connection = AWSMySQLConn()
    # if company == "DN":
    data_orders = connection.execute_query(
        "select order_key, order_date, project_description, client_name,"
        "client_location, project_value, scope_of_work, order_status, project_incharge from RajVijtechOrdersNew order by 1 desc;")
    # elif company == "RJ":
    # data_orders = connection.execute_query(
    #     "select order_key, order_date, project_description, client_name,"
    #     "client_location, project_value, scope_of_work, order_status, project_incharge from DNSyndicateOrdersNew order by order_date desc;")

    data_upcoming_projects = connection.execute_query(
        "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
        "client_location, lead_status, follow_up_person from RajGroupEnquiryList order by 1 desc;")

    en_keys = list(data_upcoming_projects['enquiry_key'])


    client_data = ['Other']
    client_data_all = connection.execute_query("select client_name, client_location from RajGroupClientList group by 1,2;")
    for i, j in zip(list(client_data_all['client_name']), list(client_data_all['client_location'])):
        client_data.append(i+" -- "+j)


    return html.Div([
    html.Div([
        html.Div([
            dcc.Link('HOME', href='/', refresh=True),
        ], className="one columns"),
        html.Div([
            dcc.Link('REFRESH', href='/dash5/', refresh=True),
        ], className="one columns"),
        html.Div([
            dcc.Dropdown(
                id='file_options',
                options=[{'value': i, 'label': i} for i in ['Raj Vijtech Orders']],
                placeholder='Select File to Download'
            ),
        ], className="two columns"),
        html.Div([
            html.A('Download', id='my_link'),
        ], className="two columns"),
    ], className="row"),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tab1', value='tab-1', label='Work Order Dashboard', children=[
            html.Div([
                html.Div([
                    # Pie-chart reflecting scope wise orders
                    dcc.Graph(
                        id='orders_scope_pie_chart',
                        figure=orders_scope_pie_data(data_orders)
                    ),
                ], className="pretty_container six columns"),

                html.Div([
                    # Pie-chart reflecting status wise orders
                    dcc.Graph(
                        id='orders_status_pie_chart',
                        figure=orders_status_pie_data(data_orders)
                    ),
                ], className="pretty_container six columns")

            ], className="row"),
            # Data Table - Work Orders
            dash_table.DataTable(
                id='orders_table',
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
                    'textAlign': 'center',
                    'whiteSpace': 'normal',
                    'minHeight': '30px',
                    # 'height': 'auto',
                    # 'overflow': 'scroll',
                    # 'textOverflow': 'ellipsis',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                fixed_rows={'headers': True, 'data': 0},
                # tooltip_data=[
                #     {
                #         column: {'value': str(value), 'type': 'markdown'}
                #         for column, value in row.items()
                #     } for row in data_orders.to_dict('rows')
                # ],
                # tooltip_duration=None,
                # css=[{
                #     'selector': '.dash-cell div.dash-cell-value',
                #     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                # }],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="single",
                editable=False,
                columns=[{"name": i, "id": i} for i in data_orders.columns],
                data=data_orders.to_dict('records')
            ),

        ]),
        dcc.Tab(id='tab2', value='tab-2', label='Raj Group Order Form', children=[
            html.Div([
                html.Div([
                    html.H3("Project Details"),
                    html.Header("Enquiry Key"),
                    dcc.Dropdown(
                        id='order_enquiry_key',
                        options=[{'value': i, 'label': i} for i in en_keys],
                    ),
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                            'Load Order Key',
                        ),
                        id='order_key_load_button',
                        message='Are you sure you want to continue?'
                    ),
                    html.Header("Order Key"),
                    dcc.Input(
                        id='order_key',
                        type='text',
                        placeholder='Order Key is locked for User',
                        size=50,
                        disabled=True
                    ),
                    html.Header("Order Date", className="required"),
                    dcc.DatePickerSingle(
                        id='order_date',
                        placeholder='Select a Date',
                        with_portal=True,
                        display_format="YYYY-MM-DD",
                    ),
                    html.Header("PO No"),
                    dcc.Input(
                        id='order_po_no',
                        type='text',
                        placeholder='Enter Client PO No',
                        size=50
                    ),
                    html.Header("Project Description"),
                    dcc.Input(
                        id='order_project_description',
                        type='text',
                        placeholder='Enter Project Description',
                        size=50
                    ),
                    html.Header("Scope of Work", className="required"),
                    dcc.Dropdown(
                        id='order_scope_of_work',
                        options=[{'value': i, 'label': i} for i in sow],
                    ),
                ], className="four columns"),
                html.Div([
                    html.H3("Client Details"),
                    html.Header("Client Dropdown", className="required"),
                    dcc.Dropdown(
                        id='order_client_dropdown',
                        options=[{'value': i, 'label': i} for i in client_data]
                    ),
                    html.Header("Client Name", className="required"),
                    dcc.Input(
                        id='order_client_name',
                        type='text',
                        placeholder='Enter Client Name',
                        size=50,
                    ),
                    html.Header("Client Location", className="required"),
                    dcc.Input(
                        id='order_client_location',
                        type='text',
                        placeholder='Enter Client Location',
                        size=50
                    ),
                    html.Header("Existing Client"),
                    dcc.RadioItems(
                        id='order_existing_client',
                        options=[{'value': 'YES', 'label': 'YES'},
                                 {'value': 'NO', 'label': 'NO'}]
                    ),
                ], className="four columns"),
            ], className="row"),

            html.H3("Contact Details"),
            html.Div([
                html.Div(id="order_add_contact_div"),
                html.Header("Add Another Contact"),
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Add Contact',
                    ),
                    id='order_add_another_contact',
                    message='Are you sure you want to continue?'
                ),
            ], className="row"),

            html.H3("Local Office Details"),

            html.Div([
                html.Div([
                    html.Header("Order No/Tender File No"),
                    dcc.Input(
                        id='order_order_no',
                        type='text',
                        placeholder='Order No is locked for User',
                        size=50,
                        disabled=True
                    ),
                    html.Header("File No"),
                    dcc.Input(
                        id='order_file_no',
                        type='text',
                        placeholder='File No',
                        size=50
                    ),
                    html.Header("Status", className="required"),
                    dcc.Dropdown(
                        id='order_status',
                        options=[{'value': i, 'label': i} for i in order_status]
                    ),
                    html.Header("Project Incharge", className="required"),
                    dcc.Input(
                        id='order_project_incharge',
                        type='text',
                        placeholder='Project Incharge',
                        size=50
                    ),
                ], className="four columns"),
                html.Div([
                    html.Header("Raj Group Office", className="required"),
                    dcc.Dropdown(
                        id='order_raj_group_office',
                        options=[{'value': i, 'label': i} for i in raj_group_office]
                    ),
                    html.Header("Project Value"),
                    dcc.Input(
                        id='order_project_value',
                        type='text',
                        placeholder='Tentative Project Value',
                        size=50
                    ),
                    html.Header("Remarks"),
                    dcc.Input(
                        id='order_remarks',
                        type='text',
                        placeholder='Remarks',
                        size=50
                    ),
                    html.Header("Computer Location"),
                    dcc.Input(
                        id='order_comp_location',
                        type='text',
                        placeholder='Computer Location',
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
                        id='order_submit_button',
                        message='Are you sure you want to continue?'
                    ),
                ], className="six columns"),
                html.Div([
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                            'Close',
                        ),
                        id='order_close_button',
                        message='Are you sure you want to continue?'
                    )
                ], className="six columns"),
                dcc.ConfirmDialog(
                    id='order_modal_display',
                    message='Please fill all required values marked in RED!!',
                ),
            ], className="row"),
        ])
    ]),
    html.Div(id='tabs-content')
], className="page")


def dn_order_layout():
    connection = AWSMySQLConn()
    # data_orders_dn = connection.execute_query(
    #     "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
    #     "client_location, lead_status, follow_up_person from RajGroupEnquiryList order by 1 desc;")

    data_orders_dn = connection.execute_query(
        "select order_key, order_date, project_description, client_name,"
        "client_location, project_value, scope_of_work, order_status, project_incharge from DNSyndicateOrdersNew order by 1 desc;")

    data_upcoming_projects = connection.execute_query(
        "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
        "client_location, lead_status, follow_up_person from RajGroupEnquiryList order by 1 desc;")

    en_keys = list(data_upcoming_projects['enquiry_key'])


    client_data = ['Other']
    client_data_all = connection.execute_query("select client_name, client_location from RajGroupClientList group by 1,2;")
    for i, j in zip(list(client_data_all['client_name']), list(client_data_all['client_location'])):
        client_data.append(i+" -- "+j)


    return html.Div([
    html.Div([
        html.Div([
            dcc.Link('HOME', href='/', refresh=True),
        ], className="one columns"),
        html.Div([
            dcc.Link('REFRESH', href='/dash3/', refresh=True),
        ], className="one columns"),
    ], className="row"),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(id='tab1', value='tab-1', label='Work Order Dashboard', children=[
            html.Div([
                html.Div([
                    # Pie-chart reflecting scope wise orders
                    dcc.Graph(
                        id='orders_scope_pie_chart',
                        figure=orders_scope_pie_data(data_orders_dn)
                    ),
                ], className="pretty_container six columns"),

                html.Div([
                    # Pie-chart reflecting status wise orders
                    dcc.Graph(
                        id='orders_status_pie_chart',
                        figure=orders_status_pie_data(data_orders_dn)
                    ),
                ], className="pretty_container six columns")

            ], className="row"),
            # Data Table - Work Orders
            dash_table.DataTable(
                id='orders_table',
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
                    'textAlign': 'center',
                    'whiteSpace': 'normal',
                    'minHeight': '30px',
                    # 'height': 'auto',
                    # 'overflow': 'scroll',
                    # 'textOverflow': 'ellipsis',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                fixed_rows={'headers': True, 'data': 0},
                # tooltip_data=[
                #     {
                #         column: {'value': str(value), 'type': 'markdown'}
                #         for column, value in row.items()
                #     } for row in data_orders.to_dict('rows')
                # ],
                # tooltip_duration=None,
                # css=[{
                #     'selector': '.dash-cell div.dash-cell-value',
                #     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                # }],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="single",
                editable=False,
                columns=[{"name": i, "id": i} for i in data_orders_dn.columns],
                data=data_orders_dn.to_dict('records')
            ),
        ]),
        dcc.Tab(id='tab2', value='tab-2', label='Raj Group Order Form', children=[
            html.Div([
                html.Div([
                    html.H3("Project Details"),
                    html.Header("Enquiry Key"),
                    dcc.Dropdown(
                        id='order_enquiry_key',
                        options=[{'value': i, 'label': i} for i in en_keys],
                    ),
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                            'Load Order Key',
                        ),
                        id='order_key_load_button',
                        message='Are you sure you want to continue?'
                    ),
                    html.Header("Order Key"),
                    dcc.Input(
                        id='order_key',
                        type='text',
                        placeholder='Order Key is locked for User',
                        size=50,
                        disabled=True
                    ),
                    html.Header("Order Date", className="required"),
                    dcc.DatePickerSingle(
                        id='order_date',
                        placeholder='Select a Date',
                        with_portal=True,
                        display_format="YYYY-MM-DD",
                    ),
                    html.Header("PO No"),
                    dcc.Input(
                        id='order_po_no',
                        type='text',
                        placeholder='Enter Client PO No',
                        size=50
                    ),
                    html.Header("Project Description"),
                    dcc.Input(
                        id='order_project_description',
                        type='text',
                        placeholder='Enter Project Description',
                        size=50
                    ),
                    html.Header("Scope of Work", className="required"),
                    dcc.Dropdown(
                        id='order_scope_of_work',
                        options=[{'value': i, 'label': i} for i in sow],
                    ),
                ], className="four columns"),
                html.Div([
                    html.H3("Client Details"),
                    html.Header("Client Dropdown", className="required"),
                    dcc.Dropdown(
                        id='order_client_dropdown',
                        options=[{'value': i, 'label': i} for i in client_data]
                    ),
                    html.Header("Client Name", className="required"),
                    dcc.Input(
                        id='order_client_name',
                        type='text',
                        placeholder='Enter Client Name',
                        size=50,
                    ),
                    html.Header("Client Location", className="required"),
                    dcc.Input(
                        id='order_client_location',
                        type='text',
                        placeholder='Enter Client Location',
                        size=50
                    ),
                    html.Header("Existing Client"),
                    dcc.RadioItems(
                        id='order_existing_client',
                        options=[{'value': 'YES', 'label': 'YES'},
                                 {'value': 'NO', 'label': 'NO'}]
                    ),
                ], className="four columns"),
            ], className="row"),

            html.H3("Contact Details"),
            html.Div([
                html.Div(id="order_add_contact_div"),
                html.Header("Add Another Contact"),
                dcc.ConfirmDialogProvider(
                    children=html.Button(
                        'Add Contact',
                    ),
                    id='order_add_another_contact',
                    message='Are you sure you want to continue?'
                ),
            ], className="row"),

            html.H3("Local Office Details"),

            html.Div([
                html.Div([
                    html.Header("Order No/Tender File No"),
                    dcc.Input(
                        id='order_order_no',
                        type='text',
                        placeholder='Order No is locked for User',
                        size=50,
                        disabled=True
                    ),
                    html.Header("File No"),
                    dcc.Input(
                        id='order_file_no',
                        type='text',
                        placeholder='File No',
                        size=50
                    ),
                    html.Header("Status", className="required"),
                    dcc.Dropdown(
                        id='order_status',
                        options=[{'value': i, 'label': i} for i in order_status]
                    ),
                    html.Header("Project Incharge", className="required"),
                    dcc.Input(
                        id='order_project_incharge',
                        type='text',
                        placeholder='Project Incharge',
                        size=50
                    ),
                ], className="four columns"),
                html.Div([
                    html.Header("Raj Group Office", className="required"),
                    dcc.Dropdown(
                        id='order_raj_group_office',
                        options=[{'value': i, 'label': i} for i in raj_group_office]
                    ),
                    html.Header("Project Value"),
                    dcc.Input(
                        id='order_project_value',
                        type='text',
                        placeholder='Tentative Project Value',
                        size=50
                    ),
                    html.Header("Remarks"),
                    dcc.Input(
                        id='order_remarks',
                        type='text',
                        placeholder='Remarks',
                        size=50
                    ),
                    html.Header("Computer Location"),
                    dcc.Input(
                        id='order_comp_location',
                        type='text',
                        placeholder='Computer Location',
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
                        id='order_submit_button',
                        message='Are you sure you want to continue?'
                    ),
                ], className="six columns"),
                html.Div([
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                            'Close',
                        ),
                        id='order_close_button',
                        message='Are you sure you want to continue?'
                    )
                ], className="six columns"),
                dcc.ConfirmDialog(
                    id='order_modal_display',
                    message='Please fill all required values marked in RED!!',
                ),
            ], className="row"),
        ])
    ]),
    html.Div(id='tabs-content')
], className="page")


# def re_order_layout():
#     connection = AWSMySQLConn()
#     # data_orders_dn = connection.execute_query(
#     #     "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
#     #     "client_location, lead_status, follow_up_person from RajGroupEnquiryList order by 1 desc;")
#
#     data_orders_re = connection.execute_query(
#         "select order_key, order_date, project_description, client_name,"
#         "client_location, project_value, scope_of_work, order_status, project_incharge from RajEnterpriseOrdersNew order by order_date desc;")
#
#     data_upcoming_projects = connection.execute_query(
#         "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
#         "client_location, lead_status, follow_up_person from RajGroupEnquiryList order by 1 desc;")
#
#     en_keys = list(data_upcoming_projects['enquiry_key'])
#
#
#     client_data = ['Other']
#     client_data_all = connection.execute_query("select client_name, client_location from RajGroupClientList group by 1,2;")
#     for i, j in zip(list(client_data_all['client_name']), list(client_data_all['client_location'])):
#         client_data.append(i+" -- "+j)
#
#
#     return html.Div([
#     html.Div([
#         html.Div([
#             dcc.Link('HOME', href='/', refresh=True),
#         ], className="one columns"),
#         html.Div([
#             dcc.Link('REFRESH', href='/dash4/', refresh=True),
#         ], className="one columns"),
#     ], className="row"),
#     dcc.Tabs(id='tabs', value='tab-1', children=[
#         dcc.Tab(id='tab1', value='tab-1', label='Work Order Dashboard', children=[
#             html.Div([
#                 html.Div([
#                     # Pie-chart reflecting scope wise orders
#                     dcc.Graph(
#                         id='orders_scope_pie_chart',
#                         figure=orders_scope_pie_data(data_orders_re)
#                     ),
#                 ], className="pretty_container six columns"),
#
#                 html.Div([
#                     # Pie-chart reflecting status wise orders
#                     dcc.Graph(
#                         id='orders_status_pie_chart',
#                         figure=orders_status_pie_data(data_orders_re)
#                     ),
#                 ], className="pretty_container six columns")
#
#             ], className="row"),
#             # Data Table - Work Orders
#             dash_table.DataTable(
#                 id='orders_table',
#                 style_data={'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
#                 style_table={
#                     'maxHeight': '30',
#                     'overflowY': 'scroll'
#                 },
#                 style_header={
#                     'backgroundColor': 'rgb(230, 230, 230)',
#                     'fontWeight': 'bold'
#                 },
#                 style_cell={
#                     'textAlign': 'center',
#                     # 'height': 'auto',
#                     # 'overflow': 'scroll',
#                     # 'textOverflow': 'ellipsis',
#                 },
#                 style_data_conditional=[
#                     {
#                         'if': {'row_index': 'odd'},
#                         'backgroundColor': 'rgb(248, 248, 248)'
#                     }
#                 ],
#                 fixed_rows={'headers': True, 'data': 0},
#                 # tooltip_data=[
#                 #     {
#                 #         column: {'value': str(value), 'type': 'markdown'}
#                 #         for column, value in row.items()
#                 #     } for row in data_orders.to_dict('rows')
#                 # ],
#                 # tooltip_duration=None,
#                 # css=[{
#                 #     'selector': '.dash-cell div.dash-cell-value',
#                 #     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
#                 # }],
#                 filter_action="native",
#                 sort_action="native",
#                 sort_mode="multi",
#                 row_selectable="single",
#                 editable=False,
#                 columns=[{"name": i, "id": i} for i in data_orders_re.columns],
#                 data=data_orders_re.to_dict('records')
#             ),
#         ]),
#         dcc.Tab(id='tab2', value='tab-2', label='Raj Group Order Form', children=[
#             html.Div([
#                 html.Div([
#                     html.H3("Project Details"),
#                     html.Header("Enquiry Key"),
#                     dcc.Dropdown(
#                         id='order_enquiry_key',
#                         options=[{'value': i, 'label': i} for i in en_keys],
#                     ),
#                     html.Header("Order Key"),
#                     dcc.Input(
#                         id='order_key',
#                         type='text',
#                         placeholder='Order Key is locked for User',
#                         size=50,
#                         disabled=True
#                     ),
#                     html.Header("Order Date", className="required"),
#                     dcc.DatePickerSingle(
#                         id='order_date',
#                         placeholder='Select a Date',
#                         with_portal=True,
#                         display_format="YYYY-MM-DD",
#                     ),
#                     html.Header("PO No"),
#                     dcc.Input(
#                         id='order_po_no',
#                         type='text',
#                         placeholder='Enter Client PO No',
#                         size=50
#                     ),
#                     html.Header("Project Description"),
#                     dcc.Input(
#                         id='order_project_description',
#                         type='text',
#                         placeholder='Enter Project Description',
#                         size=50
#                     ),
#                     html.Header("Scope of Work", className="required"),
#                     dcc.Dropdown(
#                         id='order_scope_of_work',
#                         options=[{'value': i, 'label': i} for i in sow],
#                     ),
#                 ], className="four columns"),
#                 html.Div([
#                     html.H3("Client Details"),
#                     html.Header("Client Dropdown", className="required"),
#                     dcc.Dropdown(
#                         id='order_client_dropdown',
#                         options=[{'value': i, 'label': i} for i in client_data]
#                     ),
#                     html.Header("Client Name", className="required"),
#                     dcc.Input(
#                         id='order_client_name',
#                         type='text',
#                         placeholder='Enter Client Name',
#                         size=50,
#                     ),
#                     html.Header("Client Location", className="required"),
#                     dcc.Input(
#                         id='order_client_location',
#                         type='text',
#                         placeholder='Enter Client Location',
#                         size=50
#                     ),
#                     html.Header("Existing Client"),
#                     dcc.RadioItems(
#                         id='order_existing_client',
#                         options=[{'value': 'YES', 'label': 'YES'},
#                                  {'value': 'NO', 'label': 'NO'}]
#                     ),
#                 ], className="four columns"),
#             ], className="row"),
#
#             html.H3("Contact Details"),
#             html.Div([
#                 html.Div(id="order_add_contact_div"),
#                 html.Header("Add Another Contact"),
#                 dcc.ConfirmDialogProvider(
#                     children=html.Button(
#                         'Add Contact',
#                     ),
#                     id='order_add_another_contact',
#                     message='Are you sure you want to continue?'
#                 ),
#             ], className="row"),
#
#             html.H3("Local Office Details"),
#
#             html.Div([
#                 html.Div([
#                     html.Header("Order No"),
#                     dcc.Input(
#                         id='order_order_no',
#                         type='text',
#                         placeholder='Order No',
#                         size=50
#                     ),
#                     html.Header("File No"),
#                     dcc.Input(
#                         id='order_file_no',
#                         type='text',
#                         placeholder='File No',
#                         size=50
#                     ),
#                     html.Header("Status", className="required"),
#                     dcc.Dropdown(
#                         id='order_status',
#                         options=[{'value': i, 'label': i} for i in order_status]
#                     ),
#                     html.Header("Project Incharge", className="required"),
#                     dcc.Input(
#                         id='order_project_incharge',
#                         type='text',
#                         placeholder='Project Incharge',
#                         size=50
#                     ),
#                 ], className="four columns"),
#                 html.Div([
#                     html.Header("Raj Group Office", className="required"),
#                     dcc.Dropdown(
#                         id='order_raj_group_office',
#                         options=[{'value': i, 'label': i} for i in raj_group_office]
#                     ),
#                     html.Header("Project Value"),
#                     dcc.Input(
#                         id='order_project_value',
#                         type='text',
#                         placeholder='Tentative Project Value',
#                         size=50
#                     ),
#                     html.Header("Remarks"),
#                     dcc.Input(
#                         id='order_remarks',
#                         type='text',
#                         placeholder='Remarks',
#                         size=50
#                     ),
#                     html.Header("Computer Location"),
#                     dcc.Input(
#                         id='order_comp_location',
#                         type='text',
#                         placeholder='Computer Location',
#                         size=50
#                     ),
#                 ], className="four columns"),
#             ], className="row"),
#             html.Div([
#                 html.Div([
#                     dcc.ConfirmDialogProvider(
#                         children=html.Button(
#                             'Submit',
#                         ),
#                         id='order_submit_button',
#                         message='Are you sure you want to continue?'
#                     ),
#                 ], className="six columns"),
#                 html.Div([
#                     dcc.ConfirmDialogProvider(
#                         children=html.Button(
#                             'Close',
#                         ),
#                         id='order_close_button',
#                         message='Are you sure you want to continue?'
#                     )
#                 ], className="six columns"),
#                 dcc.ConfirmDialog(
#                     id='order_modal_display',
#                     message='Please fill all required values marked in RED!!',
#                 ),
#             ], className="row"),
#         ])
#     ]),
#     html.Div(id='tabs-content')
# ], className="page")

if __name__ == '__main__':
    connection = AWSMySQLConn()
    data = connection.execute_query("select * from RajGroupEnquiryList;")
    print(lead_stages_bar_data(data))


