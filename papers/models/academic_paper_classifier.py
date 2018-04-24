from typing import Dict, Optional

import numpy
from overrides import overrides
import torch
import torch.nn.functional as F

from allennlp.common import Params
from allennlp.common.checks import ConfigurationError
from allennlp.data import Vocabulary
from allennlp.modules import FeedForward, Seq2VecEncoder, TextFieldEmbedder
from allennlp.models.model import Model
from allennlp.nn import InitializerApplicator, RegularizerApplicator
from allennlp.nn import util

from papers.training.metrics.multilabel_f1 import MultiLabelF1Measure

@Model.register("paper_classifier")
class AcademicPaperClassifier(Model):
    """
    This ``Model`` performs text classification for an academic paper.  We assume we're given a
    title and an abstract, and we predict some output label.
python -m allennlp.run train experiments/venue_classifier.json -s /tmp/your_output_dir_here --include-package my_library

    The basic model structure: we'll embed the title and the abstract, and encode each of them with
    separate Seq2VecEncoders, getting a single vector representing the content of each.  We'll then
    concatenate those two vectors, and pass the result through a feedforward network, the output of
    which we'll use as our scores for each label.

    Parameters
    ----------
    vocab : ``Vocabulary``, required
        A Vocabulary, required in order to compute sizes for input/output projections.
    text_field_embedder : ``TextFieldEmbedder``, required
        Used to embed the ``tokens`` ``TextField`` we get as input to the model.
    title_encoder : ``Seq2VecEncoder``
        The encoder that we will use to convert the title to a vector.
    abstract_encoder : ``Seq2VecEncoder``
        The encoder that we will use to convert the abstract to a vector.
    classifier_feedforward : ``FeedForward``
    initializer : ``InitializerApplicator``, optional (default=``InitializerApplicator()``)
        Used to initialize the model parameters.
    regularizer : ``RegularizerApplicator``, optional (default=``None``)
        If provided, will be used to calculate the regularization penalty during training.
    """
    def __init__(self, vocab: Vocabulary,
                 text_field_embedder: TextFieldEmbedder,
                 text_encoder: Seq2VecEncoder,
                 classifier_feedforward: FeedForward,
                 initializer: InitializerApplicator = InitializerApplicator(),
                 regularizer: Optional[RegularizerApplicator] = None) -> None:
        super(AcademicPaperClassifier, self).__init__(vocab, regularizer)

        self.text_field_embedder = text_field_embedder
        self.num_classes = self.vocab.get_vocab_size("labels")
        self.text_encoder = text_encoder
        self.classifier_feedforward = classifier_feedforward

        if text_field_embedder.get_output_dim() != text_encoder.get_input_dim():
            raise ConfigurationError("The output dimension of the text_field_embedder must match the "
                                     "input dimension of the title_encoder. Found {} and {}, "
                                     "respectively.".format(text_field_embedder.get_output_dim(),
                                                            text_encoder.get_input_dim()))

        self.f1 = MultiLabelF1Measure()
        self.loss = torch.nn.MultiLabelSoftMarginLoss()

        initializer(self)

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        precision, recall, f1 = self.f1.get_metric(reset)
        return {
            "precision": precision,
            "recall": recall,
            "f1": f1
    }

    @overrides
    def forward(self,  # type: ignore
                text: Dict[str, torch.LongTensor],
                labels: torch.LongTensor = None) -> Dict[str, torch.Tensor]:
        # pylint: disable=arguments-differ
        """
        Parameters
        ----------
        text : Dict[str, Variable], required
            The output of ``TextField.as_array()``.
        labels : Variable, optional (default = None)
            A variable representing the label for each instance in the batch.

        Returns
        -------
        An output dictionary consisting of:
        class_probabilities : torch.FloatTensor
            A tensor of shape ``(batch_size, num_classes)`` representing a distribution over the
            label classes for each instance.
        loss : torch.FloatTensor, optional
            A scalar loss to be optimised.
        """
        embedded_text = self.text_field_embedder(text)
        text_mask = util.get_text_field_mask(text)
        encoded_text = self.text_encoder(embedded_text, text_mask)

        logits = self.classifier_feedforward(torch.cat([encoded_text], dim=-1))
        probabilities = torch.nn.functional.sigmoid(logits)
        output_dict = {'logits': logits,
                       "probabilities": probabilities}
        if labels is not None:
            loss = self.loss(logits, labels.squeeze(-1).float())
            label_data = labels.squeeze(-1).data.long()
            predictions = (logits.data > 0.0).long()
            self.f1(predictions, label_data)
            output_dict["loss"] = loss

        return output_dict


    @overrides
    def decode(self, output_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Does a simple argmax over the class probabilities, converts indices to string labels, and
        adds a ``"label"`` key to the dictionary with the result.
        """
        class_probabilities = F.softmax(output_dict['logits'], dim=-1)

        predictions = class_probabilities.cpu().data.numpy()
        top5_indexes = predictions.argsort()[-5:][::-1]
        top5_predictions = predictions[top5_indexes]
        labels = [self.vocab.get_token_from_index(x, namespace="labels")
                  for x in top5_indexes]
        output_dict['top5'] = dict(zip(labels, top5_predictions))
        output_dict['all_predictions'] = predictions
        output_dict['all_labels_predictions'] = self.vocab.get_index_to_token_vocabulary('labels')
        return output_dict

    @classmethod
    def from_params(cls, vocab: Vocabulary, params: Params) -> 'AcademicPaperClassifier':
        embedder_params = params.pop("text_field_embedder")
        text_field_embedder = TextFieldEmbedder.from_params(vocab, embedder_params)
        text_encoder = Seq2VecEncoder.from_params(params.pop("text_encoder"))
        classifier_feedforward = FeedForward.from_params(params.pop("classifier_feedforward"))

        initializer = InitializerApplicator.from_params(params.pop('initializer', []))
        regularizer = RegularizerApplicator.from_params(params.pop('regularizer', []))

        return cls(vocab=vocab,
                   text_field_embedder=text_field_embedder,
                   text_encoder=text_encoder,
                   classifier_feedforward=classifier_feedforward,
                   initializer=initializer,
                   regularizer=regularizer)
