import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn



connection = AWSMySQLConn()
data = connection.execute_query("select enquiry_key, offer_date from RajGroupEnquiryList where offer_date!='0000-00-00';")
for index, row in data.iterrows():
    print(row['enquiry_key'], row['offer_date'])
    connection.insert_query("RajGroupFollowUpLog", "(time_stamp, enquiry_key)", [str(row['offer_date']), row['enquiry_key']])




