from datetime import datetime
import pandas as pd 


def get_current_date():
    return datetime.now().strftime("%B %d, %Y")

def get_user_sub(): 
    df = pd.read_csv("/Users/winsonchen/Developer/watsonxHack/backend/database/subscriptions.csv")
    # print(df)

    return df.to_dict(orient="records")

def format_table(subs):
    if not subs:
        return "No subscriptions found."
    column = "Service Name | Tier | Amount | Catergory | Frequency | Renewal date | Provider | Bank | Last four | Credict Card expiring soon | Activity in 6 months\n"
    column = subs[0].keys()
    column = " | ".join(column) + "\n"
    rows = "\n".join([ ' | '.join([ str(sub[key]) for key in sub.keys() ]) for sub in subs])
    # formated = "\n".join([f"{sub['Service_id']} | {sub['Tier']} | {sub['Amount']} | {sub['Catergory']} | {sub['Frequency']} | {sub['Renewal date']} | {sub['Provider']} | {sub['Bank']} | {sub['Last four']} | {sub['Credict Card expiring soon']} | {sub['Credict Card expiring soon']}" for sub in subs])
    
    formated = column + rows 
    return formated