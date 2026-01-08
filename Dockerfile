# Documentation Development Environment
FROM node:20-slim

# Install useful markdown and documentation tools
RUN npm install -g \
    markdownlint-cli \
    markdown-pdf \
    markdown-link-check

# Install git for version control
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy workspace files
COPY . /workspace

# Expose port for any potential web previews
EXPOSE 8080

# Default command
CMD ["/bin/bash"]
