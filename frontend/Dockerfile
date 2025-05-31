FROM node:18-bullseye-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3002

CMD ["npm", "run", "start", "--", "--port", "3002"]
