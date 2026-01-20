# utils/api_handler.py

import requests
import re


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    try:
        url = "https://dummyjson.com/products?limit=100"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('products', [])
        
        # Extract relevant fields
        product_list = [
            {
                'id': p.get('id'),
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'price': p.get('price'),
                'rating': p.get('rating')
            }
            for p in products
        ]
        
        print(f"✓ Successfully fetched {len(product_list)} products from API")
        return product_list
        
    except requests.exceptions.RequestException as e:
        print(f"✗ API Error: {e}")
        return []
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Returns: dictionary mapping product IDs to info
    """
    mapping = {}
    
    for product in api_products:
        product_id = product.get('id')
        if product_id:
            mapping[product_id] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }
    
    return mapping

def _extract_id_from_second_digit_onwards(product_id):
    """
    Extracts numeric ID from ProductID by taking digits from the 2nd digit onwards.

    Examples:
    - P102 -> 2   ("02" -> 2)
    - P172 -> 72
    - P2   -> None (no 2nd digit)

    Returns: int ID, or None if not possible.
    """
    if not product_id:
        return None
    
    # Remove 'P' prefix if present
    numeric_part = product_id.lstrip('Pp')

    # Keep digits only (defensive)
    digits = "".join(ch for ch in numeric_part if ch.isdigit())
    if len(digits) < 2:
        return None

    try:
        return int(digits[1:])  # from 2nd digit onwards
    except ValueError:
        return None
    

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Returns: list of enriched transaction dictionaries
    """
    enriched = []
    
    for txn in transactions:
        # Create enriched transaction copy
        enriched_txn = txn.copy()
        
        try:
            # Extract numeric ID from ProductID (P101 → 101, P5 → 5)
            product_id_str = txn.get('ProductID', '')
            api_product_id = _extract_id_from_second_digit_onwards(product_id_str)
            if api_product_id is not None:
                # Check if ID exists in product_mapping
                if api_product_id in product_mapping:
                    product_info = product_mapping[api_product_id]
                    enriched_txn['API_Category'] = product_info.get('category')
                    enriched_txn['API_Brand'] = product_info.get('brand')
                    enriched_txn['API_Rating'] = product_info.get('rating')
                    enriched_txn['API_Match'] = True
                else:
                    enriched_txn['API_Category'] = None
                    enriched_txn['API_Brand'] = None
                    enriched_txn['API_Rating'] = None
                    enriched_txn['API_Match'] = False
            else:
                enriched_txn['API_Category'] = None
                enriched_txn['API_Brand'] = None
                enriched_txn['API_Rating'] = None
                enriched_txn['API_Match'] = False
                
        except Exception as e:
            # Handle errors gracefully
            enriched_txn['API_Category'] = None
            enriched_txn['API_Brand'] = None
            enriched_txn['API_Rating'] = None
            enriched_txn['API_Match'] = False
        
        enriched.append(enriched_txn)
    
    # Save enriched data
    save_enriched_data(enriched)
    
    return enriched


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """
    try:
        # Create directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            f.write(header)
            
            # Write data
            for txn in enriched_transactions:
                line = (
                    f"{txn['TransactionID']}|"
                    f"{txn['Date']}|"
                    f"{txn['ProductID']}|"
                    f"{txn['ProductName']}|"
                    f"{txn['Quantity']}|"
                    f"{txn['UnitPrice']}|"
                    f"{txn.get('CustomerID', '')}|"
                    f"{txn['Region']}|"
                    f"{txn.get('API_Category') or ''}|"
                    f"{txn.get('API_Brand') or ''}|"
                    f"{txn.get('API_Rating') or ''}|"
                    f"{txn.get('API_Match', False)}\n"
                )
                f.write(line)
        
        print(f"✓ Enriched data saved to: {filename}")
        
    except Exception as e:
        print(f"✗ Error saving enriched data: {e}")


from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # 1. HEADER
        f.write("=" * 60 + "\n")
        f.write(" " * 15 + "SALES ANALYTICS REPORT\n")
        f.write(" " * 10 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(" " * 10 + f"Records Processed: {len(transactions)}\n")
        f.write("=" * 60 + "\n\n")
        
        # 2. OVERALL SUMMARY
        total_revenue = calculate_total_revenue(transactions)
        total_txns = len(transactions)
        avg_order = total_revenue / total_txns if total_txns > 0 else 0
        
        dates = [txn['Date'] for txn in transactions]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
        
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_txns}\n")
        f.write(f"Average Order Value:  ₹{avg_order:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")
        
        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Region':<15} {'Sales':<20} {'% of Total':<15} {'Transactions'}\n")
        f.write("-" * 60 + "\n")
        
        region_data = region_wise_sales(transactions)
        for region, data in region_data.items():
            f.write(f"{region:<15} ₹{data['total_sales']:<18,.2f} {data['percentage']:<14.2f}% {data['transaction_count']}\n")
        f.write("\n")
        
        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<6} {'Product Name':<25} {'Quantity':<12} {'Revenue'}\n")
        f.write("-" * 60 + "\n")
        
        top_products = top_selling_products(transactions, 5)
        for i, (product, qty, revenue) in enumerate(top_products, 1):
            f.write(f"{i:<6} {product:<25} {qty:<12} ₹{revenue:,.2f}\n")
        f.write("\n")
        
        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Order Count'}\n")
        f.write("-" * 60 + "\n")
        
        customers = customer_analysis(transactions)
        for i, (cust_id, data) in enumerate(list(customers.items())[:5], 1):
            f.write(f"{i:<6} {cust_id:<15} ₹{data['total_spent']:<18,.2f} {data['purchase_count']}\n")
        f.write("\n")
        
        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers'}\n")
        f.write("-" * 60 + "\n")
        
        daily_data = daily_sales_trend(transactions)
        for date, data in list(daily_data.items())[:10]:  # Show first 10 days
            f.write(f"{date:<15} ₹{data['revenue']:<18,.2f} {data['transaction_count']:<15} {data['unique_customers']}\n")
        f.write("\n")
        
        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 60 + "\n")
        
        peak_day = find_peak_sales_day(transactions)
        f.write(f"Best Selling Day: {peak_day[0]} (₹{peak_day[1]:,.2f}, {peak_day[2]} transactions)\n\n")
        
        low_products = low_performing_products(transactions, 10)
        if low_products:
            f.write("Low Performing Products (Quantity < 10):\n")
            for product, qty, revenue in low_products[:5]:
                f.write(f"  - {product}: {qty} units, ₹{revenue:,.2f}\n")
        else:
            f.write("No low performing products found.\n")
        f.write("\n")
        
        # Average transaction value per region
        f.write("Average Transaction Value by Region:\n")
        for region, data in region_data.items():
            avg_txn = data['total_sales'] / data['transaction_count'] if data['transaction_count'] > 0 else 0
            f.write(f"  {region}: ₹{avg_txn:,.2f}\n")
        f.write("\n")
        
        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 60 + "\n")
        
        enriched_count = sum(1 for txn in enriched_transactions if txn.get('API_Match'))
        success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
        
        f.write(f"Total Products Enriched: {enriched_count}/{len(enriched_transactions)}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n\n")
        
        # Products that couldn't be enriched
        failed_products = set()
        for txn in enriched_transactions:
            if not txn.get('API_Match'):
                failed_products.add(txn.get('ProductID', 'Unknown'))
        
        if failed_products:
            f.write("Products that couldn't be enriched:\n")
            for pid in sorted(failed_products):
                f.write(f"  - {pid}\n")
        else:
            f.write("All products successfully enriched!\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write(" " * 20 + "END OF REPORT\n")
        f.write("=" * 60 + "\n")
    
    print(f"✓ Report saved to: {output_file}")