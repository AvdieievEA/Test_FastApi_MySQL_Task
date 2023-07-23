import pandas as pd

from connection import engine
from db.models import User, Base


def fill_db():
    Base.metadata.create_all(engine)
    csv_files = {
        'users': 'db/raw_data/users.csv',
        'dictionaries': 'db/raw_data/dictionary.csv',
        'credits': 'db/raw_data/credits.csv',
        'plans': 'db/raw_data/plans.csv',
        'payments': 'db/raw_data/payments.csv',
    }
    for table_name, csv_file in csv_files.items():
        df = pd.read_csv(csv_file)

        if table_name == 'users':
            df[['id', 'login', 'registration_date']] = df['id\tlogin\tregistration_date'].str.split('\t', expand=True)
            df.drop(columns=['id\tlogin\tregistration_date'], inplace=True)
            df['registration_date'] = pd.to_datetime(df['registration_date'], format='%d.%m.%Y', errors='coerce')

        elif table_name == 'dictionaries':
            df[['id', 'name']] = df['id\tname'].str.split('\t', expand=True)
            df.drop(columns=['id\tname'], inplace=True)

        elif table_name == 'payments':
            df[
                ['id', 'credit_id', 'payment_date', 'type_id', 'sum']
            ] = df[
                'id\tcredit_id\tpayment_date\ttype_id\tsum'
            ].str.split('\t', expand=True)
            df.drop(columns=[
                'id\tcredit_id\tpayment_date\ttype_id\tsum'
            ], inplace=True)
            df['payment_date'] = pd.to_datetime(df['payment_date'], format='%d.%m.%Y', errors='coerce')

        elif table_name == 'credits':
            df[
                ['id', 'user_id', 'issuance_date', 'return_date',
                 'actual_return_date', ' body', 'percent']
            ] = df[
                'id\tuser_id\tissuance_date\treturn_date\tactual_return_date\tbody\tpercent'
            ].str.split('\t', expand=True)
            df.drop(columns=[
                'id\tuser_id\tissuance_date\treturn_date\tactual_return_date\tbody\tpercent'
            ], inplace=True)
            df['issuance_date'] = pd.to_datetime(df['issuance_date'], format='%d.%m.%Y', errors='coerce')
            df['return_date'] = pd.to_datetime(df['return_date'], format='%d.%m.%Y', errors='coerce')
            df['actual_return_date'] = pd.to_datetime(df['actual_return_date'], format='%d.%m.%Y', errors='coerce')
            df['actual_return_date'] = df['actual_return_date'].where(pd.notna(df['actual_return_date']), None)

        elif table_name == 'plans':
            df[
                ['id', 'period', 'sum', 'category_id']
            ] = df[
                'id\tperiod\tsum\tcategory_id'
            ].str.split('\t', expand=True)
            df.drop(columns=[
                'id\tperiod\tsum\tcategory_id'
            ], inplace=True)
            df['period'] = pd.to_datetime(df['period'], format='%d.%m.%Y', errors='coerce')

        df.to_sql(table_name, engine, if_exists='append', index=False)
