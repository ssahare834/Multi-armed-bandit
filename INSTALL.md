# Installation & Setup Guide

Complete guide to setting up the Multi-Armed Bandit News Recommender on your system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Verification](#verification)
4. [Running the Application](#running-the-application)
5. [Development Setup](#development-setup)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- **Python 3.8+** (Python 3.11 recommended)
- **pip** (Python package installer)
- **Git** (for cloning the repository)

### Optional
- **Docker** (for containerized deployment)
- **Virtual environment tool** (venv, conda, or virtualenv)

### Check Your Python Version

```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.11.x` or higher

---

## Installation Methods

### Method 1: Standard Installation (Recommended)

**Step 1: Clone the Repository**

```bash
git clone https://github.com/yourusername/bandit-news-recommender.git
cd bandit-news-recommender
```

**Step 2: Create Virtual Environment (Recommended)**

```bash
# Using venv (built-in)
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

# Using conda
conda create -n bandit python=3.11
conda activate bandit
```

**Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Run the Application**

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

### Method 2: Docker Installation

**Step 1: Install Docker**

- **Windows/Mac**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Follow [official instructions](https://docs.docker.com/engine/install/)

**Step 2: Build and Run**

```bash
# Clone repository
git clone https://github.com/yourusername/bandit-news-recommender.git
cd bandit-news-recommender

# Build Docker image
docker build -t bandit-recommender .

# Run container
docker run -p 8501:8501 bandit-recommender
```

**Using Docker Compose (Alternative)**

```bash
docker-compose up
```

Visit `http://localhost:8501`

---

### Method 3: Quick Test (No Installation)

Try the **live demo**: [https://your-app-url.streamlit.app](https://your-app-url.streamlit.app)

---

## Verification

### Verify Installation

```bash
# Check Python packages
pip list | grep -E "streamlit|numpy|pandas|plotly|scipy"

# Expected output:
# numpy         1.24.3
# pandas        2.0.3
# plotly        5.18.0
# scipy         1.11.4
# streamlit     1.31.0
```

### Run Tests

```bash
# Install pytest (if not already installed)
pip install pytest

# Run all tests
pytest test_algorithms.py -v

# Expected: All tests should pass
```

### Test Application

```bash
# Start the app
streamlit run app.py

# You should see:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

---

## Running the Application

### Basic Usage

```bash
# From project directory with activated virtual environment
streamlit run app.py
```

### Custom Port

```bash
streamlit run app.py --server.port=8080
```

### Custom Host (for remote access)

```bash
streamlit run app.py --server.address=0.0.0.0
```

### Production Mode

```bash
streamlit run app.py --server.headless=true --server.port=8501
```

---

## Development Setup

### Install Development Dependencies

```bash
# Install additional tools
pip install pytest pytest-cov black flake8 mypy jupyter

# Or use requirements-dev.txt if provided
pip install -r requirements-dev.txt
```

### Code Formatting

```bash
# Format code with Black
black *.py

# Check linting
flake8 *.py

# Type checking
mypy *.py
```

### Running Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Open analysis_notebook.ipynb
```

### Development Workflow

```bash
# 1. Make changes to code
vim app.py

# 2. Run tests
pytest

# 3. Format code
black *.py

# 4. Test locally
streamlit run app.py

# 5. Commit changes
git add .
git commit -m "Your message"
git push
```

---

## Troubleshooting

### Issue: `streamlit: command not found`

**Solution:**
```bash
# Ensure streamlit is installed
pip install streamlit

# Or reinstall
pip install --upgrade streamlit

# Check installation
which streamlit
```

---

### Issue: `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
# Activate your virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then reinstall
pip install -r requirements.txt
```

---

### Issue: Port 8501 already in use

**Solution:**

```bash
# Find process using port 8501
# On Linux/Mac:
lsof -i :8501

# On Windows:
netstat -ano | findstr :8501

# Kill the process or use different port
streamlit run app.py --server.port=8502
```

---

### Issue: Application is slow

**Solutions:**

1. **Reduce simulation size**
   - Use fewer rounds (100-500)
   - Reduce number of simulations

2. **Clear cache**
   ```bash
   # Delete Streamlit cache
   rm -rf ~/.streamlit/cache
   ```

3. **Close other applications**
   - Free up RAM
   - Close browser tabs

---

### Issue: Plots not displaying

**Solutions:**

1. **Clear browser cache**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

2. **Try different browser**
   - Chrome, Firefox, or Safari

3. **Check JavaScript**
   - Enable JavaScript in browser settings

---

### Issue: Import errors with scipy

**Solution:**
```bash
# Reinstall scipy with --force
pip install --force-reinstall scipy

# Or install from conda (if using conda)
conda install scipy
```

---

### Issue: Docker build fails

**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t bandit-recommender .

# Check Docker version
docker --version
```

---

### Issue: Virtual environment activation doesn't work

**Windows (PowerShell):**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

---

## Platform-Specific Notes

### Windows

- Use **PowerShell** or **Command Prompt** as administrator
- Backslashes (`\`) in paths
- May need to enable script execution for venv

### macOS

- Xcode Command Line Tools may be required:
  ```bash
  xcode-select --install
  ```
- Use `python3` and `pip3` explicitly if needed

### Linux (Ubuntu/Debian)

- Install additional packages:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-pip python3-venv
  ```

---

## Environment Variables

### Optional Configuration

Create `.env` file (not committed to git):

```bash
# Custom port
STREAMLIT_SERVER_PORT=8501

# Logging level
STREAMLIT_LOGGER_LEVEL=info

# Disable telemetry
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

Load in application:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Next Steps

After successful installation:

1. ✅ Read [QUICKSTART.md](QUICKSTART.md) for basic usage
2. ✅ Explore the application interface
3. ✅ Run sample simulations
4. ✅ Read [README.md](README.md) for detailed documentation
5. ✅ Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options

---

## Getting Help

If you're still stuck:

1. **Check Documentation**: [README.md](README.md)
2. **Search Issues**: [GitHub Issues](https://github.com/yourusername/bandit-recommender/issues)
3. **Ask Question**: Open a new issue
4. **Email**: your.email@example.com

---

## System Requirements

### Minimum
- **OS**: Windows 10, macOS 10.14+, Ubuntu 20.04+
- **RAM**: 2GB
- **Disk**: 500MB free space
- **CPU**: 2 cores
- **Internet**: For installation only

### Recommended
- **OS**: Latest stable version
- **RAM**: 4GB+
- **Disk**: 1GB+ free space
- **CPU**: 4+ cores
- **Internet**: For real-time updates

---

**Happy Installing! 🚀**

*Last updated: January 2026*
