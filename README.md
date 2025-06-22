# Legal Patterns Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Open Legal Tools](https://img.shields.io/badge/Open%20Legal%20Tools-Core-purple)](https://github.com/open-legal-tools)

Shared patterns and utilities for legal document processing across the Open Legal Tools ecosystem.

## Features

- **Court Name Normalization**: Convert abbreviations to full names
- **Document Type Detection**: Identify contracts, motions, briefs, etc.
- **Party Name Extraction**: Extract plaintiff and defendant from case names
- **Legal Entity Recognition**: Identify corporations, LLCs, etc.
- **Common Regex Patterns**: Paragraph numbers, footnotes, dates, page numbers
- **Text Cleaning**: Fix common OCR errors in legal documents

## Installation

```bash
pip install legal-patterns
```

## Quick Start

```python
from legal_patterns import (
    extract_document_type,
    normalize_court_name,
    extract_party_names,
    LegalPatterns
)

# Identify document type
doc_type = extract_document_type("This motion for summary judgment...")
# Returns: "motion"

# Normalize court names
court = normalize_court_name("9th Cir.")
# Returns: "Ninth Circuit"

# Extract party names
plaintiff, defendant = extract_party_names("Smith v. Jones")
# Returns: ("Smith", "Jones")

# Use regex patterns
pattern = LegalPatterns.PARAGRAPH_NUMBER
match = pattern.match("[42] The defendant argues...")
# match.group(1) returns "42"
```

## Available Patterns

### Document Structure
- `PARAGRAPH_NUMBER`: Matches `[n]` style paragraph numbers
- `SECTION_NUMBER`: Matches `§ n.n` style section numbers
- `ARTICLE_NUMBER`: Matches article numbers (Roman or Arabic)

### References
- `FOOTNOTE_REFERENCE`: Matches footnote references like `word^1`
- `FOOTNOTE_TEXT`: Matches footnote text like `^1 See Smith v. Jones`
- `PAGE_RANGE`: Matches page references like `pp. 123-456`

### Entities
- `CORPORATION`: Matches corporate designators (Inc., LLC, Corp.)
- `PARTY_NAME`: Extracts parties from case names

### Temporal
- `LEGAL_DATE`: Matches dates in legal format

## Utility Functions

### `extract_document_type(text: str) -> str`
Analyzes text to determine document type (contract, motion, brief, etc.)

### `normalize_court_name(abbr: str) -> str`
Expands court abbreviations to full names

### `extract_party_names(case: str) -> Tuple[str, str]`
Splits case names into plaintiff and defendant

### `is_legal_entity(text: str) -> bool`
Checks if text contains a legal entity

### `extract_paragraph_numbers(text: str) -> List[int]`
Extracts all paragraph numbers from document

### `clean_legal_text(text: str) -> str`
Cleans and normalizes legal text, fixing common OCR errors

## Court Abbreviations

The library includes mappings for:
- Federal courts (Supreme Court, Circuit Courts, District Courts)
- Common state court abbreviations
- Specialized courts

## Document Types

Recognizes these document categories:
- **Contract**: agreements, covenants, deeds, leases
- **Motion**: motions, petitions, applications
- **Brief**: briefs, memoranda
- **Complaint**: complaints, claims
- **Order**: orders, judgments, rulings
- **Opinion**: opinions, decisions
- **Statute**: statutes, acts, codes
- **Regulation**: regulations, rules, CFR

## Integration with Document Processor

Legal Patterns is the foundational library used by [Document Processor](https://github.com/open-legal-tools/document-processor) and other Open Legal Tools projects.

### Example Integration

```python
# In document-processor/processor.py
from legal_patterns import (
    extract_document_type,
    extract_party_names,
    clean_legal_text,
    LegalPatterns
)

class DocumentProcessor:
    def __init__(self):
        self.patterns = LegalPatterns()
    
    def process_legal_document(self, text):
        # Clean OCR errors
        cleaned_text = clean_legal_text(text)
        
        # Identify document type
        doc_type = extract_document_type(cleaned_text)
        
        # Extract structure
        paragraphs = self.patterns.PARAGRAPH_NUMBER.findall(cleaned_text)
        sections = self.patterns.SECTION_NUMBER.findall(cleaned_text)
        
        # Extract parties if case document
        if doc_type in ['opinion', 'order', 'brief']:
            plaintiff, defendant = extract_party_names(cleaned_text)
        
        return {
            'type': doc_type,
            'text': cleaned_text,
            'structure': {
                'paragraphs': paragraphs,
                'sections': sections
            },
            'parties': {
                'plaintiff': plaintiff,
                'defendant': defendant
            }
        }
```

### Using with Core Citation Tools

```python
from legal_patterns import LegalPatterns
from core_citation_tools import CitationExtractor

# Combine pattern detection with citation extraction
patterns = LegalPatterns()
extractor = CitationExtractor()

# Find footnotes that might contain citations
footnotes = patterns.FOOTNOTE_TEXT.findall(document_text)
for footnote in footnotes:
    citations = extractor.extract(footnote)
    # Process citations...
```

## Related Projects

This library is designed to work seamlessly with:
- [**Document Processor**](https://github.com/open-legal-tools/document-processor): Advanced OCR and document parsing
- [**Core Citation Tools**](https://github.com/open-legal-tools/core-citation-tools): Citation extraction and validation
- [**CourtListener API**](https://github.com/open-legal-tools/courtlistener-api): Legal research integration
- All other Open Legal Tools projects

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see LICENSE file

## Part of Open Legal Tools

This library is part of the [Open Legal Tools](https://github.com/open-legal-tools) ecosystem.