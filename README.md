# Academic Paper classifier based on SCOPUS categories

## Usage
Paper classifier taking as input a JSON with follow fields :

```
title: string,
abstract: string
```

And returning probabilities for 4 categories :
- health sciences
- life sciences
- physical sciences
- social sciences

## Training

To train a model :

```
python -m allennlp.run train allen_trainer/scopus_classifier.json \
    -s model \
    --include-package papers
```
## Making Predictions

```
allennlp predict model/model.tar.gz \
    scopus_test.json \
    --include-package papers \
    --predictor paper-classifier \
    --output-file scopus_test_pred.json
```

## Running web server to demo

```
python -m allennlp.service.server_simple \
    --archive-path model/model.tar.gz \
    --predictor paper-classifier \
    --include-package papers \
    --title "Paper classifier based on SCOPUS categories" \
    --field-name title \
    --field-name abstract
```
