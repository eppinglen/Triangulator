FROM continuumio/miniconda3
COPY Triangulator.yml Triangulator.yml
RUN conda env create --name Triangulator --file Triangulator.yml
RUN echo "source activate Triangulator" > ~/.bashrc
ENV PATH /opt/conda/envs/Triangulator/bin:$PATH
COPY app /app
ENTRYPOINT ["python3", "-u", "/app/prescription_app.py"]
