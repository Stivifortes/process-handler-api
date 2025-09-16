# Legal Process Analysis API

This API was developed as part of a code challenge to demonstrate the ability to create a robust system for analyzing legal process PDFs using modern technologies and AI capabilities.

## 🎯 Challenge Overview

Create a REST API that can:
1. Receive a public PDF URL containing legal process information
2. Extract and analyze the content using Google's Gemini AI
3. Generate a structured JSON response with process details
4. Store the analysis results in a database

## 🛠 Technical Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy
- **AI Integration**: Google Gemini 2.5 Flash
- **Python Version**: 3.13
- **Key Libraries**:
  - `google-generativeai`: For AI-powered text extraction
  - `pydantic`: For data validation
  - `sqlalchemy`: For database operations
  - `aiosqlite`: For async database support
  - `python-multipart`: For handling file uploads

## 🏗 Project Structure

```
process-handler-api/
├── src/
│   ├── main.py                 # Application entry point
│   ├── application/
│   │   ├── dto.py             # Data transfer objects
│   │   └── services.py        # Business logic
│   ├── domain/
│   │   ├── interfaces.py      # Abstract interfaces
│   │   └── schemas.py         # Data models
│   ├── infrastructure/
│   │   ├── llm_client.py      # Gemini AI integration
│   │   ├── pdf_downloader.py  # PDF handling
│   │   └── storage.py         # Database operations
│   └── routes/
│       └── process_routes.py   # API endpoints
└── tests/
    └── test_process_extraction.py
```

## ✨ Features

- **PDF Analysis**: Extract structured information from legal process PDFs
- **AI-Powered**: Uses Google Gemini 2.5 Flash for intelligent content analysis
- **Structured Output**: Generates standardized JSON with:
  - Case summary
  - Chronological timeline of events
  - Evidence analysis with page references
  - Potential flaws or observations
- **Persistent Storage**: Saves all analyses for future reference
- **Async Operations**: Built with async/await pattern for better performance

## 🚀 Getting Started

1. Clone the repository
2. Set up environment variables:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   cd src
   uvicorn main:app --reload
   ```

## 📡 API Endpoints

### POST /extract
Analyzes a legal process PDF from a provided URL.

#### Request
```json
{
    "url": "https://example.com/legal-process.pdf",
    "case_id": "0809090-86.2024.8.12.0021"
}
```

#### Response
```json
{
    "case_id": "LIT-2025-001",
    "resume": "Summary of the case...",
    "timeline": [
        {
            "event_id": 1,
            "event_name": "Event Name",
            "event_description": "Description",
            "event_date": "2025-09-16",
            "event_page_init": 1,
            "event_page_end": 1
        }
    ],
    "evidence": [
        {
            "evidence_id": 1,
            "evidence_name": "Evidence Name",
            "evidence_flaw": "Potential Issues",
            "evidence_page_init": 1,
            "evidence_page_end": 1
        }
    ],
    "persisted_at": "2025-09-16T21:16:32.379176"
}
```

## 💡 Design Decisions

- **Clean Architecture**: Separated into domain, application, and infrastructure layers
- **Dependency Injection**: Interfaces for key components enabling easy testing and maintenance
- **Async First**: Built with async/await for better performance with I/O operations
- **Error Handling**: Comprehensive error handling for AI responses and PDF processing
- **Type Safety**: Extensive use of Pydantic models for data validation

## 🔒 Security Considerations

- Validates input URLs before processing
- Sanitizes and validates AI responses
- Uses environment variables for sensitive data
- Implements proper error handling and logging

## 🤝 Contributing

This is a code challenge project, but contributions for improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is open-source and available under the MIT License.
