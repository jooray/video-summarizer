from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage
from .chat_venice_api import ChatVeniceAPI

class Summarizer:
    def __init__(self, transcript: str, prompts: dict, context_size: int, model: str, api_key: str, api_base: str):
        self.transcript = transcript
        self.prompts = prompts
        self.context_size = context_size
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        self.llm = ChatVeniceAPI(model=self.model, api_key=self.api_key, base_url=self.api_base)

    def split_transcript(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.context_size,
            chunk_overlap=0
        )
        return text_splitter.split_text(self.transcript)

    def generate_summary(self, text_chunk: str, prompt: str):
        message = HumanMessage(content=f"{prompt}\n\n{text_chunk}")
        response = self.llm.invoke([message])
        return response.content.strip()

    def summarize(self):
        chunks = self.split_transcript()
        short_summary = self.generate_summary(chunks[0], self.prompts['short_summary'])

        if len(chunks) == 1:
            detailed_summary = self.generate_summary(chunks[0], self.prompts['detailed_summary'])
        else:
            chunk_summaries = []
            for chunk in chunks:
                chunk_summaries.append(self.generate_summary(chunk, self.prompts['detailed_summary']))
            detailed_summary = self.generate_summary("\n\n".join(chunk_summaries), self.prompts['merge_summary'])

        return short_summary, detailed_summary
