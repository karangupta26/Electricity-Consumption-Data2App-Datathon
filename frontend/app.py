
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache
def getmonthlydata():
    df=pd.read_csv("Monthly_Consumption.csv")
    return df
@st.cache
def getprimarydata():
    df=pd.read_csv("Electricity_data.csv")
    return df
@st.cache(allow_output_mutation=True)
def getsecondarydata():
    df=pd.read_csv("Final_data.csv")
    return df
@st.cache
def genrate_df(df,month):
    tempdf=df[['State',month+'2019',month+'2020']]
    return tempdf

@st.cache
def generate_state_df(df,state):
    montharr=['Jan ','Feb ','Mar ','Apr ','May ','June ','July ','Aug ','Sep ','Oct ','Nov ','Dec ']
    tempdf=pd.DataFrame(columns=['Month','2019','2020'])
    for i in range(10):
        for index,row in df.iterrows():
            #print(row['State'])
            if row['State']==state:
                data={'Month':montharr[i],'2019':row[montharr[i]+'2019'],'2020':row[montharr[i]+'2020']}
                tempdf=tempdf.append(data,ignore_index=True)
    return tempdf
@st.cache
def genrate_yearly_consumption(df):
    montharr=['Jan ','Feb ','Mar ','Apr ','May ','June ','July ','Aug ','Sep ','Oct ']
    tempdf=pd.DataFrame(columns=['2019','2020'])
    month2019=0
    month2020=0
    for month in montharr:
        for index,row in df.iterrows():
            month2019=month2019 + row[month+'2019']
            month2020=month2020 + row[month+'2020']
    data={'2019':month2019,'2020':month2020}
    tempdf=tempdf.append(data,ignore_index=True)
    return tempdf
    
@st.cache
def genrate_comparison_type_of_day(df):
    df['year']=pd.DatetimeIndex(df['Date']).year
    type_of_day='Working'
    year=2019

    tempdf=pd.DataFrame(columns=['Electricity Consumed','Type of Day','Year'])

    for j in range(4):
        consumption=0
        for i in range(10):
            for index,row in df.iterrows():
                if row['year']==year and row['Type of Day']==type_of_day and row['Month'] == i+1:
                    consumption = consumption + row['Electricity Consumed']
        data={'Electricity Consumed':consumption,'Type of Day':type_of_day,'Year':year}
        tempdf=tempdf.append(data,ignore_index=True)
        if j==0:
            year=2019
            type_of_day='Holiday'
            consumption=0
        if j==1:
            year=2020
            type_of_day='Working'
            comsumption=0
        if j==2:
            year=2020
            type_of_day='Holiday'
            consumption=0
        
    return tempdf
@st.cache
def comparison_monthly_average(df,state):
    montharr=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sep','Oct']
    days=[31,28,31,30,31,30,31,31,30,31]
    tempdf=pd.DataFrame(columns=['Electricity Consumed','Month','Year'])
    year=['2019','2020']
    for i in range(10):
        for j in range(2):
            for index,row in df.iterrows():
                #print(row['State'])
                if row['State']==state:
                    if j==1 and montharr[i]=='Feb':
                        data={'Electricity Consumed':row[montharr[i]+" "+year[j]]/(days[i]+1),'Month':montharr[i],'Year':year[j]}
                    else:
                        data={'Electricity Consumed':row[montharr[i]+" "+year[j]]/days[i],'Month':montharr[i],'Year':year[j]}
                    tempdf=tempdf.append(data,ignore_index=True)
    return tempdf
@st.cache
def comparison_of_seasonal_consumption(df):
    seasonarr=['WINTER', 'SUMMER', 'MONSOON', 'AUTUMN']
    tempdf=pd.DataFrame(columns=['Electricity Consumed','Year','Season'])
    year=['2019','2020']
    for i in seasonarr:
        for j in range(2):
            consumption=0
            for index,row in df.iterrows():
                if row['Season']==i and row['year']==int(year[j]) and row['Month'] != 11 and row['Month'] != 12:
                    consumption += consumption + row['Electricity Consumed']
            data={'Electricity Consumed':consumption,'Year':year[j],"Season":i}
            tempdf=tempdf.append(data,ignore_index=True)
    return tempdf

###################################################

primarydatadf=getprimarydata()
monthlydatadf=getmonthlydata()
secondarydatadf=getsecondarydata()
###################################################
type_of_data=st.selectbox('Which Data you want to see ?',['Primary Data','Secondary Data','Monthly Data'])

if type_of_data=='Primary Data':
    st.dataframe(pd.read_csv('Electricity_data.csv'))
if type_of_data=='Secondary Data':
    st.dataframe(pd.read_csv('Final_Data.csv'))
if type_of_data=='Monthly Data':
    st.dataframe(pd.read_csv('Monthly_Consumption'))

###################################################
st.write("Comparison of Electricity state wise based on month.")
month =st.selectbox('Select a Month ?',['Jan ','Feb ','Mar ','Apr ','May ','June ','July ','Aug ','Sep ','Oct ','Nov ','Dec '])

chart_df=genrate_df(monthlydatadf,month)
st.line_chart(chart_df.rename(columns={'State':'index'}).set_index('index'))

###################################################
st.write("Yearly Consumption")
yearlydf=genrate_yearly_consumption(monthlydatadf)
fig1,ax1=plt.subplots()
ax1=sns.barplot(data=yearlydf)
st.pyplot(fig1)

###################################################
state1=st.selectbox('Consumption of Electricity by State in month wise ?',list(monthlydatadf['State']))
statedf=generate_state_df(monthlydatadf,state1)
st.line_chart(statedf.rename(columns={'Month':'index'}).set_index('index'))

##################################################
st.write(" Comparison on working days vs Holidays in 2019/2020")
df=getsecondarydata()
comparisondf=genrate_comparison_type_of_day(df)
fig2,ax2=plt.subplots()
ax2=sns.barplot(x='Year',y='Electricity Consumed',hue='Type of Day',data=comparisondf)
st.pyplot(fig2)

####################################################
st.write("Comparison of consumed electricty based on average")
state2=st.selectbox('Select State for monthly average?',list(monthlydatadf['State']))
monthlyavgdf=comparison_monthly_average(monthlydatadf,state2)
fig3,ax3=plt.subplots()
ax3=sns.barplot(x='Month',y='Electricity Consumed',hue='Year',data=monthlyavgdf)
st.pyplot(fig3)