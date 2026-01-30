"""
Multi-Armed Bandit Algorithms Implementation
Author: Portfolio Project
Description: Core implementations of Epsilon-Greedy, UCB, and Thompson Sampling algorithms
"""

import numpy as np
from typing import List, Tuple, Optional
from abc import ABC, abstractmethod


class BanditAlgorithm(ABC):
    """Abstract base class for bandit algorithms"""
    
    def __init__(self, n_arms: int):
        """
        Initialize bandit algorithm
        
        Args:
            n_arms: Number of arms (articles/options)
        """
        self.n_arms = n_arms
        self.counts = np.zeros(n_arms)  # Number of times each arm was pulled
        self.values = np.zeros(n_arms)  # Estimated value (CTR) for each arm
        self.total_pulls = 0
        self.total_reward = 0
        self.rewards_history = []
        self.arm_history = []
        
    @abstractmethod
    def select_arm(self, context: Optional[np.ndarray] = None) -> int:
        """Select an arm to pull"""
        pass
    
    def update(self, arm: int, reward: float):
        """
        Update algorithm state after observing reward
        
        Args:
            arm: Arm that was pulled
            reward: Observed reward (0 or 1 for clicks)
        """
        self.counts[arm] += 1
        self.total_pulls += 1
        self.total_reward += reward
        
        # Incremental average update
        n = self.counts[arm]
        value = self.values[arm]
        self.values[arm] = ((n - 1) / n) * value + (1 / n) * reward
        
        self.rewards_history.append(reward)
        self.arm_history.append(arm)
    
    def get_metrics(self) -> dict:
        """Get current performance metrics"""
        return {
            'total_pulls': self.total_pulls,
            'total_reward': self.total_reward,
            'average_reward': self.total_reward / max(1, self.total_pulls),
            'counts': self.counts.copy(),
            'values': self.values.copy(),
            'rewards_history': self.rewards_history.copy(),
            'arm_history': self.arm_history.copy()
        }
    
    def reset(self):
        """Reset the algorithm state"""
        self.counts = np.zeros(self.n_arms)
        self.values = np.zeros(self.n_arms)
        self.total_pulls = 0
        self.total_reward = 0
        self.rewards_history = []
        self.arm_history = []


class EpsilonGreedy(BanditAlgorithm):
    """
    Epsilon-Greedy Algorithm
    
    With probability epsilon, explore randomly.
    With probability (1-epsilon), exploit the best known arm.
    """
    
    def __init__(self, n_arms: int, epsilon: float = 0.1):
        """
        Args:
            n_arms: Number of arms
            epsilon: Exploration probability (0 to 1)
        """
        super().__init__(n_arms)
        self.epsilon = epsilon
        self.exploration_count = 0
        self.exploitation_count = 0
    
    def select_arm(self, context: Optional[np.ndarray] = None) -> int:
        """Select arm using epsilon-greedy strategy"""
        if np.random.random() < self.epsilon:
            # Explore: choose random arm
            self.exploration_count += 1
            return np.random.randint(0, self.n_arms)
        else:
            # Exploit: choose best arm
            self.exploitation_count += 1
            # Break ties randomly
            max_value = np.max(self.values)
            best_arms = np.where(self.values == max_value)[0]
            return np.random.choice(best_arms)
    
    def set_epsilon(self, epsilon: float):
        """Update epsilon value"""
        self.epsilon = max(0.0, min(1.0, epsilon))
    
    def get_exploration_ratio(self) -> float:
        """Get ratio of exploration vs exploitation"""
        total = self.exploration_count + self.exploitation_count
        return self.exploration_count / max(1, total)


class UCB(BanditAlgorithm):
    """
    Upper Confidence Bound (UCB1) Algorithm
    
    Selects arm with highest upper confidence bound:
    UCB(arm) = estimated_value + c * sqrt(log(total_pulls) / pulls(arm))
    """
    
    def __init__(self, n_arms: int, c: float = 2.0):
        """
        Args:
            n_arms: Number of arms
            c: Confidence level parameter (typically sqrt(2))
        """
        super().__init__(n_arms)
        self.c = c
    
    def select_arm(self, context: Optional[np.ndarray] = None) -> int:
        """Select arm using UCB strategy"""
        # Pull each arm at least once
        for arm in range(self.n_arms):
            if self.counts[arm] == 0:
                return arm
        
        # Calculate UCB for each arm
        ucb_values = np.zeros(self.n_arms)
        for arm in range(self.n_arms):
            bonus = self.c * np.sqrt(np.log(self.total_pulls) / self.counts[arm])
            ucb_values[arm] = self.values[arm] + bonus
        
        # Select arm with highest UCB
        max_ucb = np.max(ucb_values)
        best_arms = np.where(ucb_values == max_ucb)[0]
        return np.random.choice(best_arms)
    
    def set_c(self, c: float):
        """Update confidence parameter"""
        self.c = max(0.1, c)
    
    def get_ucb_values(self) -> np.ndarray:
        """Get current UCB values for all arms"""
        if self.total_pulls == 0:
            return np.zeros(self.n_arms)
        
        ucb_values = np.zeros(self.n_arms)
        for arm in range(self.n_arms):
            if self.counts[arm] == 0:
                ucb_values[arm] = np.inf
            else:
                bonus = self.c * np.sqrt(np.log(self.total_pulls) / self.counts[arm])
                ucb_values[arm] = self.values[arm] + bonus
        
        return ucb_values


class ThompsonSampling(BanditAlgorithm):
    """
    Thompson Sampling (Bayesian) Algorithm
    
    Maintains Beta distribution for each arm's CTR.
    Samples from each distribution and picks the arm with highest sample.
    """
    
    def __init__(self, n_arms: int, alpha_prior: float = 1.0, beta_prior: float = 1.0):
        """
        Args:
            n_arms: Number of arms
            alpha_prior: Prior successes (Beta distribution alpha parameter)
            beta_prior: Prior failures (Beta distribution beta parameter)
        """
        super().__init__(n_arms)
        self.alpha = np.ones(n_arms) * alpha_prior  # Successes + prior
        self.beta = np.ones(n_arms) * beta_prior    # Failures + prior
    
    def select_arm(self, context: Optional[np.ndarray] = None) -> int:
        """Select arm using Thompson Sampling"""
        # Sample from Beta distribution for each arm
        samples = np.random.beta(self.alpha, self.beta)
        
        # Select arm with highest sample
        max_sample = np.max(samples)
        best_arms = np.where(samples == max_sample)[0]
        return np.random.choice(best_arms)
    
    def update(self, arm: int, reward: float):
        """Update Beta distribution parameters"""
        super().update(arm, reward)
        
        # Update Beta parameters
        if reward > 0:
            self.alpha[arm] += 1
        else:
            self.beta[arm] += 1
    
    def reset(self):
        """Reset algorithm state"""
        super().reset()
        self.alpha = np.ones(self.n_arms)
        self.beta = np.ones(self.n_arms)
    
    def get_confidence_intervals(self, confidence: float = 0.95) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get confidence intervals for each arm's CTR
        
        Args:
            confidence: Confidence level (default 95%)
            
        Returns:
            Tuple of (lower_bounds, upper_bounds)
        """
        from scipy import stats
        
        alpha_val = (1 - confidence) / 2
        lower = np.zeros(self.n_arms)
        upper = np.zeros(self.n_arms)
        
        for arm in range(self.n_arms):
            lower[arm] = stats.beta.ppf(alpha_val, self.alpha[arm], self.beta[arm])
            upper[arm] = stats.beta.ppf(1 - alpha_val, self.alpha[arm], self.beta[arm])
        
        return lower, upper
    
    def get_distributions(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get current Beta distribution parameters"""
        return self.alpha.copy(), self.beta.copy()


class ContextualBandit:
    """
    Contextual Bandit using Linear models
    
    Extends basic bandits with user/context features.
    Uses linear regression to estimate reward given context and arm.
    """
    
    def __init__(self, n_arms: int, n_features: int, alpha: float = 1.0):
        """
        Args:
            n_arms: Number of arms
            n_features: Number of context features
            alpha: Regularization parameter
        """
        self.n_arms = n_arms
        self.n_features = n_features
        self.alpha = alpha
        
        # Initialize parameters for each arm
        self.A = [np.identity(n_features) * alpha for _ in range(n_arms)]  # Design matrix
        self.b = [np.zeros(n_features) for _ in range(n_arms)]  # Response vector
        self.theta = [np.zeros(n_features) for _ in range(n_arms)]  # Parameter estimates
        
        self.total_pulls = 0
        self.total_reward = 0
        self.counts = np.zeros(n_arms)
        self.rewards_history = []
        self.arm_history = []
    
    def select_arm(self, context: np.ndarray, use_ucb: bool = True) -> int:
        """
        Select arm given context
        
        Args:
            context: Feature vector for current user/context
            use_ucb: Whether to use UCB-style exploration
            
        Returns:
            Selected arm index
        """
        context = context.reshape(-1, 1)  # Column vector
        scores = np.zeros(self.n_arms)
        
        for arm in range(self.n_arms):
            # Update theta estimate
            try:
                self.theta[arm] = np.linalg.solve(self.A[arm], self.b[arm])
            except np.linalg.LinAlgError:
                self.theta[arm] = np.zeros(self.n_features)
            
            # Calculate score
            score = self.theta[arm].T @ context
            
            if use_ucb:
                # Add uncertainty bonus (LinUCB)
                A_inv = np.linalg.inv(self.A[arm])
                uncertainty = np.sqrt(context.T @ A_inv @ context)
                score += self.alpha * uncertainty
            
            scores[arm] = score.item()
        
        # Select arm with highest score
        return np.argmax(scores)
    
    def update(self, arm: int, context: np.ndarray, reward: float):
        """
        Update model after observing reward
        
        Args:
            arm: Selected arm
            context: Context features
            reward: Observed reward
        """
        context = context.reshape(-1, 1)
        
        # Update design matrix and response vector
        self.A[arm] += context @ context.T
        self.b[arm] += (reward * context).flatten()
        
        # Update statistics
        self.counts[arm] += 1
        self.total_pulls += 1
        self.total_reward += reward
        self.rewards_history.append(reward)
        self.arm_history.append(arm)
    
    def get_metrics(self) -> dict:
        """Get performance metrics"""
        return {
            'total_pulls': self.total_pulls,
            'total_reward': self.total_reward,
            'average_reward': self.total_reward / max(1, self.total_pulls),
            'counts': self.counts.copy(),
            'rewards_history': self.rewards_history.copy(),
            'arm_history': self.arm_history.copy()
        }
    
    def reset(self):
        """Reset the algorithm state"""
        self.A = [np.identity(self.n_features) * self.alpha for _ in range(self.n_arms)]
        self.b = [np.zeros(self.n_features) for _ in range(self.n_arms)]
        self.theta = [np.zeros(self.n_features) for _ in range(self.n_arms)]
        self.total_pulls = 0
        self.total_reward = 0
        self.counts = np.zeros(self.n_arms)
        self.rewards_history = []
        self.arm_history = []
