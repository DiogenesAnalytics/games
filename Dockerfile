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

# add pyenv to the PATH for all shells (login, interactive, non-interactive)
ENV PATH="/root/.pyenv/bin:$PATH"
RUN echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile \
    && echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile \
    && echo 'eval "$(pyenv init -)"' >> ~/.bash_profile \
    && echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile \
    && echo 'export PATH="$HOME/.pyenv/shims:$PATH"' >> ~/.bash_profile

# ensure the shell loads these for non-interactive shells
RUN echo 'if [ -n "$PS1" ]; then . ~/.bash_profile; fi' >> ~/.bashrc

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
