FROM public.ecr.aws/lambda/python:3.11
# Pre-install setuptools
RUN pip install setuptools

# Copy requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]