# Lease Abstraction Research Findings

## Overview
Lease abstraction is the process of extracting critical data points from lease agreements to enable efficient property management and tenant onboarding/offboarding.

## Key Data Fields for Extraction

### Critical for Compliance (Required Fields)
1. **Lease number (name)** - Unique identifier for each lease
2. **Begin Date** - When the lease starts and payment schedule begins
3. **Base End Date** - Date when lease is scheduled to terminate
4. **Incremental Borrowing Rate (IBR)** - Discount rate for present value calculations
5. **Economic Life** - Expected useful life of the asset
6. **Fair Value** - Fair value of underlying lease asset
7. **Rent Payment** - Amount of rent paid each period
8. **Payment due dates** - Step payments and uneven payment schedules
9. **Payment Frequency** - How often payments are made (monthly, annually, etc.)
10. **Repayment Mode** - Payments in advance or in arrears

### Special Accounting Data
1. **Renewal Options** - Early renewal, expansion, end of term options
2. **End of Term events** - Auto-renewal clauses, early termination options
3. **Initial Direct Costs/Lease Incentives** - Upfront costs and incentives
4. **Guaranteed Residual Value** - Amount owed at end of term
5. **Asset in Service date** - When property/asset is available for use
6. **Special Depreciation** - Different depreciation methods if needed
7. **Asset Adjustments** - Additions/subtractions from initial lease liability
8. **Deferred Rent Rollover** - Deferred rent from prior lease
9. **Salvage Value** - Portion not to be depreciated

### Optional Vendor and Lease Management
1. **Lessor Information** - Vendor number, contact details
2. **Lessee Notifications** - Reminders for option/termination dates

### Additional Tenant Information (for residential)
1. **Tenant Name** - Legal name(s) of tenant(s)
2. **Tenant Contact Information** - Phone, email, emergency contact
3. **Property Address** - Unit number, street address, city, state, zip
4. **Security Deposit Amount** - Amount paid and date received
5. **Pet Information** - Pet type, breed, deposit/fees
6. **Parking Information** - Assigned parking spaces
7. **Utilities** - Which utilities tenant is responsible for
8. **Move-in Date** - Actual move-in date
9. **Lease Type** - Fixed term, month-to-month, etc.
10. **Special Clauses** - Any special terms or conditions

## Yardi Integration Insights

### Yardi Smart Lease (AI Solution)
- Yardi has built-in AI-powered lease abstraction called "Smart Lease"
- Fully integrated with Yardi Voyager 8
- Features:
  - AI-driven lease abstraction pulls key terms, dates, clauses into Voyager tables
  - Smart search across portfolio
  - Auto-tagging and bookmarks
  - Real-time editing
  - Confidence scores for AI extractions
  - Full integration with Voyager 8

### Yardi Import Requirements
- Yardi supports CSV/Excel imports for tenant data
- ETL (Extract, Transform, Load) imports available
- YtoY method for acquisitions from other Yardi customers
- Field mapping is critical - must match Yardi's mandatory fields
- Import process: Admin > Toolbox > Import/Export > Import Trans CSV

## Pain Points to Address
1. **Manual data entry** - Time-consuming and error-prone
2. **Disconnected systems** - Lease data in one system, property management in another
3. **Searching difficulty** - Hard to find specific terms across large portfolios
4. **Data confidence** - Uncertainty about accuracy of extracted data
5. **Delayed workflows** - Manual processes create bottlenecks

## Solution Approach for Custom Tool
1. Use AI/LLM for intelligent PDF extraction
2. Handle scanned documents (OCR capability)
3. Generate two outputs:
   - Excel file formatted for Yardi automatic import
   - Structured document with all extracted data for manual review/entry
4. Include confidence scores for extracted fields
5. Allow user review and correction before export
6. Support batch processing of multiple leases

## Technical Considerations
- PDF text extraction + OCR for scanned documents
- LLM-based intelligent field extraction
- Structured data validation
- Excel generation with proper formatting for Yardi
- User-friendly Streamlit interface
- Error handling and data quality checks
