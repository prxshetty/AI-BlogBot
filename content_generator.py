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
            prompt = f"""
                Based on the following content, create a blog post that mimics the desired style:

                Content: {content[:2000]}  # Limiting content length for API constraints

                Structure and Formatting:
                - Title: Start with an engaging, thought-provoking headline, often in the form of a question or a call to action. Use a subtitle for clarity or intrigue.
                - Author: Include your name and a timestamp to personalize the content.
                - Introduction: Start with a rhetorical or thought-provoking question to immediately engage the reader. Introduce the topic in a way that highlights its importance or relevance.
                - Subheadings: Use concise, descriptive subheadings to guide the reader through the article.
                - Lists: Include bulleted or numbered lists where applicable to break down complex ideas or steps.
                - Figures and Examples: Use concrete examples, diagrams, or case studies to support the explanation, often referring to "Figure X" for clarity.
                - Conclusion: End with a takeaway message or actionable advice, emphasizing key learnings or future implications.

                Tone and Style:
                - Conversational but authoritative: Balance technical depth with an accessible voice. Address the reader directly when relevant.
                - Visual aids: Suggest figures or tables when the content becomes highly technical.
                - Relatability: Incorporate comparisons to everyday experiences or simpler analogies to explain complex ideas.
                - Call to action: Use an encouraging tone to inspire the reader to explore, try, or implement what they’ve learned.

                Language Techniques:
                - Use short paragraphs for readability.
                - Combine specific metrics and stats with broader insights.
                - Highlight innovative or surprising aspects with engaging phrases.
                - Use rhetorical devices like alliteration, parallelism, and questions for engagement.
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