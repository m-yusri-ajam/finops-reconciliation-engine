import pandas as pd
import logging
from datetime import datetime
from thefuzz import process

# --- 1. The Cleaning logic ---
def clean_text(bs_csv, il_csv):
    """Cleans raw text and normalizes Vendor names to prepare for merging.
    bs_csv: The bank statement raw csv.
    il_csv: The internal ledger raw csv.
    returns: Two DataFrames bs_df, il_df."""
    bs_df = bs_csv
    il_df = il_csv

    bs_df[['Vendor', 'Ext1', 'Ext2']] = bs_df['Description'].str.split(' ', expand=True)
    bs_df = bs_df.drop(columns=['Description', 'Ext1', 'Ext2'])
    bs_df.loc[bs_df['Vendor'] == "MISC", 'Vendor'] = bs_df['Vendor'].str.capitalize()

    il_df['Vendors'] = il_df['Vendor']
    il_df[['Vendor', 'Ext1', 'Ext2']] = il_df['Vendors'].str.split(' ', expand=True)
    il_df = il_df.drop(columns=['Vendors', 'Ext1', 'Ext2'])

    logging.info(f"Cleaning of {len(bs_csv)} bank statement and {len(il_csv)} ledger entries complete!")
    return bs_df, il_df

# --- 2. The fuzzing logic ---
def get_fuzzy_match(ledger_vendor, bank_choices):
    """Calculates similarity scores between bank and ledger names for vendors.
    ledger_vendor: Ledger Vendor named produced by thefuzz.process.
    bank_choices: Unique list of Vendors in bank statement DataFrame.
    result: returns a list stating whether the variance is zero (matched), or whether a variance is present (needs review)."""
    result = process.extractOne(ledger_vendor, choices=bank_choices)

    if not result:
        return "NEEDS REVIEW: No Match Found"
    
    match, score = result[0], result[1]

    if score >= 90:
        return f"NEEDS REVIEW: Missing from Bank (Found {match} {score}%)"
    else:
        return f"NEEDS REVIEW: No Match Found ({score}%)"

    # --- Logging Configuration ---

current_date = datetime.now().strftime('%Y-%m-%d')
log_filename = f"data/recon_log_{current_date}.log"

    # --- Initializing Logger ---
logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - {levelname} - {message}',
    style='{',
    handlers=[logging.FileHandler(log_filename, mode='a', delay=False),
              logging.StreamHandler()]
)

# --- 3. The Execution of the function ---
def main():
    """The main function that applies the reconciliation logic."""
    logging.info("Starting Reconciliation Process...")

    bs_csv = pd.read_csv("data/bank_statement.csv")
    il_csv = pd.read_csv("data/internal_ledger.csv")

    bs_df, il_df = clean_text(bs_csv=bs_csv, il_csv=il_csv)

    merged_df = pd.merge(il_df, bs_df,
                    left_on=['Vendor', 'Amount'], 
                    right_on=['Vendor', 'Bank_Amount'], 
                    how='left')
    merged_df['Bank_Amount'] = merged_df['Bank_Amount'].fillna(0)
    logging.info("Merging Complete.")

    # --- The Variance calculation ---
    merged_df['Variance'] = (merged_df['Amount'] - merged_df['Bank_Amount']).abs()
    logging.info("Variance calculations complete.")

    # --- The fuzzing logic ---
    bank_choices = bs_df['Vendor'].unique()
    unmatched = merged_df['Bank_Amount'] == 0

    merged_df.loc[unmatched, 'Bank Suggestion'] = merged_df.loc[unmatched, 'Vendor'].apply(
        lambda x: get_fuzzy_match(x, bank_choices))
    
    merged_df['Bank Suggestion'] = merged_df['Bank Suggestion'].fillna("EXACT MATCH")
    logging.info("Fuzzing complete.")

    # --- Exporting the reports ---
    passed_mark = (merged_df['Variance'] < 0.01) & (merged_df['Bank Suggestion'] == "EXACT MATCH")

    passed_df = merged_df[passed_mark]
    passed_df.to_csv('data/reconciled_final.csv')
    logging.info("Reconciled list exported.")

    review_df = merged_df[~passed_mark]
    review_df.to_csv('data/audit_required.csv')
    logging.info("Audit list exported.")

    detailed_flags = (review_df['Vendor'] + " (" + review_df['Bank Suggestion'] + ")").unique().tolist()
    review_vendors = ", ".join(detailed_flags)

    # --- Final Results of Reconciliation ---
    logging.info(f"Reconciliation Complete!")
    logging.info(f"    - Total Entries: {len(merged_df)}")
    logging.info(f"    - Perfect Audits: {len(passed_df)}")
    logging.info(f"    - Needs Review: {len(review_df)}")
    logging.info(f"    - Flagged Vendors: {review_vendors}")
    logging.info(f"    - Total Variance: ${round(merged_df['Variance'].sum(), 2)}")

    # --- The Summary Table ---
    if not review_df.empty:
        top_errors = review_df.groupby('Vendor')['Variance'].sum().sort_values(ascending=False).head(3)
        summary = review_df.groupby('Vendor').agg({'Variance': 'sum', 'TXN_ID': lambda x: list(x[:5])}).sort_values('Variance', ascending=False)
        
        logging.info("--- TOP 3 DISCREPANCIES ---")
        for vendor, amount in top_errors.items():
            logging.info(f"    {vendor}: ${amount:,.2f}")

        logging.info("--- TOP DISCREPANCIES BY VENDOR ---")
        for vendor, row in summary.iterrows():
            txn_list = ", ".join(map(str, row['TXN_ID']))
            logging.info(f"    {vendor}: ${row['Variance']:,.2f} | Txn IDs: [{txn_list}]")


if __name__ == "__main__":
    try:
        main()
    finally:
        logging.shutdown()