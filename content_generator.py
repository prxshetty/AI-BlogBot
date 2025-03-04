import asyncio
from typing import Optional
import logging
from dotenv import load_dotenv
import os
from groq import Groq
from openai import OpenAI
from prompts import BlogPrompts

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self, llm_provider: str, api_key: Optional[str] = None):
        self.llm_provider = llm_provider
        
        # Initialize appropriate client based on provider
        if "openai" in llm_provider or "google" in llm_provider or "anthropic" in llm_provider:
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            if not self.api_key:
                raise ValueError("API key is required for OpenRouter")
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key
            )
            self.use_openrouter = True
        else:
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("API key is required for GROQ")
            self.client = Groq(api_key=self.api_key)
            self.use_openrouter = False
        
        # Define model info with TPM limits
        self.model_info = {
            # Groq Models
            "llama-3.3-70b-versatile": {"tpm": 6000},
            "llama-3.1-8b-instant": {"tpm": 6000},
            "mixtral-8x7b-32768": {"tpm": 5000},
            "deepseek-r1-distill-llama-70b": {"tpm": 6000},
            "gemma2-9b-it": {"tpm": 15000},
            # OpenRouter Models
            "openai/gpt-4-turbo-preview": {"tpm": 15000},
            "google/gemini-pro": {"tpm": 30000},
            "anthropic/claude-3-opus": {"tpm": 200000},
            "google/gemini-1.5-pro": {"tpm": 100000}
        }
        
        self.model_data = self.model_info.get(self.llm_provider, {"tpm": 6000})
        logger.info(f"Using model {self.llm_provider} with TPM: {self.model_data['tpm']}")

    def _get_prompt_template(self, source_type: str, blog_type: str) -> str:
        return BlogPrompts.BLOG_TEMPLATES[source_type][blog_type]

    async def generate_content(self, data: dict, blog_type: str) -> str:
        try:
            content = data.get('content', '')
            if not content:
                raise ValueError("No content provided for blog generation")
                
            source_type = data.get('source_type', 'website')
            logger.info(f"🤖 Generating blog post from {source_type} content...")
            
            # Estimate token count
            estimated_tokens = len(content) // 4
            logger.info(f"Estimated content tokens: {estimated_tokens}")
            
            # If content is too large, take a portion that fits within TPM limit
            if estimated_tokens > self.model_data['tpm']:
                content_portion = int(self.model_data['tpm'] * 0.7 * 4)  # 70% of TPM limit in chars
                content = content[:content_portion]
                logger.info(f"Content truncated to fit within TPM limit: {self.model_data['tpm']}")
            
            prompt = self._get_prompt_template(source_type, blog_type).format(content)
            
            def make_api_call():
                try:
                    if self.use_openrouter:
                        return self.client.chat.completions.create(
                            extra_headers={
                                "HTTP-Referer": "https://github.com/yourusername/Blog-Bot",  # Update with your repo URL
                                "X-Title": "Blog-Bot"
                            },
                            model=self.llm_provider,
                            messages=[
                                {"role": "system", "content": BlogPrompts.SYSTEM_PROMPTS[blog_type]},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=2000
                        )
                    else:
                        return self.client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": BlogPrompts.SYSTEM_PROMPTS[blog_type]},
                                {"role": "user", "content": prompt}
                            ],
                            model=self.llm_provider,
                            temperature=0.7,
                            max_tokens=2000
                        )
                except Exception as e:
                    if "413" in str(e) or "too large" in str(e).lower():
                        raise ValueError(f"Content too large for model {self.llm_provider}. Try using a model with larger context window.")
                    raise
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, make_api_call)
            
            if not response or not response.choices:
                raise ValueError("No response generated from API")
                
            logger.info("✅ Blog post generated successfully!")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"❌ Error generating content: {str(e)}")
            raise