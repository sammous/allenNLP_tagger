# Academic Paper/Document classifier based on SCOPUS categories

## Usage
Paper classifier taking as input a JSON with follow fields :

```
text: string
```

And returning probabilities for over 237 categories extracted from SCOPUS.

## Training

To train a model :

```
python -m allennlp.run train allen_trainer/scopus_classifier.json \
    -s model \
    --include-package papers
```

## Making Predictions

Making predictions on a JSON file :

```
allennlp predict model/model.tar.gz \
    scopus_test.json \
    --include-package papers \
    --predictor paper-classifier \
    --output-file scopus_test_pred.json
```

## Demo

### Visualisation demo for a text classifier.
The folder `demo` contains the front app to demo a model trained via [allenNLP](allennlp.org) with some visualisations. Examples can be previewed on their [demo website](demo.allennlp.org/).
### Requirements

allenNLP server must be running with a classification model (allenNLP simple server) on port `8000`.

Example command :

```
python -m allennlp.service.server_simple \
    --archive-path model/model.tar.gz \
    --predictor paper-classifier \
    --include-package papers \
```
