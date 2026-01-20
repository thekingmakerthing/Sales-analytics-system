# utils/data_processor.py

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (total revenue)
    """
    total = sum(txn['Quantity'] * txn['UnitPrice'] for txn in transactions)
    return total


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary with region statistics
    """
    region_data = {}
    
    # Aggregate by region
    for txn in transactions:
        region = txn['Region']
        amount = txn['Quantity'] * txn['UnitPrice']
        
        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0,
                'percentage': 0.0
            }
        
        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1
    
    # Calculate percentages
    total_revenue = sum(data['total_sales'] for data in region_data.values())
    for region in region_data:
        region_data[region]['percentage'] = (region_data[region]['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0
    
    # Sort by total_sales descending
    sorted_regions = dict(sorted(region_data.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    
    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = {}
    
    # Aggregate by product
    for txn in transactions:
        product = txn['ProductName']
        quantity = txn['Quantity']
        revenue = txn['Quantity'] * txn['UnitPrice']
        
        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }
        
        product_data[product]['quantity'] += quantity
        product_data[product]['revenue'] += revenue
    
    # Convert to list of tuples
    product_list = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
    ]
    
    # Sort by quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    return product_list[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary of customer statistics
    """
    customer_data = {}
    
    for txn in transactions:
        customer = txn['CustomerID']
        if not customer:  # Skip empty customer IDs
            continue
        
        amount = txn['Quantity'] * txn['UnitPrice']
        product = txn['ProductName']
        
        if customer not in customer_data:
            customer_data[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'avg_order_value': 0.0,
                'products_bought': []
            }
        
        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        
        if product not in customer_data[customer]['products_bought']:
            customer_data[customer]['products_bought'].append(product)
    
    # Calculate average order value
    for customer in customer_data:
        total = customer_data[customer]['total_spent']
        count = customer_data[customer]['purchase_count']
        customer_data[customer]['avg_order_value'] = total / count if count > 0 else 0
    
    # Sort by total_spent descending
    sorted_customers = dict(sorted(customer_data.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    return sorted_customers


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """
    daily_data = {}
    
    for txn in transactions:
        date = txn['Date']
        revenue = txn['Quantity'] * txn['UnitPrice']
        customer = txn['CustomerID']
        
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }
        
        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        if customer:
            daily_data[date]['unique_customers'].add(customer)
    
    # Convert sets to counts
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(daily_data[date]['unique_customers'])
    
    # Sort chronologically
    sorted_daily = dict(sorted(daily_data.items()))
    
    return sorted_daily


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """
    daily_data = daily_sales_trend(transactions)
    
    if not daily_data:
        return (None, 0.0, 0)
    
    peak_date = max(daily_data.items(), key=lambda x: x[1]['revenue'])
    
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['transaction_count'])


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = {}
    
    # Aggregate by product
    for txn in transactions:
        product = txn['ProductName']
        quantity = txn['Quantity']
        revenue = txn['Quantity'] * txn['UnitPrice']
        
        if product not in product_data:
            product_data[product] = {
                'quantity': 0,
                'revenue': 0.0
            }
        
        product_data[product]['quantity'] += quantity
        product_data[product]['revenue'] += revenue
    
    # Filter products below threshold
    low_products = [
        (product, data['quantity'], data['revenue'])
        for product, data in product_data.items()
        if data['quantity'] < threshold
    ]
    
    # Sort by quantity ascending
    low_products.sort(key=lambda x: x[1])
    
    return low_products