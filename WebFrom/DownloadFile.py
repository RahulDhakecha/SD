import pandas as pd
import sys, os
print(os.path.dirname(os.path.realpath(__file__)))
data = pd.read_excel("/Users/rahuldhakecha/RajGroup/OrderList/RajElectricalOrders.xls")

path = os.path.dirname(os.path.realpath(__file__)) + '/temp.xlsx'
print(path)
print(os.system('scp -i /Users/rahuldhakecha/RajGroup/credentials/RajGroup.pem /Users/rahuldhakecha/RajGroup/OrderList/RajElectricalOrders.xls'
                'ubuntu@ec2-18-237-178-54.us-west-2.compute.amazonaws.com:~/RajGroup/'))
# data.to_excel("temp.xlsx")


'scp -i /Users/rahuldhakecha/RajGroup/credentials/RajGroup.pem /Users/rahuldhakecha/RajGroup/OrderList/RajElectricalOrders.xls ubuntu@ec2-18-237-178-54.us-west-2.compute.amazonaws.com:~/RajGroup/'

'scp -i /Users/rahuldhakecha/RajGroup/credentials/RajGroup.pem ubuntu@ec2-18-237-178-54.us-west-2.compute.amazonaws.com:~/RajGroup/RajElectricalOrders.xls /Users/rahuldhakecha/RajGroup/'