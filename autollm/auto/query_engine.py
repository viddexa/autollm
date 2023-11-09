from typing import Optional, Sequence, Union

from llama_index import Document, ServiceContext, VectorStoreIndex
from llama_index.embeddings.utils import EmbedType
from llama_index.indices.query.base import BaseQueryEngine

from autollm.auto.llm import AutoLiteLLM
from autollm.auto.service_context import AutoServiceContext
from autollm.auto.vector_store_index import AutoVectorStoreIndex
from autollm.utils.env_utils import load_config_and_dotenv


def create_query_engine(
        documents: Sequence[Document] = None,
        system_prompt: str = None,
        query_wrapper_prompt: str = None,
        enable_cost_calculator: bool = True,
        embed_model: Union[str, EmbedType] = "default",  # ["default", "local"]
        llm_model: str = "gpt-3.5-turbo",
        llm_api_base: Optional[str] = None,
        llm_max_tokens: Optional[int] = None,
        llm_temperature: float = 0.1,
        vector_store_params: dict = None,
        chunk_size: Optional[int] = 512,
        chunk_overlap: Optional[int] = None,
        context_window: Optional[int] = None,
        query_engine_params: dict = None) -> BaseQueryEngine:
    """
    Create a query engine from parameters.

    Parameters:
        documents (Sequence[Document]): Sequence of llama_index.Document instances.
        system_prompt (str): The system prompt to use for the query engine.
        query_wrapper_prompt (str): The query wrapper prompt to use for the query engine.
        enable_cost_calculator (bool): Flag to enable cost calculator logging.
        embed_model (Union[str, EmbedType]): The embedding model to use for generating embeddings. "default" for OpenAI,
                                            "local" for HuggingFace or use full identifier (e.g., local:intfloat/multilingual-e5-large)
        llm_params (dict): Parameters for the LLM.
        vector_store_params (dict): Parameters for the vector store.
        service_context_params (dict): Parameters for the service context.
        query_engine_params (dict): Parameters for the query engine.

    Returns:
        A llama_index.BaseQueryEngine instance.
    """
    vector_store_params = {
        "vector_store_type": "LanceDBVectorStore"
    } if vector_store_params is None else vector_store_params
    query_engine_params = {"similarity_top_k": 6} if query_engine_params is None else query_engine_params

    llm = AutoLiteLLM.from_defaults(
        model=llm_model, api_base=llm_api_base, max_tokens=llm_max_tokens, temperature=llm_temperature)
    service_context = AutoServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        system_prompt=system_prompt,
        query_wrapper_prompt=query_wrapper_prompt,
        enable_cost_calculator=enable_cost_calculator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        context_window=context_window)
    vector_store_index = AutoVectorStoreIndex.from_defaults(
        **vector_store_params, documents=documents, service_context=service_context)

    return vector_store_index.as_query_engine(**query_engine_params)


class AutoQueryEngine:
    """
    AutoQueryEngine for query execution and optionally logging the query cost.

    ```python
    from autollm.auto.query_engine import AutoQueryEngine

    # Create an AutoQueryEngine from a config file and .env file
    query_engine = AutoQueryEngine.from_config("config.yaml", ".env")

    # Create an AutoQueryEngine from a vector store index and service context
    query_engine = AutoQueryEngine.from_instances(vector_store_index, service_context)

    # Create an AutoQueryEngine from defaults
    query_engine = AutoQueryEngine.from_defaults(
      documents=documents,
      system_prompt=system_prompt,
      query_wrapper_prompt=query_wrapper_prompt,
      enable_cost_calculator=enable_cost_calculator,
      embed_model=embed_model,
      llm_params=llm_params,
      vector_store_params=vector_store_params,
      service_context_params=service_context_params,
      query_engine_params=query_engine_params
    )
    ```
    """

    @staticmethod
    def from_instances(
            vector_store_index: VectorStoreIndex, service_context: ServiceContext,
            **kwargs) -> BaseQueryEngine:
        """
        Create an AutoQueryEngine from a vector store index and a service context.

        Parameters:
            vector_store_index: llama_index.VectorStoreIndex instance.
            service_context: llama_index.ServiceContext instance.
            **kwargs: Keyword arguments for the query engine.

        Returns:
            A llama_index.BaseQueryEngine instance.
        """

        return vector_store_index.as_query_engine(service_context=service_context, **kwargs)

    @staticmethod
    def from_defaults(
            documents: Sequence[Document] = None,
            system_prompt: str = None,
            query_wrapper_prompt: str = None,
            enable_cost_calculator: bool = True,
            embed_model: Union[str, EmbedType] = "default",  # ["default", "local"]
            llm_params: dict = None,
            vector_store_params: dict = None,
            service_context_params: dict = None,
            query_engine_params: dict = None) -> BaseQueryEngine:
        """
        Create an AutoQueryEngine from default parameters.

        Parameters:
            documents (Sequence[Document]): Sequence of llama_index.Document instances.
            system_prompt (str): The system prompt to use for the query engine.
            query_wrapper_prompt (str): The query wrapper prompt to use for the query engine.
            enable_cost_calculator (bool): Flag to enable cost calculator logging.
            embed_model (Union[str, EmbedType]): The embedding model to use for generating embeddings. "default" for OpenAI,
                                                "local" for HuggingFace or use full identifier (e.g., local:intfloat/multilingual-e5-large)
            llm_params (dict): Parameters for the LLM.
            vector_store_params (dict): Parameters for the vector store.
            service_context_params (dict): Parameters for the service context.
            query_engine_params (dict): Parameters for the query engine.

        Returns:
            A llama_index.BaseQueryEngine instance.
        """

        return create_query_engine(
            documents=documents,
            system_prompt=system_prompt,
            query_wrapper_prompt=query_wrapper_prompt,
            enable_cost_calculator=enable_cost_calculator,
            embed_model=embed_model,
            llm_params=llm_params,
            vector_store_params=vector_store_params,
            service_context_params=service_context_params,
            query_engine_params=query_engine_params)

    @staticmethod
    def from_parameters(
            documents: Sequence[Document] = None,
            system_prompt: str = None,
            query_wrapper_prompt: str = None,
            enable_cost_calculator: bool = True,
            embed_model: Union[str, EmbedType] = "default",  # ["default", "local"]
            llm_params: dict = None,
            vector_store_params: dict = None,
            service_context_params: dict = None,
            query_engine_params: dict = None) -> BaseQueryEngine:
        """
        DEPRECATED. Use AutoQueryEngine.from_defaults instead.

        Create an AutoQueryEngine from parameters.

        Parameters:
            documents (Sequence[Document]): Sequence of llama_index.Document instances.
            system_prompt (str): The system prompt to use for the query engine.
            query_wrapper_prompt (str): The query wrapper prompt to use for the query engine.
            enable_cost_calculator (bool): Flag to enable cost calculator logging.
            embed_model (Union[str, EmbedType]): The embedding model to use for generating embeddings. "default" for OpenAI,
                                                "local" for HuggingFace or use full identifier (e.g., local:intfloat/multilingual-e5-large)
            llm_params (dict): Parameters for the LLM.
            vector_store_params (dict): Parameters for the vector store.
            service_context_params (dict): Parameters for the service context.
            query_engine_params (dict): Parameters for the query engine.

        Returns:
            A llama_index.BaseQueryEngine instance.
        """

        # deprecation warning
        import warnings
        warnings.warn(
            "AutoQueryEngine.from_parameters is deprecated, use AutoQueryEngine.from_defaults instead.",
            DeprecationWarning)

        # call from_defaults
        return AutoQueryEngine.from_defaults(
            documents=documents,
            system_prompt=system_prompt,
            query_wrapper_prompt=query_wrapper_prompt,
            enable_cost_calculator=enable_cost_calculator,
            embed_model=embed_model,
            llm_params=llm_params,
            vector_store_params=vector_store_params,
            service_context_params=service_context_params,
            query_engine_params=query_engine_params)

    @staticmethod
    def from_config(
            config_file_path: str,
            env_file_path: str = None,
            documents: Sequence[Document] = None) -> BaseQueryEngine:
        """
        Create an AutoQueryEngine from a config file and optionally a .env file.

        Parameters:
            config_file_path (str): Path to the YAML configuration file.
            env_file_path (str): Path to the .env file.
            documents (Sequence[Document]): Sequence of llama_index.Document instances.

        Returns:
            A llama_index.BaseQueryEngine instance.
        """

        config = load_config_and_dotenv(config_file_path, env_file_path)
        # Get the first task configuration
        config = config['tasks'][0]

        return create_query_engine(
            documents=documents,
            system_prompt=config.get('system_prompt'),
            query_wrapper_prompt=config.get('query_wrapper_prompt'),
            enable_cost_calculator=config.get('enable_cost_calculator'),
            embed_model=config.get('embed_model', 'default'),
            llm_params=config.get('llm_params'),
            vector_store_params=config.get('vector_store_params'),
            service_context_params=config.get('service_context_params'),
            query_engine_params=config.get('query_engine_params'))
