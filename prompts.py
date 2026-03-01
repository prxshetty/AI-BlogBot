class BlogPrompts:
    """Blog prompt templates and system messages for different types of blog posts."""

    SYSTEM_PROMPTS = {
        "standard": "You are a professional blog writer who creates engaging, well-structured content. Your writing is clear, informative, and optimized for readability.",
        "opinionated": "You are a tech thought leader who writes compelling, opinionated blog posts. Your writing is bold, insightful, and backed by technical expertise and real-world experience.",
        "seo": "You are an SEO-focused content writer who creates search-engine optimized blog posts. Your content is keyword-rich, well-structured with proper headings, and designed to rank well in search results.",
    }

    BLOG_TEMPLATES = {
        "youtube": {
            "standard": """Create a well-structured blog post in MARKDOWN format based on this YouTube video content:

{content}

Write an engaging article that captures the key insights and presents them in a clear, readable format.

FORMAT YOUR RESPONSE IN PROPER MARKDOWN:
- Use ## for main section headings (H2)
- Use ### for subsections (H3)
- Use **bold** for emphasis and key terms
- Use *italics* for subtle emphasis
- Use bullet points (-) or numbered lists (1.) where appropriate
- Use > for blockquotes when citing key points
- Use `code` for technical terms or code snippets
- Use ```language for code blocks if needed
- Include a compelling title as the first line (## Title)
- Structure: Introduction, main body sections, and conclusion""",
            "opinionated": """Create a bold, opinionated tech blog post in MARKDOWN format based on this YouTube video content:

{content}

Write a thought-provoking article that takes a strong stance on the topic, challenges conventional thinking, and provides unique technical insights backed by the video content.

FORMAT YOUR RESPONSE IN PROPER MARKDOWN:
- Use ## for main section headings (H2)
- Use ### for subsections (H3)
- Use **bold** for strong opinions and key arguments
- Use *italics* for subtle emphasis
- Use bullet points (-) or numbered lists (1.) for arguments
- Use > for blockquotes when making powerful statements
- Use `code` for technical terms or code snippets
- Use ```language for code blocks if needed
- Include a compelling, opinionated title as the first line (## Title)
- Structure: Hook introduction, main arguments, counterarguments, conclusion""",
            "seo": """Create an SEO-optimized blog post in MARKDOWN format based on this YouTube video content:

{content}

Write a search-engine friendly article with proper markdown structure.

FORMAT YOUR RESPONSE IN PROPER MARKDOWN:
- Start with a compelling ## Title with target keywords
- Include a meta description as a blockquote at the top
- Use ## for main section headings (H2) with keywords
- Use ### for subsections (H3)
- Use **bold** for important keywords and phrases
- Use bullet points (-) or numbered lists (1.) for easy scanning
- Use > for key takeaways or important quotes
- Use `code` for technical terms
- Use ```language for code blocks if needed
- Structure for featured snippets (how-to steps, definitions, lists)
- Include internal linking suggestions in [brackets]""",
        },
        "webpage": {
            "standard": """Create a well-structured blog post in MARKDOWN format based on this webpage content:

{content}

Write an engaging article that captures the key insights and presents them in a clear, readable format.

FORMAT YOUR RESPONSE IN PROPER MARKDOWN:
- Use ## for main section headings (H2)
- Use ### for subsections (H3)
- Use **bold** for emphasis and key terms
- Use *italics* for subtle emphasis
- Use bullet points (-) or numbered lists (1.) where appropriate
- Use > for blockquotes when citing key points
- Use `code` for technical terms or code snippets
- Use ```language for code blocks if needed
- Include a compelling title as the first line (## Title)
- Structure: Introduction, main body sections, and conclusion""",
            "opinionated": """Create a bold, opinionated tech blog post in MARKDOWN format based on this webpage content:

{content}

Write a thought-provoking article that takes a strong stance on the topic, challenges conventional thinking, and provides unique technical insights backed by the webpage content.

FORMAT YOUR RESPONSE IN PROPER MARKDOWN:
- Use ## for main section headings (H2)
- Use ### for subsections (H3)
- Use **bold** for strong opinions and key arguments
- Use *italics* for subtle emphasis
- Use bullet points (-) or numbered lists (1.) for arguments
- Use > for blockquotes when making powerful statements
- Use `code` for technical terms or code snippets
- Use ```language for code blocks if needed
- Include a compelling, opinionated title as the first line (## Title)
- Structure: Hook introduction, main arguments, counterarguments, conclusion""",
            "seo": """Create an SEO-optimized blog post in MARKDOWN format based on this webpage content:

{content}

Write a search-engine friendly article with proper markdown structure.

FORMAT YOUR RESPONSE IN PROPER MARKDOWN:
- Start with a compelling ## Title with target keywords
- Include a meta description as a blockquote at the top
- Use ## for main section headings (H2) with keywords
- Use ### for subsections (H3)
- Use **bold** for important keywords and phrases
- Use bullet points (-) or numbered lists (1.) for easy scanning
- Use > for key takeaways or important quotes
- Use `code` for technical terms
- Use ```language for code blocks if needed
- Structure for featured snippets (how-to steps, definitions, lists)
- Include internal linking suggestions in [brackets]""",
        },      
    }