import vectorbt as vbt
import pandas as pd
import sqlite3
from datetime import datetime

class PortfiloAnalyzer:

    def __init__(self, price_data=None, result=None):
        self.price_data = price_data
        self.buy_signals = result.buy
        self.sell_signals = result.sell

    def analyze(self):

        if self.price_data is None or self.buy_signals is None or self.sell_signals is None:
            raise ValueError("Price data and signals must be provided for analysis.")

        portfolio = vbt.Portfolio.from_signals(
            close=self.price_data,
            entries=self.buy_signals,
            exits=self.sell_signals
        )

        # total_return = portfolio.total_return()

        total_return_df = portfolio.total_return().to_frame(name='total_return')
        total_return_df.reset_index(inplace=True)  # Flatten the MultiIndex

        total_return_df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Connect to database (creates it if it doesn't exist)
        conn = sqlite3.connect('MTXTrading.db')
        
        # cursor = conn.cursor()
        # try:
        #     cursor.execute('ALTER TABLE total_returns ADD COLUMN timestamp TEXT')
        #     conn.commit()
        # except sqlite3.OperationalError as e:
        #     if 'duplicate column name' not in str(e):
        #         raise  # re-raise only if it's a different error

        # Save DataFrame to SQL table
        total_return_df.to_sql('total_returns', conn, if_exists='append' , index=False)

        # Close connection
        conn.close()

        return portfolio.stats()