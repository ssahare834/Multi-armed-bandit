"""
Simulation Environment for Multi-Armed Bandit Recommendation System
Simulates user interactions with news articles
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd


@dataclass
class Article:
    """Represents a news article"""
    id: int
    title: str
    category: str
    true_ctr: float  # True click-through rate
    topic_features: np.ndarray  # Feature vector for contextual bandits


@dataclass
class User:
    """Represents a user with preferences"""
    id: int
    age: int
    location: str
    preferred_categories: List[str]
    reading_history: List[int]
    feature_vector: np.ndarray


class NewsEnvironment:
    """
    Simulation environment for news recommendation
    """
    
    def __init__(self, n_articles: int = 10, seed: Optional[int] = None):
        """
        Args:
            n_articles: Number of news articles to simulate
            seed: Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
        
        self.n_articles = n_articles
        self.articles = self._generate_articles()
        self.true_ctrs = np.array([article.true_ctr for article in self.articles])
        self.optimal_arm = np.argmax(self.true_ctrs)
        self.optimal_ctr = self.true_ctrs[self.optimal_arm]
        
    def _generate_articles(self) -> List[Article]:
        """Generate synthetic news articles with varying CTRs"""
        categories = ['Politics', 'Technology', 'Sports', 'Entertainment', 
                     'Business', 'Science', 'Health', 'World']
        
        articles = []
        
        # Generate CTRs with some structure
        # A few high-performing articles, many medium, some low
        ctrs = np.random.beta(2, 5, self.n_articles)  # Skewed distribution
        ctrs = 0.05 + ctrs * 0.25  # Scale to 0.05-0.30 range
        ctrs = np.sort(ctrs)[::-1]  # Sort descending
        
        titles = [
            "Breaking: Major Policy Changes Announced",
            "Tech Giant Unveils Revolutionary AI System",
            "Championship Game Ends in Dramatic Fashion",
            "Celebrity Interview: Exclusive Insights",
            "Market Analysis: What Investors Need to Know",
            "Scientific Breakthrough in Climate Research",
            "Health Tips: Expert Recommendations",
            "Global Summit Addresses Critical Issues",
            "Innovation in Renewable Energy Sector",
            "Sports Star Makes Historic Achievement",
            "Entertainment Industry Trends 2025",
            "Economic Forecast for Next Quarter",
            "Medical Advances in Treatment Options",
            "International Relations Update",
            "Startup Success Story Inspires Many"
        ]
        
        for i in range(self.n_articles):
            category = categories[i % len(categories)]
            title = titles[i] if i < len(titles) else f"Article {i+1}: {category} News"
            
            # Generate topic features (for contextual bandits)
            topic_features = np.random.randn(5)
            topic_features = topic_features / np.linalg.norm(topic_features)
            
            articles.append(Article(
                id=i,
                title=title,
                category=category,
                true_ctr=ctrs[i],
                topic_features=topic_features
            ))
        
        return articles
    
    def pull_arm(self, arm: int) -> float:
        """
        Simulate user interaction with article
        
        Args:
            arm: Article index
            
        Returns:
            1 if clicked, 0 if not clicked
        """
        click_prob = self.true_ctrs[arm]
        return float(np.random.random() < click_prob)
    
    def generate_user(self) -> User:
        """Generate a random user with preferences"""
        ages = [18, 25, 35, 45, 55, 65]
        locations = ['US-East', 'US-West', 'Europe', 'Asia', 'Other']
        
        categories = list(set([article.category for article in self.articles]))
        
        user_id = np.random.randint(0, 100000)
        age = np.random.choice(ages)
        location = np.random.choice(locations)
        preferred_categories = list(np.random.choice(categories, 
                                                     size=min(3, len(categories)), 
                                                     replace=False))
        
        # Generate user feature vector
        # Features: [age_normalized, location_encoded, category_preferences...]
        age_norm = age / 100.0
        location_encoded = locations.index(location) / len(locations)
        
        feature_vector = np.array([age_norm, location_encoded, 0.5, 0.5, 0.5])
        
        return User(
            id=user_id,
            age=age,
            location=location,
            preferred_categories=preferred_categories,
            reading_history=[],
            feature_vector=feature_vector
        )
    
    def contextual_pull(self, arm: int, user: User) -> float:
        """
        Simulate user interaction considering user preferences
        
        Args:
            arm: Article index
            user: User object
            
        Returns:
            1 if clicked, 0 if not clicked
        """
        article = self.articles[arm]
        base_ctr = article.true_ctr
        
        # Boost CTR if article matches user preferences
        if article.category in user.preferred_categories:
            boost = 0.1
        else:
            boost = 0.0
        
        # Age-based preferences (example)
        if user.age < 35 and article.category in ['Technology', 'Entertainment']:
            boost += 0.05
        elif user.age >= 55 and article.category in ['Health', 'Business']:
            boost += 0.05
        
        adjusted_ctr = min(0.95, base_ctr + boost)
        
        return float(np.random.random() < adjusted_ctr)
    
    def get_article_info(self) -> pd.DataFrame:
        """Get DataFrame with article information"""
        data = {
            'Article ID': [a.id for a in self.articles],
            'Title': [a.title for a in self.articles],
            'Category': [a.category for a in self.articles],
            'True CTR': [a.true_ctr for a in self.articles]
        }
        return pd.DataFrame(data)
    
    def calculate_regret(self, arm_history: List[int]) -> np.ndarray:
        """
        Calculate cumulative regret over time
        
        Args:
            arm_history: List of arms pulled over time
            
        Returns:
            Cumulative regret array
        """
        optimal_reward = self.optimal_ctr
        actual_rewards = [self.true_ctrs[arm] for arm in arm_history]
        
        regret = optimal_reward - np.array(actual_rewards)
        cumulative_regret = np.cumsum(regret)
        
        return cumulative_regret


def run_simulation(algorithm, environment: NewsEnvironment, 
                   n_rounds: int, use_context: bool = False) -> Dict:
    """
    Run simulation of bandit algorithm in environment
    
    Args:
        algorithm: Bandit algorithm instance
        environment: NewsEnvironment instance
        n_rounds: Number of rounds to simulate
        use_context: Whether to use contextual features
        
    Returns:
        Dictionary with simulation results
    """
    results = {
        'rewards': [],
        'arms': [],
        'regret': [],
        'ctr_evolution': []
    }
    
    cumulative_reward = 0
    
    for t in range(n_rounds):
        # Generate user (for contextual bandits)
        user = environment.generate_user() if use_context else None
        
        # Select arm
        if use_context and hasattr(algorithm, 'select_arm'):
            if isinstance(algorithm, type(algorithm)) and hasattr(algorithm, 'n_features'):
                # Contextual bandit
                arm = algorithm.select_arm(user.feature_vector)
            else:
                arm = algorithm.select_arm()
        else:
            arm = algorithm.select_arm()
        
        # Pull arm and observe reward
        if use_context and user is not None:
            reward = environment.contextual_pull(arm, user)
        else:
            reward = environment.pull_arm(arm)
        
        # Update algorithm
        if use_context and hasattr(algorithm, 'update') and user is not None:
            if isinstance(algorithm, type(algorithm)) and hasattr(algorithm, 'n_features'):
                algorithm.update(arm, user.feature_vector, reward)
            else:
                algorithm.update(arm, reward)
        else:
            algorithm.update(arm, reward)
        
        # Record results
        cumulative_reward += reward
        results['rewards'].append(reward)
        results['arms'].append(arm)
        
        # Calculate current CTR
        current_ctr = cumulative_reward / (t + 1)
        results['ctr_evolution'].append(current_ctr)
    
    # Calculate regret
    results['regret'] = environment.calculate_regret(results['arms'])
    
    return results


def compare_algorithms(algorithms: Dict, environment: NewsEnvironment,
                      n_rounds: int, n_simulations: int = 10) -> pd.DataFrame:
    """
    Compare multiple algorithms over multiple simulations
    
    Args:
        algorithms: Dictionary of {name: algorithm_instance}
        environment: NewsEnvironment instance
        n_rounds: Number of rounds per simulation
        n_simulations: Number of simulations to average over
        
    Returns:
        DataFrame with comparison results
    """
    results = []
    
    for name, algorithm in algorithms.items():
        total_rewards = []
        final_regrets = []
        
        for _ in range(n_simulations):
            algorithm.reset()
            sim_results = run_simulation(algorithm, environment, n_rounds)
            
            total_rewards.append(sum(sim_results['rewards']))
            final_regrets.append(sim_results['regret'][-1])
        
        results.append({
            'Algorithm': name,
            'Avg Total Reward': np.mean(total_rewards),
            'Std Total Reward': np.std(total_rewards),
            'Avg Final Regret': np.mean(final_regrets),
            'Std Final Regret': np.std(final_regrets),
            'Avg CTR': np.mean(total_rewards) / n_rounds
        })
    
    return pd.DataFrame(results)
