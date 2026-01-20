# utils/file_handler.py

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                # Skip header row and remove empty lines
                data_lines = [line.strip() for line in lines[1:] if line.strip()]
                return data_lines
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found. Please ensure the file exists in the correct location.")
    
    raise ValueError(f"Error: Unable to read file '{filename}' with any supported encoding.")


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    Returns: list of dictionaries
    """
    transactions = []
    
    for line in raw_lines:
        fields = line.split('|')
        
        # Skip rows with incorrect number of fields
        if len(fields) != 8:
            continue
        
        try:
            # Clean and parse fields
            transaction = {
                'TransactionID': fields[0].strip(),
                'Date': fields[1].strip(),
                'ProductID': fields[2].strip(),
                'ProductName': fields[3].strip().replace(',', ''),  # Remove commas
                'Quantity': int(fields[4].strip().replace(',', '')),  # Remove commas, convert to int
                'UnitPrice': float(fields[5].strip().replace(',', '')),  # Remove commas, convert to float
                'CustomerID': fields[6].strip(),
                'Region': fields[7].strip()
            }
            transactions.append(transaction)
        except (ValueError, IndexError):
            # Skip rows with conversion errors
            continue
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """
    total_parsed = len(transactions)
    valid_transactions = []
    invalid_count = 0
    
    # Validation Rules
    for txn in transactions:
        is_valid = True
        
        # Quantity must be > 0
        if txn.get('Quantity', 0) <= 0:
            is_valid = False
        
        # UnitPrice must be > 0
        if txn.get('UnitPrice', 0) <= 0:
            is_valid = False
        
        # All required fields must be present
        required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                          'Quantity', 'UnitPrice', 'Region']
        if not all(txn.get(field) for field in required_fields):
            is_valid = False
        
        # TransactionID must start with 'T'
        if not txn.get('TransactionID', '').startswith('T'):
            is_valid = False
        
        # ProductID must start with 'P'
        if not txn.get('ProductID', '').startswith('P'):
            is_valid = False
        
        # CustomerID must start with 'C' (allow empty for some cases)
        customer_id = txn.get('CustomerID', '')
        if customer_id and not customer_id.startswith('C'):
            is_valid = False
        
        if is_valid:
            valid_transactions.append(txn)
        else:
            invalid_count += 1
    
    valid_after_cleaning = len(valid_transactions)
    
    # Print validation summary in required format
    print("\nValidation Summary:")
    print("-" * 50)
    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {valid_after_cleaning}")
    print("-" * 50)
    
    # Display available regions
    regions = set(txn['Region'] for txn in valid_transactions if txn.get('Region'))
    print(f"\nAvailable Regions: {', '.join(sorted(regions))}")
    
    # Display transaction amount range
    amounts = [txn['Quantity'] * txn['UnitPrice'] for txn in valid_transactions]
    if amounts:
        print(f"Transaction Amount Range: ₹{min(amounts):,.2f} - ₹{max(amounts):,.2f}")
    
    # Apply filters
    filtered_transactions = valid_transactions.copy()
    filtered_by_region = 0
    filtered_by_amount = 0
    
    if region:
        before_filter = len(filtered_transactions)
        filtered_transactions = [txn for txn in filtered_transactions if txn.get('Region') == region]
        filtered_by_region = before_filter - len(filtered_transactions)
        print(f"After region filter ({region}): {len(filtered_transactions)} records")
    
    if min_amount is not None or max_amount is not None:
        before_filter = len(filtered_transactions)
        filtered_transactions = [
            txn for txn in filtered_transactions
            if (min_amount is None or txn['Quantity'] * txn['UnitPrice'] >= min_amount) and
               (max_amount is None or txn['Quantity'] * txn['UnitPrice'] <= max_amount)
        ]
        filtered_by_amount = before_filter - len(filtered_transactions)
        print(f"After amount filter: {len(filtered_transactions)} records")
    
    filter_summary = {
        'total_input': total_parsed,
        'invalid': invalid_count,
        'valid_after_cleaning': valid_after_cleaning,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }
    
    return (filtered_transactions, invalid_count, filter_summary)