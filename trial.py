import sys
sys.path.append("/Users/rahuldhakecha/RajGroup/SD/WebFrom/")
from Connections.AWSMySQL import AWSMySQLConn
from datetime import datetime as dt
from datetime import date
import pandas as pd
import time
pd.set_option("display.max_columns", None, "display.max_rows", None)


connection = AWSMySQLConn()

lead_status = ['OPEN', 'CONTACTED', 'VISITED', 'ENQUIRY', 'OFFER', 'WON', 'CLOSE', 'HOLD', 'REGRET', 'LETTER']
lead_status.remove('LETTER')
print(lead_status)