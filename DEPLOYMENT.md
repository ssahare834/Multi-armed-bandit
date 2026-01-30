# Deployment Guide

This guide covers deploying the Multi-Armed Bandit News Recommender to various platforms.

## Table of Contents

1. [Streamlit Cloud (Recommended)](#streamlit-cloud)
2. [Heroku](#heroku)
3. [AWS EC2](#aws-ec2)
4. [Docker](#docker)
5. [Google Cloud Platform](#gcp)

---

## Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy this app with zero configuration.

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/bandit-recommender.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Choose main branch
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://yourusername-bandit-recommender.streamlit.app`

### Configuration

The app uses `.streamlit/config.toml` for theming and settings. No additional configuration needed!

---

## Heroku

Deploy to Heroku for more control over the deployment environment.

### Prerequisites
- Heroku CLI installed
- Heroku account

### Steps

1. **Create required files**

   Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

   Create `runtime.txt`:
   ```
   python-3.11.0
   ```

2. **Initialize Heroku app**
   ```bash
   heroku login
   heroku create your-bandit-app-name
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Open your app**
   ```bash
   heroku open
   ```

### Cost
- Free tier available (with limitations)
- Hobby tier: $7/month
- Professional: $25/month

---

## AWS EC2

For production deployments with custom scaling.

### Prerequisites
- AWS account
- SSH key pair

### Steps

1. **Launch EC2 Instance**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.medium (recommended) or t2.small (minimum)
   - Security Group: Open port 8501

2. **Connect to instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements.txt
   ```

4. **Run with systemd**

   Create `/etc/systemd/system/bandit-app.service`:
   ```ini
   [Unit]
   Description=Bandit Recommender App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/bandit-recommender
   ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable bandit-app
   sudo systemctl start bandit-app
   ```

5. **Access app**: `http://your-ec2-ip:8501`

### Optional: Use Nginx as reverse proxy

1. **Install Nginx**
   ```bash
   sudo apt install nginx
   ```

2. **Configure Nginx**
   
   Create `/etc/nginx/sites-available/bandit`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

3. **Enable site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/bandit /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## Docker

Containerize your app for consistent deployments.

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and run

```bash
# Build image
docker build -t bandit-recommender .

# Run container
docker run -p 8501:8501 bandit-recommender

# Run with docker-compose
docker-compose up
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

### Deploy to Docker Hub

```bash
# Tag image
docker tag bandit-recommender yourusername/bandit-recommender:latest

# Push to Docker Hub
docker push yourusername/bandit-recommender:latest
```

---

## Google Cloud Platform (GCP)

Deploy to Google Cloud Run for serverless deployment.

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Steps

1. **Build and push to Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/your-project-id/bandit-recommender
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy bandit-recommender \
     --image gcr.io/your-project-id/bandit-recommender \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8501
   ```

3. **Your app will be live at**: The URL provided by Cloud Run

### Cost
- Pay per use
- Generous free tier
- ~$0.40 per million requests

---

## Performance Optimization

### 1. Caching

Add caching to expensive operations:

```python
import streamlit as st

@st.cache_data
def load_simulation_data(n_rounds):
    # Expensive operation
    return data

@st.cache_resource
def load_environment(seed):
    return NewsEnvironment(seed=seed)
```

### 2. Session State

Use session state to persist data:

```python
if 'environment' not in st.session_state:
    st.session_state.environment = NewsEnvironment()
```

### 3. Lazy Loading

Load visualizations only when needed:

```python
with st.expander("Advanced Metrics"):
    # Only rendered when expanded
    plot_detailed_metrics()
```

---

## Monitoring

### Streamlit Cloud
- Built-in metrics dashboard
- View logs in real-time
- Monitor resource usage

### Self-Hosted
Use tools like:
- **Prometheus** + **Grafana** for metrics
- **ELK Stack** for logs
- **Sentry** for error tracking

---

## SSL/HTTPS

### Streamlit Cloud
- Automatic HTTPS

### Self-Hosted with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Troubleshooting

### App won't start
1. Check Python version: `python --version`
2. Verify dependencies: `pip list`
3. Check logs: `streamlit run app.py --logger.level debug`

### Port already in use
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>
```

### Memory issues
- Reduce simulation size
- Use caching
- Increase instance size

---

## Security Best Practices

1. **Environment Variables**
   - Never commit API keys
   - Use `.env` file (add to `.gitignore`)
   - Use secrets management in production

2. **HTTPS Only**
   - Always use SSL in production
   - Redirect HTTP to HTTPS

3. **Rate Limiting**
   - Implement rate limiting for public apps
   - Use Nginx or CloudFlare

4. **Input Validation**
   - Validate all user inputs
   - Sanitize data before processing

---

## Scaling

### Horizontal Scaling
- Use load balancer (AWS ELB, GCP Load Balancer)
- Multiple app instances
- Shared state with Redis

### Vertical Scaling
- Increase CPU/memory
- Optimize code
- Use caching aggressively

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Streamlit Cloud | ✅ Yes | N/A | Portfolio projects |
| Heroku | Limited | $7-$25/mo | Small apps |
| AWS EC2 | 12 months | $10-$50/mo | Production |
| GCP Cloud Run | Generous | Pay-per-use | Scalable apps |
| Docker (self-host) | N/A | Server cost | Full control |

---

## Support

For deployment issues:
- GitHub Issues: [repo-link]
- Email: your.email@example.com
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)

---

**Last Updated**: January 2026
