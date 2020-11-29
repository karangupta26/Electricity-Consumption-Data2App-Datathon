
import pandas as pd
import numpy as np 
import streamlit as st
import streamlit_observable as observable
import pandas as pd
import numpy as np
import pydeck as pdk


@st.cache
def getdata():
    df=pd.read_csv("Monthly_Consumption.csv")
    return df
@st.cache
def genrate_df(df,month):
    tempdf=df[['State',month+'2019',month+'2020']]
    return tempdf

df=getdata()


#year = st.selectbox('Display the map of which year?',('2019','2020'))
month =st.selectbox('Month ?',['Jan ','Feb ','Mar ','Apr ','May ','June ','July ','Aug ','Sep ','Oct ','Nov ','Dec '])

chart_df=genrate_df(df,month)
st.line_chart(chart_df.rename(columns={'State':'index'}).set_index('index'))

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
state=st.selectbox('State ?',list(df['State']))
statedf=generate_state_df(df,state)
st.line_chart(statedf.rename(columns={'Month':'index'}).set_index('index'))


