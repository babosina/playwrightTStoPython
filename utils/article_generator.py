from typing import Any

from faker import Faker
from request_data.POST_article import NEW_ARTICLE_DATA
from copy import deepcopy


def generate_article() -> dict[str, Any]:
    article_payload = deepcopy(NEW_ARTICLE_DATA)
    article_payload["article"]["title"] = Faker().sentence()
    article_payload["article"]["description"] = Faker().sentence(nb_words=6)
    article_payload["article"]["body"] = Faker().paragraph(nb_sentences=3)
    return article_payload
