from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import re
pd.set_option("display.max_columns", None)

# RajElectricalsClients is updated
# Using RajElectricalsClients, update RajGroupClientList and RajGroupClientRepresentativeList

connection = AWSMySQLConn()
# data = connection.execute_query("select * from RajGroupPOoverall limit 10")
# print(data)

fields_client_list = "(client_name, client_location)"
fields_client_rep_list = "(contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation, " \
                         "client_name, client_location)"


data = pd.read_excel("/Users/rahuldhakecha/RajGroup/ClientList/RajElectricalsClients.xlsx")
data = data.fillna(0)
# print(data.head())
client_rep_data = data[['company',
                    'location',
                    'raj_group_office',
                    'technical_person',
                    'technical_contact_number',
                    'technical_contact_email',
                    'management_person',
                    'management_contact_number',
                    'management_contact_email',
                    'purchase_person',
                    'purchase_contact_number',
                    'purchase_contact_email']].groupby(['company',
                    'location',
                    'technical_person',
                    'technical_contact_number',
                    'technical_contact_email',
                    'management_person',
                    'management_contact_number',
                    'management_contact_email',
                    'purchase_person',
                    'purchase_contact_number',
                    'purchase_contact_email'], as_index=False).count()[['company',
                    'location',
                    'technical_person',
                    'technical_contact_number',
                    'technical_contact_email',
                    'management_person',
                    'management_contact_number',
                    'management_contact_email',
                    'purchase_person',
                    'purchase_contact_number',
                    'purchase_contact_email']]

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


client_rep_data.apply(lambda row : split_row(row['purchase_person'],
                     row['purchase_contact_number'], row['purchase_contact_email'],
                                             "Purchase", str(row['company']), str(row['location'])), axis = 1)

# for index, row in client_rep_data.iterrows():
#     if index==2:
#         continue
#     if row['technical_person'] != 0 or row['technical_contact_number']!=0 or row['technical_contact_email']!=0:
#         print(row['technical_person'], row['technical_contact_number'], row['technical_contact_email'])
#         str1 = re.split(r'[,/]', str(row['technical_person']))
#         str2 = re.split(r'[,/]', str(row['technical_contact_number']))
#         str3 = re.split(r'[,/]', str(row['technical_contact_email']))
#         l1 = len(str1)
#         l2 = len(str2)
#         l3 = len(str3)
#         print("Coming here"+str(index))
#         if l1>1 or l2>1 or l3>1:
#             N = max(l1,l2,l3)
#             str1 += [''] * (N - l1)
#             str2 += [''] * (N - l2)
#             str3 += [''] * (N - l3)
#         for i, j, k in zip(str1, str2, str3):
#             print("Coming here1")
#             values = [i.strip(), j.strip(), k.strip(), "Technical", str(row['company']), str(row['location'])]
#             print(values)
            # connection.insert_query(table_name="RajGroupClientRepresentativeList",
            #                         fields=fields_client_rep_list, values=values)
    #
    # if index == 5:
    #     break

