FROM python:3.6

RUN mkdir /usr/src/app
RUN mkdir /usr/src/app/static
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_md
RUN python -m spacy link en_core_web_md en

COPY ./NLU-Core/data /usr/src/app/NLUdata

RUN python -m rasa_nlu.train -c NLUdata/nlu_config.yml --data NLUdata/nlu_data.md -o models --fixed_model_name nlu --project current --verbose

RUN python -m rasa_core.train -d NLUdata/domain.yml -s NLUdata/stories.md -o models/current/dialogue --epochs 200

COPY . /usr/src/app

EXPOSE 5005

CMD ["./entrypoint.sh"]

