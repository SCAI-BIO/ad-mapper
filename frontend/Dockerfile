FROM node:18 as build-stage

WORKDIR /app
COPY . .

ENV VUE_APP_BASEPATH=variable-mapper/
ENV VUE_APP_API=https://ad-mapper.scai.fraunhofer.de/api

WORKDIR /app/variable-mapper 
RUN npm install
RUN npm run build

# Stage 2: Serve Vue app with Nginx
FROM nginx:1.25.1 as prod-stage
COPY --from=build-stage /app/variable-mapper/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]