"""
Legal Patterns Library
Common patterns and utilities for legal document processing
"""

import re
from typing import Dict, List, Pattern, Tuple

# Court abbreviations mapping
COURT_ABBREVIATIONS = {
    # Federal Courts
    "S. Ct.": "Supreme Court",
    "U.S.": "United States Supreme Court",
    
    # Circuit Courts
    "1st Cir.": "First Circuit",
    "2d Cir.": "Second Circuit",
    "3d Cir.": "Third Circuit",
    "4th Cir.": "Fourth Circuit",
    "5th Cir.": "Fifth Circuit",
    "6th Cir.": "Sixth Circuit",
    "7th Cir.": "Seventh Circuit",
    "8th Cir.": "Eighth Circuit",
    "9th Cir.": "Ninth Circuit",
    "10th Cir.": "Tenth Circuit",
    "11th Cir.": "Eleventh Circuit",
    "D.C. Cir.": "D.C. Circuit",
    "Fed. Cir.": "Federal Circuit",
    
    # District Courts
    "D.": "District",
    "E.D.": "Eastern District",
    "W.D.": "Western District",
    "N.D.": "Northern District",
    "S.D.": "Southern District",
    "C.D.": "Central District",
    "M.D.": "Middle District",
    
    # State Courts
    "Sup. Ct.": "Supreme Court",
    "App.": "Appellate",
    "App. Div.": "Appellate Division",
    "Ct. App.": "Court of Appeals",
    "Super. Ct.": "Superior Court",
}

# Common legal document types
DOCUMENT_TYPES = {
    "contract": ["agreement", "contract", "covenant", "deed", "lease"],
    "motion": ["motion", "petition", "application", "request"],
    "brief": ["brief", "memorandum", "memo"],
    "complaint": ["complaint", "petition", "claim"],
    "order": ["order", "judgment", "decree", "ruling", "decision"],
    "opinion": ["opinion", "decision", "judgment"],
    "statute": ["statute", "act", "code", "law"],
    "regulation": ["regulation", "rule", "cfr", "administrative"],
}

# Legal formatting patterns
class LegalPatterns:
    """Common regex patterns for legal document processing"""
    
    # Paragraph numbering patterns
    PARAGRAPH_NUMBER = re.compile(r'^\s*\[(\d+)\]\s*')
    SECTION_NUMBER = re.compile(r'^\s*§\s*(\d+(?:\.\d+)*)\s*')
    ARTICLE_NUMBER = re.compile(r'^\s*Article\s+([IVXLCDM]+|\d+)\s*', re.IGNORECASE)
    
    # Footnote patterns
    FOOTNOTE_REFERENCE = re.compile(r'(\w+)\s*\^(\d+)')
    FOOTNOTE_TEXT = re.compile(r'^\s*\^(\d+)\s*(.+)')
    
    # Date patterns
    LEGAL_DATE = re.compile(
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December|'
        r'Jan\.?|Feb\.?|Mar\.?|Apr\.?|May\.?|Jun\.?|Jul\.?|Aug\.?|Sep\.?|Sept\.?|Oct\.?|Nov\.?|Dec\.?)\s+'
        r'\d{1,2},?\s+\d{4}\b'
    )
    
    # Page number patterns
    PAGE_NUMBER = re.compile(r'^\s*(?:Page\s+)?(\d+)\s*$', re.IGNORECASE)
    PAGE_RANGE = re.compile(r'\bpp?\.\s*(\d+)(?:\s*-\s*(\d+))?\b')
    
    # Legal entity patterns
    CORPORATION = re.compile(r'\b(?:Inc\.|LLC|L\.L\.C\.|Corp\.|Corporation|Company|Co\.)\b')
    PARTY_NAME = re.compile(r'^([A-Z][A-Za-z\s,\.]+?)\s+v\.\s+([A-Z][A-Za-z\s,\.]+?)(?:\s*,|$)')

def extract_document_type(text: str) -> str:
    """
    Determine the type of legal document based on content
    
    Args:
        text: Document text
        
    Returns:
        Document type (contract, motion, brief, etc.)
    """
    text_lower = text.lower()
    
    for doc_type, keywords in DOCUMENT_TYPES.items():
        for keyword in keywords:
            if keyword in text_lower:
                return doc_type
    
    return "unknown"

def normalize_court_name(court_abbr: str) -> str:
    """
    Expand court abbreviation to full name
    
    Args:
        court_abbr: Court abbreviation (e.g., "9th Cir.")
        
    Returns:
        Full court name
    """
    # Check direct match
    if court_abbr in COURT_ABBREVIATIONS:
        return COURT_ABBREVIATIONS[court_abbr]
    
    # Check components
    parts = []
    for part in court_abbr.split():
        if part in COURT_ABBREVIATIONS:
            parts.append(COURT_ABBREVIATIONS[part])
        else:
            parts.append(part)
    
    return " ".join(parts)

def extract_party_names(case_name: str) -> Tuple[str, str]:
    """
    Extract plaintiff and defendant names from case citation
    
    Args:
        case_name: Case name (e.g., "Smith v. Jones")
        
    Returns:
        Tuple of (plaintiff, defendant)
    """
    match = LegalPatterns.PARTY_NAME.match(case_name)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # Fallback to simple split
    if " v. " in case_name:
        parts = case_name.split(" v. ", 1)
        return parts[0].strip(), parts[1].strip()
    
    return case_name, ""

def format_legal_date(date_str: str) -> str:
    """
    Standardize legal date format
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Standardized date format
    """
    # This is a simple implementation - could be expanded
    return date_str.strip()

def is_legal_entity(text: str) -> bool:
    """
    Check if text contains a legal entity (corporation, LLC, etc.)
    
    Args:
        text: Text to check
        
    Returns:
        True if legal entity found
    """
    return bool(LegalPatterns.CORPORATION.search(text))

def extract_paragraph_numbers(text: str) -> List[int]:
    """
    Extract all paragraph numbers from text
    
    Args:
        text: Document text
        
    Returns:
        List of paragraph numbers
    """
    numbers = []
    for line in text.split('\n'):
        match = LegalPatterns.PARAGRAPH_NUMBER.match(line)
        if match:
            numbers.append(int(match.group(1)))
    return numbers

def clean_legal_text(text: str) -> str:
    """
    Clean and normalize legal text
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common OCR errors in legal text
    replacements = {
        r'\bl\b': '1',  # Common OCR error: l -> 1
        r'\bO\b': '0',  # Common OCR error: O -> 0
        r'§§': '§',     # Double section symbols
        r'\s+\.': '.',  # Space before period
        r'\s+,': ',',   # Space before comma
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    
    return text.strip()

# Export all public items
__all__ = [
    'COURT_ABBREVIATIONS',
    'DOCUMENT_TYPES',
    'LegalPatterns',
    'extract_document_type',
    'normalize_court_name',
    'extract_party_names',
    'format_legal_date',
    'is_legal_entity',
    'extract_paragraph_numbers',
    'clean_legal_text',
]