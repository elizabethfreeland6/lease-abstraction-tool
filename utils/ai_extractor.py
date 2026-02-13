"""
AI-Powered Lease Data Extraction Module
Uses OpenAI GPT to extract structured data from lease documents
"""

import json
import os
from openai import OpenAI
from typing import Dict, Optional

# Initialize OpenAI client (API key is pre-configured in environment)
client = OpenAI()

EXTRACTION_PROMPT_TEMPLATE = """You are a professional lease document abstraction specialist with expertise in property management and Yardi systems.

Your task is to extract key information from the following lease agreement text and return it as a structured JSON object. For EACH field, you must also provide the exact text snippet from the document where you found that information.

CRITICAL INSTRUCTIONS:
1. Read the ENTIRE document carefully before extracting
2. For dates, look for explicit date formats (MM/DD/YYYY, Month DD, YYYY, etc.)
3. Pay special attention to sections labeled "Lease Term", "Financial Terms", "Rent", "Dates", etc.
4. Extract the EXACT values as they appear in the document
5. For each field, include a "source" field with the exact text snippet where you found it
6. If you cannot find a field, use null for the value and "Not found in document" for the source

Extract the following fields with their source text:

**Tenant Information:**
- tenant_name: Full legal name of the tenant(s)
- tenant_name_source: Exact text snippet where tenant name was found
- tenant_email: Email address
- tenant_email_source: Exact text snippet where email was found
- tenant_phone: Phone number
- tenant_phone_source: Exact text snippet where phone was found

**Property Information:**
- property_address: Complete property address
- property_address_source: Source text
- unit_number: Unit or apartment number
- unit_number_source: Source text
- property_type: Type of property (apartment, house, condo, etc.)
- property_type_source: Source text
- square_footage: Size in square feet (as number)
- square_footage_source: Source text

**Lease Terms:**
- lease_number: Lease agreement number or ID
- lease_number_source: Source text
- lease_start_date: Start date (format: YYYY-MM-DD) - LOOK CAREFULLY for "Lease Start Date", "Commencement Date", "Start Date", "begins on", etc.
- lease_start_date_source: EXACT text snippet showing the start date
- lease_end_date: End date (format: YYYY-MM-DD) - LOOK CAREFULLY for "Lease End Date", "Termination Date", "End Date", "expires on", etc.
- lease_end_date_source: EXACT text snippet showing the end date
- lease_term_months: Length of lease in months (as number)
- lease_term_months_source: Source text
- lease_type: Type of lease (Fixed Term, Month-to-Month, etc.)
- lease_type_source: Source text

**Financial Terms:**
- monthly_rent: Monthly rent amount (as number, no currency symbols)
- monthly_rent_source: Source text
- security_deposit: Security deposit amount (as number)
- security_deposit_source: Source text
- pet_deposit: Pet deposit amount if applicable (as number)
- pet_deposit_source: Source text
- payment_due_date: Day of month payment is due (as number 1-31)
- payment_due_date_source: Source text
- late_fee_type: Type of late fee ("percentage" or "flat_amount")
- late_fee_type_source: Source text
- late_fee_percentage: Late fee as percentage (e.g., 10 for 10%) if applicable
- late_fee_percentage_source: Source text
- late_fee_flat_amount: Late fee as flat dollar amount if applicable
- late_fee_flat_amount_source: Source text
- late_fee_grace_period: Grace period for late fees in days (as number)
- late_fee_grace_period_source: Source text

**Additional Terms:**
- parking_spaces: Number of parking spaces (as number)
- parking_spaces_source: Source text
- pet_allowed: Whether pets are allowed (true/false)
- pet_allowed_source: Source text
- pet_type: Type/breed of pet if mentioned
- pet_type_source: Source text
- utilities_included: List of utilities included (water, electric, gas, etc.)
- utilities_included_source: Source text
- renewal_options: Any renewal or extension options mentioned
- renewal_options_source: Source text
- early_termination_clause: Early termination terms if any
- early_termination_clause_source: Source text
- maintenance_responsibilities: Who is responsible for what maintenance
- maintenance_responsibilities_source: Source text

**Metadata:**
- confidence_score: Your confidence in the extraction accuracy (0.0 to 1.0)

IMPORTANT RULES:
1. Return ONLY valid JSON, no additional text or explanation
2. ALWAYS include BOTH the value field AND its corresponding _source field
3. For source fields, copy the EXACT text from the document (20-50 words of context)
4. If you find a value, you MUST also find and include its source text
5. ONLY use "Not found in document" if the value is truly null or empty
6. Format all dates as YYYY-MM-DD (convert from any format you find)
7. Format all currency values as numbers without symbols (e.g., 1500.00 not $1,500)
8. Be EXTREMELY precise with dates - look for explicit date statements
9. Look in the beginning sections for lease dates, and financial sections for rent/deposits

EXAMPLES of correct source citations:

Example 1 - Property Address:
"property_address": "5380 Hickory Hollow Pkwy, Antioch, TN 37013",
"property_address_source": "Property Address: 5380 Hickory Hollow Pkwy, Antioch, TN 37013"

Example 2 - Lease Start Date:
"lease_start_date": "2026-03-01",
"lease_start_date_source": "This Lease Agreement shall commence on March 1, 2026 and continue for a period of twelve months."

Example 3 - Monthly Rent:
"monthly_rent": 1500.00,
"monthly_rent_source": "Tenant agrees to pay monthly rent in the amount of $1,500.00 due on the first day of each month."

Example 4 - Square Footage:
"square_footage": 4274,
"square_footage_source": "The property consists of approximately 4,274 square feet of living space."

Example 5 - Late Fee (Percentage):
"late_fee_type": "percentage",
"late_fee_type_source": "Tenant shall pay Landlord a late charge equal to ten percent (10%) of such payment.",
"late_fee_percentage": 10,
"late_fee_percentage_source": "Tenant shall pay Landlord a late charge equal to ten percent (10%) of such payment.",
"late_fee_flat_amount": null,
"late_fee_flat_amount_source": "Not found in document"

Example 6 - Late Fee (Flat Amount):
"late_fee_type": "flat_amount",
"late_fee_type_source": "A late fee of $75.00 will be charged for any payment received after the grace period.",
"late_fee_percentage": null,
"late_fee_percentage_source": "Not found in document",
"late_fee_flat_amount": 75.00,
"late_fee_flat_amount_source": "A late fee of $75.00 will be charged for any payment received after the grace period."

REMEMBER: If you extracted a value, you MUST have found it somewhere - include that source text!

Lease Document Text:
{lease_text}

Return the extracted data as JSON:"""

def extract_lease_data(lease_text: str, filename: str = "") -> Optional[Dict]:
    """
    Extract structured lease data from raw text using AI with source citations
    
    Args:
        lease_text: Raw text extracted from lease PDF
        filename: Name of the source file (for reference)
        
    Returns:
        Dictionary containing extracted lease data with source citations, or None if extraction fails
    """
    try:
        # Prepare the prompt
        prompt = EXTRACTION_PROMPT_TEMPLATE.format(lease_text=lease_text[:20000])  # Increased limit
        
        # Call OpenAI API with better parameters for accuracy
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional lease abstraction specialist. For EVERY field you extract, you MUST include the source text from the document. Extract data accurately with source citations and return only valid JSON. Pay special attention to dates and financial terms. If you found a value, you MUST include where you found it in the corresponding _source field."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.05,  # Even lower temperature for more consistency
            max_tokens=3000  # Increased for source citations
        )
        
        # Extract the response
        response_text = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        # Sometimes the model wraps JSON in markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()
        
        # Parse JSON
        lease_data = json.loads(response_text)
        
        # Add source filename
        lease_data['source_filename'] = filename
        
        # Validate and clean the data
        lease_data = validate_and_clean_data(lease_data)
        
        return lease_data
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {str(e)}")
        print(f"Response text: {response_text}")
        return None
    except Exception as e:
        print(f"Error extracting lease data: {str(e)}")
        return None

def validate_and_clean_data(data: Dict) -> Dict:
    """
    Validate and clean extracted lease data
    
    Args:
        data: Raw extracted data dictionary
        
    Returns:
        Cleaned and validated data dictionary
    """
    # Define default values for required fields
    defaults = {
        'tenant_name': '',
        'tenant_name_source': 'Not found in document',
        'tenant_email': '',
        'tenant_email_source': 'Not found in document',
        'tenant_phone': '',
        'tenant_phone_source': 'Not found in document',
        'emergency_contact_name': '',
        'emergency_contact_name_source': 'Not found in document',
        'emergency_contact_phone': '',
        'emergency_contact_phone_source': 'Not found in document',
        'property_address': '',
        'property_address_source': 'Not found in document',
        'unit_number': '',
        'unit_number_source': 'Not found in document',
        'property_type': '',
        'property_type_source': 'Not found in document',
        'square_footage': 0,
        'square_footage_source': 'Not found in document',
        'lease_number': '',
        'lease_number_source': 'Not found in document',
        'lease_start_date': '',
        'lease_start_date_source': 'Not found in document',
        'lease_end_date': '',
        'lease_end_date_source': 'Not found in document',
        'lease_term_months': 0,
        'lease_term_months_source': 'Not found in document',
        'lease_type': '',
        'lease_type_source': 'Not found in document',
        'monthly_rent': 0,
        'monthly_rent_source': 'Not found in document',
        'security_deposit': 0,
        'security_deposit_source': 'Not found in document',
        'pet_deposit': 0,
        'pet_deposit_source': 'Not found in document',
        'payment_due_date': 1,
        'payment_due_date_source': 'Not found in document',
        'late_fee_amount': 0,
        'late_fee_amount_source': 'Not found in document',
        'late_fee_grace_period': 0,
        'late_fee_grace_period_source': 'Not found in document',
        'parking_spaces': 0,
        'parking_spaces_source': 'Not found in document',
        'pet_allowed': False,
        'pet_allowed_source': 'Not found in document',
        'pet_type': '',
        'pet_type_source': 'Not found in document',
        'utilities_included': '',
        'utilities_included_source': 'Not found in document',
        'renewal_options': '',
        'renewal_options_source': 'Not found in document',
        'early_termination_clause': '',
        'early_termination_clause_source': 'Not found in document',
        'maintenance_responsibilities': '',
        'maintenance_responsibilities_source': 'Not found in document',
        'confidence_score': 0.5
    }
    
    # Merge with defaults
    for key, default_value in defaults.items():
        if key not in data or data[key] is None:
            data[key] = default_value
    
    # Convert numeric fields
    numeric_fields = [
        'square_footage', 'lease_term_months', 'monthly_rent', 
        'security_deposit', 'pet_deposit', 'payment_due_date',
        'late_fee_amount', 'late_fee_grace_period', 'parking_spaces'
    ]
    
    for field in numeric_fields:
        try:
            data[field] = float(data[field]) if data[field] else 0
        except (ValueError, TypeError):
            data[field] = 0
    
    # Convert boolean fields
    if isinstance(data.get('pet_allowed'), str):
        data['pet_allowed'] = data['pet_allowed'].lower() in ['true', 'yes', '1']
    
    # Handle utilities_included - convert list to string if needed
    if isinstance(data.get('utilities_included'), list):
        data['utilities_included'] = ', '.join(data['utilities_included'])
    
    # Ensure confidence score is between 0 and 1
    try:
        confidence = float(data.get('confidence_score', 0.5))
        data['confidence_score'] = max(0.0, min(1.0, confidence))
    except (ValueError, TypeError):
        data['confidence_score'] = 0.5
    
    return data

def extract_batch_lease_data(lease_texts: list, filenames: list = None) -> list:
    """
    Extract lease data from multiple documents
    
    Args:
        lease_texts: List of raw text strings from lease PDFs
        filenames: List of source filenames (optional)
        
    Returns:
        List of dictionaries containing extracted lease data
    """
    if filenames is None:
        filenames = [f"document_{i+1}" for i in range(len(lease_texts))]
    
    results = []
    for text, filename in zip(lease_texts, filenames):
        data = extract_lease_data(text, filename)
        if data:
            results.append(data)
    
    return results

def get_confidence_level(score: float) -> str:
    """
    Convert confidence score to human-readable level
    
    Args:
        score: Confidence score (0.0 to 1.0)
        
    Returns:
        Confidence level string (High, Medium, Low)
    """
    if score >= 0.8:
        return "High"
    elif score >= 0.5:
        return "Medium"
    else:
        return "Low"
