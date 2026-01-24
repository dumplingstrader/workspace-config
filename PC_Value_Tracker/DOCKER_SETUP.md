# PC Value Tracker - Docker Setup Guide

## Prerequisites
- Docker Desktop installed
- Docker Compose installed (included with Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended)
```bash
# Build and start container
docker-compose up -d

# Enter container
docker-compose exec pc-value-tracker bash

# Inside container - run scripts
python scripts/generate_monthly_report.py --input data/master_combined.json --month 2026-01
python scripts/generate_quarterly_insights.py --input data/master_combined.json --quarter 2026-Q1
python scripts/create_leadership_presentation_template.py --quarter 2025-Q4 --input data/master_combined.json

# Exit container
exit

# Stop container
docker-compose down
```

### Option 2: Using Docker directly
```bash
# Build image
docker build -t pc-value-tracker .

# Run container with volume mounts
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/submissions:/app/submissions \
  -v $(pwd)/templates:/app/templates \
  pc-value-tracker

# Inside container - run scripts (same as above)
```

## Container Structure

```
/app/                           ← Working directory
├── requirements.txt            ← Python dependencies (auto-installed)
├── scripts/                    ← Python scripts
│   ├── generate_monthly_report.py
│   ├── generate_quarterly_insights.py
│   ├── create_monthly_report_template.py
│   └── create_leadership_presentation_template.py
├── data/                       ← Mounted volume (persistent)
│   └── master_combined.json
├── output/                     ← Mounted volume (persistent)
├── submissions/                ← Mounted volume (persistent)
├── templates/                  ← Mounted volume (persistent)
└── docs/                       ← Documentation
```

## Volume Mounts
All data directories are mounted as volumes for persistence:
- `./data:/app/data` - Master JSON data
- `./output:/app/output` - Generated reports
- `./submissions:/app/submissions` - Team submissions
- `./templates:/app/templates` - Template files

Files created in these directories persist after container stops.

## Development Workflow

### 1. Start Container
```bash
docker-compose up -d
docker-compose exec pc-value-tracker bash
```

### 2. Generate Reports (Inside Container)
```bash
# Monthly report for January 2026
python scripts/generate_monthly_report.py \
  --input data/master_combined.json \
  --month 2026-01 \
  --output output/monthly_report_2026-01.xlsx

# Quarterly insights for Q4 2025
python scripts/generate_quarterly_insights.py \
  --input data/master_combined.json \
  --quarter 2025-Q4 \
  --output output/quarterly_insights_2025-Q4.xlsx

# Blank PowerPoint template
python scripts/create_leadership_presentation_template.py

# Auto-filled presentation from Q4 2025 data
python scripts/create_leadership_presentation_template.py \
  --quarter 2025-Q4 \
  --input data/master_combined.json
```

### 3. Access Generated Files
All output files are available on host machine in `./output/` directory.

### 4. Stop Container
```bash
exit  # Exit bash
docker-compose down
```

## Troubleshooting

### Permission Issues
If you encounter permission errors on Linux/Mac:
```bash
# Fix ownership
sudo chown -R $USER:$USER data/ output/ submissions/ templates/
```

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Python Package Issues
```bash
# Rebuild with fresh dependencies
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Transferring to Another Machine

### Export Container
```bash
# Save image
docker save pc-value-tracker:latest | gzip > pc-value-tracker.tar.gz

# Transfer pc-value-tracker.tar.gz to new machine

# Load image on new machine
docker load < pc-value-tracker.tar.gz
```

### Export Project (Without Docker)
```bash
# On current machine
tar -czf pc-value-tracker-project.tar.gz \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='.git' \
  --exclude='output/*.xlsx' \
  --exclude='output/*.pptx' \
  .

# Transfer to new machine and extract
tar -xzf pc-value-tracker-project.tar.gz

# Build and run on new machine
docker-compose up -d
```

## Container vs Local Development

| Feature | Docker Container | Local Python |
|---------|-----------------|--------------|
| **Setup** | `docker-compose up -d` | `python -m venv .venv; pip install -r requirements.txt` |
| **Isolation** | Fully isolated environment | Uses system Python/venv |
| **Portability** | Works identically everywhere | May have OS differences |
| **Performance** | Slight overhead | Native speed |
| **Data Persistence** | Via volume mounts | Direct file access |
| **Best For** | Cross-machine consistency | Quick local iteration |

## Environment Variables

Set in `docker-compose.yml` or via `-e` flag:
```yaml
environment:
  - PYTHONUNBUFFERED=1          # Real-time console output
  - PYTHONDONTWRITEBYTECODE=1   # No .pyc files
```

## Next Steps
1. Place `master_combined.json` in `data/` directory
2. Start container: `docker-compose up -d`
3. Enter container: `docker-compose exec pc-value-tracker bash`
4. Run scripts (see Development Workflow above)
5. Access output files from host machine `output/` directory

## Support
See main README.md and SETUP.md for detailed usage instructions.
