import random
import string

class ArticleGenerator:
    @staticmethod
    def generate_article_data(title_prefix="Test Article"):
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        title = f"{title_prefix} {random_str}"
        description = f"Description for {title}"
        body = f"Body for {title}. This is a test article created by Junie."
        tag_list = ["test", "ai-powered"]
        
        return {
            "article": {
                "title": title,
                "description": description,
                "body": body,
                "tagList": tag_list
            }
        }
