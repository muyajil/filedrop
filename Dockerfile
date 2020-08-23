FROM continuumio/miniconda3:4.8.2

SHELL ["/bin/bash", "-c"]

ADD ./environment.yml /environment.yml

RUN conda update -n base -c defaults conda
RUN conda env create -f /environment.yml
RUN echo "source activate filedrop" > ~/.bashrc
ENV PATH /opt/conda/envs/filedrop/bin:$PATH
RUN mkdir /uploads
ENV UPLOAD_PATH /uploads

ADD ./filedrop /filedrop

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--timeout", "120", "--workers", "4", "--bind", "0.0.0.0:5000", "filedrop.app:create_app()"]