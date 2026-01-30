"""
Unit tests for Multi-Armed Bandit algorithms
"""

import pytest
import numpy as np
from bandit_algorithms import EpsilonGreedy, UCB, ThompsonSampling, ContextualBandit
from simulation import NewsEnvironment, run_simulation


class TestEpsilonGreedy:
    """Test cases for Epsilon-Greedy algorithm"""
    
    def test_initialization(self):
        """Test proper initialization"""
        algo = EpsilonGreedy(n_arms=5, epsilon=0.1)
        
        assert algo.n_arms == 5
        assert algo.epsilon == 0.1
        assert len(algo.counts) == 5
        assert len(algo.values) == 5
        assert np.all(algo.counts == 0)
        assert np.all(algo.values == 0)
    
    def test_epsilon_bounds(self):
        """Test epsilon is properly bounded"""
        algo = EpsilonGreedy(n_arms=5, epsilon=0.1)
        
        # Test valid epsilon
        algo.set_epsilon(0.5)
        assert algo.epsilon == 0.5
        
        # Test lower bound
        algo.set_epsilon(-0.1)
        assert algo.epsilon == 0.0
        
        # Test upper bound
        algo.set_epsilon(1.5)
        assert algo.epsilon == 1.0
    
    def test_arm_selection(self):
        """Test arm selection is within valid range"""
        algo = EpsilonGreedy(n_arms=5, epsilon=0.1)
        
        for _ in range(100):
            arm = algo.select_arm()
            assert 0 <= arm < 5
    
    def test_update_mechanism(self):
        """Test reward update mechanism"""
        algo = EpsilonGreedy(n_arms=3, epsilon=0.0)
        
        # Update arm 0 with reward 1
        algo.update(0, 1.0)
        assert algo.counts[0] == 1
        assert algo.values[0] == 1.0
        
        # Update arm 0 again with reward 0
        algo.update(0, 0.0)
        assert algo.counts[0] == 2
        assert algo.values[0] == 0.5  # Average of 1 and 0
    
    def test_exploitation(self):
        """Test that algorithm exploits with epsilon=0"""
        algo = EpsilonGreedy(n_arms=3, epsilon=0.0)
        
        # Manually set values
        algo.values = np.array([0.1, 0.5, 0.3])
        algo.counts = np.array([10, 10, 10])
        
        # Should always select arm 1 (highest value)
        selections = [algo.select_arm() for _ in range(100)]
        assert all(arm == 1 for arm in selections)
    
    def test_reset(self):
        """Test reset functionality"""
        algo = EpsilonGreedy(n_arms=3, epsilon=0.1)
        
        # Make some updates
        algo.update(0, 1.0)
        algo.update(1, 0.5)
        
        # Reset
        algo.reset()
        
        assert np.all(algo.counts == 0)
        assert np.all(algo.values == 0)
        assert algo.total_pulls == 0


class TestUCB:
    """Test cases for UCB algorithm"""
    
    def test_initialization(self):
        """Test proper initialization"""
        algo = UCB(n_arms=5, c=2.0)
        
        assert algo.n_arms == 5
        assert algo.c == 2.0
        assert len(algo.counts) == 5
    
    def test_initial_exploration(self):
        """Test that UCB pulls each arm once initially"""
        algo = UCB(n_arms=5, c=2.0)
        
        # First 5 selections should be each arm once
        selected_arms = set()
        for _ in range(5):
            arm = algo.select_arm()
            selected_arms.add(arm)
            algo.update(arm, 1.0)
        
        assert selected_arms == {0, 1, 2, 3, 4}
    
    def test_ucb_values(self):
        """Test UCB value calculation"""
        algo = UCB(n_arms=3, c=2.0)
        
        # Pull each arm once
        for arm in range(3):
            algo.update(arm, 0.5)
        
        # UCB values should be calculated correctly
        ucb_values = algo.get_ucb_values()
        assert len(ucb_values) == 3
        assert all(val >= 0.5 for val in ucb_values)  # All should be >= mean
    
    def test_c_parameter(self):
        """Test setting c parameter"""
        algo = UCB(n_arms=3, c=2.0)
        
        algo.set_c(3.0)
        assert algo.c == 3.0
        
        # Test lower bound
        algo.set_c(0.05)
        assert algo.c == 0.1  # Should be clamped to minimum


class TestThompsonSampling:
    """Test cases for Thompson Sampling algorithm"""
    
    def test_initialization(self):
        """Test proper initialization"""
        algo = ThompsonSampling(n_arms=5)
        
        assert algo.n_arms == 5
        assert len(algo.alpha) == 5
        assert len(algo.beta) == 5
        assert np.all(algo.alpha == 1.0)
        assert np.all(algo.beta == 1.0)
    
    def test_beta_update(self):
        """Test Beta distribution parameter updates"""
        algo = ThompsonSampling(n_arms=3)
        
        # Update with success
        algo.update(0, 1.0)
        assert algo.alpha[0] == 2.0
        assert algo.beta[0] == 1.0
        
        # Update with failure
        algo.update(0, 0.0)
        assert algo.alpha[0] == 2.0
        assert algo.beta[0] == 2.0
    
    def test_arm_selection(self):
        """Test arm selection is valid"""
        algo = ThompsonSampling(n_arms=5)
        
        for _ in range(100):
            arm = algo.select_arm()
            assert 0 <= arm < 5
    
    def test_confidence_intervals(self):
        """Test confidence interval calculation"""
        algo = ThompsonSampling(n_arms=3)
        
        # Make some updates
        for _ in range(10):
            algo.update(0, 1.0)
        for _ in range(10):
            algo.update(1, 0.0)
        
        lower, upper = algo.get_confidence_intervals()
        
        # Arm 0 should have high CTR estimate
        assert lower[0] > lower[1]
        assert upper[0] > upper[1]
        
        # Intervals should be valid
        assert all(0 <= l <= u <= 1 for l, u in zip(lower, upper))


class TestContextualBandit:
    """Test cases for Contextual Bandit"""
    
    def test_initialization(self):
        """Test proper initialization"""
        algo = ContextualBandit(n_arms=3, n_features=5, alpha=1.0)
        
        assert algo.n_arms == 3
        assert algo.n_features == 5
        assert len(algo.A) == 3
        assert len(algo.b) == 3
        assert len(algo.theta) == 3
    
    def test_arm_selection(self):
        """Test arm selection with context"""
        algo = ContextualBandit(n_arms=3, n_features=5)
        
        context = np.random.randn(5)
        arm = algo.select_arm(context)
        
        assert 0 <= arm < 3
    
    def test_update(self):
        """Test update mechanism"""
        algo = ContextualBandit(n_arms=3, n_features=5)
        
        context = np.random.randn(5)
        arm = 0
        reward = 1.0
        
        algo.update(arm, context, reward)
        
        assert algo.counts[arm] == 1
        assert algo.total_pulls == 1


class TestNewsEnvironment:
    """Test cases for News Environment"""
    
    def test_initialization(self):
        """Test environment initialization"""
        env = NewsEnvironment(n_articles=10, seed=42)
        
        assert env.n_articles == 10
        assert len(env.articles) == 10
        assert len(env.true_ctrs) == 10
    
    def test_article_properties(self):
        """Test article properties are valid"""
        env = NewsEnvironment(n_articles=10, seed=42)
        
        for article in env.articles:
            assert 0.05 <= article.true_ctr <= 0.30
            assert article.id >= 0
            assert len(article.title) > 0
            assert len(article.category) > 0
    
    def test_pull_arm(self):
        """Test arm pulling returns valid rewards"""
        env = NewsEnvironment(n_articles=5, seed=42)
        
        for _ in range(100):
            arm = np.random.randint(0, 5)
            reward = env.pull_arm(arm)
            assert reward in [0.0, 1.0]
    
    def test_regret_calculation(self):
        """Test regret calculation"""
        env = NewsEnvironment(n_articles=5, seed=42)
        
        # Always pull optimal arm
        arm_history = [env.optimal_arm] * 100
        regret = env.calculate_regret(arm_history)
        
        # Regret should be zero
        assert np.all(regret == 0)
        
        # Pull worst arm
        worst_arm = np.argmin(env.true_ctrs)
        arm_history = [worst_arm] * 100
        regret = env.calculate_regret(arm_history)
        
        # Regret should be positive and increasing
        assert regret[-1] > 0
        assert np.all(np.diff(regret) >= 0)


class TestSimulation:
    """Test cases for simulation functions"""
    
    def test_run_simulation(self):
        """Test running a simulation"""
        env = NewsEnvironment(n_articles=5, seed=42)
        algo = EpsilonGreedy(n_arms=5, epsilon=0.1)
        
        results = run_simulation(algo, env, n_rounds=100)
        
        assert 'rewards' in results
        assert 'arms' in results
        assert 'regret' in results
        assert 'ctr_evolution' in results
        
        assert len(results['rewards']) == 100
        assert len(results['arms']) == 100
    
    def test_compare_algorithms(self):
        """Test algorithm comparison"""
        env = NewsEnvironment(n_articles=5, seed=42)
        
        algorithms = {
            'EG': EpsilonGreedy(5, epsilon=0.1),
            'UCB': UCB(5, c=2.0),
            'TS': ThompsonSampling(5)
        }
        
        comparison = compare_algorithms(algorithms, env, n_rounds=100, n_simulations=5)
        
        assert len(comparison) == 3
        assert 'Algorithm' in comparison.columns
        assert 'Avg Total Reward' in comparison.columns
        assert 'Avg Final Regret' in comparison.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
