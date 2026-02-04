FROM node:20-slim
WORKDIR /app

# 先搬 package.json 嚟裝 dependencies
COPY package*.json ./
RUN npm install

# 再搬其他 code
COPY . .

# 確保 node_modules/.bin 喺 PATH 入面
ENV PATH /app/node_modules/.bin:$PATH

CMD ["npm", "run", "dev", "--", "--host"]