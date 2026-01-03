# Multi-stage build for React dashboard
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build argument for API URL (defaults to localhost for standalone, or api:8000 for docker-compose)
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# Build for production
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install serve and curl for healthcheck
RUN npm install -g serve && \
    apk add --no-cache curl

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Start the server
CMD ["serve", "-s", "dist", "-l", "3000"]

