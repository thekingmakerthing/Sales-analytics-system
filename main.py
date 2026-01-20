# main.py
from pathlib import Path
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, generate_sales_report


def main():
    """
    Main execution function
    """
    try:
        # Print welcome message
        print("=" * 60)
        print(" " * 18 + "SALES ANALYTICS SYSTEM")
        print("=" * 60)
        
        # 1. Read sales data file
        print("\n[1/10] Reading sales data...")
        base_dir = Path(__file__).parent
        data_file = base_dir / 'data' / 'sales_data.txt'
        raw_lines = read_sales_data(str(data_file))
        print(f"✓ Successfully read {len(raw_lines)} transactions")
        
        # 2. Parse and clean transactions
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")
        
        # 3. Display filter options
        print("\n[3/10] Filter Options Available:")
        
        
        
        regions = sorted(set(t.get('Region', 'Unknown') for t in transactions))
        print(f"Regions: {', '.join(regions)}")
              
        # Show transaction amount range
        amounts = [t.get('Quantity', 0) * t.get('UnitPrice', 0) for t in transactions if t.get('Quantity') and t.get('UnitPrice')]
        if amounts:
            min_amount = min(amounts)
            max_amount = max(amounts)
            print(f"Amount Range: ₹{min_amount:,.2f} - ₹{max_amount:,.2f}")
        print()

        region_filter = None
        min_amount_filter = None
        max_amount_filter = None

        # 4. Ask if user wants to filter
        filter_choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        if filter_choice == 'y':
            region_input = input("Enter region to filter (or press Enter to skip): ").strip()
            if region_input:
                region_filter = region_input
            
            min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
            if min_input:
                try:
                    min_amount_filter = float(min_input)
                except ValueError:
                    print("Invalid amount, skipping minimum filter")
            
            max_input = input("Enter maximum amount (or press Enter to skip): ").strip()
            if max_input:
                try:
                    max_amount_filter = float(max_input)
                except ValueError:
                    print("Invalid amount, skipping maximum filter")
        
        # 5. Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_txns, invalid_count, filter_summary = validate_and_filter(
            transactions, 
            region=region_filter, 
            min_amount=min_amount_filter, 
            max_amount=max_amount_filter
        )
        print(f"\n✓ Validation complete - {filter_summary['final_count']} records ready for analysis")
        
        # 6. Perform data analyses
        print("\n[5/10] Analyzing sales data...")
        
        total_rev = calculate_total_revenue(valid_txns)
        print(f"  Total Revenue: ₹{total_rev:,.2f}")
        
        regions = region_wise_sales(valid_txns)
        print(f"  Regions Analyzed: {len(regions)}")
        
        top_prods = top_selling_products(valid_txns, 5)
        print(f"  Top Products Identified: {len(top_prods)}")
        
        customers = customer_analysis(valid_txns)
        print(f"  Customers Analyzed: {len(customers)}")
        
        daily = daily_sales_trend(valid_txns)
        print(f"  Days Analyzed: {len(daily)}")
        
        peak = find_peak_sales_day(valid_txns)
        print(f"  Peak Sales Day: {peak[0]}")
        
        low_prods = low_performing_products(valid_txns, 10)
        print(f"  Low Performing Products: {len(low_prods)}")
        
        print("✓ Analysis complete")
        
        # 7. Fetch products from API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")
        
        # 8. Enrich sales data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_txns = enrich_sales_data(valid_txns, product_mapping)
        
        enriched_count = sum(1 for txn in enriched_txns if txn.get('API_Match'))
        success_rate = (enriched_count / len(enriched_txns) * 100) if enriched_txns else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_txns)} transactions ({success_rate:.1f}%)")
        
        # 9. Save enriched data (already done in enrich_sales_data)
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")
        
        # 10. Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_txns, enriched_txns)
        
        # Complete
        print("\n[10/10] Process Complete!")
        print("=" * 60)
        print("\nGenerated Files:")
        print("  - data/enriched_sales_data.txt")
        print("  - output/sales_report.txt")
        print("\n" + "=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("Please ensure 'data/sales_data.txt' exists.")
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()