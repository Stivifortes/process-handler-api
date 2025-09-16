from domain.interfaces import ILlmClient, IStorageRepository, IPdfDownloader
from domain.schemas import ProcessExtraction
from application.dto import ExtractProcessRequest


class ProcessExtractionService:
    def __init__(
        self,
        llm_client: ILlmClient,
        storage: IStorageRepository,
        pdf_downloader: IPdfDownloader
    ):
        self.llm_client = llm_client
        self.storage = storage
        self.pdf_downloader = pdf_downloader

    async def extract_process(self, request: ExtractProcessRequest) -> ProcessExtraction:
        # Download PDF
        pdf_content = await self.pdf_downloader.download_pdf(request.pdf_url)
        
        # Process with LLM
        extraction = await self.llm_client.analyze_pdf(pdf_content)
        print(extraction)
        extraction.case_id = request.case_id
        
        # Save to storage
        await self.storage.save_extraction(extraction)
        
        return extraction
