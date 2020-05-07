from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
from datetime import datetime as dt

connection = AWSMySQLConn()
# data = connection.execute_query("select * from RajGroupPOoverall limit 10")
# print(data)

## create individual table for 4 companies

## populate each table separately

fields = "(sr_no, day_value, month_value, year_value, po_no, company, location, sector, project_description, po_value, project_status," \
         "project_incharge, turnkey, eht, bbt, solar, civil_telecom, liaison, testing, maintenance_servicing, retrofitting, " \
         "sitc, supply_only, itc_only, technical_person, technical_contact_number, technical_contact_email," \
         "management_person, management_contact_number, management_contact_email," \
         "purchase_person, purchase_contact_number, purchase_contact_email)"

fields_enquiry_list = "(enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client, " \
                      "contact_person_name, contact_person_mobile, contact_person_email, internal_lead, external_lead, " \
                      "lead_status, contact_date, visit_date, enquiry_date, offer_date, raj_group_office, " \
                      "follow_up_person, tentative_project_value, quotation_number, remarks)"

# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajElectricalOrders.xls")
# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajEnterpriseOrders.xlsx")
# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/DNSyndicateOrders.xlsx")
# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/EnquiryList/RajGroupEnquiryList.xlsx")
# data = data.fillna(0)
# print(data.head)

# for index, row in data.iterrows():
#     values = [row['SR'],
#           round(row['DD']),
#           round(row['MM']),
#           round(row['YY']),
#           row['PO No.'],
#           row['Cus. Name'],
#           row['Location'],
#           '',
#           row['Subject'],
#           row['Total Cost'],
#           row['Status'],
#           row['Project incharge'],
#           row['Turnkey'],
#           row['66KV Switchyard'],
#           row['BBT'],
#           row['Solar'],
#           row['Civil/Telecom'],
#           row['Liaison'],
#           row['Testing'],
#           row['Maintenance/Servicing'],
#           row['Retrofitting'],
#           row['SITC'],
#           row['Supply only'],
#           row['ITC only'],
#           row['Technical -Contact Person'],
#           row['Technical - Contact Email'],
#           row['Technical -Contact Number'],
#           row['Management - Contact Person'],
#           row['Management - Contact Email'],
#           row['Management - Contact Number'],
#           row['Purchase -Contact Person'],
#           row['Purchase - Contact Email'],
#           row['Purchase -Contact Number']]
#     connection.insert_query(table_name="RajElectricalsOrders", fields=fields, values=values)


# for index, row in data.iterrows():
#     values = ['',
#           round(row['DD']),
#           round(row['MM']),
#           round(row['YY']),
#           row['PO No.'],
#           row['Cus. Name'],
#           row['Location'],
#           row['Sector'],
#           row['Subject'],
#           row['Total Cost'],
#           row['Status'],
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           '',
#           row['Technical -Contact Person'],
#           row['Technical - Contact Email'],
#           row['Technical -Contact Number'],
#           row['Management - Contact Person'],
#           row['Management - Contact Email'],
#           row['Management - Contact Number'],
#           row['Purchase -Contact Person'],
#           row['Purchase - Contact Email'],
#           row['Purchase -Contact Number']]
#     connection.insert_query(table_name="RajEnterpriseOrders", fields=fields, values=values)


# for index, row in data.iterrows():
#     print(index)
#     if index<=743:
#         continue
#     try:
#         values = ['',
#               round(row['DD']),
#               round(row['MM']),
#               round(row['YY']),
#               row['Work Order No.'],
#               row['Compny Name'],
#               row['Location'],
#               '',
#               row['Subject'],
#               row['Total Cost'],
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '',
#               '']
#         connection.insert_query(table_name="DNSyndicateOrders", fields=fields, values=values)
#     except:
#         continue


# for index, row in data.iterrows():
#     print(index)
#     try:
#         values = [row['Enquiry Key'],
#                   row['Entry Date'],
#                   row['Project Description'],
#                   row['Scope of Work'],
#                   row['Client'],
#                   row['Location'],
#                   row['Existing Client'],
#                   row['Contact Person Name'],
#                   row['Contact Person Mobile'],
#                   row['Contact Person Email'],
#                   row['Internal Lead'],
#                   row['External Lead'],
#                   row['Status'],
#                   row['Contact Date'],
#                   row['Visit Date'],
#                   row['Enquiry Date'],
#                   row['Offer Date'],
#                   row['Raj Group Office'],
#                   row['Follow Up Person'],
#                   row['Tentative Project Value'],
#                   row['Quotation Number'],
#                   row['Remarks']]
#         connection.insert_query(table_name="RajGroupEnquiryList", fields=fields_enquiry_list, values=values)
#     except:
#         continue

############################################################################################################
#  PUSHING RAJ ENTERPRISE BILLING DATA FROM 2008 TO 2016 TO RAJENTERPRISEORDERS TABLE ON DB. HERE WE ARE USING BILLING
#  INFORMATION TO POPULATE ORDERS TABLE SO THERE MIGHT ME SOME DEFINITE DISCREPANCIES ESPECIALLY IN DATES
############################################################################################################


data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajEnterpriseOrders/Bill Records - v2/RajEntr/bill 2015-16.xlsx", sheet_name=0)
data = data.fillna(0)
# print(data)
data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
data = data.fillna(0)
# print(data['DATE'])
for index, row in data.iterrows():
    try:
        # print(dt.strftime(row['DATE']))
        date = row['DATE'].strftime("%d-%m-%Y")
        day = date.split("-")[0]
        month = date.split("-")[1]
        year = date.split("-")[2]
        print(day, month, year)
        values = ['',
                  day,
                  month,
                  year,
                  '',
                  row['COMPANY NAME'],
                  '',
                  '',
                  row['WORK'],
                  row['Amount'],
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '']
        connection.insert_query(table_name="RajEnterpriseOrders", fields=fields, values=values)
    except:
        continue