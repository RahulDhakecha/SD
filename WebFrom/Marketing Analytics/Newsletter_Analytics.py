from Connections.AWSMySQL import AWSMySQLConn
import pandas as pd
import re


last_campaign_sent = pd.read_csv("/Users/rahuldhakecha/RajGroup/Newsletter/Post Covid Effects - 2020.04.13/Reports/members_Raj_Group_Newsletter_After_Covid_Part_1_sent_Apr_27_2020.csv")
all_emails = pd.read_csv("/Users/rahuldhakecha/RajGroup/Newsletter/Post Covid Effects - 2020.04.27/Mailing List/MailingList-2020.04.27.csv")

# print(all_emails['contact_person_email'])
# print(last_campaign_sent['Email Address'])

# remove clients to which previous newsletter was sent
new_mailing_list = [x for x in list(all_emails['contact_person_email']) if x not in list(last_campaign_sent['Email Address'])]
# print(new_mailing_list)

df_new_mailing_list = pd.DataFrame(new_mailing_list, columns=['Emails'])
df_new_mailing_list.to_csv("/Users/rahuldhakecha/RajGroup/Newsletter/Post Covid Effects - 2020.04.27/Mailing List/MailingList-excludePrevMails-2020.04.27.csv", index=False)