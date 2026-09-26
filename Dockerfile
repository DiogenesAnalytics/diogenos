# jupyter base image
FROM ghcr.io/diogenesanalytics/scipy-notebook:master AS jupyter

# first turn off git safe.directory
RUN git config --global safe.directory '*'

# turn off poetry venv
ENV POETRY_VIRTUALENVS_CREATE=false

# set src target dir
WORKDIR /usr/local/src/diogenos

# get src
COPY . .

# now install source
RUN poetry install

# test base image
FROM ghcr.io/diogenesanalytics/python-testing:master AS testing

# set src target dir
WORKDIR /usr/local/src/diogenos

# get src
COPY . .

# now install development dependencies
RUN poetry install --with dev -C .

# final stage to run nox setup
FROM testing AS final

# Run nox to set up Python versions
RUN nox -s setup_python
