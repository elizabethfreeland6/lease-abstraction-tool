# Lease Abstraction Tool - Architecture & Design

## Application Overview
A Streamlit-based web application that automates lease document abstraction for Yardi property management system integration.

## Core Features
1. **PDF Upload & Processing** - Support for both digital and scanned lease PDFs
2. **AI-Powered Data Extraction** - Intelligent field extraction using LLM
3. **Interactive Review & Correction** - User interface for reviewing and editing extracted data
4. **Dual Export System**:
   - Excel file formatted for Yardi automatic import
   - Structured document (PDF/Excel) for manual data entry reference
5. **Batch Processing** - Handle multiple lease documents at once
6. **Confidence Scoring** - Display confidence levels for extracted fields

## Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **PDF Processing**: PyPDF2, pdfplumber, pdf2image
- **OCR**: pytesseract (for scanned documents)
- **AI/LLM**: OpenAI API (GPT-4.1-mini for cost-effective extraction)
- **Data Processing**: pandas, openpyxl
- **Export Generation**: openpyxl (Excel), reportlab/fpdf2 (PDF)

## Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
├─────────────────────────────────────────────────────────────┤
│  Upload → Process → Review → Export                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   PDF Processing Layer                       │
├─────────────────────────────────────────────────────────────┤
│  • Text Extraction (pdfplumber)                             │
│  • OCR for Scanned Docs (pytesseract)                       │
│  • Image Preprocessing                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   AI Extraction Engine                       │
├─────────────────────────────────────────────────────────────┤
│  • LLM-based field extraction                               │
│  • Structured JSON output                                    │
│  • Confidence scoring                                        │
│  • Field validation                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Data Processing Layer                      │
├─────────────────────────────────────────────────────────────┤
│  • Data validation & normalization                          │
│  • Date formatting                                           │
│  • Currency formatting                                       │
│  • Field mapping to Yardi schema                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Export Generation                         │
├─────────────────────────────────────────────────────────────┤
│  Export 1: Yardi Import Excel                               │
│  Export 2: Structured Reference Document                     │
└─────────────────────────────────────────────────────────────┘
```

## Data Schema

### Core Lease Fields (for extraction)
```json
{
  "tenant_information": {
    "tenant_name": "string",
    "tenant_email": "string",
    "tenant_phone": "string",
    "emergency_contact_name": "string",
    "emergency_contact_phone": "string"
  },
  "property_information": {
    "property_address": "string",
    "unit_number": "string",
    "property_type": "string",
    "square_footage": "number"
  },
  "lease_terms": {
    "lease_number": "string",
    "lease_start_date": "date",
    "lease_end_date": "date",
    "lease_term_months": "number",
    "lease_type": "string"
  },
  "financial_terms": {
    "monthly_rent": "number",
    "security_deposit": "number",
    "pet_deposit": "number",
    "payment_frequency": "string",
    "payment_due_date": "number",
    "late_fee_amount": "number",
    "late_fee_grace_period": "number"
  },
  "additional_terms": {
    "utilities_included": "array",
    "parking_spaces": "number",
    "pet_allowed": "boolean",
    "pet_type": "string",
    "renewal_options": "string",
    "early_termination_clause": "string",
    "maintenance_responsibilities": "string"
  },
  "metadata": {
    "extraction_date": "datetime",
    "confidence_score": "number",
    "document_type": "string"
  }
}
```

## User Workflow

### 1. Upload Phase
- User uploads one or multiple PDF lease documents
- System validates file format and size
- Display upload status and document list

### 2. Processing Phase
- Extract text from PDFs (with OCR fallback for scanned docs)
- Send extracted text to LLM for structured data extraction
- Parse LLM response into structured format
- Calculate confidence scores for each field
- Display progress indicator

### 3. Review Phase
- Display extracted data in organized form
- Show confidence scores with color coding (high/medium/low)
- Allow inline editing of any field
- Provide original PDF preview for reference
- Validate required fields

### 4. Export Phase
- Generate two export files:
  - **Yardi Import Excel**: Formatted with Yardi-specific columns
  - **Reference Document**: Comprehensive structured view with all fields
- Provide download buttons for both files
- Option to process another batch

## LLM Extraction Prompt Strategy

### Prompt Template
```
You are a lease document abstraction specialist. Extract the following information from the lease agreement text provided.

Extract these fields and return as JSON:
- Tenant Information: name, email, phone, emergency contact
- Property Information: address, unit, type, size
- Lease Terms: start date, end date, lease number, term length
- Financial Terms: rent amount, deposits, fees, payment terms
- Additional Terms: utilities, parking, pets, special clauses

Rules:
1. Return ONLY valid JSON
2. Use null for missing fields
3. Format dates as YYYY-MM-DD
4. Format currency as numbers without symbols
5. Include confidence level (0-1) for each field

Lease Document Text:
{lease_text}
```

## Yardi Excel Export Format

### Column Mapping (example structure)
| Column Name | Data Type | Source Field | Required |
|------------|-----------|--------------|----------|
| TenantName | Text | tenant_name | Yes |
| UnitNumber | Text | unit_number | Yes |
| LeaseStartDate | Date | lease_start_date | Yes |
| LeaseEndDate | Date | lease_end_date | Yes |
| MonthlyRent | Currency | monthly_rent | Yes |
| SecurityDeposit | Currency | security_deposit | No |
| TenantEmail | Text | tenant_email | No |
| TenantPhone | Text | tenant_phone | No |
| ParkingSpaces | Number | parking_spaces | No |
| PetDeposit | Currency | pet_deposit | No |

## Error Handling Strategy
1. **PDF Processing Errors**: Fallback to OCR if text extraction fails
2. **LLM API Errors**: Retry logic with exponential backoff
3. **Missing Required Fields**: Highlight in red, prevent export until filled
4. **Invalid Data Formats**: Show validation errors with correction hints
5. **File Size Limits**: Warn user and suggest document splitting

## Security Considerations
- No persistent storage of lease documents
- API keys stored in environment variables
- Session-based temporary file storage
- Automatic cleanup after session ends
- No logging of sensitive tenant information

## Performance Optimization
- Async processing for multiple documents
- Caching of extracted text
- Batch API calls where possible
- Progress indicators for long operations
- Lazy loading of PDF previews

## Future Enhancements (Phase 2)
1. Template customization for different lease types
2. Integration with Yardi API for direct upload
3. Historical data tracking and analytics
4. Multi-language support
5. Custom field mapping configuration
6. Bulk processing with queue management
