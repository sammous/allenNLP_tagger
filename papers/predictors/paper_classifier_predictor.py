from typing import Tuple, List

from overrides import overrides

from allennlp.common.util import JsonDict
from allennlp.data import Instance
from allennlp.service.predictors.predictor import Predictor

@Predictor.register('paper-classifier')
class PaperClassifierPredictor(Predictor):
    """"Predictor wrapper for the AcademicPaperClassifier"""
    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Tuple[Instance, JsonDict]:
        text = json_dict['text']
        instance = self._dataset_reader.text_to_instance(text=text)
        return instance, {}
