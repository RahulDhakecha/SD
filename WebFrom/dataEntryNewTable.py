import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn


connection = AWSMySQLConn()

# ## data entry in RajGroupFollowUpLog
# data = connection.execute_query("select enquiry_key, offer_date from RajGroupEnquiryList where offer_date!='0000-00-00';")
# for index, row in data.iterrows():
#     print(row['enquiry_key'], row['offer_date'])
#     connection.insert_query("RajGroupFollowUpLog", "(time_stamp, enquiry_key)", [str(row['offer_date']), row['enquiry_key']])

# ## data entry in RajGroupClientList
# data = connection.execute_query("select enquiry_key, client_name, client_location from RajGroupEnquiryList;")
# for index, row in data.iterrows():
#     print(row['enquiry_key'], row['client_name'], row['client_location'])
#     connection.insert_query("RajGroupClientList", "(client_name, client_location, enquiry_key)", [row['client_name'],
#                                                                                                   row['client_location'],
#                                                                                                   row['enquiry_key']])

## data entry in RajGroupClientRepresentativeList
data = connection.execute_query("select enquiry_key, client_name, client_location, contact_person_name,"
                                "contact_person_mobile, contact_person_email from RajGroupEnquiryList;")
for index, row in data.iterrows():
    print(row['enquiry_key'], row['client_name'], row['client_location'], row['contact_person_name'])
    connection.insert_query("RajGroupClientRepresentativeList", "(contact_person_name, contact_person_mobile,"
                                                  "contact_person_email, client_name, client_location, enquiry_key)",
                                                    [row['contact_person_name'], row['contact_person_mobile'],
                                                                                                  row['contact_person_email'],
                                                                                                  row['client_name'],
                                                                                                  row['client_location'],
                                                                                                  row['enquiry_key']])

