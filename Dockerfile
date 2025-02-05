# jupyter base image
FROM quay.io/jupyter/scipy-notebook:lab-4.1.5 AS jupyter

# first turn off git safe.directory
RUN git config --global safe.directory '*'

# turn off poetry venv
ENV POETRY_VIRTUALENVS_CREATE=false

# set src target dir
WORKDIR /usr/local/src/games

# get src
COPY . .

# get poetry
RUN pip install poetry

# config max workers
RUN poetry config installer.max-workers 10

# now install source
RUN poetry install

# test base image
FROM python:3.11.8 AS testing

# install pyenv
RUN curl https://pyenv.run | bash

# Configure pyenv in the shell
ENV PATH="/root/.pyenv/bin:$PATH"
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc \
    && echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# turn off poetry venv
ENV POETRY_VIRTUALENVS_CREATE=false

# set src target dir
WORKDIR /usr/local/src/games

# get src
COPY . .

# get poetry
RUN pip install poetry

# config max workers
RUN poetry config installer.max-workers 10

# now install development dependencies
RUN poetry install --with dev -C .
