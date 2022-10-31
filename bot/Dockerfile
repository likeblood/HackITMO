FROM python:3.8

# copy the requirements file into the image
COPY ./requirements.txt /bot/requirements.txt

# switch working directory
WORKDIR /bot

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# copy every content from the local file to the image
COPY . /bot
