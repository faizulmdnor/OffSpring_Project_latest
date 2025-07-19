import os
import random
import pandas as pd
from offsprings import sql_offsprings

with sql_offsprings() as db:
    data = {
        'full_name': ['Faizul Bin Md Nor', 'Noorazreena Bin Mohamad Tahir'],
        'kad_pengenalan': ['790307-07-5023', '800725-02-5340'],
        'email_personal':['faizul.mdnoor@gmail.com', 'noorazreenatahir@gmail.com'],
        'phone_number': ['0195727169', '0164457169'],
        'id_gender':[110, 120],
        'id_cat':[44, 43]
    }

    df_data = pd.DataFrame(data)
    db.insert_into_table(table_name='person', df=df_data)