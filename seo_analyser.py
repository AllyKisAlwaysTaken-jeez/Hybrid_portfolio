def seo_recommendations(industry):
    keywords = {
        "tech": ["innovation", "cloud", "AI", "scalable"],
        "design": ["UX", "responsive", "branding"]
    }
    return {"recommended_keywords": keywords.get(industry.lower(), ["portfolio", "professional"]),
            "meta_tags": ["title", "description", "keywords"]}
