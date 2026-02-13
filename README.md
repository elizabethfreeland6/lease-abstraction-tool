# Lease Abstraction Tool for Yardi

An AI-powered Streamlit application that automates lease document abstraction for Yardi property management system integration. This tool extracts key information from lease PDFs and generates Yardi-compatible exports.

## Features

- **📤 PDF Upload & Processing** - Upload single or multiple lease PDF documents
- **🤖 AI-Powered Extraction** - Intelligent field extraction using OpenAI GPT models
- **✏️ Interactive Review** - Review and edit extracted data before export
- **📊 Dual Export System**:
  - **Yardi Import Excel** - Formatted for automatic import into Yardi
  - **Reference Document** - Comprehensive structured view for manual data entry
- **🎯 Confidence Scoring** - AI confidence levels for each extraction
- **📋 Batch Processing** - Handle multiple lease documents simultaneously

## Extracted Data Fields

### Tenant Information
- Tenant name, email, phone
- Emergency contact details

### Property Information
- Property address, unit number
- Property type, square footage

### Lease Terms
- Lease number, start/end dates
- Lease term length, lease type

### Financial Terms
- Monthly rent, security deposit
- Pet deposits, late fees
- Payment due dates and terms

### Additional Terms
- Parking spaces, pet policies
- Utilities included
- Renewal options
- Early termination clauses
- Maintenance responsibilities

## Installation

### Prerequisites
- Python 3.11 or higher
- OpenAI API key (pre-configured in this environment)

### Setup

1. **Install required packages:**
```bash
pip install -r requirements.txt
```

2. **Environment Variables:**
The OpenAI API key is already configured in your environment. If running elsewhere, create a `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Running the Application

1. **Start the Streamlit application:**
```bash
streamlit run app.py
```

2. **Access the web interface:**
The application will open in your default browser at `http://localhost:8501`

### Workflow

#### Step 1: Upload & Process
1. Navigate to the "Upload & Process" tab
2. Click "Browse files" and select one or more lease PDF documents
3. Click "Process Documents" to extract data using AI
4. Wait for processing to complete (progress bar will show status)

#### Step 2: Review & Edit
1. Navigate to the "Review & Edit" tab
2. Select a document from the dropdown to review
3. Review all extracted fields
4. Edit any incorrect or missing information
5. Click "Save Changes" to update the data

#### Step 3: Export
1. Navigate to the "Export" tab
2. Generate exports:
   - **Yardi Import Excel**: Click "Generate Yardi Excel" → Download the file
   - **Reference Document**: Click "Generate Reference Document" → Download the file
3. Use the Yardi Import Excel for automatic import into Yardi
4. Use the Reference Document as a guide for manual data entry

## File Structure

```
lease_abstraction_tool/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env.example               # Environment variable template
├── uploads/                   # Temporary storage for uploaded PDFs
├── exports/                   # Generated export files
└── utils/                     # Utility modules
    ├── __init__.py
    ├── pdf_processor.py       # PDF text extraction
    ├── ai_extractor.py        # AI-powered data extraction
    └── export_generator.py    # Export file generation
```

## Technical Details

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **PDF Processing**: pdfplumber (text extraction)
- **AI/LLM**: OpenAI GPT-4.1-mini (cost-effective extraction)
- **Data Processing**: pandas, openpyxl
- **Export Generation**: openpyxl (Excel formatting)

### AI Extraction Process
1. Extract raw text from PDF using pdfplumber
2. Send text to OpenAI GPT model with structured prompt
3. Parse JSON response into standardized data structure
4. Validate and clean extracted data
5. Calculate confidence scores for extraction quality

### Yardi Excel Format
The generated Excel file includes these columns mapped to Yardi fields:
- TenantName, TenantEmail, TenantPhone
- PropertyAddress, UnitNumber, PropertyType, SquareFootage
- LeaseNumber, LeaseStartDate, LeaseEndDate, LeaseTermMonths, LeaseType
- MonthlyRent, SecurityDeposit, PetDeposit
- PaymentDueDate, LateFeeAmount, LateFeeGracePeriod
- ParkingSpaces, PetAllowed, PetType
- EmergencyContactName, EmergencyContactPhone
- UtilitiesIncluded, SourceFile

## Troubleshooting

### PDF Text Extraction Issues
**Problem**: "Could not extract sufficient text from document"

**Solutions**:
- The PDF may be scanned or image-based
- OCR functionality can be enabled (requires additional setup)
- Try converting the PDF to a text-based format first

### AI Extraction Errors
**Problem**: Failed to extract data or low confidence scores

**Solutions**:
- Ensure the PDF contains a standard lease agreement format
- Check that the document is readable and not corrupted
- Review and manually correct fields in the Review & Edit tab

### Missing Fields
**Problem**: Some fields are empty after extraction

**Solutions**:
- The information may not be present in the lease document
- Manually fill in missing fields in the Review & Edit tab
- Check the original PDF to verify the information exists

## Best Practices

1. **Document Quality**: Use high-quality, text-based PDFs for best results
2. **Review Before Export**: Always review extracted data before generating exports
3. **Batch Processing**: Process multiple leases at once for efficiency
4. **Field Validation**: Check required fields (tenant name, dates, rent) are populated
5. **Backup**: Keep original PDF files as reference

## Customization

### Adding Custom Fields
To add custom fields to extraction:

1. Update the extraction prompt in `utils/ai_extractor.py`
2. Add field validation in `validate_and_clean_data()` function
3. Update the Streamlit form in `app.py` review tab
4. Add column mapping in `utils/export_generator.py`

### Modifying Yardi Export Format
To customize the Yardi Excel format:

1. Edit column mappings in `generate_yardi_excel()` function
2. Adjust column widths and formatting as needed
3. Update field names to match your Yardi configuration

## Security & Privacy

- **No Persistent Storage**: Uploaded PDFs are stored temporarily and can be deleted after processing
- **API Security**: OpenAI API key is stored in environment variables
- **Session-Based**: Data is stored in session state and cleared when browser is closed
- **No Logging**: Sensitive tenant information is not logged

## Performance

- **Processing Time**: ~5-15 seconds per document (depends on document length)
- **Batch Processing**: Multiple documents processed sequentially
- **API Costs**: Uses GPT-4.1-mini for cost-effective extraction (~$0.01-0.03 per document)

## Future Enhancements

Potential improvements for future versions:

1. **OCR Integration**: Full support for scanned documents
2. **Direct Yardi API**: Upload data directly to Yardi via API
3. **Template System**: Custom templates for different lease types
4. **Analytics Dashboard**: Track extraction accuracy and processing metrics
5. **Multi-language Support**: Support for non-English lease documents
6. **Bulk Queue**: Advanced queue management for large batches
7. **Field Mapping Config**: User-configurable field mappings
8. **Historical Tracking**: Database for tracking processed leases

## Support

For issues, questions, or feature requests, please refer to the architecture and design documents included with this tool.

## License

This tool is provided as-is for internal use in property management operations.

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Developed for**: Yardi Property Management Integration
