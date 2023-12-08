FROM node:14-slim
LABEL authors="hugohu"

WORKDIR /app

COPY . /app

RUN pip install npm
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install -g aws-cdk

EXPOSE 8080

CMD ["sh", "-c", "cdk bootstrap && cdk synth & cdk deploy"]


