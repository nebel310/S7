FROM node:23.10

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

# Запускаем приложение
CMD ["npm", "run", "dev"]