# Lease Abstraction Tool - User Guide

## Quick Start Guide

This guide will help you get started with the Lease Abstraction Tool for Yardi in just a few minutes.

## What This Tool Does

The Lease Abstraction Tool automates the tedious process of manually entering lease data into Yardi. It:

1. **Reads** your lease PDF documents
2. **Extracts** key information using AI
3. **Generates** two types of exports:
   - Excel file for automatic Yardi import
   - Reference document for manual data entry

## Before You Begin

### What You Need
- Lease agreements in PDF format (digital PDFs work best)
- A web browser (Chrome, Firefox, Safari, or Edge)
- Internet connection

### What to Prepare
- Gather all lease PDFs you want to process
- Ensure PDFs are readable (not password-protected or corrupted)
- Have access to original documents for verification

## Step-by-Step Instructions

### Step 1: Launch the Application

1. Open your terminal or command prompt
2. Navigate to the tool directory:
   ```bash
   cd lease_abstraction_tool
   ```
3. Start the application:
   ```bash
   streamlit run app.py
   ```
4. Your web browser will automatically open to the application

### Step 2: Upload Your Lease Documents

1. You'll see three tabs at the top: **Upload & Process**, **Review & Edit**, and **Export**
2. Make sure you're on the **Upload & Process** tab
3. Click the **"Browse files"** button
4. Select one or more lease PDF files from your computer
5. You'll see a list of uploaded files with their sizes

**Tips:**
- You can upload multiple files at once
- Supported format: PDF only
- Recommended: Start with 1-3 documents to test

### Step 3: Process the Documents

1. Click the **"🚀 Process Documents"** button
2. Watch the progress bar as the tool:
   - Extracts text from each PDF
   - Analyzes the content with AI
   - Structures the data
3. You'll see success messages for each processed document
4. Processing typically takes 5-15 seconds per document

**What to Watch For:**
- ✅ Green success messages = document processed successfully
- ⚠️ Yellow warnings = partial extraction (review carefully)
- ❌ Red errors = processing failed (check document quality)

### Step 4: Review and Edit Extracted Data

1. Click the **"Review & Edit"** tab
2. Use the dropdown menu to select a document to review
3. You'll see all extracted information organized in sections:
   - 👤 Tenant Information
   - 🏠 Property Information
   - 📅 Lease Terms
   - 💰 Financial Terms
   - 📝 Additional Terms

4. **Review each field carefully:**
   - Check for accuracy against the original lease
   - Look for missing information
   - Verify dates are correct
   - Confirm financial amounts

5. **Edit any incorrect fields:**
   - Click in any field to edit
   - Type the correct information
   - Use proper formats (dates, currency, etc.)

6. Click **"💾 Save Changes"** when done

**Important Fields to Verify:**
- ✓ Tenant name (must be exact legal name)
- ✓ Lease start and end dates
- ✓ Monthly rent amount
- ✓ Property address and unit number
- ✓ Security deposit amount

### Step 5: Generate Exports

1. Click the **"Export"** tab
2. You'll see two export options:

#### Option A: Yardi Import Excel
- Click **"📥 Generate Yardi Excel"**
- Click **"⬇️ Download Yardi Import Excel"**
- This file is formatted for automatic import into Yardi
- Use this for bulk tenant setup in Yardi

#### Option B: Reference Document
- Click **"📥 Generate Reference Document"**
- Click **"⬇️ Download Reference Document"**
- This file contains all extracted data in a readable format
- Use this as a reference when manually entering data into Yardi

**Both exports include:**
- All tenant and property information
- Complete lease terms and financial details
- Additional clauses and special terms
- Source filename for reference

### Step 6: Import into Yardi

#### For Automatic Import (Yardi Excel):
1. Open Yardi Voyager
2. Navigate to: **Admin > Toolbox > Import/Export > Import Trans CSV**
3. Select the downloaded Yardi Import Excel file
4. Follow Yardi's import wizard
5. Verify the imported data in Yardi

#### For Manual Entry (Reference Document):
1. Open the Reference Document in Excel
2. Open Yardi and navigate to tenant setup
3. Use the document as a guide to enter each field
4. Check off each section as you complete it

## Understanding Confidence Scores

The tool assigns confidence scores to extractions:

- **🟢 High (80-100%)**: Very confident - data likely accurate
- **🟡 Medium (50-79%)**: Moderately confident - review recommended
- **🔴 Low (0-49%)**: Low confidence - verify carefully

**What to do:**
- High confidence: Quick review usually sufficient
- Medium confidence: Compare with original document
- Low confidence: Carefully verify all fields

## Common Scenarios

### Scenario 1: Processing a Single Lease
**Best for:** Individual tenant onboarding

1. Upload one PDF
2. Process and review
3. Generate both exports
4. Import into Yardi or enter manually

**Time estimate:** 3-5 minutes

### Scenario 2: Bulk Processing Multiple Leases
**Best for:** New property acquisition, lease renewals

1. Upload 10-20 PDFs at once
2. Process all documents
3. Review each one systematically
4. Generate exports
5. Use Yardi Import Excel for bulk upload

**Time estimate:** 5-10 minutes per document

### Scenario 3: Lease Renewal
**Best for:** Existing tenant lease updates

1. Upload new lease PDF
2. Process and review
3. Pay special attention to:
   - New lease dates
   - Updated rent amount
   - Any changed terms
4. Generate exports and update Yardi

**Time estimate:** 3-5 minutes

## Troubleshooting Common Issues

### Issue: "Could not extract sufficient text"

**Cause:** PDF is scanned or image-based

**Solutions:**
1. Check if PDF is searchable (try selecting text)
2. If scanned, consider re-scanning at higher quality
3. Use OCR software to convert to text-based PDF
4. As last resort, manually enter data

### Issue: Many fields are empty

**Cause:** Lease format is non-standard or information is missing

**Solutions:**
1. Check the original PDF for the missing information
2. Manually fill in the fields in Review & Edit tab
3. Some fields may genuinely not be in the lease
4. Leave optional fields empty if not applicable

### Issue: Dates are incorrect

**Cause:** Date format confusion or OCR errors

**Solutions:**
1. Always verify dates against original document
2. Use the date picker in Review & Edit tab
3. Ensure dates are in YYYY-MM-DD format
4. Check for transposed numbers (e.g., 03/05 vs 05/03)

### Issue: Financial amounts are wrong

**Cause:** Number extraction errors or formatting issues

**Solutions:**
1. Verify all dollar amounts carefully
2. Check for decimal point errors
3. Ensure no extra zeros or missing digits
4. Compare with original lease document

## Best Practices

### Before Processing
✓ Ensure PDFs are high quality and readable  
✓ Check that documents are complete (all pages)  
✓ Remove any password protection  
✓ Have original documents ready for verification

### During Review
✓ Review every field, even if confidence is high  
✓ Pay extra attention to financial terms  
✓ Verify dates are in correct format  
✓ Check tenant names match legal documents  
✓ Confirm property addresses are complete

### After Export
✓ Keep original PDFs as backup  
✓ Save exported files with clear naming  
✓ Verify data in Yardi after import  
✓ Document any manual corrections needed

## Tips for Efficiency

1. **Batch Similar Leases**: Process leases from the same property together
2. **Use Consistent Naming**: Name your PDFs clearly (e.g., "Unit3B_Johnson_2026.pdf")
3. **Review Immediately**: Review and edit right after processing while details are fresh
4. **Create Checklist**: Use a checklist of required fields to verify
5. **Save Regularly**: Save changes frequently when editing multiple documents

## Data Security

- Uploaded files are stored temporarily only
- No data is permanently saved on the server
- Session data clears when you close the browser
- API communications are encrypted
- Original PDFs remain on your computer

## Getting Help

If you encounter issues:

1. **Check this guide** for troubleshooting steps
2. **Review the README** for technical details
3. **Check error messages** for specific guidance
4. **Verify document quality** if extraction fails
5. **Try with a different document** to isolate issues

## Keyboard Shortcuts

- **Tab**: Move to next field in forms
- **Shift + Tab**: Move to previous field
- **Ctrl/Cmd + S**: Save changes (in some browsers)
- **Ctrl/Cmd + R**: Refresh application

## Frequently Asked Questions

**Q: Can I process scanned documents?**  
A: Basic scanned documents may work, but text-based PDFs give best results. High-quality scans are recommended.

**Q: How many documents can I process at once?**  
A: You can upload multiple documents. For best performance, process 10-20 at a time.

**Q: What if a field isn't in my lease?**  
A: Leave it empty or enter "N/A". Not all leases have all fields.

**Q: Can I save my work and come back later?**  
A: Data is stored in your browser session. Complete processing in one session or export data before closing.

**Q: Is my data secure?**  
A: Yes. Data is processed securely and not permanently stored. Close your browser to clear all data.

**Q: Can I customize the Yardi export format?**  
A: Yes, but it requires technical modifications. See README for customization instructions.

**Q: What if the AI extracts wrong information?**  
A: Always review and correct in the Review & Edit tab before exporting. The tool is designed for review, not blind trust.

## Next Steps

After mastering the basics:

1. Process a test batch of leases
2. Verify accuracy of exports in Yardi
3. Develop your own workflow and checklist
4. Train team members on the tool
5. Provide feedback for improvements

---

**Remember**: This tool is designed to save you time, but always verify critical information before importing into Yardi. When in doubt, double-check against the original lease document.

**Happy Processing!** 🏢📄✨
