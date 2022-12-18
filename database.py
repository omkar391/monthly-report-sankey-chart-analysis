from deta import Deta

import os
from dotenv import load_dotenv


load_dotenv(".env")
DATA_KEY=os.getenv("DATA_KEY")

deta = Deta(DATA_KEY)

#put key in environment veriable


db = deta.Base("monthly_reports")

def insert_period(period,incomes, expenses,comment):
    return db.put({"key":period,
                   "incomes":incomes,
                   "expenses":expenses,
                   "comment":comment})
    
    
def fetch_all_periods():
    res=db.fetch()
    return res.items

def get_period(period):
    return db.get(period)