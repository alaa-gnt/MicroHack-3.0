# Stage 1: Build
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install --network-timeout=100000
COPY . .
# Set API URL for build time
ENV VITE_API_URL=http://localhost:8000/api/v1
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
# Copy custom nginx config if needed, or just use default
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
