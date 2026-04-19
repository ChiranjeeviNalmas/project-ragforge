from app.pipelines.base import BaseRAGPipeline
from app.pipelines.file_search import FileSearchPipeline


# creates the right pipeline based on the pipeline_type string
class PipelineFactory:

    def __init__(self):
        # registry maps pipeline name to its class
        self._registry = {
            "file_search": FileSearchPipeline,
        }

    # instantiates and returns the correct pipeline
    def create(self, pipeline_type: str) -> BaseRAGPipeline:
        if pipeline_type not in self._registry:
            raise ValueError(f"Unknown pipeline: {pipeline_type}. Choose: {list(self._registry)}")
        return self._registry[pipeline_type]()
