"""
@author: Aditi
"""

import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

json_file = open('loan_data_json.json')
data = json.load(json_file)

loandata = pd.DataFrame(data)

#basic insights from data
loandata.info()
loandata['purpose'].unique()

loandata.describe()
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#annual income
loandata['income'] = np.exp(loandata['log.annual.inc'])

#categorising credit score
cat = []
for x in range(0, len(loandata)):
    try:
        if 300<=loandata['fico'][x]<400:
            category = 'Very Poor'
        elif 400<=loandata['fico'][x]<600:
            category = 'Poor'
        elif 600<=loandata['fico'][x]<660:
            category = 'Fair'
        elif 660<=loandata['fico'][x]<700:
             category = 'Good'
        elif 700<=loandata['fico'][x]:
             category = 'Excellent'
        else:
            category = 'unknown'
    except:
        category = 'unknown'  
    cat.append(category)
    
ficocat = pd.Series(cat)
loandata['fico.category'] = ficocat

#new column for categorising interest rate
loandata.loc[loandata['int.rate']>=0.12, loandata['int.rate.type']] = 'High'
loandata.loc[loandata['int.rate']<0.12, loandata['int.rate.type']] = 'Low'

#plot of number of loans in each fico cat
catplot = loandata.groupby(['fico.category']).size()
catplot.plot.bar()
plt.show()

#count by purpose and its plot
purposeplot = loandata.groupby(['purpose']).size()
purposeplot.plot.bar()
plt.show()

#scatterplot for annual income of a person and their dti
ypoint = loandata['income']
xpoint = loandata['dti']
plt.scatter(xpoint, ypoint)
plt.show()

#writing loandata to csv
loandata.to_csv('loandata_cleaned.csv', index = True)