
sow = ['Turnkey', '66KV Switchyard', 'BBT', 'Solar', 'Civil/Telecom', 'Liaison', 'Testing', 'Maintenance/Servicing',
       'Retrofitting', 'SITC', 'Supply only', 'ITC only']
lead_status = ['OPEN', 'CONTACTED', 'VISITED', 'ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD']
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
                    'Samir']

fields_enquiry_list = "(enquiry_key, entry_date, project_description, scope_of_work, client_name, client_location, existing_client, " \
                      "contact_person_name, contact_person_mobile, contact_person_email, internal_lead, external_lead, " \
                      "lead_status, contact_date, visit_date, enquiry_date, offer_date, raj_group_office, " \
                      "follow_up_person, tentative_project_value, quotation_number, remarks)"

fields_followup_log = "(enquiry_key, offer_key, offer_location)"