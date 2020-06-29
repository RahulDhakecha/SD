import sys, os
sys.path.append(os.path.join(sys.path[0], 'DashLayouts'))
from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import re
from fixedVariables import sow_code
from datetime import datetime as dt
pd.set_option("display.max_columns", None, "display.max_rows", None)

# RajElectricalsClients is updated
# Using RajElectricalsClients, update RajGroupClientList and RajGroupClientRepresentativeList

connection = AWSMySQLConn()
# data = connection.execute_query("select * from RajGroupPOoverall limit 10")
# print(data)

fields_client_list = "(client_name, client_location, po_key)"
fields_client_rep_list = "(contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation, " \
                         "client_name, client_location, po_key)"
fields_re_orders =  "(enquiry_key, order_key, order_date, po_no, project_description, scope_of_work, client_name, " \
                          "client_location, existing_client, order_no, file_no, order_status, project_incharge, " \
                          "raj_group_office,  project_value, remarks, comp_location)"

fields_dn_syn_orders =  "(enquiry_key, order_key, order_date, po_no, project_description, scope_of_work, client_name, " \
                          "client_location, existing_client, order_no, file_no, order_status, project_incharge, " \
                          "raj_group_office,  project_value, remarks, comp_location)"

fields_rv_orders =  "(enquiry_key, order_key, order_date, po_no, project_description, scope_of_work, client_name, " \
                          "client_location, existing_client, order_no, file_no, order_status, project_incharge, " \
                          "raj_group_office,  project_value, remarks, comp_location)"

# #######################   D.N. Syndicate    ################################################
# # data = pd.read_excel("/Users/rahuldhakecha/RajGroup/ClientList/RajElectricalsClients.xlsx")
# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/DNSyndicateOrders/DN-ORDER LIST_12.05.20_wo_pw.xlsx")
# data = data.fillna(0)
# # data.drop_duplicates(inplace=True)
# # print(data)
# print(data.shape)
# # print(data.head())
# # client_rep_data = data[['company',
# #                     'location',
# #                     'raj_group_office',
# #                     'technical_person',
# #                     'technical_contact_number',
# #                     'technical_contact_email',
# #                     'management_person',
# #                     'management_contact_number',
# #                     'management_contact_email',
# #                     'purchase_person',
# #                     'purchase_contact_number',
# #                     'purchase_contact_email']].groupby(['company',
# #                     'location',
# #                     'technical_person',
# #                     'technical_contact_number',
# #                     'technical_contact_email',
# #                     'management_person',
# #                     'management_contact_number',
# #                     'management_contact_email',
# #                     'purchase_person',
# #                     'purchase_contact_number',
# #                     'purchase_contact_email'], as_index=False).count()[['company',
# #                     'location',
# #                     'technical_person',
# #                     'technical_contact_number',
# #                     'technical_contact_email',
# #                     'management_person',
# #                     'management_contact_number',
# #                     'management_contact_email',
# #                     'purchase_person',
# #                     'purchase_contact_number',
# #                     'purchase_contact_email']]
#
# # client_data = data[['company',
# #                     'location',
# #                     'raj_group_office']].groupby(['company',
# #                     'location'], as_index=False).count()[['company', 'location']]
#
#
# #lambda function which can be applied to all rows for pushing contact info into RajGroupClientRepresentativeList
# def split_row(v1, v2, v3, v4, v5, v6):
#     if v1 != 0 or v2 != 0 or v3 != 0:
#         print(v1, v2, v3)
#         str1 = re.split(r'[,/]', str(v1))
#         str2 = re.split(r'[,/]', str(v2))
#         str3 = re.split(r'[,/]', str(v3))
#         l1 = len(str1)
#         l2 = len(str2)
#         l3 = len(str3)
#         if l1>1 or l2>1 or l3>1:
#             N = max(l1,l2,l3)
#             str1 += [''] * (N - l1)
#             str2 += [''] * (N - l2)
#             str3 += [''] * (N - l3)
#         for i, j, k in zip(str1, str2, str3):
#             values = [i.strip(), j.strip(), k.strip(), v4, v5, v6]
#             # print(values)
#             connection.insert_query(table_name="RajGroupClientRepresentativeList",
#                                     fields=fields_client_rep_list, values=values)
#
#
# for index, row in data.iterrows():
#     if index < 1460:
#         continue
#     # if index > 1470:
#     #     break
#     try:
#
#         ## update RajElectricalsOrdersNew
#         if int(row['YY'])==4:
#             yr = 2004
#         elif int(row['YY'])==5:
#             yr = 2005
#         elif int(row['YY'])==6:
#             yr = 2006
#         elif int(row['YY'])==7:
#             yr = 2007
#         elif int(row['YY'])==8:
#             yr = 2008
#         elif int(row['YY'])==9:
#             yr = 2009
#         elif int(row['YY'])==10:
#             yr = 2010
#         elif int(row['YY'])==11:
#             yr = 2011
#         elif int(row['YY'])==12:
#             yr = 2012
#         elif int(row['YY'])==13:
#             yr = 2013
#         elif int(row['YY'])==14:
#             yr = 2014
#         elif int(row['YY'])==15:
#             yr = 2015
#         elif int(row['YY'])==16:
#             yr = 2016
#         elif int(row['YY'])==17:
#             yr = 2017
#         elif int(row['YY'])==18:
#             yr = 2018
#         elif int(row['YY'])==19:
#             yr = 2019
#         elif int(row['YY'])==20:
#             yr = 2020
#         else:
#             yr = 0
#         order_date = str(yr) + "-" + str(int(row['MM'])).zfill(2) + "-" + str(int(row['DD'])).zfill(2)
#
#         # Scope fo Work
#         if str(row['M/S'])=='M':
#             scope_of_work = "Supply only"
#         elif str(row['M/S'])=='M/S':
#             scope_of_work = "SITC"
#         elif str(row['M/S'])=='S':
#             scope_of_work = "ITC only"
#         else:
#             scope_of_work = ''
#
#         ## generate order key
#         order_key = "{}-{}-{}-ORD-{}-{}-{}".format("DN",
#                                                    str(row['Compny Name']).strip().split(" ")[0],
#                                                    str(row.iloc[9]).strip().split(" ")[0],
#                                                    sow_code[scope_of_work] if scope_of_work != '' else '',
#                                                    str(dt.now().year),
#                                                    str(index + 1).zfill(4))
#
#
#         if str(row['OK/NOT']).lower().strip() == 'ok':
#             status = "COMPLETE"
#         elif str(row['OK/NOT']).lower().strip() == 'not':
#             status = "ON HAND"
#         else:
#             status = ""
#
#         values_dn_syn_orders = ['',
#                                   order_key,
#                                   order_date,
#                                   row['Work Order No.'],
#                                   row['Subject'],
#                                   scope_of_work,
#                                   row['Compny Name'],
#                                   row.iloc[9],
#                                   '',
#                                   row['No. Given'],
#                                   '',
#                                   status,
#                                   '',
#                                   "D.N. Syndicate",
#                                   row['Total Cost'],
#                                   '',
#                                   ''
#                                   ]
#         print(values_dn_syn_orders)
#         connection.insert_query(table_name="DNSyndicateOrdersNew", fields=fields_dn_syn_orders, values=values_dn_syn_orders)
#
#         ## update RajGroupClientList
#         connection.insert_query(table_name="RajGroupClientList", fields=fields_client_list,
#                                 values=[row['Compny Name'],
#                                         row.iloc[9],
#                                         order_key])
#
#         ## update RajGroupClientRepresentativeList
#         # data_client_reps = connection.execute_query("select contact_person_name, contact_person_mobile, contact_person_email, "
#         #                                             "contact_person_designation, client_name, client_location "
#         #                                             "from RajGroupClientRepresentativeList where client_name='{}' and "
#         #                                             "client_location='{}' group by 1,2,3,4,5,6;".
#         #                          format(row['Cus. Name'], row['Location']))
#         # if not data_client_reps.empty:
#         #     if str(row['Cus. Name']).strip() not in ['L&T', 'Cairn Energy', 'Reliance Ind. Ltd.', 'RIL corporate IT LTD', 'ESSAR']:
#         #         for i, r in data_client_reps.iterrows():
#         #             print("Coming here")
#         #             connection.insert_query(table_name="RajGroupClientRepresentativeList", fields=fields_client_rep_list,
#         #                                     values=[r['contact_person_name'],
#         #                                             r['contact_person_mobile'],
#         #                                             r['contact_person_email'],
#         #                                             r['contact_person_designation'],
#         #                                             r['client_name'],
#         #                                             r['client_location'],
#         #                                             order_key])
#     except:
#         print("Error for following row:"+str(row))
#################################################################################################




# #######################   Raj Enterprise    ################################################
# # data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajEnterpriseOrders/Bill Records - v2/RajEntr/bill 2015-16.xlsx", sheet_name=0)
# data = connection.execute_query("select * from RajEnterpriseOrders;")
# data = data.fillna(0)
# print(data.shape)
# # print(data.head())
#
# #lambda function which can be applied to all rows for pushing contact info into RajGroupClientRepresentativeList
# def split_row(v1, v2, v3, v4, v5, v6):
#     if v1 != 0 or v2 != 0 or v3 != 0:
#         print(v1, v2, v3)
#         str1 = re.split(r'[,/]', str(v1))
#         str2 = re.split(r'[,/]', str(v2))
#         str3 = re.split(r'[,/]', str(v3))
#         l1 = len(str1)
#         l2 = len(str2)
#         l3 = len(str3)
#         if l1>1 or l2>1 or l3>1:
#             N = max(l1,l2,l3)
#             str1 += [''] * (N - l1)
#             str2 += [''] * (N - l2)
#             str3 += [''] * (N - l3)
#         for i, j, k in zip(str1, str2, str3):
#             values = [i.strip(), j.strip(), k.strip(), v4, v5, v6]
#             # print(values)
#             connection.insert_query(table_name="RajGroupClientRepresentativeList",
#                                     fields=fields_client_rep_list, values=values)
#
# ctr = 1419
# for index, row in data.iterrows():
#     if index <= 100:
#         continue
#     # if index > 200:
#     #     break
#
#     try:
#         if int(row['year_value'])==4:
#             yr = 2004
#         elif int(row['year_value'])==5:
#             yr = 2005
#         elif int(row['year_value'])==6:
#             yr = 2006
#         elif int(row['year_value'])==7:
#             yr = 2007
#         elif int(row['year_value'])==8:
#             yr = 2008
#         elif int(row['year_value'])==9:
#             yr = 2009
#         elif int(row['year_value'])==10:
#             yr = 2010
#         elif int(row['year_value'])==11:
#             yr = 2011
#         elif int(row['year_value'])==12:
#             yr = 2012
#         elif int(row['year_value'])==13:
#             yr = 2013
#         elif int(row['year_value'])==14:
#             yr = 2014
#         elif int(row['year_value'])==15:
#             yr = 2015
#         elif int(row['year_value'])==16:
#             yr = 2016
#         elif int(row['year_value'])==17:
#             yr = 2017
#         elif int(row['year_value'])==18:
#             yr = 2018
#         elif int(row['year_value'])==19:
#             yr = 2019
#         elif int(row['year_value'])==20:
#             yr = 2020
#         else:
#             yr = 0
#         order_date = str(yr) + "-" + str(int(row['month_value'])).zfill(2) + "-" + str(int(row['day_value'])).zfill(2)
#         # try:
#         #     date = row['DATE'].strftime("%d-%m-%Y")
#         #     day = str(date).split("-")[0]
#         #     month = str(date).split("-")[1]
#         #     year = str(date).split("-")[2]
#         # except:
#         #     day = str(row['DATE']).split("-")[0]
#         #     month = str(row['DATE']).split("-")[1]
#         #     year = str(row['DATE']).split("-")[2]
#         ## update RajElectricalsOrdersNew
#
#         # order_date = str(year) + "-" + str(int(month)).zfill(2) + "-" + str(int(day)).zfill(2)
#
#         ## generate order key
#         order_key = "{}-{}-{}-ORD-{}-{}-{}".format("RE",
#                                                    str(row['company']).strip().split(" ")[0],
#                                                    str(row['location']).strip().split(" ")[0],
#                                                    '',
#                                                    str(dt.now().year),
#                                                    str(ctr + 1).zfill(4))
#         ctr += 1
#
#
#         # values_re_orders = ['',
#         #                   order_key,
#         #                   order_date,
#         #                   '',
#         #                   row['WORK'],
#         #                   '',
#         #                   row['COMPANY NAME'],
#         #                   '',
#         #                   '',
#         #                   '',
#         #                   '',
#         #                   'COMPLETED',
#         #                   '',
#         #                   "Raj Enterprise",
#         #                   row['Amount'],
#         #                   '',
#         #                   ''
#         #                   ]
#         values_re_orders = ['',
#                           order_key,
#                           order_date,
#                           row['po_no'],
#                           row['project_description'],
#                           '',
#                           row['company'],
#                           row['location'],
#                           '',
#                           '',
#                           '',
#                           row['project_status'],
#                           '',
#                           "Raj Enterprise",
#                           row['po_value'],
#                           '',
#                           ''
#                           ]
#         print(values_re_orders)
#         connection.insert_query(table_name="RajEnterpriseOrdersNew", fields=fields_re_orders, values=values_re_orders)
#
#         ## update RajGroupClientList
#         connection.insert_query(table_name="RajGroupClientList", fields=fields_client_list,
#                                 values=[row['company'],
#                                         row['location'],
#                                         order_key])
#
#     except:
#         print("Error for following row:"+str(row))
# #################################################################################################



# #######################   Raj Vijtech    ################################################
# # data = pd.read_excel("/Users/rahuldhakecha/RajGroup/ClientList/RajElectricalsClients.xlsx")
# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajVijtechOrders/LIST OF ORDER-RAJ VIJ.xls")
# data = data.fillna(0)
# # data.drop_duplicates(inplace=True)
# # print(data)
# print(data.shape)
# # print(data.head())
# # client_rep_data = data[['company',
# #                     'location',
# #                     'raj_group_office',
# #                     'technical_person',
# #                     'technical_contact_number',
# #                     'technical_contact_email',
# #                     'management_person',
# #                     'management_contact_number',
# #                     'management_contact_email',
# #                     'purchase_person',
# #                     'purchase_contact_number',
# #                     'purchase_contact_email']].groupby(['company',
# #                     'location',
# #                     'technical_person',
# #                     'technical_contact_number',
# #                     'technical_contact_email',
# #                     'management_person',
# #                     'management_contact_number',
# #                     'management_contact_email',
# #                     'purchase_person',
# #                     'purchase_contact_number',
# #                     'purchase_contact_email'], as_index=False).count()[['company',
# #                     'location',
# #                     'technical_person',
# #                     'technical_contact_number',
# #                     'technical_contact_email',
# #                     'management_person',
# #                     'management_contact_number',
# #                     'management_contact_email',
# #                     'purchase_person',
# #                     'purchase_contact_number',
# #                     'purchase_contact_email']]
#
# # client_data = data[['company',
# #                     'location',
# #                     'raj_group_office']].groupby(['company',
# #                     'location'], as_index=False).count()[['company', 'location']]
#
#
# #lambda function which can be applied to all rows for pushing contact info into RajGroupClientRepresentativeList
# def split_row(v1, v2, v3, v4, v5, v6):
#     if v1 != 0 or v2 != 0 or v3 != 0:
#         print(v1, v2, v3)
#         str1 = re.split(r'[,/]', str(v1))
#         str2 = re.split(r'[,/]', str(v2))
#         str3 = re.split(r'[,/]', str(v3))
#         l1 = len(str1)
#         l2 = len(str2)
#         l3 = len(str3)
#         if l1>1 or l2>1 or l3>1:
#             N = max(l1,l2,l3)
#             str1 += [''] * (N - l1)
#             str2 += [''] * (N - l2)
#             str3 += [''] * (N - l3)
#         for i, j, k in zip(str1, str2, str3):
#             values = [i.strip(), j.strip(), k.strip(), v4, v5, v6]
#             # print(values)
#             connection.insert_query(table_name="RajGroupClientRepresentativeList",
#                                     fields=fields_client_rep_list, values=values)
#
#
# for index, row in data.iterrows():
#     # if index < 1460:
#     #     continue
#     # if index > 10:
#     #     break
#     try:
#
#         ## update RajElectricalsOrdersNew
#         if int(row['YY'])==4:
#             yr = 2004
#         elif int(row['YY'])==5:
#             yr = 2005
#         elif int(row['YY'])==6:
#             yr = 2006
#         elif int(row['YY'])==7:
#             yr = 2007
#         elif int(row['YY'])==8:
#             yr = 2008
#         elif int(row['YY'])==9:
#             yr = 2009
#         elif int(row['YY'])==10:
#             yr = 2010
#         elif int(row['YY'])==11:
#             yr = 2011
#         elif int(row['YY'])==12:
#             yr = 2012
#         elif int(row['YY'])==13:
#             yr = 2013
#         elif int(row['YY'])==14:
#             yr = 2014
#         elif int(row['YY'])==15:
#             yr = 2015
#         elif int(row['YY'])==16:
#             yr = 2016
#         elif int(row['YY'])==17:
#             yr = 2017
#         elif int(row['YY'])==18:
#             yr = 2018
#         elif int(row['YY'])==19:
#             yr = 2019
#         elif int(row['YY'])==20:
#             yr = 2020
#         else:
#             yr = 0
#         order_date = str(yr) + "-" + str(int(row['MM'])).zfill(2) + "-" + str(int(row['DD'])).zfill(2)
#
#
#         ## generate order key
#         order_key = "{}-ODR-{}-{}".format("RV",
#                                                    str(dt.now().year),
#                                                    str(index + 1).zfill(4))
#
#
#
#         values_rv_orders = ['',
#                                   order_key,
#                                   order_date,
#                                   row['WORK ORDER NO.'],
#                                   row['Subject'],
#                                   '',
#                                   row['Cus. Name'],
#                                   row['Location'],
#                                   '',
#                                   row['NO Given'],
#                                   row['File no.'],
#                                   row['Status'],
#                                   row['Supervisor'],
#                                   "Raj Vijtech Pvt Ltd",
#                                   row['Total Cost'],
#                                   '',
#                                   ''
#                                   ]
#         print(values_rv_orders)
#         connection.insert_query(table_name="RajVijtechOrdersNew", fields=fields_rv_orders, values=values_rv_orders)
#
#         ## update RajGroupClientList
#         connection.insert_query(table_name="RajGroupClientList", fields=fields_client_list,
#                                 values=[row['Cus. Name'],
#                                         row['Location'],
#                                         order_key])
#
#         ## update RajGroupClientRepresentativeList
#         # data_client_reps = connection.execute_query("select contact_person_name, contact_person_mobile, contact_person_email, "
#         #                                             "contact_person_designation, client_name, client_location "
#         #                                             "from RajGroupClientRepresentativeList where client_name='{}' and "
#         #                                             "client_location='{}' group by 1,2,3,4,5,6;".
#         #                          format(row['Cus. Name'], row['Location']))
#         # if not data_client_reps.empty:
#         #     if str(row['Cus. Name']).strip() not in ['L&T', 'Cairn Energy', 'Reliance Ind. Ltd.', 'RIL corporate IT LTD', 'ESSAR']:
#         #         for i, r in data_client_reps.iterrows():
#         #             print("Coming here")
#         #             connection.insert_query(table_name="RajGroupClientRepresentativeList", fields=fields_client_rep_list,
#         #                                     values=[r['contact_person_name'],
#         #                                             r['contact_person_mobile'],
#         #                                             r['contact_person_email'],
#         #                                             r['contact_person_designation'],
#         #                                             r['client_name'],
#         #                                             r['client_location'],
#         #                                             order_key])
#     except:
#         print("Error for following row:"+str(row))
# #################################################################################################


###################################  Update Hyperlinks   ##############################################################
# def add_hyperlink(comp_location, order_key):
#     return '=HYPERLINK("{}","{}")'.format(comp_location, order_key)
#
# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajVijtechOrders/LIST OF ORDER-RAJ VIJ.xlsx")
# data_from_dashboard = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajVijtechOrders/Raj_Vijtech_Order_List.xlsx")
# # print(data_from_dashboard.head())
#
# for i,j in zip(data.iterrows(), data_from_dashboard.iterrows()):
#     order_key = "{}-ODR-{}-{}".format("RV", str(dt.now().year), str(j[0] + 1).zfill(4))
#     link = r'{}'.format(i[1]['material']).replace('\\', '\\\\')
#     connection.execute("update RajVijtechOrdersNew set comp_location='{}' where order_key='{}'".format(link, order_key))
#################################################################################################



###################################  Update Prev Order Key to New Format##############################################################

data = connection.execute_query("select order_key from RajElectricalsOrdersNew;")

# print(data)
errors = []
for i, j in data.iterrows():
    # if i < 433:
    #     continue
    # print(j['order_key'])
    try:
        old_order_key = j['order_key']
        new_order_key = str(j['order_key']).split("-")[0] + "-ODR-" + str(j['order_key']).split("-")[-2] + "-" + \
                        str(j['order_key']).split("-")[-1]
        print(new_order_key)
        connection.execute(
            "update RajElectricalsOrdersNew set order_key='{}' where order_key='{}';".format(new_order_key, old_order_key))
    except:
        errors.append(old_order_key)
#################################################################################################