from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd

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

# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajElectricalOrders.xls")
# data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajEnterpriseOrders.xlsx")
data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/DNSyndicateOrders.xlsx")
data = data.fillna(0)
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


for index, row in data.iterrows():
    values = ['',
          round(row['DD']),
          round(row['MM']),
          round(row['YY']),
          row['Work Order No.'],
          row['Compny Name'],
          row.ix[9],
          '',
          row['Subject'],
          row['Total Cost'],
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
    print(values)
    break
    # connection.insert_query(table_name="DNSyndicateOrders", fields=fields, values=values)

