import tiktoken
from typing import AsyncGenerator
import asyncio

from ..core.settings import settings
from ..clients.openai import OpenaiClient
from ..clients.qdrant import QdrantClient
from ..models.responses.search import PostSearchResponse


base_prompt = """Given the user input and the list of most reference dandisets, propose which dandisets the user might be interested in using.
Explain your decision based on the information of the reference dandisets.
Suggest only the dandisets which you consider to be most relevant. There can be multiple relevant dandisets.
Always start your answers always with: "The most relevant dandisets for your question are:" 
Unless you consider there are no relevant dandisets, in which case only reply: "There are no relevant dandisets for your question"
Structure your answer as a numbered list, with one suggestion per item.
---
User input: {user_input}
---
Reference dandisets:
{dandisets_text}
---
Begin:"""


base_prompt_methods = """Given the user input and the list of most reference dandisets, propose which dandisets the user might be interested in using.
Explain your decision based on the information of the reference dandisets. Avoid copying text for explanations.
Suggest only the dandisets which you consider to be most relevant. There can be multiple relevant dandisets. You do not need to use all of them, just select the most relevant ones.
Importantly, your response should give emphasis to the methods and techniques used, for examplo electrophyisiology, imaging, behavioral recordings, etc.
Always start your answers always with: "The most relevant dandisets for your question are:" 
Unless you consider there are no relevant dandisets, in which case only reply: "There are no relevant dandisets for your question".
Format your answer in Markdown, and organize it as a numbered options, with one suggestion per item. 
In the top of each item, include the dandiset title, wrapped by a link to the dandiset url.
For each item, include a paragraph with an objective explanation of why you consider this dandiset relevant.
For example:

1. [title](url) \n

Explain why this dandiset is relevant...


2. [title](url) \n

Explain why this dandiset is relevant...
...
---
User input: {user_input}
---
Reference dandisets:
{dandisets_text}
---
Begin:"""


max_num_tokens = {
    "gpt-3.5-turbo": 4000,
    "gpt-3.5-turbo-16k": 16000,
    "gpt-4": 8000,
    "gpt-4-32k": 32000,
}


async def async_wrapper(external_func, kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: external_func(**kwargs))


class SearchService:

    def __init__(
        self,
        qdrant_host: str=settings.QDRANT_HOST,
        qdrant_port: int=settings.QDRANT_PORT,
    ):
        self.openai_client = OpenaiClient()
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)

    async def suggest_relevant_dandisets(
        self, 
        user_input: str,
        collection_name: str,
        model: str = "gpt-3.5-turbo", 
        method: int = 1,
        stream: bool = False,
    ) -> AsyncGenerator[str, None]:
        if method == "simple":
            ordered_similarity_results = await async_wrapper(
                self.qdrant_client.query_from_user_input,
                dict(
                    text=user_input, 
                    collection_name=collection_name, 
                    top_k=6
                )
            )
        elif method == "keywords":
            keywords = await async_wrapper(
                self.openai_client.keywords_extraction,
                dict(user_input=user_input)
            )
            # keywords_2 = self.openai_client.prepare_keywords_for_semantic_search(keywords)
            # ordered_similarity_results = self.qdrant_client.query_all_keywords(
            #     keywords=keywords_2, 
            #     collection_name=collection_name,
            #     top_k=10
            # )
            ordered_similarity_results = await async_wrapper(
                self.qdrant_client.query_from_user_input,
                dict(
                    text=" ".join(keywords), 
                    collection_name=collection_name, 
                    top_k=6
                )
            )
        else:
            raise ValueError("method must be 1 or 2")
        dandisets_text = await async_wrapper(
            self.openai_client.add_ordered_similarity_results_to_prompt,
            dict(similarity_results=ordered_similarity_results)
        )
        prompt = await async_wrapper(
            self.prepare_prompt,
            dict(user_input=user_input, dandisets_text=dandisets_text, model=model)
        )
        async for result in self.openai_client.get_llm_chat_answer(prompt, model=model, stream=stream):
            yield result
    
    def prepare_prompt(
        self, 
        user_input: str, 
        dandisets_text: str, 
        model: str = "gpt-3.5-turbo"
    ) -> str:
        prompt = base_prompt_methods.format(user_input=user_input, dandisets_text=dandisets_text)
        encoding = tiktoken.encoding_for_model(model)
        excess_tokens = len(encoding.encode(prompt)) - max_num_tokens[model]
        if excess_tokens > 0:
            dandiset_text_tokens = encoding.encode(dandisets_text)
            dandisets_text = encoding.decode(dandiset_text_tokens[:-excess_tokens])
            prompt = base_prompt_methods.format(user_input=user_input, dandisets_text=dandisets_text)
        return prompt