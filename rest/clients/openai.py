from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from typing import List
from pathlib import Path
import json
import uuid
import openai
from typing import AsyncGenerator

from ..core.settings import settings
from .dandi import DandiClient


class OpenaiClient:

    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.dandi_client = DandiClient()
        self.embeddings_client = OpenAIEmbeddings()


    def get_embedding_simple(self, text: str) -> list:
        """Get embedding for a single text"""
        return self.embeddings_client.embed_query(text)


    def get_embeddings(self, metadata_list: List[dict], max_num_sets: int = None, save_to_file: bool = False) -> List:
        """Get embeddings for all metadata fields, organizes them as list of objects similar to Qdrant points"""
        if not max_num_sets:
            max_num_sets = len(metadata_list)
        query_list = [self.dandi_client.stringify_relevant_metadata(m) for m in metadata_list[:max_num_sets]]
        embeddings = self.embeddings_client.embed_documents(
            texts=query_list,
            chunk_size=len(query_list),
        )
        # Prepare Qdrant Points
        qdrant_points = [
            {
                "id": str(uuid.uuid4()),
                "vector": emb,
                "payload": metadata_list[i],
            } for i, emb in enumerate(embeddings)
        ]
        if save_to_file and len(qdrant_points) > 0:
            with open(str(Path.cwd() / "data/qdrant_points.json"), "w") as f:
                json.dump(qdrant_points, f)
        return qdrant_points


    def keywords_extraction(self, user_input: str, model: str = "gpt-3.5-turbo"):
        schema = {
            "properties": {
                "species": {
                    "type": "string",
                    "description": "Biological species taxonomies",
                },
                "approaches": {
                    "type": "string",
                    "description": "Experimental approaches in neuroscience, such as electrophysiology, calcium imaging, etc.",
                },
                "measurement_techniques": {
                    "type": "string",
                    "description": "Measurement techniques, such as patch clamp, two-photon imaging, spike sorting, etc.",
                },
                "variables_measured": {
                    "type": "string",
                    "description": "Variables measured, such as membrane potential, spike rate, position, etc.",
                },
                "anatomy": {
                    "type": "string",
                    "description": "Anatomical regions, such as hippocampus, cortex, etc.",
                },
                "disease": {
                    "type": "string",
                    "description": "Disease models, such as Alzheimer's, Parkinson's, etc.",
                },
                "cell_types": {
                    "type": "string",
                    "description": "Cell types, such as pyramidal, interneuron, etc.",
                },
                "drugs": {
                    "type": "string",
                    "description": "Drugs, such as ketamine, nitrous oxide, etc.",
                }
            },
            "required": [],
        }
        llm = ChatOpenAI(
            model=model,
            temperature=0
        )
        chain = create_extraction_chain(schema, llm)
        keywords_extracted = list(chain.run(user_input))

        # Temporary fallback to extracting nouns (if no schema-related keywords found)
        if any(isinstance(item, str) for item in keywords_extracted):
            # import nltk 
            # nltk.download(['punkt', 'averaged_perceptron_tagger'])
            # words = nltk.word_tokenize(user_input)
            # pos_tags = nltk.pos_tag(words)
            # keywords_extracted = [noun for noun, tag in pos_tags if tag.startswith("N")]
            # return keywords_extracted
            return list(set(user_input.split()))

        return self.prepare_keywords_for_semantic_search(keywords_extracted)


    def prepare_keywords_for_semantic_search(self, keywords_list: list) -> list:
        keywords_set = set()
        for obj in keywords_list:
            for _, v in obj.items():
                if v:
                    keywords_set.add(v.lower())
        return list(keywords_set)


    def add_ordered_similarity_results_to_prompt(self, similarity_results: list, prompt: str = ""):
        for r in similarity_results:
            dandiset_id = r[0].split("/")[0].split("DANDI:")[1]
            score = r[1]
            m = self.dandi_client.get_dandiset_metadata(dandiset_id=dandiset_id)
            m2 = self.dandi_client.collect_relevant_metadata(metadata_list=[m])[0]
            m2["relevance_score"] = f"relevance score: {score}"
            text = ""
            for k, v in m2.items():
                if isinstance(v, list):
                    if len(v) > 0:
                        text += k + ": " + ", ".join(v) + "\n"
                elif "DANDI:" in v:
                    text += f'{v.replace("DANDI:", "Dandiset number:")}\n'
                else:
                    text += k + ": " + f"{v}\n"
            
            prompt += f"\n{text}"
        return prompt


    async def get_llm_chat_answer(
        self, 
        prompt: str, 
        system_prompt: str = None, 
        model: str = "gpt-3.5-turbo",
        stream: bool = False
    ) -> AsyncGenerator[str, None]:
        if system_prompt is None:
            system_prompt = "You are a helpful neuroscience research assistant, you give brief and informative suggestions to users questions, always based on a list of relevant reference dandi sets."
        completion = await openai.ChatCompletion.acreate(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=stream,
        )
        async for message in completion:
            if not message.choices[0]["delta"].get("role", None):
                if message.choices[0]["delta"].get("content"):
                    yield message.choices[0]["delta"].get("content")
