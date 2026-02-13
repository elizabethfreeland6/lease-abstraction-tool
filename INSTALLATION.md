# Installation & Deployment Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.11 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB for application and dependencies
- **Internet**: Required for AI processing

### Software Dependencies
- Python 3.11+
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, or Edge)

## Installation Methods

### Method 1: Quick Install (Recommended)

1. **Extract the application:**
```bash
tar -xzf lease_abstraction_tool.tar.gz
cd lease_abstraction_tool
```

2. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# On Linux/macOS
export OPENAI_API_KEY="your_api_key_here"

# On Windows (Command Prompt)
set OPENAI_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"
```

4. **Run the application:**
```bash
# On Linux/macOS
./run.sh

# On Windows
streamlit run app.py
```

### Method 2: Manual Installation

1. **Clone or download the repository:**
```bash
# If using git
git clone <repository_url>
cd lease_abstraction_tool

# Or extract from archive
tar -xzf lease_abstraction_tool.tar.gz
cd lease_abstraction_tool
```

2. **Create a virtual environment (recommended):**
```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
```

5. **Run the application:**
```bash
streamlit run app.py
```

## Configuration

### OpenAI API Key Setup

1. **Obtain an API key:**
   - Visit https://platform.openai.com/api-keys
   - Create an account or sign in
   - Generate a new API key
   - Copy the key (you won't be able to see it again)

2. **Configure the key:**

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="sk-..."
```

**Option B: .env File**
Create a `.env` file in the project directory:
```
OPENAI_API_KEY=sk-...
```

**Option C: System Environment Variable**
- **Windows**: System Properties → Environment Variables
- **macOS/Linux**: Add to `~/.bashrc` or `~/.zshrc`

### Application Settings

The application uses default settings that work for most cases. Advanced users can modify:

**File: `utils/ai_extractor.py`**
- `model`: Change AI model (default: gpt-4.1-mini)
- `temperature`: Adjust extraction consistency (default: 0.1)
- `max_tokens`: Modify response length (default: 2000)

**File: `app.py`**
- Page title and icon
- Upload file size limits
- Session state configuration

## Deployment Options

### Option 1: Local Deployment (Single User)

**Best for**: Individual use, testing, small teams

1. Install on a local machine
2. Run when needed
3. Access at `http://localhost:8501`

**Pros**: Simple, no server needed  
**Cons**: Only accessible on local machine

### Option 2: Network Deployment (Team)

**Best for**: Small teams, department use

1. Install on a network-accessible computer
2. Configure Streamlit to accept external connections:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
3. Access from other computers: `http://<server-ip>:8501`

**Pros**: Team access, centralized  
**Cons**: Requires always-on computer, basic security

### Option 3: Cloud Deployment (Enterprise)

**Best for**: Large teams, enterprise use

#### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Configure secrets (API keys)
4. Deploy with one click

#### AWS/Azure/GCP
1. Set up a virtual machine
2. Install dependencies
3. Configure firewall rules
4. Use reverse proxy (nginx) for HTTPS
5. Set up authentication if needed

**Pros**: Professional, scalable, secure  
**Cons**: Requires cloud expertise, ongoing costs

### Option 4: Docker Deployment

**Best for**: Consistent environments, DevOps workflows

1. **Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

2. **Build and run:**
```bash
docker build -t lease-abstraction-tool .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key lease-abstraction-tool
```

## Security Considerations

### API Key Security
- ✓ Never commit API keys to version control
- ✓ Use environment variables or secrets management
- ✓ Rotate keys periodically
- ✓ Monitor API usage for anomalies

### Application Security
- ✓ Use HTTPS in production (reverse proxy)
- ✓ Implement authentication for team deployments
- ✓ Restrict file upload sizes
- ✓ Regularly update dependencies
- ✓ Monitor for security vulnerabilities

### Data Security
- ✓ Ensure uploaded files are deleted after processing
- ✓ Don't log sensitive tenant information
- ✓ Use secure connections for API calls
- ✓ Comply with data protection regulations (GDPR, CCPA)

## Troubleshooting Installation

### Issue: Python version too old
```bash
# Check Python version
python3 --version

# Install Python 3.11+ from python.org or use package manager
```

### Issue: pip install fails
```bash
# Upgrade pip
pip3 install --upgrade pip

# Try with --user flag
pip3 install --user -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Streamlit won't start
```bash
# Check if port 8501 is in use
lsof -i :8501  # Linux/macOS
netstat -ano | findstr :8501  # Windows

# Use different port
streamlit run app.py --server.port 8502
```

### Issue: OpenAI API errors
```bash
# Verify API key is set
echo $OPENAI_API_KEY  # Linux/macOS
echo %OPENAI_API_KEY%  # Windows

# Test API key
python3 -c "from openai import OpenAI; client = OpenAI(); print('API key valid')"
```

### Issue: Module not found errors
```bash
# Reinstall dependencies
pip3 install -r requirements.txt --force-reinstall

# Check Python path
python3 -c "import sys; print(sys.path)"
```

## Updating the Application

### Update to New Version
```bash
# Backup your current installation
cp -r lease_abstraction_tool lease_abstraction_tool_backup

# Extract new version
tar -xzf lease_abstraction_tool_v2.tar.gz

# Update dependencies
cd lease_abstraction_tool
pip3 install -r requirements.txt --upgrade
```

### Update Dependencies Only
```bash
pip3 install -r requirements.txt --upgrade
```

## Uninstallation

### Remove Application
```bash
# If using virtual environment
deactivate
rm -rf venv

# Remove application directory
rm -rf lease_abstraction_tool

# Remove package archive
rm lease_abstraction_tool.tar.gz
```

### Remove Python Packages
```bash
pip3 uninstall -r requirements.txt -y
```

## Performance Optimization

### For Large Batches
1. Increase system resources (RAM, CPU)
2. Process documents in smaller batches
3. Consider cloud deployment with auto-scaling

### For Faster Processing
1. Use faster AI model (if available)
2. Reduce max_tokens in AI extraction
3. Optimize PDF processing settings

### For Multiple Users
1. Deploy on server with adequate resources
2. Use load balancing for high traffic
3. Implement caching strategies

## Backup and Maintenance

### Regular Backups
```bash
# Backup application
tar -czf backup_$(date +%Y%m%d).tar.gz lease_abstraction_tool/

# Backup exports
tar -czf exports_backup_$(date +%Y%m%d).tar.gz lease_abstraction_tool/exports/
```

### Maintenance Tasks
- Weekly: Check for dependency updates
- Monthly: Review API usage and costs
- Quarterly: Security audit and key rotation
- Annually: Major version updates

## Support and Resources

### Documentation
- `README.md` - Technical overview
- `USER_GUIDE.md` - User instructions
- `INSTALLATION.md` - This file

### Getting Help
1. Check documentation first
2. Review error messages carefully
3. Search for similar issues online
4. Check Streamlit and OpenAI documentation

### Useful Links
- Streamlit Documentation: https://docs.streamlit.io
- OpenAI API Documentation: https://platform.openai.com/docs
- Python Documentation: https://docs.python.org

---

**Installation Complete!** You're ready to start abstracting leases. See `USER_GUIDE.md` for usage instructions.
