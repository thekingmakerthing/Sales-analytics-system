# Sales Analytics System

A comprehensive Python-based sales data analytics system that processes sales data, integrates with external APIs, performs analysis, and generates detailed reports.

## Features

- **Data Processing**: Read, parse, and validate sales data from pipe-delimited files
- **Data Filtering**: Filter transactions by region and amount range
- **Analytics**: 
  - Calculate total revenue
  - Region-wise sales analysis
  - Top-selling products identification
  - Customer purchase pattern analysis
  - Daily sales trends
  - Peak sales day identification
  - Low-performing product detection
- **API Integration**: Fetch product data from DummyJSON API and enrich sales data
- **Report Generation**: Generate comprehensive formatted text reports

## Project Structure

```
sales-analytics-system/
├── README.md
├── main.py
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── api_handler.py
│   └── report.py
├── data/
│   └── sales_data.txt (provided)
├── output/
└── requirements.txt
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sales-analytics-system.git
   cd sales-analytics-system
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

- Python 3.7 or higher
- requests library (for API calls)

## Setup

1. Ensure the `data/sales_data.txt` file is in the correct location
2. The script will automatically create `output/` directory for reports
3. Enriched data will be saved to `data/enriched_sales_data.txt`

## Usage

### Running the System

```bash
python main.py
```

### Interactive Options

When you run the program, you'll be prompted:

1. **Filter Data**: Choose whether to filter the data
   - If yes, you can filter by:
     - Region (North, South, East, West)
     - Minimum amount
     - Maximum amount

2. **Processing**: The system will automatically:
   - Read and parse sales data
   - Validate transactions
   - Perform analytics
   - Fetch product data from API
   - Enrich sales data
   - Generate comprehensive report

### Example Run

```
========================================
      SALES ANALYTICS SYSTEM
========================================

[1/10] Reading sales data...
✓ Successfully read 78 transactions

[2/10] Parsing and cleaning data...
✓ Parsed 78 records

[3/10] Filter Options Available:

Available Regions: East, North, South, West
Transaction Amount Range: ₹149.00 - ₹819,896.00

Do you want to filter data? (y/n): n

[4/10] Validating transactions...
✓ Valid: 75 | Invalid: 3

[5/10] Analyzing sales data...
  Total Revenue: ₹1,545,234.00
  Regions Analyzed: 4
✓ Analysis complete

[6/10] Fetching product data from API...
✓ Successfully fetched 100 products from API
✓ Fetched 100 products

[7/10] Enriching sales data...
✓ Enriched data saved to: data/enriched_sales_data.txt
✓ Enriched 68/75 transactions (90.7%)

[8/10] Saving enriched data...
✓ Saved to: data/enriched_sales_data.txt

[9/10] Generating report...
✓ Report saved to: output/sales_report.txt

[10/10] Process Complete!
========================================

Generated Files:
  - data/enriched_sales_data.txt
  - output/sales_report.txt

========================================
```

## Output Files

### 1. enriched_sales_data.txt
Contains the original sales data enriched with API information:
- API_Category
- API_Brand
- API_Rating
- API_Match (success indicator)

### 2. sales_report.txt
Comprehensive report including:
- Overall summary (total revenue, transactions, average order value)
- Region-wise performance
- Top 5 products
- Top 5 customers
- Daily sales trend
- Product performance analysis
- API enrichment summary

## Data Validation Rules

Transactions are validated based on:
- Quantity must be > 0
- UnitPrice must be > 0
- All required fields must be present
- TransactionID must start with 'T'
- ProductID must start with 'P'
- CustomerID must start with 'C'

## API Integration

The system integrates with the DummyJSON API (https://dummyjson.com) to fetch product information and enrich sales data with additional details like category, brand, and ratings.

## Error Handling

The system includes robust error handling for:
- File not found errors
- Encoding issues (tries UTF-8, Latin-1, CP1252)
- API connection errors
- Data validation errors
- Type conversion errors

## Troubleshooting

**Issue**: File not found error
- **Solution**: Ensure `data/sales_data.txt` exists in the correct location

**Issue**: API timeout
- **Solution**: Check your internet connection and try again

**Issue**: Import errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is created for educational purposes.

## Author

Arbab Husain

## Acknowledgments

- DummyJSON API for providing test product data
- Python community for excellent libraries