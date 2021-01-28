import sys, os
sys.path.append(os.path.join(sys.path[0], 'DashLayouts'))
sys.path.append(os.path.dirname(sys.path[0]))
from urllib.request import Request, urlopen
from lxml.html import parse
from Connections.AWSMySQL import AWSMySQLConn
follow_up_person = ['Rahul Dhakecha',
                    'Rajesh Kunjadiya',
                    'Ashish Dhakecha',
                    'Dhiren Sankaliya',
                    'Anil Kathiriya',
                    'Kinjal Dhakecha',
                    'Hiren Paghdal',
                    'Praful Shyani',
                    'Milan Kheni',
                    'Akash Barvaliya',
                    'Ankit Ribadiya']

sow = ['Turnkey', '66KV Switchyard', 'BBT', 'Solar', 'Civil/Telecom', 'Liaison', 'Testing', 'Maintenance/Servicing',
       'Retrofitting', 'SITC', 'Supply only', 'ITC only']

connection = AWSMySQLConn()
for scope in sow:
    print(scope, connection.execute_query("select avg(temp.time_difference) as avg_time "
                                          "from "
                                          "( "
                                          "select ifnull(timestampdiff(day,A.first_offer_time,B.time_stamp), timestampdiff(day,A.first_offer_time,current_timestamp())) as time_difference from  "
                                          "(select X.enquiry_key, X.first_offer_time from (select enquiry_key, min(time_stamp) as first_offer_time from RajGroupFollowUpLog group by 1) as X "
                                          "inner join RajGroupEnquiryList as Y  "
                                          "on X.enquiry_key=Y.enquiry_key "
                                          "and Y.scope_of_work='{}')  as A "
                                          "left join  "
                                          "(select * from RajGroupLeadStatus where lead_status!='OPEN' and lead_status!='CONTACTED' and lead_status!='VISITED'  "
                                          "and lead_status!='ENQUIRY' and lead_status!='OFFER') as B "
                                          "on A.enquiry_key=B.enquiry_key "
                                          "and A.first_offer_time<=B.time_stamp) as temp;".format(scope)));
