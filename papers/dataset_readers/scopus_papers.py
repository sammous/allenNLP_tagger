from typing import Dict, List
import json
import logging
import csv
from overrides import overrides
import tqdm

from allennlp.common import Params
from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import LabelField, TextField, ListField, MetadataField
from allennlp.data.instance import Instance
from allennlp.data.tokenizers import Tokenizer, WordTokenizer
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@DatasetReader.register("scopus")
class ScopusDatasetReader(DatasetReader):
    """
    Reads a JSON-lines file containing papers from the Semantic Scholar database, and creates a
    dataset suitable for document classification using these papers.

    Expected format for each input line: {"paperAbstract": "text", "title": "text", "venue": "text"}

    The JSON could have other fields, too, but they are ignored.

    The output of ``read`` is a list of ``Instance`` s with the fields:
        title: ``TextField``
        abstract: ``TextField``
        labels: List(``LabelField``)

    where the ``label`` is derived from the venue of the paper.

    Parameters
    ----------
    lazy : ``bool`` (optional, default=False)
        Passed to ``DatasetReader``.  If this is ``True``, training will start sooner, but will
        take longer per batch.  This also allows training with datasets that are too large to fit
        in memory.
    tokenizer : ``Tokenizer``, optional
        Tokenizer to use to split the title and abstrct into words or other kinds of tokens.
        Defaults to ``WordTokenizer()``.
    token_indexers : ``Dict[str, TokenIndexer]``, optional
        Indexers used to define input token representations. Defaults to ``{"tokens":
        SingleIdTokenIndexer()}``.
    """
    def __init__(self,
                 lazy: bool = True,
                 tokenizer: Tokenizer = None,
                 token_indexers: Dict[str, TokenIndexer] = None) -> None:
        super().__init__(lazy)
        self._tokenizer = tokenizer or WordTokenizer()
        self._token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}

    @overrides
    def _read(self, file_path):
        with open(file_path, 'r') as data_file:
            reader = csv.reader(data_file)
            _, _, _, *labels_header = next(reader, None)  # skip the headers
            for row in tqdm.tqdm(reader):
                abstract, _, title, *labels = row
                yield self.text_to_instance(title, abstract, labels)

    @overrides
    def text_to_instance(self, title: str, abstract: str, labels: List[str] = None) -> Instance:  # type: ignore
        # pylint: disable=arguments-differ
        tokenized_title = self._tokenizer.tokenize(title)
        tokenized_abstract = self._tokenizer.tokenize(abstract)
        title_field = TextField(tokenized_title, self._token_indexers)
        abstract_field = TextField(tokenized_abstract, self._token_indexers)
        fields = {'title': title_field, 'abstract': abstract_field}
        if not labels:
            labels = [0 for i in range(len(labels))]

        # Because the labels are already 0 or 1, skip_indexing.
        fields['labels'] = ListField([
        LabelField((label, int(l)), skip_indexing=True) for (l, i) in zip(self.labels_header, labels)
        ])

        return Instance(fields)

    @classmethod
    def from_params(cls, params: Params) -> 'ScopusDatasetReader':
        lazy = params.pop('lazy', True)
        tokenizer = Tokenizer.from_params(params.pop('tokenizer', {}))
        token_indexers = TokenIndexer.dict_from_params(params.pop('token_indexers', {}))
        params.assert_empty(cls.__name__)
        return cls(lazy=lazy, tokenizer=tokenizer, token_indexers=token_indexers)

@DatasetReader.register("scopus_text")
class ScopusTextDatasetReader(DatasetReader):
    """
    Reads a JSON-lines file containing papers from the Semantic Scholar database, and creates a
    dataset suitable for document classification using these papers.

    Expected format for each input line: {"text": "text", labels: List(int)}

    The JSON could have other fields, too, but they are ignored.

    The output of ``read`` is a list of ``Instance`` s with the fields:
        text: ``TextField``
        labels: List(``LabelField``)

    where the ``label`` is derived from the venue of the paper.

    Parameters
    ----------
    lazy : ``bool`` (optional, default=False)
        Passed to ``DatasetReader``.  If this is ``True``, training will start sooner, but will
        take longer per batch.  This also allows training with datasets that are too large to fit
        in memory.
    tokenizer : ``Tokenizer``, optional
        Tokenizer to use to split the title and abstrct into words or other kinds of tokens.
        Defaults to ``WordTokenizer()``.
    token_indexers : ``Dict[str, TokenIndexer]``, optional
        Indexers used to define input token representations. Defaults to ``{"tokens":
        SingleIdTokenIndexer()}``.
    """
    def __init__(self,
                 lazy: bool = True,
                 tokenizer: Tokenizer = None,
                 token_indexers: Dict[str, TokenIndexer] = None) -> None:
        super().__init__(lazy)
        self._tokenizer = tokenizer or WordTokenizer()
        self._token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}

    @overrides
    def _read(self, file_path):
        with open(file_path, 'r') as data_file:
            reader = csv.reader(data_file)
            _, _, _, *labels_header = next(reader, None)  # skip the headers
            for row in tqdm.tqdm(reader):
                abstract, _, title, *labels = row
                text = ' '.join([title, abstract])
                yield self.text_to_instance(text, labels, labels_header)

    @overrides
    def text_to_instance(self, text: str, labels: List[str] = None, header: List[str] = None) -> Instance:  # type: ignore
        # pylint: disable=arguments-differ
        tokenized_text = self._tokenizer.tokenize(text)
        text_field = TextField(tokenized_text, self._token_indexers)
        fields = {'text': text_field}
        if not labels:
            labels = [0 for i in range(237)]

        fields['labels'] = ListField([
        LabelField(int(l), skip_indexing=True) for l in labels
        ])
        fields['metadata'] = MetadataField(header)
        return Instance(fields)

    @classmethod
    def from_params(cls, params: Params) -> 'ScopusDatasetReader':
        lazy = params.pop('lazy', True)
        tokenizer = Tokenizer.from_params(params.pop('tokenizer', {}))
        token_indexers = TokenIndexer.dict_from_params(params.pop('token_indexers', {}))
        params.assert_empty(cls.__name__)
        return cls(lazy=lazy, tokenizer=tokenizer, token_indexers=token_indexers)
