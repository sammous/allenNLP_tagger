FROM allennlp/allennlp:latest

COPY model/ model/
COPY tagger/ tagger/
COPY allen_trainer/ allen_trainer/

EXPOSE 8000

ENTRYPOINT [ "python -m allennlp.service.server_simple \
    --archive-path model/model.tar.gz \
    --predictor paper-classifier \
    --include-package tagger " ]