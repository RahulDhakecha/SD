from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import re
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
fields_raj_elec_orders =  "(enquiry_key, order_key, order_date, po_no, project_description, scope_of_work, client_name, " \
                          "client_location, existing_client, order_no, file_no, order_status, project_incharge, " \
                          "raj_group_office,  project_value, remarks, comp_location)"


# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/ClientList/RajElectricalsClients.xlsx")
data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajElectricalOrders.xls")
data = data.fillna(0)
# data.drop_duplicates(inplace=True)
# print(data)
print(data.shape)
# print(data.head())
# client_rep_data = data[['company',
#                     'location',
#                     'raj_group_office',
#                     'technical_person',
#                     'technical_contact_number',
#                     'technical_contact_email',
#                     'management_person',
#                     'management_contact_number',
#                     'management_contact_email',
#                     'purchase_person',
#                     'purchase_contact_number',
#                     'purchase_contact_email']].groupby(['company',
#                     'location',
#                     'technical_person',
#                     'technical_contact_number',
#                     'technical_contact_email',
#                     'management_person',
#                     'management_contact_number',
#                     'management_contact_email',
#                     'purchase_person',
#                     'purchase_contact_number',
#                     'purchase_contact_email'], as_index=False).count()[['company',
#                     'location',
#                     'technical_person',
#                     'technical_contact_number',
#                     'technical_contact_email',
#                     'management_person',
#                     'management_contact_number',
#                     'management_contact_email',
#                     'purchase_person',
#                     'purchase_contact_number',
#                     'purchase_contact_email']]

# client_data = data[['company',
#                     'location',
#                     'raj_group_office']].groupby(['company',
#                     'location'], as_index=False).count()[['company', 'location']]


#lambda function which can be applied to all rows for pushing contact info into RajGroupClientRepresentativeList
def split_row(v1, v2, v3, v4, v5, v6):
    if v1 != 0 or v2 != 0 or v3 != 0:
        print(v1, v2, v3)
        str1 = re.split(r'[,/]', str(v1))
        str2 = re.split(r'[,/]', str(v2))
        str3 = re.split(r'[,/]', str(v3))
        l1 = len(str1)
        l2 = len(str2)
        l3 = len(str3)
        if l1>1 or l2>1 or l3>1:
            N = max(l1,l2,l3)
            str1 += [''] * (N - l1)
            str2 += [''] * (N - l2)
            str3 += [''] * (N - l3)
        for i, j, k in zip(str1, str2, str3):
            values = [i.strip(), j.strip(), k.strip(), v4, v5, v6]
            # print(values)
            connection.insert_query(table_name="RajGroupClientRepresentativeList",
                                    fields=fields_client_rep_list, values=values)


# def push_client_info_to_db():
#     client_rep_data.apply(lambda row : split_row(row['purchase_person'],
#                      row['purchase_contact_number'], row['purchase_contact_email'],
#                                              "Purchase", str(row['company']), str(row['location'])), axis = 1)

for index, row in data.iterrows():
    if index < 1386:
        continue
    try:
        ## generate order key
        order_key = "{}-{}-{}-ORD-{}-{}-{}".format("RJ",
                                                             str(row['Cus. Name']).strip().split(" ")[0],
                                                             str(row['Location']).strip().split(" ")[0],
                                                             "",
                                                             str(dt.now().year),
                                                             str(index + 1).zfill(4))


        ## update RajElectricalsOrdersNew
        if int(row['YY'])==4:
            yr = 2004
        elif int(row['YY'])==5:
            yr = 2005
        elif int(row['YY'])==6:
            yr = 2006
        elif int(row['YY'])==7:
            yr = 2007
        elif int(row['YY'])==8:
            yr = 2008
        elif int(row['YY'])==9:
            yr = 2009
        elif int(row['YY'])==10:
            yr = 2010
        elif int(row['YY'])==11:
            yr = 2011
        elif int(row['YY'])==12:
            yr = 2012
        elif int(row['YY'])==13:
            yr = 2013
        elif int(row['YY'])==14:
            yr = 2014
        elif int(row['YY'])==15:
            yr = 2015
        elif int(row['YY'])==16:
            yr = 2016
        elif int(row['YY'])==17:
            yr = 2017
        elif int(row['YY'])==18:
            yr = 2018
        elif int(row['YY'])==19:
            yr = 2019
        elif int(row['YY'])==20:
            yr = 2020
        else:
            yr = 0
        order_date = str(yr) + "-" + str(int(row['MM'])).zfill(2) + "-" + str(int(row['DD'])).zfill(2)
        values_raj_elec_orders = ['',
                                  order_key,
                                  order_date,
                                  row['PO No.'],
                                  row['Subject'],
                                  '',
                                  row['Cus. Name'],
                                  row['Location'],
                                  '',
                                  row['Order NO Given'],
                                  row['File no.'],
                                  row['Status'],
                                  row['Project incharge'],
                                  "Raj Electricals",
                                  row['Total Cost'],
                                  '',
                                  ''
                                  ]
        print(values_raj_elec_orders)
        connection.insert_query(table_name="RajElectricalsOrdersNew", fields=fields_raj_elec_orders, values=values_raj_elec_orders)

        ## update RajGroupClientList
        connection.insert_query(table_name="RajGroupClientList", fields=fields_client_list,
                                values=[row['Cus. Name'],
                                        row['Location'],
                                        order_key])

        ## update RajGroupClientRepresentativeList
        data_client_reps = connection.execute_query("select contact_person_name, contact_person_mobile, contact_person_email, "
                                                    "contact_person_designation, client_name, client_location "
                                                    "from RajGroupClientRepresentativeList where client_name='{}' and "
                                                    "client_location='{}' group by 1,2,3,4,5,6;".
                                 format(row['Cus. Name'], row['Location']))
        if not data_client_reps.empty:
            if str(row['Cus. Name']).strip() not in ['L&T', 'Cairn Energy', 'Reliance Ind. Ltd.', 'RIL corporate IT LTD', 'ESSAR']:
                for i, r in data_client_reps.iterrows():
                    # print("Coming here")
                    connection.insert_query(table_name="RajGroupClientRepresentativeList", fields=fields_client_rep_list,
                                            values=[r['contact_person_name'],
                                                    r['contact_person_mobile'],
                                                    r['contact_person_email'],
                                                    r['contact_person_designation'],
                                                    r['client_name'],
                                                    r['client_location'],
                                                    order_key])
    except:
        print("Error for following row:"+str(row))
