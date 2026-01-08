# Experion HMI FAT Documentation

Factory Acceptance Test support documentation and checklists for Honeywell Experion R520 HMI graphics validation.

## Contents

- **Experion_HMI_FAT_Support_Document_REVISED.md** - Main FAT support document with comprehensive checklists
- **Experion_HMI_Copilot_Prompts.md** - VS Code Copilot prompts for HMI development tasks
- **Graphics/Checklist.md** - Graphics validation checklist reference

## Docker Setup

### Option 1: VS Code Dev Container (Recommended)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Install [VS Code](https://code.visualstudio.com/) with the **Dev Containers** extension
3. Open this folder in VS Code
4. Click "Reopen in Container" when prompted (or press F1 → "Dev Containers: Reopen in Container")
5. VS Code will build the container and reopen with all tools installed

### Option 2: Docker Compose

```powershell
# Build and start the container
docker-compose up -d

# Access the container shell
docker-compose exec documentation bash

# Stop the container
docker-compose down
```

### Option 3: Standard Docker

```powershell
# Build the image
docker build -t experion-hmi-docs .

# Run the container
docker run -it -v ${PWD}:/workspace -p 8080:8080 experion-hmi-docs

# Or run on Linux/Mac
docker run -it -v $(pwd):/workspace -p 8080:8080 experion-hmi-docs
```

## Tools Included

- **markdownlint-cli** - Markdown linting
- **markdown-pdf** - PDF generation from markdown
- **markdown-link-check** - Verify links in documentation
- **Git** - Version control

## Usage Examples

```bash
# Lint markdown files
markdownlint *.md

# Check for broken links
markdown-link-check Experion_HMI_FAT_Support_Document_REVISED.md

# Generate PDF (if needed)
markdown-pdf Experion_HMI_FAT_Support_Document_REVISED.md
```

## Sharing with Team

1. **Share the folder** - Zip the entire directory and share, or use Git
2. **Recipients open in VS Code** - They'll be prompted to open in container
3. **Identical environment** - Everyone works in the same containerized setup

## Standards Reference

- **AMP-LAR-AUT-SPC-0050 Rev 1** - Honeywell HMI Style Guide
- **Experion R520** - Target PKS version
- **ASM Protocols** - Abnormal Situation Management (grayscale graphics)

## Contact

Marathon Petroleum Process Controls Engineer (PCE)
