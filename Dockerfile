FROM continuumio/miniconda3:4.8.2

SHELL ["/bin/bash", "-c"]

ADD ./environment.yml /environment.yml

RUN apt-get update && apt-get install -y cron

RUN conda update -n base -c defaults conda
RUN conda env create -f /environment.yml
RUN echo "source activate filedrop" > ~/.bashrc
ENV PATH /opt/conda/envs/filedrop/bin:$PATH
RUN mkdir /uploads
ENV UPLOAD_PATH /uploads
ENV FLASK_APP=filedrop.app:create_app

ADD ./filedrop /filedrop
ADD entrypoint.sh /entrypoint.sh

RUN touch /var/spool/cron/crontabs/root
RUN flask crontab add

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]