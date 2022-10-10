# start by pulling the python image
FROM amd64/python:3.9-buster

RUN pip install -U pip
RUN pip install --upgrade setuptools
RUN pip install catboost

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# CMD ["__main__.py" ]