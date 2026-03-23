import pandas as pd
import numpy as np

def generate_recon():
    rows = 1000
    # Internal Ledger (The Source)
    ledger = pd.DataFrame({
        'TXN_ID': [f'INT-{1000+i}' for i in range(rows)],
        'Amount': np.random.uniform(100, 5000, size=rows).round(2),
        'Vendor': np.random.choice(['AWS', 'Google', 'Azure', 'Stripe', 'Oracle'], rows)
    })
    
    # Bank Statement (The "Truth" - with noise)
    bank = ledger.copy()
    bank.columns = ['Statement_Ref', 'Bank_Amount', 'Description']
    
    # Introduce 5% Discrepancies
    for i in range(0, rows, 20): 
        bank.at[i, 'Bank_Amount'] += 0.05 # Small decimal error
        bank.at[i, 'Description'] = "UNKNOWN VENDOR" # Obfuscated name
        
    ledger.to_csv('data/internal_ledger.csv', index=False)
    bank.to_csv('data/bank_statement.csv', index=False)
    print("✅ FinOps Seed Data Created.")

if __name__ == "__main__":
    generate_recon()
