# 📰 Multi-Armed Bandit News Recommendation System

An interactive demonstration of exploration vs exploitation tradeoffs in recommendation systems using Multi-Armed Bandit algorithms.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Project Overview

This project implements a real-time news article recommendation system that learns from user clicks using three classic bandit algorithms:
- **Epsilon-Greedy**: Simple exploration-exploitation with configurable randomness
- **UCB (Upper Confidence Bound)**: Optimistic algorithm with theoretical guarantees
- **Thompson Sampling**: Bayesian approach with posterior sampling

### Key Features

✅ **Real-time Learning**: Algorithms adapt as they receive user feedback  
✅ **Interactive Visualization**: Side-by-side algorithm comparison  
✅ **Parameter Tuning**: Adjust epsilon, confidence levels in real-time  
✅ **Contextual Extension**: Support for user demographics and preferences  
✅ **Comprehensive Metrics**: Regret curves, CTR evolution, exploration ratios  
✅ **Export Functionality**: Download results as JSON/CSV  

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bandit-news-recommender.git
cd bandit-news-recommender

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Docker Installation (Optional)

```bash
# Build the Docker image
docker build -t bandit-recommender .

# Run the container
docker run -p 8501:8501 bandit-recommender
```

## 📊 How It Works

### The Multi-Armed Bandit Problem

Imagine you're at a casino with multiple slot machines (bandits), each with unknown payout rates. The multi-armed bandit problem asks: **How do you maximize your winnings?**

In our news recommendation context:
- Each **arm** = a news article
- Each **pull** = showing an article to a user
- **Reward** = 1 if user clicks, 0 otherwise
- **Goal** = Maximize total clicks while learning which articles are best

### The Exploration-Exploitation Dilemma

- **Exploration**: Try different articles to learn their true CTR
- **Exploitation**: Show the article you currently think is best

Balancing these is crucial for optimal performance!

## 🧮 Algorithms Explained

### 1. Epsilon-Greedy (ε-greedy)

**Idea**: With probability ε, explore randomly. Otherwise, exploit the best known arm.

```python
if random() < epsilon:
    return random_arm()  # Explore
else:
    return best_arm()     # Exploit
```

**Parameters**:
- `epsilon` (ε): Exploration probability (0 to 1)
  - Higher ε = more exploration
  - Lower ε = more exploitation

**Pros**: Simple, intuitive, easy to implement  
**Cons**: Wastes exploration on clearly bad arms

### 2. Upper Confidence Bound (UCB)

**Idea**: Select the arm with highest upper confidence bound, optimistically assuming uncertain arms might be best.

```
UCB(arm) = estimated_value + c × sqrt(ln(total_pulls) / pulls(arm))
          └─────┬─────┘       └──────────┬──────────┘
         exploitation         exploration bonus
```

**Parameters**:
- `c`: Confidence level (typically √2 ≈ 1.414)
  - Higher c = more exploration
  - Lower c = more exploitation

**Pros**: Theoretical guarantees, no randomness  
**Cons**: Can be overly optimistic early on

### 3. Thompson Sampling

**Idea**: Maintain a probability distribution over each arm's true CTR. Sample from each distribution and pick the arm with highest sample.

For binary rewards (click/no-click), we use the **Beta distribution**:
- Start with Beta(1, 1) = Uniform(0, 1)
- After click: Beta(α+1, β)
- After no-click: Beta(α, β+1)

**Parameters**:
- `alpha_prior`: Prior successes (default: 1)
- `beta_prior`: Prior failures (default: 1)

**Pros**: Often best performance, naturally balances exploration/exploitation  
**Cons**: Requires more computation (sampling)

## 📈 Evaluation Metrics

### Cumulative Regret

**Regret** = (Optimal reward - Actual reward)

Measures how much better we could have done if we knew the best arm from the start.

```
Regret(t) = Σ (R_optimal - R_actual)
```

**Lower is better!**

### Click-Through Rate (CTR)

```
CTR = Total Clicks / Total Impressions
```

Tracks learning progress over time. Should converge to optimal CTR.

### Exploration Ratio

```
Exploration Ratio = Explorations / (Explorations + Exploitations)
```

Shows balance between learning and earning.

## 🎮 Using the Application

### 1. Configure Simulation

In the sidebar:
- Set number of rounds (100-5000)
- Select which algorithms to compare
- Adjust algorithm parameters
- Choose number of simulations for averaging

### 2. Run Simulation

Click **"Run Simulation"** to:
- Simulate user interactions
- Train all selected algorithms
- Generate comparison metrics
- Visualize results

### 3. Analyze Results

**Overview Tab**:
- System summary
- Optimal article information
- Algorithm explanations

**Performance Comparison Tab**:
- Cumulative regret curves
- CTR evolution over time
- Arm selection frequencies
- Summary statistics table

**Algorithm Details Tab**:
- Per-algorithm metrics
- Value estimates vs true CTRs
- Thompson Sampling distributions
- Confidence intervals

**Articles Info Tab**:
- All articles with true CTRs
- CTR distribution visualization
- Best article highlighted

**Export Results Tab**:
- Download JSON results
- Download CSV comparison
- Simulation summary

## 🔬 Advanced: Contextual Bandits

Contextual bandits extend basic bandits by considering **context** (user features) when making decisions.

### User Features
- Age group
- Geographic location
- Reading history
- Time of day
- Device type

### Linear Contextual Bandit (LinUCB)

For each arm, maintain:
```
θ_a = A_a^(-1) × b_a
```

Where:
- `A_a`: Design matrix (features × features)
- `b_a`: Response vector
- `θ_a`: Parameter estimates

Selection:
```
score(arm, context) = θ_a^T × context + α × sqrt(context^T × A_a^(-1) × context)
                      └─────┬─────┘       └──────────────┬──────────────┘
                      exploitation         exploration (uncertainty)
```

## 📁 System Structure

```
bandit-news-recommender/
├── app.py                    
├── bandit_algorithms.py      
├── simulation.py            
├── requirements.txt          
├── README.md                
├── notebooks/
│   └── analysis.ipynb       
├── docs/
│   ├── blog_post.md         
│   └── algorithms.md        
└── tests/
    └── test_algorithms.py   
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch 
3. Commit changes 
4. Push to branch 
5. Open a Pull Request

## 👤 Author

**Siddhant Sahare**
- Portfolio: [yourportfolio.com]((https://siddhantsahare.netlify.app/))
- LinkedIn: [linkedin.com/in/yourname]((https://www.linkedin.com/in/siddhant-sahare-91bb931a6/))


## 🙏 Acknowledgments

- Inspired by classic bandit algorithms research
- Built with Streamlit for interactive ML demos
- Special thanks to the RL community

## 📧 Contact

Questions? Reach out at ssahare834@gmail.com

---

⭐ **If you found this helpful, please star the repository!** ⭐

---

**Last Updated**: January 2026
