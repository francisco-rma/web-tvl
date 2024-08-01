FROM node:20 as buildContainer

WORKDIR /app

COPY ./package.json ./package-lock.json /app/

RUN npm install

COPY ./ /app/

RUN npm run build

FROM node:20-alpine

WORKDIR /app
COPY --from=buildContainer /app/package.json /app

# Get all the code needed to run the app
COPY --from=buildContainer /app/dist /app/dist

EXPOSE 4000
EXPOSE 443

ENV NODE_ENV production
CMD ["npm", "run", "serve:ssr:ui"]