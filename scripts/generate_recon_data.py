import pandas as pd
import numpy as np
import os

def generate_recon():
    # --- STEP 1: ROBUST PATH LOGIC ---
    # Get the directory of the script and find the root 'data' folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)
    data_path = os.path.join(root_dir, 'data')

    # Create data directory if it doesn't exist
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    rows = 1000
    
    # --- STEP 2: CREATE INTERNAL LEDGER ---
    ledger = pd.DataFrame({
        'TXN_ID': [f'INT-{1000+i}' for i in range(rows)],
        'Amount': np.random.uniform(100, 5000, size=rows).round(2),
        'Vendor': np.random.choice(['AWS Cloud Services', 'Google LLC', 'Azure Microsoft', 'Stripe Payments', 'Oracle Corp'], rows)
    })
    
    # --- STEP 3: CREATE BANK STATEMENT (The "Truth" with noise) ---
    bank = ledger.copy()
    bank.columns = ['Statement_Ref', 'Bank_Amount', 'Description']
    
    # Introduce 5% Discrepancies (Every 20th row)
    for i in range(0, rows, 20): 
        # Simulation: A small rounding error (classic in multi-currency or tax calcs)
        bank.at[i, 'Bank_Amount'] = (bank.at[i, 'Bank_Amount'] + 0.05).round(2)
        # Simulation: Bank statement uses shorthand/obfuscated names
        bank.at[i, 'Description'] = "MISC VENDOR" 
        
    # --- STEP 4: EXPORT TO CSV ---
    ledger_file = os.path.join(data_path, 'internal_ledger.csv')
    bank_file = os.path.join(data_path, 'bank_statement.csv')
    
    ledger.to_csv(ledger_file, index=False)
    bank.to_csv(bank_file, index=False)
    
    print(f"✅ FinOps Seed Data Created at: {data_path}")

if __name__ == "__main__":
    generate_recon()