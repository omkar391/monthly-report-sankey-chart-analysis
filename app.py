import streamlit as st 
import plotly.graph_objects as go

import numpy as np
import matplotlib.pyplot as plt


import calendar
from datetime import datetime

from streamlit_option_menu import option_menu

import database as db



#------------SETTINGS----------------
incomes=["Salary","Blog","Other"]
expenses=['Rent',"Utilities","Groceries","Car","other Expenses","savings"]
currency="Rs"
page_title="Income and Expenses tracker"
page_icon= ":moneybag:"
layout="centered"

#-----------------------------------------

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_icon+' '+page_title+"  "+ page_icon)

#------DROP DOWN VALUES FOR SELECTING THE PERIOD ----------------

#current = datetime.today().year
years = [2022,2023]
months=list(calendar.month_name[1:])

#---Data Interface------

def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods

#-------HIDE FOOTER AND HEADER ------------------
hide_style="""
<style>
#MainMenu {visibility:hidden;}
footer {visibility : hidden;}
header {visibility : hidden;}
</style>
"""
st.markdown(hide_style,unsafe_allow_html=True)

#---NAVIGATION BAR--------------
select =option_menu(
    menu_title=None,
    options=['Data Entry', 'Data Visualization'],
    icons=["pencil-fill","bar-chart-fill"],
    orientation="horizontal",
)

#-----------INPUT & SAVE PERIODS-------------------

if select=='Data Entry':
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form",clear_on_submit=True):
        col1,col2=st.columns(2)
        col1.selectbox('Select Month:',months,key='month')
        col2.selectbox('Select Year:',years,key='year')
        
        "--"
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income} :", min_value=0,format='%i',step=10,key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense} :", min_value=0,format='%i',step=10,key=expense)
                
        with st.expander("Comment"):
            comment=st.text_area('',placeholder=" Enter a Comment here .....")
            
        "-----"
        
        submittted = st.form_submit_button("Save Data")     
        if submittted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            db.insert_period(period,incomes,expenses,comment)

            st.success("Data Saved!")
        
if select ==   'Data Visualization':      
    #-------PLOT PERIODS-------
        
    st.header("Data Visualization")
    with st.form("saved_periods"):
        # TODO: get periods
        period = st.selectbox("Select Period :-",get_all_periods())
        submittted = st.form_submit_button("-- Plot Period --")
        if submittted:
            period_data = db.get_period(period)
            comment=period_data.get("comment")
            expenses=period_data.get("expenses")
            incomes = period_data.get("incomes")
            # Creat metrics
            total_income = sum(incomes.values())
            total_expenses = sum(expenses.values())
            remain_budget = total_income - total_expenses
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expenses",f'{total_expenses} {currency}')
            col3.metric("Balence",f'{remain_budget} {currency}')
                
                
            # Creat sanky chart ------
            label = list(incomes.keys()) +["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + ([len(incomes)] * len(expenses))
            values = list(incomes.values()) + list(expenses.values())
            target = [len(incomes)]* len(incomes) + [label.index(expense) for expense in expenses.keys()]
                
            #data to dict,dict to sankey------------
            link=dict(source=source,target=target,value=values)
            node=dict(label=label,pad=20, thickness=30, color='pink')
            data=go.Sankey(link=link,node=node)
                
            #plot itl
            fig =go.Figure(data)
            fig.update_layout(margin=dict(l=0,r=0,t=5,b=5))
            st.plotly_chart(fig, use_container_width=True)
            
            
            
            
                
                
        
        
        
        
    
    
    
        