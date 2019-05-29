{% if cookiecutter.use_intel_python == "yes" %}
FROM continuumio/miniconda3:latest
{% else %}
FROM python:3.7
{% endif %}

RUN addgroup --system critsandcoffee \
    && adduser --system --group api_admin

RUN mkdir /API_CODE
WORKDIR /API_CODE

COPY . /API_CODE/

{% if cookiecutter.use_intel_python == "yes" %}
COPY requirements.pip.txt requirements.pip.txt
COPY requirements.conda.txt requirements.conda.txt
RUN conda update conda
RUN conda install pip
RUN pip install -U pip
RUN pip install -r requirements.pip.txt
RUN conda install --file=requirements.conda.txt
RUN conda install -c anaconda gunicorn
RUN conda update --update-all
{% else %}
RUN pip install -r requirements.pip.txt
{% endif %}

{% if cookiecutter.use_celery == "yes" %}
# needed for docker-compose file that use redis as result-backend
RUN pip install celery[redis]
{% endif %}

COPY ./Docker_scripts/start /start
RUN chmod +x /start
RUN chown api_admin /start

COPY ./Docker_scripts/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown api_admin /entrypoint


RUN chown -R api_admin /API_CODE

USER api_admin

ENTRYPOINT ["/entrypoint"]