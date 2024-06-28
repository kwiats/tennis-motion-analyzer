FROM node:current-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install -g serve

COPY . .

RUN npm run build

EXPOSE 4200

CMD ["serve", "-s", "dist", "-l", "4200"]
