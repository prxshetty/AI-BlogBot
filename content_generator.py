import asyncio
from typing import Optional
from openai import OpenAI

class ContentGenerator:
    def __init__(self, llm_provider: str, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key)
        self.llm_provider = llm_provider
        self.api_key = api_key

    async def generate_content(self, data: dict, template: str) -> str:
        try:
            content = data.get('content', '')
            extracted_data = data.get('extracted_data', {})
            prompt = f"""Based on the following content, create a well-structured blog post:
            
            Content: {content[:2000]}  # Limiting content length for API constraints
            
            Please create a blog post that:
            1. Has a compelling title
            2. Includes an introduction
            3. Contains 3-4 main sections
            4. Ends with a conclusion
            5. Uses a professional tone
            """
            def make_openai_call():
                return self.client.chat.completions.create(
                    model=self.llm_provider,
                    messages=[
                        {"role": "system", "content": "You are a professional blog writer"},
                        {"role": "user", "content": prompt}
                    ]
                )
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, make_openai_call)

            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {str(e)}" 