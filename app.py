import streamlit as st
import os
from datetime import datetime
import json
from utils.pdf_processor import extract_text_from_pdf
from utils.ai_extractor import extract_lease_data
from utils.export_generator import generate_yardi_excel, generate_reference_document

# Page configuration
st.set_page_config(
    page_title="Lease Abstraction Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = {}
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .source-citation {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-left: 3px solid #1f77b4;
        margin-top: 0.3rem;
        margin-bottom: 0.8rem;
        font-size: 0.85rem;
        font-style: italic;
        color: #495057;
        border-radius: 3px;
    }
    .source-label {
        font-weight: bold;
        color: #1f77b4;
        font-size: 0.75rem;
        margin-bottom: 0.2rem;
    }
    .confidence-high {
        background-color: #d4edda;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .confidence-medium {
        background-color: #fff3cd;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .confidence-low {
        background-color: #f8d7da;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .field-container {
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

def show_field_with_source(label, value, source, help_text=None):
    """Display a field with its source citation"""
    st.markdown(f'<div class="source-label">📍 Source from lease:</div>', unsafe_allow_html=True)
    if source and source != "Not found in document":
        st.markdown(f'<div class="source-citation">"{source}"</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="source-citation" style="color: #dc3545;">⚠️ Not found in document - please verify</div>', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">🏢 Lease Abstraction Tool for Yardi</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>Welcome!</strong> This tool automates lease document abstraction for Yardi property management system.
        Upload your lease PDFs, review extracted data with source citations, and generate Yardi-compatible exports.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        **Step 1:** Upload lease PDF(s)
        
        **Step 2:** Click 'Process Documents'
        
        **Step 3:** Review & edit extracted data
        - Each field shows where it was found
        - Verify accuracy against source text
        
        **Step 4:** Generate exports
        - Yardi Import Excel
        - Reference Document
        """)
        
        st.divider()
        
        st.header("ℹ️ About")
        st.markdown("""
        This tool uses AI to extract key information from lease documents including:
        - Tenant information
        - Property details
        - Lease terms & dates
        - Financial terms
        - Additional clauses
        
        **NEW:** Each field now shows the exact text from the lease where it was found!
        """)
        
        if st.button("🔄 Reset Application"):
            st.session_state.clear()
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "✏️ Review & Edit", "📊 Export"])
    
    with tab1:
        upload_and_process_tab()
    
    with tab2:
        review_and_edit_tab()
    
    with tab3:
        export_tab()

def upload_and_process_tab():
    st.markdown('<div class="sub-header">Upload Lease Documents</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more lease PDF documents"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        
        # Display uploaded files
        with st.expander("📁 Uploaded Files", expanded=True):
            for idx, file in enumerate(uploaded_files, 1):
                st.write(f"{idx}. {file.name} ({file.size / 1024:.2f} KB)")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🚀 Process Documents", type="primary", use_container_width=True):
                process_documents(uploaded_files)
        
        with col2:
            if st.session_state.processing_complete:
                st.success("✅ Processing complete! Go to 'Review & Edit' tab")

def process_documents(uploaded_files):
    """Process uploaded PDF documents and extract lease data"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_extracted_data = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        # Update progress
        progress = (idx + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"Processing {uploaded_file.name}...")
        
        try:
            # Save uploaded file temporarily
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract text from PDF
            status_text.text(f"Extracting text from {uploaded_file.name}...")
            extracted_text = extract_text_from_pdf(file_path)
            
            if not extracted_text or len(extracted_text.strip()) < 100:
                st.warning(f"⚠️ Could not extract sufficient text from {uploaded_file.name}. The document may be scanned or image-based.")
                continue
            
            # Extract lease data using AI
            status_text.text(f"Analyzing lease data from {uploaded_file.name}...")
            lease_data = extract_lease_data(extracted_text, uploaded_file.name)
            
            if lease_data:
                all_extracted_data.append({
                    'filename': uploaded_file.name,
                    'data': lease_data,
                    'extracted_at': datetime.now().isoformat()
                })
                st.success(f"✅ Successfully processed {uploaded_file.name}")
            else:
                st.error(f"❌ Failed to extract data from {uploaded_file.name}")
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            continue
    
    # Store extracted data in session state
    if all_extracted_data:
        st.session_state.extracted_data = all_extracted_data
        st.session_state.processing_complete = True
        st.session_state.uploaded_files = uploaded_files
        
        progress_bar.progress(1.0)
        status_text.text("✅ All documents processed successfully!")
    else:
        st.error("❌ No data could be extracted from the uploaded documents.")

def review_and_edit_tab():
    st.markdown('<div class="sub-header">Review & Edit Extracted Data</div>', unsafe_allow_html=True)
    
    if not st.session_state.extracted_data:
        st.info("👈 Please upload and process documents first in the 'Upload & Process' tab")
        return
    
    # Select document to review
    doc_names = [doc['filename'] for doc in st.session_state.extracted_data]
    selected_doc = st.selectbox("Select document to review:", doc_names)
    
    # Find selected document data
    doc_data = next((doc for doc in st.session_state.extracted_data if doc['filename'] == selected_doc), None)
    
    if not doc_data:
        st.error("Document data not found")
        return
    
    lease_data = doc_data['data']
    
    st.info(f"📅 Extracted on: {doc_data['extracted_at']}")
    
    # Create editable form
    with st.form(key=f"edit_form_{selected_doc}"):
        st.markdown("### 👤 Tenant Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            tenant_name = st.text_input("Tenant Name", value=lease_data.get('tenant_name', ''))
            show_field_with_source("Tenant Name", lease_data.get('tenant_name', ''), lease_data.get('tenant_name_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            tenant_email = st.text_input("Tenant Email", value=lease_data.get('tenant_email', ''))
            show_field_with_source("Tenant Email", lease_data.get('tenant_email', ''), lease_data.get('tenant_email_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            tenant_phone = st.text_input("Tenant Phone", value=lease_data.get('tenant_phone', ''))
            show_field_with_source("Tenant Phone", lease_data.get('tenant_phone', ''), lease_data.get('tenant_phone_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.info("ℹ️ **Note**: Emergency contact information is typically provided in the welcome letter, not in the lease document.")
        
        st.markdown("### 🏠 Property Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            property_address = st.text_input("Property Address", value=lease_data.get('property_address', ''))
            show_field_with_source("Property Address", lease_data.get('property_address', ''), lease_data.get('property_address_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            unit_number = st.text_input("Unit Number", value=lease_data.get('unit_number', ''))
            show_field_with_source("Unit Number", lease_data.get('unit_number', ''), lease_data.get('unit_number_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            property_type = st.text_input("Property Type", value=lease_data.get('property_type', ''))
            show_field_with_source("Property Type", lease_data.get('property_type', ''), lease_data.get('property_type_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            square_footage = st.number_input("Square Footage", value=float(lease_data.get('square_footage', 0)), min_value=0.0)
            show_field_with_source("Square Footage", lease_data.get('square_footage', ''), lease_data.get('square_footage_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 📅 Lease Terms")
        st.info("⚠️ **Important**: Verify dates carefully against the source text shown below each field")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            lease_number = st.text_input("Lease Number", value=lease_data.get('lease_number', ''))
            show_field_with_source("Lease Number", lease_data.get('lease_number', ''), lease_data.get('lease_number_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            # Parse date if it exists
            start_date_value = None
            if lease_data.get('lease_start_date'):
                try:
                    from datetime import datetime as dt
                    start_date_value = dt.strptime(lease_data.get('lease_start_date'), '%Y-%m-%d').date()
                except:
                    pass
            lease_start_date = st.date_input("Lease Start Date", value=start_date_value)
            show_field_with_source("Lease Start Date", lease_data.get('lease_start_date', ''), lease_data.get('lease_start_date_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            # Parse date if it exists
            end_date_value = None
            if lease_data.get('lease_end_date'):
                try:
                    from datetime import datetime as dt
                    end_date_value = dt.strptime(lease_data.get('lease_end_date'), '%Y-%m-%d').date()
                except:
                    pass
            lease_end_date = st.date_input("Lease End Date", value=end_date_value)
            show_field_with_source("Lease End Date", lease_data.get('lease_end_date', ''), lease_data.get('lease_end_date_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            lease_term_months = st.number_input("Lease Term (months)", value=int(lease_data.get('lease_term_months', 0)), min_value=0)
            show_field_with_source("Lease Term", lease_data.get('lease_term_months', ''), lease_data.get('lease_term_months_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            lease_type = st.selectbox("Lease Type", ["Fixed Term", "Month-to-Month", "Other"], 
                                     index=0 if lease_data.get('lease_type', '').lower() == 'fixed term' else 1)
            show_field_with_source("Lease Type", lease_data.get('lease_type', ''), lease_data.get('lease_type_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 💰 Financial Terms")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            monthly_rent = st.number_input("Monthly Rent ($)", value=float(lease_data.get('monthly_rent', 0)), min_value=0.0, step=50.0)
            show_field_with_source("Monthly Rent", lease_data.get('monthly_rent', ''), lease_data.get('monthly_rent_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            security_deposit = st.number_input("Security Deposit ($)", value=float(lease_data.get('security_deposit', 0)), min_value=0.0, step=50.0)
            show_field_with_source("Security Deposit", lease_data.get('security_deposit', ''), lease_data.get('security_deposit_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            pet_deposit = st.number_input("Pet Deposit ($)", value=float(lease_data.get('pet_deposit', 0)), min_value=0.0, step=50.0)
            show_field_with_source("Pet Deposit", lease_data.get('pet_deposit', ''), lease_data.get('pet_deposit_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            payment_due_date = st.number_input("Payment Due Date (day of month)", value=int(lease_data.get('payment_due_date', 1)), min_value=1, max_value=31)
            show_field_with_source("Payment Due Date", lease_data.get('payment_due_date', ''), lease_data.get('payment_due_date_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            late_fee_type = st.selectbox("Late Fee Type", ["percentage", "flat_amount", "none"], 
                                        index=0 if lease_data.get('late_fee_type', '').lower() == 'percentage' else (1 if lease_data.get('late_fee_type', '').lower() == 'flat_amount' else 2))
            show_field_with_source("Late Fee Type", lease_data.get('late_fee_type', ''), lease_data.get('late_fee_type_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            if late_fee_type == "percentage":
                st.markdown('<div class="field-container">', unsafe_allow_html=True)
                late_fee_percentage = st.number_input("Late Fee Percentage (%)", value=float(lease_data.get('late_fee_percentage', 0)), min_value=0.0, max_value=100.0, step=1.0)
                show_field_with_source("Late Fee %", lease_data.get('late_fee_percentage', ''), lease_data.get('late_fee_percentage_source', ''))
                st.markdown('</div>', unsafe_allow_html=True)
                late_fee_flat_amount = 0
            elif late_fee_type == "flat_amount":
                st.markdown('<div class="field-container">', unsafe_allow_html=True)
                late_fee_flat_amount = st.number_input("Late Fee Amount ($)", value=float(lease_data.get('late_fee_flat_amount', 0)), min_value=0.0, step=10.0)
                show_field_with_source("Late Fee $", lease_data.get('late_fee_flat_amount', ''), lease_data.get('late_fee_flat_amount_source', ''))
                st.markdown('</div>', unsafe_allow_html=True)
                late_fee_percentage = 0
            else:
                late_fee_percentage = 0
                late_fee_flat_amount = 0
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            late_fee_grace_period = st.number_input("Late Fee Grace Period (days)", value=int(lease_data.get('late_fee_grace_period', 0)), min_value=0)
            show_field_with_source("Grace Period", lease_data.get('late_fee_grace_period', ''), lease_data.get('late_fee_grace_period_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 📝 Additional Terms")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            parking_spaces = st.number_input("Parking Spaces", value=int(lease_data.get('parking_spaces', 0)), min_value=0)
            show_field_with_source("Parking", lease_data.get('parking_spaces', ''), lease_data.get('parking_spaces_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            pet_allowed = st.checkbox("Pet Allowed", value=lease_data.get('pet_allowed', False))
            show_field_with_source("Pet Policy", lease_data.get('pet_allowed', ''), lease_data.get('pet_allowed_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            pet_type = st.text_input("Pet Type", value=lease_data.get('pet_type', ''))
            show_field_with_source("Pet Type", lease_data.get('pet_type', ''), lease_data.get('pet_type_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            utilities_included = st.text_area("Utilities Included", value=lease_data.get('utilities_included', ''), height=100)
            show_field_with_source("Utilities", lease_data.get('utilities_included', ''), lease_data.get('utilities_included_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="field-container">', unsafe_allow_html=True)
            renewal_options = st.text_area("Renewal Options", value=lease_data.get('renewal_options', ''), height=100)
            show_field_with_source("Renewal", lease_data.get('renewal_options', ''), lease_data.get('renewal_options_source', ''))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
        
        if submitted:
            # Update the data in session state
            updated_data = {
                'tenant_name': tenant_name,
                'tenant_name_source': lease_data.get('tenant_name_source', ''),
                'tenant_email': tenant_email,
                'tenant_email_source': lease_data.get('tenant_email_source', ''),
                'tenant_phone': tenant_phone,
                'tenant_phone_source': lease_data.get('tenant_phone_source', ''),
                'property_address': property_address,
                'property_address_source': lease_data.get('property_address_source', ''),
                'unit_number': unit_number,
                'unit_number_source': lease_data.get('unit_number_source', ''),
                'property_type': property_type,
                'property_type_source': lease_data.get('property_type_source', ''),
                'square_footage': square_footage,
                'square_footage_source': lease_data.get('square_footage_source', ''),
                'lease_number': lease_number,
                'lease_number_source': lease_data.get('lease_number_source', ''),
                'lease_start_date': str(lease_start_date) if lease_start_date else '',
                'lease_start_date_source': lease_data.get('lease_start_date_source', ''),
                'lease_end_date': str(lease_end_date) if lease_end_date else '',
                'lease_end_date_source': lease_data.get('lease_end_date_source', ''),
                'lease_term_months': lease_term_months,
                'lease_term_months_source': lease_data.get('lease_term_months_source', ''),
                'lease_type': lease_type,
                'lease_type_source': lease_data.get('lease_type_source', ''),
                'monthly_rent': monthly_rent,
                'monthly_rent_source': lease_data.get('monthly_rent_source', ''),
                'security_deposit': security_deposit,
                'security_deposit_source': lease_data.get('security_deposit_source', ''),
                'pet_deposit': pet_deposit,
                'pet_deposit_source': lease_data.get('pet_deposit_source', ''),
                'payment_due_date': payment_due_date,
                'payment_due_date_source': lease_data.get('payment_due_date_source', ''),
                'late_fee_type': late_fee_type,
                'late_fee_type_source': lease_data.get('late_fee_type_source', ''),
                'late_fee_percentage': late_fee_percentage,
                'late_fee_percentage_source': lease_data.get('late_fee_percentage_source', ''),
                'late_fee_flat_amount': late_fee_flat_amount,
                'late_fee_flat_amount_source': lease_data.get('late_fee_flat_amount_source', ''),
                'late_fee_grace_period': late_fee_grace_period,
                'late_fee_grace_period_source': lease_data.get('late_fee_grace_period_source', ''),
                'parking_spaces': parking_spaces,
                'parking_spaces_source': lease_data.get('parking_spaces_source', ''),
                'pet_allowed': pet_allowed,
                'pet_allowed_source': lease_data.get('pet_allowed_source', ''),
                'pet_type': pet_type,
                'pet_type_source': lease_data.get('pet_type_source', ''),
                'utilities_included': utilities_included,
                'utilities_included_source': lease_data.get('utilities_included_source', ''),
                'renewal_options': renewal_options,
                'renewal_options_source': lease_data.get('renewal_options_source', ''),
                'confidence_score': lease_data.get('confidence_score', 0.5)
            }
            
            # Update in session state
            for doc in st.session_state.extracted_data:
                if doc['filename'] == selected_doc:
                    doc['data'] = updated_data
                    break
            
            st.success("✅ Changes saved successfully!")
            st.rerun()

def export_tab():
    st.markdown('<div class="sub-header">Generate Exports</div>', unsafe_allow_html=True)
    
    if not st.session_state.extracted_data:
        st.info("👈 Please upload and process documents first")
        return
    
    st.markdown("""
    Generate two types of exports:
    1. **Yardi Import Excel** - Formatted for automatic import into Yardi
    2. **Reference Document** - Comprehensive structured view for manual data entry
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Yardi Import Excel")
        st.markdown("Excel file formatted with Yardi-compatible columns for automatic import")
        
        if st.button("📥 Generate Yardi Excel", type="primary", use_container_width=True):
            try:
                excel_path = generate_yardi_excel(st.session_state.extracted_data)
                
                with open(excel_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Yardi Import Excel",
                        data=f,
                        file_name=f"yardi_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                st.success("✅ Yardi Excel generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating Excel: {str(e)}")
    
    with col2:
        st.markdown("### 📄 Reference Document")
        st.markdown("Detailed structured document with all extracted data for manual review")
        
        if st.button("📥 Generate Reference Document", type="primary", use_container_width=True):
            try:
                ref_path = generate_reference_document(st.session_state.extracted_data)
                
                with open(ref_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Reference Document",
                        data=f,
                        file_name=f"lease_reference_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                st.success("✅ Reference document generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating reference document: {str(e)}")
    
    st.divider()
    
    # Preview extracted data
    with st.expander("👁️ Preview Extracted Data", expanded=False):
        for doc in st.session_state.extracted_data:
            st.markdown(f"**{doc['filename']}**")
            st.json(doc['data'])

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("exports", exist_ok=True)
    
    main()
