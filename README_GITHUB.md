# 🏢 Lease Abstraction Tool for Yardi

AI-powered lease document abstraction tool that automates data extraction from PDF lease agreements and generates Yardi-compatible exports.

## 🌟 Features

- **AI-Powered Extraction**: Uses OpenAI GPT to intelligently extract lease data
- **Source Citations**: Shows exactly where each piece of data was found in the lease
- **Dual Export System**:
  - Yardi Import Excel (ready for automatic import)
  - Reference Document (formatted for manual review)
- **Smart Late Fee Handling**: Supports both percentage-based and flat amount late fees
- **Batch Processing**: Process multiple leases at once
- **Interactive Review**: Edit and validate extracted data before export

## 🚀 Live Demo

**Deployed Application**: [Your Streamlit Cloud URL will go here]

## 📋 What It Extracts

### Tenant Information
- Tenant name, email, phone

### Property Information
- Property address, unit number, type, square footage

### Lease Terms
- Lease number, start/end dates, term length, lease type

### Financial Terms
- Monthly rent, security deposit, pet deposit
- Payment due date
- Late fees (percentage or flat amount)
- Late fee grace period

### Additional Terms
- Parking spaces, pet policies
- Utilities, renewal options
- Early termination clauses
- Maintenance responsibilities

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4.1-mini
- **PDF Processing**: pdfplumber, pytesseract
- **Data Export**: pandas, openpyxl
- **Python**: 3.11+

## 📦 Installation (Local Development)

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/lease-abstraction-tool.git
cd lease-abstraction-tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install system dependencies** (for PDF processing)
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils tesseract-ocr

# macOS
brew install poppler tesseract
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open in browser**
```
http://localhost:8501
```

## ☁️ Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Push this code to your GitHub repository
2. Make sure `.gitignore` is properly configured (already included)

### Step 2: Set Up Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`

### Step 3: Configure Secrets

In Streamlit Cloud dashboard:
1. Go to your app settings
2. Click "Secrets"
3. Add your OpenAI API key:
```toml
OPENAI_API_KEY = "your-actual-api-key-here"
```

### Step 4: Deploy

Click "Deploy" and wait for the app to start!

## 🔑 API Key Setup

### Get an OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again!)

### Add to Streamlit Cloud

1. In your Streamlit Cloud app dashboard
2. Go to Settings → Secrets
3. Add:
```toml
OPENAI_API_KEY = "sk-..."
```

## 💰 Cost Estimation

**OpenAI API Usage:**
- ~$0.01-0.03 per lease document
- Based on GPT-4.1-mini pricing
- Typical 10-page lease costs about $0.02

**Example Monthly Costs:**
- 50 leases/month: ~$1-1.50
- 200 leases/month: ~$4-6
- 500 leases/month: ~$10-15

**Streamlit Cloud:**
- Free tier: Unlimited for public apps
- Private apps: $20/month per app

## 📖 Usage Guide

### Step 1: Upload Lease Documents
- Drag and drop PDF files or click "Browse files"
- Supports multiple files for batch processing
- Maximum 200MB per file

### Step 2: Process Documents
- Click "Process Documents" button
- AI extracts data from each lease
- Progress bar shows processing status

### Step 3: Review & Edit
- Review extracted data in organized sections
- Each field shows source citation from the lease
- Edit any fields that need correction
- Verify dates carefully (warning banner provided)

### Step 4: Generate Exports
- **Yardi Import Excel**: Ready for automatic import into Yardi
- **Reference Document**: Formatted spreadsheet for manual review
- Download both files for your records

## 🔒 Security & Privacy

- **No Persistent Storage**: Lease documents are processed in memory
- **Session-Based**: Each user has isolated data
- **Temporary Files**: Automatically cleaned up after processing
- **API Key Security**: Stored securely in Streamlit secrets
- **No Logging**: Sensitive lease data is not logged

## 🤝 Contributing

This is a private tool for property management. For issues or feature requests, please contact the repository owner.

## 📄 License

Proprietary - All rights reserved

## 🆘 Support

For questions or issues:
1. Check the USER_GUIDE.md for detailed instructions
2. Review INSTALLATION.md for setup help
3. Contact the repository administrator

## 📚 Documentation

- **USER_GUIDE.md**: Comprehensive user guide
- **INSTALLATION.md**: Detailed installation instructions
- **PROJECT_SUMMARY.md**: Technical overview
- **IMPROVEMENTS_V2.2.md**: Latest features and changes

## 🔄 Version History

### Version 2.2 (Current)
- Enhanced late fee handling (percentage vs. flat amount)
- Removed emergency contact fields (not in leases)
- Improved source citations
- Better AI extraction accuracy

### Version 2.1
- Fixed source citation display issues
- Enhanced AI prompts for better accuracy

### Version 2.0
- Added source citations for all fields
- Improved date extraction
- Enhanced UI with field verification

### Version 1.0
- Initial release
- Basic lease extraction
- Yardi export generation

## 🎯 Roadmap

- [ ] Support for scanned/image-based PDFs (OCR)
- [ ] Multi-language support
- [ ] Custom field mapping for different Yardi configurations
- [ ] Lease comparison tool
- [ ] Historical data analytics
- [ ] Email integration for automatic processing

## 💡 Tips for Best Results

1. **Use clear, text-based PDFs** for best extraction accuracy
2. **Review dates carefully** - they're the most critical fields
3. **Check source citations** to verify AI accuracy
4. **Process similar leases in batches** for efficiency
5. **Keep your OpenAI API key secure** - never share it

## 🏗️ Architecture

```
lease_abstraction_tool/
├── app.py                      # Main Streamlit application
├── utils/
│   ├── pdf_processor.py        # PDF text extraction
│   ├── ai_extractor.py         # OpenAI-powered data extraction
│   ├── export_generator.py     # Excel/document generation
│   └── __init__.py
├── uploads/                    # Temporary PDF storage
├── exports/                    # Generated export files
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # API key template
├── requirements.txt           # Python dependencies
├── packages.txt              # System dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🧪 Testing

To test the extraction with a sample lease:

```bash
python test_extraction.py
```

(Note: test_extraction.py is not included in the repository for security reasons)

## 📞 Contact

For access to this tool or questions about implementation, please contact your property management team administrator.

---

**Built with ❤️ for efficient property management**
