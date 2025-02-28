import asyncio
from typing import Optional
import logging
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self, llm_provider: str, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for GROQ client")
        self.client = Groq(api_key=self.api_key)
        self.llm_provider = llm_provider

    def _get_prompt_template(self, source_type: str, blog_type: str) -> str:
        """Get the appropriate prompt template based on content source and blog type."""
        if source_type == 'youtube':
            if blog_type == 'opinionated':
                return """
                    Create a compelling, opinionated tech-focused blog post in the style of Andrew Zuo's 'AI Is Killing Coding.' The piece should have:

                    Provocative, shareable title
                    - Use contrarian viewpoints, unexpected comparisons, or bold statements
                    - Consider formats like "Why [Popular Belief] Is Actually Wrong" or "The Uncomfortable Truth About [Technology]"

                    Hook-driven opening
                    - Begin with a personal anecdote, surprising statistic, or counterintuitive claim
                    - Establish your position within the first two sentences
                    - Create immediate tension between conventional wisdom and your perspective

                    Authentic voice with strategic informality
                    - Write with personality - use contractions, occasional slang, and varied sentence lengths
                    - Include pattern interrupts like "Here's the thing:" or "Let me be clear:"
                    - Incorporate strategic vulnerability ("I used to believe..." or "I was wrong about...")

                    Visual rhythm and information layering
                    - Vary paragraph length (1-5 sentences) with intentional single-sentence paragraphs for emphasis
                    - Use formatting strategically: bold for key points, italics for emphasis, and block quotes for external perspectives
                    - Include 2-3 section headers that promise and deliver specific insights

                    Evidence hierarchy
                    - Blend personal experience, industry trends, expert opinions, and data
                    - Present counterarguments fairly before dismantling them
                    - Use specific examples rather than generalizations ("When I worked at X" instead of "Many developers")

                    Narrative arc with escalating stakes
                    - Start with micro concerns before expanding to industry/societal implications
                    - Build tension by addressing potential objections as you go
                    - End with a synthesis that elevates the discussion beyond the initial premise

                    Resonant conclusion
                    - Restate your core argument with new depth
                    - Include a forward-looking statement that connects to broader trends
                    - End with either a specific call-to-action or a thought-provoking question that creates conversation

                    Authenticity markers
                    - Include 1-2 references to specific tools, communities, or events familiar to your target audience
                    - Acknowledge nuance and complexity where appropriate
                    - Express genuine enthusiasm or concern rather than manufactured outrage

                    Aim for 800-1200 words with a reading time of 4-6 minutes. The final piece should feel like a thoughtful perspective from an industry insider rather than generic content marketing.

                    Transcript: {0}
                """
            else:
                return """
                    Based on this YouTube video transcript, create an engaging blog post that captures 
                    the key insights and maintains the speaker's voice:

                    Transcript: {0}

                    Structure and Formatting:
                    - Title: Create an attention-grabbing title that reflects the video's main topic
                    - Introduction: Start with a hook that draws readers in, mentioning it's based on a video
                    - Key Points: Break down the main points discussed in the video
                    - Quotes: Include notable quotes from the speaker when relevant
                    - Timestamps: Reference key moments from the video when appropriate
                    - Conclusion: Summarize the main takeaways and include a call-to-action

                    Tone and Style:
                    - Maintain the speaker's personality and speaking style
                    - Convert spoken language into readable text while keeping authenticity
                    - Add context where needed for clarity
                    - Use a conversational yet professional tone
                    - Include relevant examples mentioned in the video
                """
        else:
            if blog_type == 'opinionated':
                return """
                    Create a compelling, opinionated tech-focused blog post in the style of Andrew Zuo's 'AI Is Killing Coding.' The piece should have:

                    Provocative, shareable title
                    - Use contrarian viewpoints, unexpected comparisons, or bold statements
                    - Consider formats like "Why [Popular Belief] Is Actually Wrong" or "The Uncomfortable Truth About [Technology]"

                    Hook-driven opening
                    - Begin with a personal anecdote, surprising statistic, or counterintuitive claim
                    - Establish your position within the first two sentences
                    - Create immediate tension between conventional wisdom and your perspective

                    Authentic voice with strategic informality
                    - Write with personality - use contractions, occasional slang, and varied sentence lengths
                    - Include pattern interrupts like "Here's the thing:" or "Let me be clear:"
                    - Incorporate strategic vulnerability ("I used to believe..." or "I was wrong about...")

                    Visual rhythm and information layering
                    - Vary paragraph length (1-5 sentences) with intentional single-sentence paragraphs for emphasis
                    - Use formatting strategically: bold for key points, italics for emphasis, and block quotes for external perspectives
                    - Include 2-3 section headers that promise and deliver specific insights

                    Evidence hierarchy
                    - Blend personal experience, industry trends, expert opinions, and data
                    - Present counterarguments fairly before dismantling them
                    - Use specific examples rather than generalizations ("When I worked at X" instead of "Many developers")

                    Narrative arc with escalating stakes
                    - Start with micro concerns before expanding to industry/societal implications
                    - Build tension by addressing potential objections as you go
                    - End with a synthesis that elevates the discussion beyond the initial premise

                    Resonant conclusion
                    - Restate your core argument with new depth
                    - Include a forward-looking statement that connects to broader trends
                    - End with either a specific call-to-action or a thought-provoking question that creates conversation

                    Authenticity markers
                    - Include 1-2 references to specific tools, communities, or events familiar to your target audience
                    - Acknowledge nuance and complexity where appropriate
                    - Express genuine enthusiasm or concern rather than manufactured outrage

                    Aim for 800-1200 words with a reading time of 4-6 minutes. The final piece should feel like a thoughtful perspective from an industry insider rather than generic content marketing.

                    Content: {0}
                """
            else:
                return """
                    Based on the following content, create a blog post that mimics the desired style:

                    Content: {0}

                    Structure and Formatting:
                    - Title: Start with an engaging, thought-provoking headline
                    - Introduction: Begin with a hook that immediately engages the reader
                    - Subheadings: Use descriptive subheadings to organize content
                    - Lists: Include bulleted or numbered lists where applicable
                    - Examples: Use concrete examples to support key points
                    - Conclusion: End with actionable takeaways

                    Tone and Style:
                    - Conversational but authoritative
                    - Clear and concise paragraphs
                    - Engaging and relatable examples
                    - Professional yet accessible language
                """

    async def generate_content(self, data: dict, blog_type: str) -> str:
        try:
            content = data.get('content', '')
            if not content:
                raise ValueError("No content provided for blog generation")
                
            source_type = data.get('source_type', 'website')
            logger.info(f"🤖 Generating blog post from {source_type} content...")
            prompt = self._get_prompt_template(source_type, blog_type).format(content)
            
            def make_groq_call():
                return self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a very popular and professional blog writer."},
                        {"role": "user", "content": prompt}
                    ],
                    model=self.llm_provider
                )
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, make_groq_call)
            
            if not response or not response.choices:
                raise ValueError("No response generated from GROQ API")
                
            logger.info("✅ Blog post generated successfully!")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"❌ Error generating content: {str(e)}")
            raise