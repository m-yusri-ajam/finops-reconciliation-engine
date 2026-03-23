import pandas as pd

bs_csv = pd.read_csv("data/bank_statement.csv")
il_csv = pd.read_csv("data/internal_ledger.csv")

def clean_text(bs_csv, il_csv):
    bs_df = bs_csv
    il_df = il_csv

    bs_df[['Vendor', 'Ext1', 'Ext2']] = bs_df['Description'].str.split(' ', expand=True)
    bs_df = bs_df.drop(columns=['Description', 'Ext1', 'Ext2'])
    bs_df.loc[bs_df['Vendor'] == "MISC", 'Vendor'] = bs_df['Vendor'].str.capitalize()

    il_df['Vendors'] = il_df['Vendor']
    il_df[['Vendor', 'Ext1', 'Ext2']] = il_df['Vendors'].str.split(' ', expand=True)
    il_df = il_df.drop(columns=['Vendors', 'Ext1', 'Ext2'])