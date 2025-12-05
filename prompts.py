class BlogPrompts:
    """Blog prompt templates and system messages for different types of blog posts."""

    SYSTEM_PROMPTS = {
        "standard": "You are a professional blog writer who creates engaging, well-structured content. Your writing is clear, informative, and optimized for readability.",
        "opinionated": "You are a tech thought leader who writes compelling, opinionated blog posts. Your writing is bold, insightful, and backed by technical expertise and real-world experience.",
        "seo": "You are an SEO-focused content writer who creates search-engine optimized blog posts. Your content is keyword-rich, well-structured with proper headings, and designed to rank well in search results.",
    }

    BLOG_TEMPLATES = {
        "youtube": {
            "standard": "Create a well-structured blog post based on this YouTube video content:\n\n{content}\n\nWrite an engaging article that captures the key insights and presents them in a clear, readable format with proper introduction, body, and conclusion.",
            "opinionated": "Create a bold, opinionated tech blog post based on this YouTube video content:\n\n{content}\n\nWrite a thought-provoking article that takes a strong stance on the topic, challenges conventional thinking, and provides unique technical insights backed by the video content.",
            "seo": "Create an SEO-optimized blog post based on this YouTube video content:\n\n{content}\n\nWrite a search-engine friendly article with:\n- A compelling title with target keywords\n- Clear H2 and H3 headings\n- Natural keyword integration\n- Meta description\n- Proper structure for featured snippets\n- Internal linking suggestions",
        },
        "webpage": {
            "standard": "Create a well-structured blog post based on this webpage content:\n\n{content}\n\nWrite an engaging article that captures the key insights and presents them in a clear, readable format with proper introduction, body, and conclusion.",
            "opinionated": "Create a bold, opinionated tech blog post based on this webpage content:\n\n{content}\n\nWrite a thought-provoking article that takes a strong stance on the topic, challenges conventional thinking, and provides unique technical insights backed by the webpage content.",
            "seo": "Create an SEO-optimized blog post based on this webpage content:\n\n{content}\n\nWrite a search-engine friendly article with:\n- A compelling title with target keywords\n- Clear H2 and H3 headings\n- Natural keyword integration\n- Meta description\n- Proper structure for featured snippets\n- Internal linking suggestions",
        },      
    }