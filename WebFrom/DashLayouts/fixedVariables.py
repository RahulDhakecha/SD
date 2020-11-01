sow = ['Turnkey', '66KV Switchyard', 'BBT', 'Solar', 'Civil/Telecom', 'Liaison', 'Testing', 'Maintenance/Servicing',
       'Retrofitting', 'SITC', 'Supply only', 'ITC only']
lead_status = ['OPEN', 'CONTACTED', 'VISITED', 'ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD', 'REGRET', 'LETTER', 'BUDGETARY']
order_status = ['ON HAND', 'FEEDBACK', 'COMPLETE', 'CANCEL', 'REGRET']

master_users = ['rahul.dhakecha@rajgrouponline.com', 'anil.kathiriya@rajgrouponline.com', 'kinjal.dhakecha@rajgrouponline.com',
                'rajesh.kunjadiya@rajgrouponline.com', 'megha.gangani@rajgrouponline.com']

raj_group_office = ['Raj Vijtech Pvt Ltd', 'Raj Electricals', 'D.N. Syndicate', 'Raj Enterprise', 'Raj Brookite']
follow_up_person = ['Rahul Dhakecha',
                    'Rajesh Kunjadiya',
                    'Ashish Dhakecha',
                    'Dhiren Sankaliya',
                    'Umang Sharma',
                    'Unmil Naik',
                    'Purvik Mistry',
                    'Kanubhai Patel',
                    'Anil Kathiriya',
                    'Divyesh Patel',
                    'Kinjal Dhakecha',
                    'Hiren Paghdal',
                    'Praful Shyani',
                    'Sachin Patel',
                    'Chirag Patel',
                    'Jitendra Kotnala',
                    'Ninad',
                    'Samir',
                    'Jaimish Modi',
                    'Milan Kheni',
                    'Akash Barvaliya',
                    'Ankit Ribadiya']

fields_enquiry_list = "(enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client, " \
                      "contact_person_name, contact_person_mobile, contact_person_email, internal_lead, external_lead, " \
                      "lead_status, contact_date, visit_date, enquiry_date, offer_date, raj_group_office, " \
                      "follow_up_person, tentative_project_value, quotation_number, remarks)"

fields_followup_log = "(enquiry_key, offer_key, offer_location, submitted_by, remarks, submitted_to)"

fields_client_list = "(client_name, client_location, enquiry_key, po_key)"

fields_client_rep_list = "(contact_person_name, contact_person_mobile, contact_person_email, contact_person_designation, " \
                         "client_name, client_location, enquiry_key, po_key)"

fields_rj_orders_list = "(enquiry_key, order_key, order_date, po_no, project_description, scope_of_work, client_name, " \
                        "client_location, existing_client, order_no, file_no, order_status, project_incharge, " \
                        "raj_group_office, project_value, remarks, comp_location, project_technical, project_management, project_supervisor)"

fields_feedback = "(order_key, recommend_score, satisfaction_score, technical_score, behavorial_score, future_services," \
                  " lesser_time, suggestion)"

sow_code = {
    'Turnkey': 'TRNK',
    '66KV Switchyard': '66KV',
    'BBT': 'BBTR',
    'Solar': 'SOLR',
    'Civil/Telecom': 'CVIL',
    'Liaison': 'LSON',
    'Testing': 'TEST',
    'Maintenance/Servicing': 'SERV',
    'Retrofitting': 'RETR',
    'SITC': 'SITC',
    'Supply only': 'SUPL',
    'ITC only': 'ITCO'
}

raj_group_office_code = {
    'Raj Electricals': 'RJ',
    'D.N. Syndicate': 'DN',
    'Raj Enterprise': 'RE',
    'Raj Vijtech Pvt Ltd': 'RV',
    'Raj Brookite': 'RB'
}

data_access_rights = {
    '%': '%',
    'rahul.dhakecha': '%',
    'Rajesh ': '%',
    'purvik.mistry': 'Dhiren Sankaliya',
    'anil kathiriya': 'Anil Kathiriya',
    'kinjal2812': '%',
    'Hirenpaghdal': 'Hiren Paghdal',
    'Praful Patel': 'Praful Shyani',
    'feni.faldu': 'Ashish Dhakecha',
    'milan.kheni1432': 'Milan Kheni',
    'Akash Barvaliya': 'Akash Barvaliya',
    'Hiren-D': '%',
    'Parimal Panchal': 'Dhiren Sankaliya',
    'Haresh Ghelani': 'Samir'
}