import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import time



# connection = AWSMySQLConn()
# # data = connection.execute_query("select enquiry_key, offer_date from RajGroupEnquiryList where offer_date!='0000-00-00'"
# #                                 "limit 1;").iloc[0]['enquiry_key']
#
# data = connection.execute_query(
#         "select enquiry_key, entry_date, project_description, scope_of_work, client_name,"
#         "client_location, lead_status, follow_up_person from RajGroupEnquiryList;")
#
#
# start_time = time.time()
# weekly_leads_data = connection.execute_query("select lead_status, count(*) as cnt from RajGroupEnquiryList group by 1")
# print(weekly_leads_data)
# print("--- %s Second seconds ---" % (time.time() - start_time))
#
# start_time = time.time()
# data_mod = data[['enquiry_key', 'scope_of_work']].groupby('scope_of_work',
#                                             as_index=False).count().rename(columns={'enquiry_key':'cnt'})
# services = list(data_mod['scope_of_work'])
# service_wise_data = list(data_mod['cnt'])
# print(services)
# print(service_wise_data)
# print("--- %s First seconds ---" % (time.time() - start_time))

add_offer_div_value = [       {       'namespace': 'dash_html_components',
                'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                             'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                                                                          'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                                                                                                                       'props': {       'children': 'Offer '
                                                                                                                                                                                    'Date'},
                                                                                                                                                       'type': 'Header'},
                                                                                                                                               {       'namespace': 'dash_core_components',
                                                                                                                                                       'props': {       'disabled': True,
                                                                                                                                                                        'id': 'offer_timestamp_id_0',
                                                                                                                                                                        'placeholder': 'Offer '
                                                                                                                                                                                       'Date '
                                                                                                                                                                                       'is '
                                                                                                                                                                                       'locked '
                                                                                                                                                                                       'for '
                                                                                                                                                                                       'User',
                                                                                                                                                                        'size': 50,
                                                                                                                                                                        'type': 'text',
                                                                                                                                                                        'value': '2020-04-15T04:24:27'},
                                                                                                                                                       'type': 'Input'}],
                                                                                                                           'className': 'four '
                                                                                                                                        'columns'},
                                                                                                          'type': 'Div'},
                                                                                                  {       'namespace': 'dash_html_components',
                                                                                                          'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                                                                                                                       'props': {       'children': 'Dispatch '
                                                                                                                                                                                    'Number'},
                                                                                                                                                       'type': 'Header'},
                                                                                                                                               {       'namespace': 'dash_core_components',
                                                                                                                                                       'props': {       'id': 'dispatch_id_0',
                                                                                                                                                                        'n_blur': 1,
                                                                                                                                                                        'n_blur_timestamp': 1586925117147,
                                                                                                                                                                        'placeholder': 'Dispatch '
                                                                                                                                                                                       'Number',
                                                                                                                                                                        'size': 50,
                                                                                                                                                                        'type': 'text',
                                                                                                                                                                        'value': 'sample_ref_1'},
                                                                                                                                                       'type': 'Input'}],
                                                                                                                           'className': 'four '
                                                                                                                                        'columns',
                                                                                                                           'n_clicks': 1,
                                                                                                                           'n_clicks_timestamp': 1586925115136},
                                                                                                          'type': 'Div'},
                                                                                                  {       'namespace': 'dash_html_components',
                                                                                                          'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                                                                                                                       'props': {       'children': 'Offer '
                                                                                                                                                                                    'Location '
                                                                                                                                                                                    'on '
                                                                                                                                                                                    'Local '
                                                                                                                                                                                    'Computer'},
                                                                                                                                                       'type': 'Header'},
                                                                                                                                               {       'namespace': 'dash_core_components',
                                                                                                                                                       'props': {       'id': 'offer_location_id_0',
                                                                                                                                                                        'n_blur': 1,
                                                                                                                                                                        'n_blur_timestamp': 1586925118900,
                                                                                                                                                                        'placeholder': 'Offer '
                                                                                                                                                                                       'Location',
                                                                                                                                                                        'size': 50,
                                                                                                                                                                        'type': 'text',
                                                                                                                                                                        'value': 'sample_loc_1'},
                                                                                                                                                       'type': 'Input'}],
                                                                                                                           'className': 'four '
                                                                                                                                        'columns',
                                                                                                                           'n_clicks': 1,
                                                                                                                           'n_clicks_timestamp': 1586925117153},
                                                                                                          'type': 'Div'}],
                                                                              'className': 'row',
                                                                              'n_clicks': 2,
                                                                              'n_clicks_timestamp': 1586925117154},
                                                             'type': 'Div'},
                                                     {       'namespace': 'dash_html_components',
                                                             'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                                                                          'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                                                                                                                       'props': {       'children': 'Offer '
                                                                                                                                                                                    'Submitted '
                                                                                                                                                                                    'By'},
                                                                                                                                                       'type': 'Header'},
                                                                                                                                               {       'namespace': 'dash_core_components',
                                                                                                                                                       'props': {       'id': 'offer_submitted_id_0',
                                                                                                                                                                        'n_blur': 1,
                                                                                                                                                                        'n_blur_timestamp': 1586925126391,
                                                                                                                                                                        'placeholder': 'Offer '
                                                                                                                                                                                       'Submitted '
                                                                                                                                                                                       'By',
                                                                                                                                                                        'size': 50,
                                                                                                                                                                        'type': 'text',
                                                                                                                                                                        'value': 'Rahul'},
                                                                                                                                                       'type': 'Input'}],
                                                                                                                           'className': 'four '
                                                                                                                                        'columns',
                                                                                                                           'n_clicks': 1,
                                                                                                                           'n_clicks_timestamp': 1586925121616},
                                                                                                          'type': 'Div'},
                                                                                                  {       'namespace': 'dash_html_components',
                                                                                                          'props': {       'children': [       {       'namespace': 'dash_html_components',
                                                                                                                                                       'props': {       'children': 'Offer '
                                                                                                                                                                                    'Remarks'},
                                                                                                                                                       'type': 'Header'},
                                                                                                                                               {       'namespace': 'dash_core_components',
                                                                                                                                                       'props': {       'id': 'offer_remarks_id_0',
                                                                                                                                                                        'n_blur': 1,
                                                                                                                                                                        'n_blur_timestamp': 1586925121607,
                                                                                                                                                                        'placeholder': 'Offer '
                                                                                                                                                                                       'Remakrs',
                                                                                                                                                                        'size': 50,
                                                                                                                                                                        'type': 'text',
                                                                                                                                                                        'value': 'dfasdfasdf'},
                                                                                                                                                       'type': 'Input'}],
                                                                                                                           'className': 'six '
                                                                                                                                        'columns',
                                                                                                                           'n_clicks': 1,
                                                                                                                           'n_clicks_timestamp': 1586925118907},
                                                                                                          'type': 'Div'}],
                                                                              'className': 'row',
                                                                              'n_clicks': 2,
                                                                              'n_clicks_timestamp': 1586925121617},
                                                             'type': 'Div'}],
                                 'n_clicks': 4,
                                 'n_clicks_timestamp': 1586925121618},
                'type': 'Div'}]

dispatch_no = add_offer_div_value[-1]['props']['children'][0]['props']['children'][1]['props']['children'][1]['props'][
    'value']
offer_location = add_offer_div_value[-1]['props']['children'][0]['props']['children'][2]['props']['children'][1]['props'][
    'value']
submitted_by = add_offer_div_value[-1]['props']['children'][1]['props']['children'][0]['props']['children'][1]['props'][
    'value']
remarks = add_offer_div_value[-1]['props']['children'][1]['props']['children'][1]['props']['children'][1]['props']['value']
followup_log_values = [dispatch_no, offer_location, submitted_by, remarks]
followup_log_mod_values = ['' if i is None else i for i in followup_log_values]
print(len(add_offer_div_value))


# for index, row in data.iterrows():
#     print(row['enquiry_key'], row['offer_date'])
#     connection.insert_query("RajGroupFollowUpLog", "(time_stamp, enquiry_key)", [str(row['offer_date']), row['enquiry_key']])




