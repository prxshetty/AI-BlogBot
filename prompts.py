class BlogPrompts:
    """Blog prompt templates and system messages for different types of blog posts."""

    SYSTEM_PROMPTS = {
        "how_to": "You are an expert technical writer who creates clear, step-by-step tutorials. Your writing is engaging, informative, and easy to follow.",
        "listicle": "You are a content creator who specializes in creating engaging list-based articles. Your content is well-researched, organized, and provides value to readers.",
        "tutorial": "You are an educational content creator who excels at creating comprehensive learning materials. Your tutorials are thorough, practical, and beginner-friendly.",
        "opinion": "You are a thought leader who writes compelling opinion pieces. Your arguments are well-reasoned, balanced, and backed by evidence.",
        "news": "You are a journalist who writes clear, objective news articles. Your reporting is factual, timely, and provides context.",
        "review": "You are an expert reviewer who provides detailed, honest, and balanced reviews. Your insights help readers make informed decisions."
    }

    BLOG_TEMPLATES = {
        "youtube": {
            "how_to": "Create a step-by-step tutorial based on this YouTube video: {title}\n\nVideo content: {content}\n\nCreate a comprehensive how-to guide that readers can follow to achieve the same results shown in the video.",
            "listicle": "Based on this YouTube video titled '{title}', create an engaging listicle article.\n\nVideo content: {content}\n\nExtract the key points and present them as a numbered or bulleted list that provides value to readers.",
            "tutorial": "Transform this YouTube video into a detailed tutorial: {title}\n\nVideo content: {content}\n\nCreate a comprehensive learning experience that goes beyond the video content and provides additional context and examples.",
            "opinion": "Watch this YouTube video and write an opinion piece: {title}\n\nVideo content: {content}\n\nShare your perspective on the topic, supporting your arguments with evidence from the video and external sources.",
            "news": "Based on this YouTube video about '{title}', write a news article.\n\nVideo content: {content}\n\nPresent the information in a journalistic style, focusing on the who, what, when, where, why, and how.",
            "review": "Review the content of this YouTube video: {title}\n\nVideo content: {content}\n\nProvide a critical analysis of the video's content, presentation, and value to viewers."
        },
        "webpage": {
            "how_to": "Transform this webpage content into a how-to guide: {title}\n\nContent: {content}\n\nCreate a step-by-step tutorial that helps readers accomplish a specific task based on the webpage information.",
            "listicle": "Based on this webpage about '{title}', create an engaging listicle.\n\nContent: {content}\n\nExtract and organize the key information into a numbered or bulleted list format.",
            "tutorial": "Convert this webpage content into a comprehensive tutorial: {title}\n\nContent: {content}\n\nDevelop a detailed learning resource that expands on the webpage content.",
            "opinion": "Read this webpage and write an opinion piece: {title}\n\nContent: {content}\n\nShare your thoughts on the topic, supporting your arguments with evidence from the webpage.",
            "news": "Based on this webpage about '{title}', write a news article.\n\nContent: {content}\n\nPresent the information in a news format, focusing on the most important aspects.",
            "review": "Review this webpage: {title}\n\nContent: {content}\n\nProvide an analysis of the webpage's content, quality, and value to readers."
        },
        "topic": {
            "how_to": "Write a how-to guide about: {topic}\n\nCreate a comprehensive step-by-step tutorial that helps readers accomplish the task or learn the skill.",
            "listicle": "Create an engaging listicle about: {topic}\n\nDevelop a well-researched list that provides valuable information and insights on the topic.",
            "tutorial": "Write a detailed tutorial on: {topic}\n\nCreate a comprehensive learning resource that thoroughly covers the subject.",
            "opinion": "Write an opinion piece about: {topic}\n\nShare your perspective on the topic, supporting your arguments with evidence and reasoning.",
            "news": "Write a news article about: {topic}\n\nPresent recent developments and information about the topic in a journalistic style.",
            "review": "Write a review about: {topic}\n\nProvide a critical analysis of the topic, discussing its strengths, weaknesses, and overall value."
        }
    }