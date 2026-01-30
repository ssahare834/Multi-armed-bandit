# Quick Start Guide

Get your Multi-Armed Bandit News Recommender running in 5 minutes!

## 🚀 Installation

### Option 1: Local Installation (Recommended for Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bandit-news-recommender.git
   cd bandit-news-recommender
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

### Option 2: Docker

```bash
# Build the image
docker build -t bandit-recommender .

# Run the container
docker run -p 8501:8501 bandit-recommender

# Visit http://localhost:8501
```

### Option 3: Try the Live Demo

Visit the deployed version: **[Live Demo](https://your-app-url.streamlit.app)**

---

## 📖 Basic Usage

### 1. Configure Your Simulation

In the **sidebar**, you can:
- 📊 Set number of rounds (100-5000)
- 🎯 Select which algorithms to compare
- ⚙️ Adjust algorithm parameters:
  - **Epsilon** for Epsilon-Greedy (0.0 to 1.0)
  - **Confidence (c)** for UCB (0.1 to 5.0)

### 2. Run the Simulation

Click the **"🚀 Run Simulation"** button to:
- Simulate user interactions with news articles
- Train all selected algorithms simultaneously
- Generate performance metrics and visualizations

### 3. Analyze Results

Navigate through the tabs:

**📊 Overview**
- System summary and metrics
- Algorithm explanations
- Optimal article information

**📈 Performance Comparison**
- Cumulative regret curves
- CTR evolution over time
- Statistical comparison table
- Arm selection frequencies

**🎯 Algorithm Details**
- Per-algorithm metrics
- Value estimates vs true CTRs
- Thompson Sampling distributions
- Confidence intervals

**📰 Articles Info**
- All articles with their true CTRs
- Category distribution
- Best article highlighted

**📥 Export Results**
- Download simulation data as JSON
- Download comparison table as CSV
- View summary report

---

## 🎓 Understanding the Results

### Cumulative Regret
- **What it shows**: How much reward was lost by not always picking the best article
- **Lower is better**: Efficient learning minimizes regret
- **Log scale**: Shows that UCB and Thompson Sampling achieve logarithmic regret

### Click-Through Rate (CTR)
- **What it shows**: Percentage of articles clicked over time
- **Convergence**: All algorithms should approach the optimal CTR (red line)
- **Speed**: Thompson Sampling typically converges fastest

### Arm Selection Frequency
- **What it shows**: How often each article was recommended
- **Best article**: Should be selected most frequently
- **Exploration**: Some selection of suboptimal articles is necessary for learning

---

## 🔬 Experiments to Try

### Experiment 1: Impact of Epsilon
1. Run with ε = 0.01 (little exploration)
2. Run with ε = 0.3 (lots of exploration)
3. Compare regret and CTR

**Expected**: Higher epsilon explores more but may have higher regret

### Experiment 2: UCB Confidence Parameter
1. Run with c = 0.5 (conservative)
2. Run with c = 5.0 (optimistic)
3. Compare performance

**Expected**: Moderate c (around √2) performs best

### Experiment 3: Algorithm Comparison
1. Run all three algorithms with default settings
2. Compare over 1000 rounds

**Expected**: Thompson Sampling usually wins, but all converge eventually

### Experiment 4: Different Time Horizons
1. Run with 100 rounds
2. Run with 5000 rounds
3. Compare how regret scales

**Expected**: Regret grows logarithmically for UCB and Thompson Sampling

---

## 💡 Tips for Best Results

1. **Start with default parameters** to get a baseline
2. **Run multiple simulations** (increase "Simulations for Comparison") for more reliable results
3. **Use longer time horizons** (1000+ rounds) to see clear convergence
4. **Export your results** to compare different configurations
5. **Read the "About" section** for algorithm explanations

---

## 🐛 Troubleshooting

### App won't start
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Simulation is slow
- Reduce number of rounds
- Reduce number of simulations
- Close other applications

### Plots not showing
- Refresh the page
- Clear browser cache
- Try a different browser

### Import errors
```bash
# Make sure you're in the correct directory
cd bandit-news-recommender

# Install missing packages
pip install streamlit numpy pandas plotly scipy
```

---

## 📚 Next Steps

### Learn More
- Read the [full README](README.md) for detailed documentation
- Explore the [Jupyter notebook](analysis_notebook.ipynb) for mathematical derivations
- Check out the [blog post](blog_post.md) for project insights

### Extend the Project
- Add new bandit algorithms (Gradient Bandit, EXP3)
- Implement contextual features with real user data
- Connect to a real-time data source
- Add A/B test comparison mode

### Deploy Your Own
- Follow the [Deployment Guide](DEPLOYMENT.md)
- Customize the UI and branding
- Add your own articles and CTRs

---

## 🎯 Key Takeaways

After running the simulation, you should understand:

✅ **Exploration vs Exploitation**: Why balancing both is crucial  
✅ **Algorithm Trade-offs**: When to use each algorithm  
✅ **Regret Minimization**: How algorithms learn over time  
✅ **Real-world Application**: How this applies to recommendation systems

---

## 🤝 Contributing

Found a bug or have a feature request?
1. Check [existing issues](https://github.com/yourusername/bandit-recommender/issues)
2. Open a new issue with details
3. Submit a pull request

---

## 📞 Get Help

- **Documentation**: [README.md](README.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/bandit-recommender/issues)
- **Email**: your.email@example.com

---

## ⭐ Enjoying the Project?

If you find this helpful:
- ⭐ Star the repository
- 🐦 Share on social media
- 📝 Write a blog post about your experiments
- 🤝 Contribute improvements

---

**Happy Experimenting! 🎉**

*Last updated: January 2026*
