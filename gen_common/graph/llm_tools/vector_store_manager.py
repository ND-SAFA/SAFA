import os
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents.base import Document
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm

from gen_common.constants.environment_constants import DEFAULT_EMBEDDING_MODEL
from gen_common.constants.graph_defaults import INCLUDE_IDS_IN_EMBEDDING_DEFAULT, SIMILARITY_THRESHOLD_DEFAULT
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.traceability.relationship_manager.abstract_relationship_manager import AbstractRelationshipManager
from gen_common.traceability.relationship_manager.embedding_types import IdType
from gen_common.util.enum_util import EnumDict
from gen_common.util.file_util import FileUtil
from gen_common.util.list_util import ListUtil
from gen_common.util.math_util import MathUtil
from gen_common.util.override import overrides
from gen_common.util.pythonisms_util import default_mutable


class VectorStoreManager(AbstractRelationshipManager):
    CONTEXT_FILE_LAYER_ID = "context_file"

    @default_mutable()
    def __init__(self, artifact_df: ArtifactDataFrame, context_files: List | str = None,
                 model_name: str = DEFAULT_EMBEDDING_MODEL,
                 vectorstore: VectorStore = None, include_ids: bool = INCLUDE_IDS_IN_EMBEDDING_DEFAULT,
                 vector_store_path: Optional[str] = None, split_docs: bool = False):
        """
        Handles adding context to a vector store for retrieval.
        :param artifact_df: Contains all artifacts in the project.
        :param context_files: List of filepaths to get context from.
        :param model_name: The name of the embedding model to use.
        :param include_ids: Whether to include ids in the content for search.
        :param vectorstore: Existing storage for embeddings of context.
        :param vector_store_path: Path to directory to store chroma database.
        :param split_docs: If True, automatically splits docs into chunks.
        """

        self.include_ids = include_ids
        self.id_to_artifacts = self._create_id_to_artifact_map(artifact_df, context_files)
        self.vector_store_path = vector_store_path
        self.split_docs = split_docs
        content_map = {a_id: artifact[ArtifactKeys.CONTENT] for a_id, artifact in self.id_to_artifacts.items()}
        super().__init__(model_name=model_name,
                         content_map=content_map)
        self.__vectorstore = vectorstore
        self.__update_vectorstore(list(self.id_to_artifacts.keys()))

    def search(self, queries: List[str] | str | Set[str],
               include_scores: bool = False,
               threshold: Optional[float] = SIMILARITY_THRESHOLD_DEFAULT,
               max_returned: int = None) -> Dict[str, List[Document] | List[Tuple[Document, float]]]:
        """
        Performs a search to find nearest artifacts to the query.
        :param queries: List of queries to search for.
        :param include_scores: If True, includes the relevance score with the doc.
        :param threshold: Similarity score threshold to filter docs by after scaling.
        :param max_returned: Max number of docs to return.
        :return: Dictionary mapping query to retrieved documents for that query.
        """
        assert threshold is not None or max_returned is not None, "Must specify a threshold or how many to return"
        if isinstance(queries, str):
            queries = [queries]
        retrieved_docs = {}
        max_returned = max_returned if max_returned is not None else len(self)
        for query in queries:
            if include_scores or threshold is not None:
                docs = self.__vectorstore.similarity_search_with_relevance_scores(query, k=max_returned)
            else:
                docs = self.__vectorstore.similarity_search(query, k=max_returned)
            if threshold is not None:
                docs = self._filter_by_scores(docs, threshold, include_scores)
            retrieved_docs[query] = docs
        return retrieved_docs

    @staticmethod
    def from_args(args: GraphArgs, **additional_params) -> "VectorStoreManager":
        """
        Creates a retriever manager from the chat state.
        :param args: Contains necessary data.
        :return: A retriever manager from the chat state.
        """
        artifact_df, context_file = VectorStoreManager._extract_context_from_args(args)
        return VectorStoreManager(artifact_df, context_file, **additional_params)

    def add_context_from_args(self, args: GraphArgs) -> None:
        """
        Adds context from the state to the store.
        :param args: The current state of chat.
        :return: The vector store to use to retrieve context docs.
        """
        artifact_df, context_file = self._extract_context_from_args(args)
        new_artifacts = self._create_id_to_artifact_map(artifact_df, context_file)
        self.id_to_artifacts.update(new_artifacts)
        updated_ids = self.update_or_add_contents(artifact_df.to_map())
        self.__update_vectorstore(updated_ids)

    def contains(self, a_id: str) -> bool:
        """
        Checks if the id is in the vectorstore already.
        :param a_id: The id of the artifact.
        :return: True if the id is in the vector already.
        """
        return a_id in self._content_map

    @classmethod
    @overrides(AbstractRelationshipManager)
    def create_from_content(cls, content_list: List[str], **kwargs) -> "VectorStoreManager":
        """
        Creates manager by constructing a content map from a list of its content.
        :param content_list: List of content.
        :param kwargs: Keyword arguments passed to manager.
        :return: The Manager.
        """
        content_list = list(set(content_list))
        artifact_dict = {ArtifactKeys.ID.value: content_list,
                         ArtifactKeys.CONTENT.value: content_list,
                         ArtifactKeys.LAYER_ID: ["context" for _ in content_list]}
        return VectorStoreManager(artifact_df=ArtifactDataFrame(artifact_dict), **kwargs)

    @overrides(AbstractRelationshipManager)
    def update_or_add_content(self, a_id: Any = None, content: str = None, artifact: EnumDict = None,
                              add_to_vector_store: bool = True) -> bool:
        """
        Updates or adds new content for an id.
        :param a_id: The id to update the content of.
        :param content: The new content.
        :param artifact: Artifact may be specified in place of id and content.
        :param add_to_vector_store: If True, automatically adds to vectorstore.
        :return: True if artifact was updated else False.
        """
        updated_artifact = super().update_or_add_content(a_id, content, artifact=artifact)
        if updated_artifact:
            artifact = self.id_to_artifacts.get(a_id, EnumDict()) if not artifact else artifact
            if a_id and content:
                artifact[ArtifactKeys.ID] = a_id
                artifact[ArtifactKeys.CONTENT] = content
            self.id_to_artifacts[a_id] = artifact
            if add_to_vector_store:
                self.__update_vectorstore([a_id])
        return updated_artifact

    @overrides(AbstractRelationshipManager)
    def update_or_add_contents(self, content_map: Dict[Any, str | EnumDict], **kwargs) -> List[str]:
        """
        Updates or adds new content for all artifacts in teh map
        :param content_map: Maps the id of the new or existing artifact to the its content
        :return: List of ids that were updated.
        """
        updated_ids = super().update_or_add_contents(content_map, add_to_vector_store=False)
        if updated_ids:
            self.__update_vectorstore(updated_ids)
        return updated_ids

    @overrides(AbstractRelationshipManager)
    def remove_artifact(self, a_id: IdType, delete_from_vector_store: bool = True) -> None:
        """
        Removes an artifact with ids from the manager.
        :param a_id: ID of the artifact to remove.
        :param delete_from_vector_store: If True, automatically deletes from vectorstore
        :return: None
        """
        removed = super().remove_artifact(a_id)
        if removed:
            self.id_to_artifacts.pop(a_id)
            if delete_from_vector_store:
                self.__vectorstore.delete([a_id])

    @overrides(AbstractRelationshipManager)
    def remove_artifacts(self, a_ids: Union[IdType, List[IdType]], **kwargs) -> List[str]:
        """
        Removes artifacts with ids from the manager.
        :param a_ids: IDs of the artifact to remove.
        :return: List of ids that were removed.
        """
        removed_ids = super().remove_artifacts(a_ids, delete_from_vector_store=False)
        if removed_ids:
            self.__vectorstore.delete(removed_ids)
        return removed_ids

    @default_mutable()
    def _get_context_from_file(self, context_files: List | str = None) -> Dict[str, Artifact]:
        """
        Gets context from a file as additional content.
        :param context_files: Context file path(s) to read.
        :return: The context file path mapped to the content as an artifact.
        """
        if not isinstance(context_files, list):
            context_files = [context_files]

        artifacts = {}
        for context_file in context_files:
            content_doc = FileUtil.read_file(context_file)
            artifacts[context_file] = Artifact(id=context_file, content=content_doc, layer_id=self.CONTEXT_FILE_LAYER_ID)
        return artifacts

    @staticmethod
    def _extract_context_from_args(args: GraphArgs) -> Tuple[ArtifactDataFrame, str]:
        """
        Extracts the relevant context elements from the state.
        :param args: Contains relevant context.
        :return: Artifact dataframe and the context file content if there is one.
        """
        artifact_df = args.dataset.artifact_df
        context_file = args.context_filepath
        return artifact_df, context_file

    def _create_id_to_artifact_map(self, artifact_df: ArtifactDataFrame, context_files: List | str) -> Dict[str, Artifact]:
        """
        Gets all artifacts from df and context files.
        :param artifact_df: Contains project artifacts.
        :param context_files: List of file paths to read context from.
        :return: Dictionary mapping artifact id to the artifact.
        """
        artifacts = {a_id: artifact for a_id, artifact in artifact_df.itertuples()}
        artifacts.update(self._get_context_from_file(context_files))
        return artifacts

    @staticmethod
    def _split_documents(context_documents: List[Document], chunk_size: int = 500, chunk_overlap: int = 0) -> List[Document]:
        """
        Splits all documents into chunks.
        :param context_documents: List of complete context docs.
        :param chunk_size: The size of the chunk to make.
        :param chunk_overlap: The overlap between chunks.
        :return: Documents split into chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        doc_splits = text_splitter.split_documents(context_documents)
        return doc_splits

    @staticmethod
    def _filter_by_scores(docs: List[Tuple[Document, float]], threshold: float,
                          include_scores: bool) -> List[Document | Tuple[Document, float]]:
        """
        Filters retrieved docs by a threshold.
        :param docs: List of docs and corresponding scores.
        :param threshold: Threshold to filter by after scaling.
        :param include_scores: True if scores should be returned alongside doc.
        :return: List of docs with scores greater than threshold after scaling.
        """
        _, max_score = docs[0]
        filtered_docs = []
        for doc, score in docs:
            score = MathUtil.convert_to_new_range(score, (0, max_score), (0, 1))
            if score > threshold:
                filtered_docs.append((doc, score) if include_scores else doc)
        return filtered_docs

    def __update_vectorstore(self, ids_to_add: List[str] = None) -> None:
        """
        Adds documents from the artifact df and context files to the store.
        :param ids_to_add: List of ids that should be added (if None, all new ones will be added)
        :return: None.
        """
        context_documents = self.__get_docs_to_add(ids_to_add)
        self.__add_to_vectorstore(context_documents)

    def __add_to_vectorstore(self, documents: List[Document] = None, batch_size: int = 100) -> None:
        """
        Adds the documents to the vector store
        :param documents: The context docs to store in retriever.
        :param batch_size: The number of docs to add at a time.
        :return: The updated vector store
        """
        vector_store = self.__get_vector_store()
        ids = [Artifact.convert_from_document(doc)[ArtifactKeys.ID] for doc in documents]
        for batch in tqdm(ListUtil.batch(documents, n=batch_size), desc="Adding embedding to vector store."):
            vector_store.add_documents(batch)

        not_contained = [a_id for a_id in ids if not self.contains(a_id)]
        assert len(not_contained) == 0, f"Not all ids have been tracked as being in the vectorstore: {not_contained}"

    def __get_vector_store(self) -> VectorStore:
        """
        Creates vector store, loads it if previous version saved at vector store path.
        :return: Vector store created.
        """
        if self.__vectorstore:
            return self.__vectorstore
        vector_params = {
            "embedding_function": HuggingFaceEmbeddings(model_name=self.model_name),
            "collection_name": str(uuid.uuid4())
        }
        if self.vector_store_path:
            os.makedirs(self.vector_store_path, exist_ok=True)
            vector_params["persist_directory"] = self.vector_store_path
            logger.info("Loading vector store from path...")
        self.__vectorstore = Chroma(**vector_params)
        return self.__vectorstore

    def __get_docs_to_add(self, ids_to_add: List[str] = None) -> List[Document]:
        """
        Gets a list of all context docs to add to vectorstore.
        :param ids_to_add: List of ids to add.
        :return: A list of all context docs to add to vectorstore.
        """
        if ids_to_add is None:
            artifacts = [artifact for a_id, artifact in self.id_to_artifacts.items() if not self.contains(a_id)]
        else:
            artifacts = [self.id_to_artifacts.get(a_id) for a_id in ids_to_add]
        context_documents: List[Document] = [Artifact.convert_to_document(a) for a in artifacts]
        if self.include_ids:
            updated_contents = AbstractRelationshipManager.add_ids_to_content(artifacts)
            for i, doc in enumerate(context_documents):
                if doc.metadata.get(ArtifactKeys.LAYER_ID) != self.CONTEXT_FILE_LAYER_ID:
                    doc.page_content = updated_contents[i]
        if self.split_docs:
            context_documents = self._split_documents(context_documents)
        return context_documents

    def _compare_artifacts(self, ids1: List[str], ids2: List[str], **kwargs) -> np.array:
        """
        Compares artifacts.
        :param ids1: Ids for the first set of artifact.
        :param ids2: Ids for the second set of artifact.
        :return: The comparison scores as a similarity matrix.
        """
        similarity_matrix = []
        for id1 in ids1:
            scores = []
            assert self.contains(id1), f"Artifact is unknown: {id1}"
            for id2 in ids2:
                assert self.contains(id2), f"Artifact is unknown: {id1}"
                docs_with_score = self.__vectorstore.similarity_search_with_score(id1,
                                                                                  filter={ArtifactKeys.ID.value: id2},
                                                                                  k=1)
                assert len(docs_with_score) == 1, f"Comparison failed for {id1} and {id2}"
                scores.append(docs_with_score[0][1])
            similarity_matrix.append(scores)
        return similarity_matrix
