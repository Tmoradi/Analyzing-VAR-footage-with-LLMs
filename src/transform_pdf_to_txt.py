import os
import base64 
from anthropic import Anthropic
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from prompt import PDF_PROMPT


def split_pdf(pdf_path: str, pages_per_chunk: int = 20):
    """Split PDF into smaller chunks"""
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    chunks = []
    
    for i in range(0, total_pages, pages_per_chunk):
        writer = PdfWriter()
        end_page = min(i + pages_per_chunk, total_pages)
        
        for page_num in range(i, end_page):
            writer.add_page(reader.pages[page_num])
        
        # Save chunk to bytes
        chunk_bytes = BytesIO()
        writer.write(chunk_bytes)
        chunk_bytes.seek(0)
        chunks.append((i, end_page, chunk_bytes.getvalue()))
    
    return chunks

def get_rules_as_text(pdf_path: str, output_path: str):
    '''Extract rules from the pdf of handbook w/ Claude Sonnet 4.5'''
    client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    
    # Split PDF into manageable chunks
    chunks = split_pdf(pdf_path, pages_per_chunk=15)
    all_rules = []
    
    for start_page, end_page, chunk_data in chunks:
        pdf_b64 = base64.standard_b64encode(chunk_data).decode('utf-8')
        
        message = client.messages.create(
            model='claude-sonnet-4-5',
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_b64
                            }
                        },
                        {
                            "type": "text",
                            "text": PDF_PROMPT
                        }
                    ]
                }
            ]
        )
        
        all_rules.append(message.content[0].text)
        print(f"Processed pages {start_page+1}-{end_page}")
    
    # Optionally: Use Claude to consolidate/deduplicate
    final_rules = "\n\n".join(all_rules)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_rules)