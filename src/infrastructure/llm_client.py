import os
import base64
import google.generativeai as genai
from io import BytesIO
from typing import BinaryIO, Dict, Any
import json
import asyncio

from domain.interfaces import ILlmClient
from domain.schemas import ProcessExtraction


class GeminiLlmClient(ILlmClient):
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def _prepare_file_part(self, pdf_content: BinaryIO) -> Dict[str, Any]:
        pdf_content.seek(0)
        pdf_bytes = pdf_content.read()
        return {
            "mime_type": "application/pdf",
            "data": base64.b64encode(pdf_bytes).decode('utf-8')
        }

    async def analyze_pdf(self, pdf_content: BinaryIO) -> ProcessExtraction:
        file_part = self._prepare_file_part(pdf_content)
        
        prompt = """Extract information from the document and create a JSON response that includes:
        1. A case ID (format: LIT-YYYY-XXX)
        2. A brief summary
        3. A timeline of events
        4. List of evidence
        
        Format the output as JSON like this:
        {
            "case_id": "LIT-2025-001",
            "resume": "summary text",
            "timeline": [{"event_id": 1, "event_name": "name", "event_description": "desc", "event_date": "2025-09-16", "event_page_init": 1, "event_page_end": 1}],
            "evidence": [{"evidence_id": 1, "evidence_name": "name", "evidence_flaw": "issue", "evidence_page_init": 1, "evidence_page_end": 1}]
        }"""

        try:
            text_response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            if not text_response.text:
                full_response = await asyncio.to_thread(
                    self.model.generate_content,
                    [{"text": prompt}, file_part]
                )
                
                if not full_response.text:
                    raise ValueError("No response received from model")
                    
                text = full_response.text
            else:
                text = text_response.text
            json_str = text.strip()
            if '```' in json_str:
                parts = json_str.split('```')
                for part in parts:
                    if '{' in part and '}' in part:
                        json_str = part.strip()
                        break
            
            start_idx = json_str.find('{')
            end_idx = json_str.rfind('}') + 1
            if start_idx != -1 and end_idx > 0:
                json_str = json_str[start_idx:end_idx]
            
            result = ProcessExtraction.model_validate_json(json_str.strip())
            return result
            
        except Exception as e:
            if isinstance(response, genai.types.GenerateContentResponse):
                error_msg = f"Error processing response: {str(e)}\n"
                if hasattr(response, 'prompt_feedback'):
                    error_msg += f"Prompt feedback: {response.prompt_feedback}\n"
                if response.candidates:
                    error_msg += f"Finish reason: {response.candidates[0].finish_reason}\n"
                error_msg += f"Raw response: {str(response)[:200]}..."
                raise ValueError(error_msg)
            raise ValueError(f"Failed to generate response: {str(e)}")
