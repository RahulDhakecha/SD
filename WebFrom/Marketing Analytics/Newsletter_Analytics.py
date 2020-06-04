import sys, os

sys.path.append('/Users/rahuldhakecha/RajGroup/SD/WebFrom')

from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import re

connection = AWSMySQLConn()

# last_campaign_sent = pd.read_csv("/Users/rahuldhakecha/RajGroup/Newsletter/Post Covid Effects - 2020.04.13/Reports/members_Raj_Group_Newsletter_After_Covid_Part_1_sent_Apr_27_2020.csv")
# all_emails = pd.read_csv("/Users/rahuldhakecha/RajGroup/Newsletter/Post Covid Effects - 2020.04.27/Mailing List/MailingList-2020.04.27.csv")
#
# # print(all_emails['contact_person_email'])
# # print(last_campaign_sent['Email Address'])
#
# # remove clients to which previous newsletter was sent
# new_mailing_list = [x for x in list(all_emails['contact_person_email']) if x not in list(last_campaign_sent['Email Address'])]
# # print(new_mailing_list)
#
# df_new_mailing_list = pd.DataFrame(new_mailing_list, columns=['Emails'])
# df_new_mailing_list.to_csv("/Users/rahuldhakecha/RajGroup/Newsletter/Post Covid Effects - 2020.04.27/Mailing List/MailingList-excludePrevMails-2020.04.27.csv", index=False)



## get current prospects
data_curr_prospects = connection.execute_query("select contact_person_email from RajGroupClientRepresentativeList "
                                               "where enquiry_key in "
                                               "(select enquiry_key from RajGroupEnquiryList where lead_status!='WON') and "
                                               "contact_person_email!='' and "
                                               "contact_person_email!='0' "
                                               "group by 1;")['contact_person_email']

data_mailing_list_01_06 = pd.read_csv("/Users/rahuldhakecha/RajGroup/Newsletter/01.06.2020/Reports/"
                                      "members_Raj_Group_Newsletter_Last_Week_At_Raj_Group_01_06_2020_sent_Jun_2_2020.csv")['Email Address']

new_mailing_list = [x for x in list(data_curr_prospects) if x not in list(data_mailing_list_01_06)]
df_new_mailing_list = pd.DataFrame(new_mailing_list, columns=['Emails'])
df_new_mailing_list.to_csv("/Users/rahuldhakecha/RajGroup/Newsletter/02.06.2020/Mailing List/mailing_list.csv", index=False)