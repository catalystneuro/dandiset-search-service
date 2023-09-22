from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from tqdm import tqdm
from pathlib import Path
import json
import uuid
import openai

from core.settings import settings
from clients.dandi import DandiClient


class OpenaiClient:

    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.dandi_client = DandiClient()
        self.embeddings_client = OpenAIEmbeddings()


    def get_embedding_simple(self, text: str) -> list:
        """Get embedding for a single text"""
        return self.embeddings_client.embed_query(text)


    def get_embeddings(self, metadata_list: list, max_num_sets: int = None, save_to_file: bool = False) -> list:
        """Get embeddings for all metadata fields, organizes them as list of objects similar to Qdrant points"""
        all_qdrant_ponits = []
        if not max_num_sets:
            max_num_sets = len(metadata_list)
        iterable = tqdm(metadata_list[:max_num_sets])
        for m in iterable:
            # print("Generating embeddings for DANDI set:", m["dandiset_id"])
            iterable.set_description(f"Processing item {m['dandiset_id']}")
            n_approaches = len(m["approaches"])
            n_measurement_techniques = len(m["measurement_techniques"])
            n_variables_measured = len(m["variables_measured"])
            n_species = len(m["species"])
            query_list = [
                m["title"],
                m["description"],
            ]
            query_list.extend(m["approaches"])
            query_list.extend(m["measurement_techniques"])
            query_list.extend(m["variables_measured"])
            query_list.extend(m["species"])
            embeddings = self.embeddings_client.embed_documents(
                texts=query_list,
                chunk_size=len(query_list),
            )
            # Prepare Qdrant Points
            qdrant_points = []
            qdrant_points.append(
                {
                    "id": str(uuid.uuid4()),
                    "vector": embeddings[0],
                    "payload": {
                        "dandiset_id": m["dandiset_id"],
                        "field": "title",
                        "text_content": m["title"],
                    }
                }
            )
            qdrant_points.append(
                {
                    "id": str(uuid.uuid4()),
                    "vector": embeddings[1],
                    "payload": {
                        "dandiset_id": m["dandiset_id"],
                        "field": "description",
                        "text_content": m["description"],
                    }
                }
            )
            for i in range(n_approaches):
                qdrant_points.append(
                    {
                        "id": str(uuid.uuid4()),
                        "vector": embeddings[2+i],
                        "payload": {
                            "dandiset_id": m["dandiset_id"],
                            "field": "approaches",
                            "text_content": m["approaches"][i],
                        }
                    }
                )
            for i in range(n_measurement_techniques):
                qdrant_points.append(
                    {
                        "id": str(uuid.uuid4()),
                        "vector": embeddings[2+n_approaches+i],
                        "payload": {
                            "dandiset_id": m["dandiset_id"],
                            "field": "measurement_techniques",
                            "text_content": m["measurement_techniques"][i],
                        }
                    }
                )
            for i in range(n_variables_measured):
                qdrant_points.append(
                    {
                        "id": str(uuid.uuid4()),
                        "vector": embeddings[2+n_approaches+n_measurement_techniques+i],
                        "payload": {
                            "dandiset_id": m["dandiset_id"],
                            "field": "variables_measured",
                            "text_content": m["variables_measured"][i],
                        }
                    }
                )
            for i in range(n_species):
                qdrant_points.append(
                    {
                        "id": str(uuid.uuid4()),
                        "vector": embeddings[2+n_approaches+n_measurement_techniques+n_variables_measured+i],
                        "payload": {
                            "dandiset_id": m["dandiset_id"],
                            "field": "species",
                            "text_content": m["species"][i],
                        }
                    }
                )
            all_qdrant_ponits.extend(qdrant_points)
            if save_to_file and len(all_qdrant_ponits) > 0:
                with open(str(Path.cwd() / "qdrant_points.json"), "w") as f:
                    json.dump(all_qdrant_ponits, f)
        return all_qdrant_ponits


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
        return chain.run(user_input)


    def prepare_keywords_for_semantic_search(self, keywords_list: list) -> list:
        keywords_set = set()
        for obj in keywords_list:
            for k, v in obj.items():
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
                    text += ", ".join(v) + "\n"
                elif "DANDI:" in v:
                    text += f'{v.replace("DANDI:", "DANDISET:")}\n'
                else:
                    text += f"{v}\n"
            
            prompt += f"\n{text}"
        return prompt


    def get_llm_chat_answer(self, prompt: str, system_prompt: str = None, model: str = "gpt-3.5-turbo"):
        if system_prompt is None:
            system_prompt = "You are a helpful neuroscience research assistant, you give brief and informative suggestions to users questions, always based on a list of relevant reference dandi sets."
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message["content"]
