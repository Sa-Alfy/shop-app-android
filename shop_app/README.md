# Shop Management App

A Streamlit-based application for managing shop inventory and sales, integrated with Google Sheets for data storage.

## Features

1. **Add Stock**
   - Add new products to inventory
   - Auto-generate unique Product IDs
   - Track Purchase Price, Selling Price, and Quantity

2. **Record Sales**
   - Select products from current inventory
   - Automatic stock quantity updates
   - Calculate total price automatically

3. **View Sales History**
   - Filter sales by time period (1 Day, 1 Week, All Time)
   - View detailed sales information
   - Export data to Excel

4. **Data Export**
   - Export Sales data with filters
   - Export complete shop data (Stock and Sales)
   - Excel format with formatted currency and dates

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd shop-app
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Google Sheets Setup**
   1. Go to Google Cloud Console
   2. Create a new project
   3. Enable Google Sheets API
   4. Create Service Account credentials
   5. Download credentials as JSON file
   6. Save the credentials file as `credentials.json` in the project root
   7. Share your Google Sheet with the service account email

4. **Configuration**
   1. Copy `.env.example` to `.env`
   2. Update `SPREADSHEET_ID` with your Google Sheet ID
   3. Make sure `credentials.json` is in the project root

5. **Running the App**
   ```bash
   streamlit run frontend/app.py
   ```

## Google Sheets Structure

1. **Stock Sheet**
   - Columns: Product Name, Date Added, Purchase Price, Selling Price, Supplier, Quantity, Product ID

2. **Sales Sheet**
   - Columns: Product ID, Date of Sale, Quantity Sold, Total Price

## Usage

1. **Adding Stock**
   - Click "Add Stock" on the home screen
   - Fill in product details
   - Submit to add to inventory

2. **Recording Sales**
   - Click "Record Sale"
   - Select product from dropdown
   - Enter quantity
   - Confirm sale

3. **Viewing Sales History**
   - Click "Sales History"
   - Use the filter options to view specific periods
   - Export data using the export buttons

4. **Data Export**
   - Use "Export Sales Data" for filtered sales data
   - Use "Export All Shop Data" for complete backup

## Error Handling

- Stock quantity validation
- Duplicate Product ID prevention
- Google Sheets connection error handling
- Data validation for all inputs

## Dependencies

- streamlit
- pandas
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- openpyxl
- python-dotenv

## Support

For any issues or questions, please open an issue in the repository.