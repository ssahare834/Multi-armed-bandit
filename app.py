"""
Interactive Multi-Armed Bandit News Recommendation System
Streamlit Application for Portfolio Demonstration
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime

# Import our modules
from bandit_algorithms import (
    EpsilonGreedy, UCB, ThompsonSampling, ContextualBandit
)
from simulation import NewsEnvironment, run_simulation, compare_algorithms


# Page configuration
st.set_page_config(
    page_title="Multi-Armed Bandit News Recommender",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'environment' not in st.session_state:
        st.session_state.environment = NewsEnvironment(n_articles=10, seed=42)
    
    if 'algorithms' not in st.session_state:
        st.session_state.algorithms = {
            'epsilon_greedy': EpsilonGreedy(10, epsilon=0.1),
            'ucb': UCB(10, c=2.0),
            'thompson': ThompsonSampling(10)
        }
    
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = None
    
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None


def plot_regret_comparison(results_dict):
    """Plot cumulative regret for multiple algorithms"""
    fig = go.Figure()
    
    for name, results in results_dict.items():
        regret = results['regret']
        fig.add_trace(go.Scatter(
            x=list(range(len(regret))),
            y=regret,
            mode='lines',
            name=name,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title="Cumulative Regret Over Time",
        xaxis_title="Round",
        yaxis_title="Cumulative Regret",
        hovermode='x unified',
        height=400
    )
    
    return fig


def plot_ctr_evolution(results_dict):
    """Plot CTR evolution over time"""
    fig = go.Figure()
    
    for name, results in results_dict.items():
        ctr = results['ctr_evolution']
        fig.add_trace(go.Scatter(
            x=list(range(len(ctr))),
            y=ctr,
            mode='lines',
            name=name,
            line=dict(width=2)
        ))
    
    # Add optimal CTR line
    optimal_ctr = st.session_state.environment.optimal_ctr
    fig.add_hline(
        y=optimal_ctr, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Optimal CTR: {optimal_ctr:.3f}"
    )
    
    fig.update_layout(
        title="Click-Through Rate (CTR) Evolution",
        xaxis_title="Round",
        yaxis_title="CTR",
        hovermode='x unified',
        height=400
    )
    
    return fig


def plot_arm_selection_frequency(results_dict):
    """Plot frequency of arm selections"""
    fig = make_subplots(
        rows=1, cols=len(results_dict),
        subplot_titles=list(results_dict.keys()),
        specs=[[{'type': 'bar'}] * len(results_dict)]
    )
    
    for idx, (name, results) in enumerate(results_dict.items(), 1):
        arms = results['arms']
        arm_counts = pd.Series(arms).value_counts().sort_index()
        
        fig.add_trace(
            go.Bar(
                x=arm_counts.index,
                y=arm_counts.values,
                name=name,
                showlegend=False
            ),
            row=1, col=idx
        )
    
    fig.update_xaxes(title_text="Article ID")
    fig.update_yaxes(title_text="Selection Count")
    fig.update_layout(height=400, title_text="Arm Selection Frequency")
    
    return fig


def plot_value_estimates(algorithm, algorithm_name):
    """Plot current value estimates vs true CTRs"""
    true_ctrs = st.session_state.environment.true_ctrs
    
    if hasattr(algorithm, 'values'):
        estimated_values = algorithm.values
    else:
        return None
    
    fig = go.Figure()
    
    # True CTRs
    fig.add_trace(go.Bar(
        x=list(range(len(true_ctrs))),
        y=true_ctrs,
        name='True CTR',
        marker_color='lightblue'
    ))
    
    # Estimated values
    fig.add_trace(go.Bar(
        x=list(range(len(estimated_values))),
        y=estimated_values,
        name='Estimated Value',
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        title=f"{algorithm_name}: Estimated Values vs True CTRs",
        xaxis_title="Article ID",
        yaxis_title="Value / CTR",
        barmode='group',
        height=400
    )
    
    return fig


def plot_thompson_sampling_distributions(algorithm):
    """Plot Beta distributions for Thompson Sampling"""
    if not isinstance(algorithm, ThompsonSampling):
        return None
    
    alpha, beta = algorithm.get_distributions()
    
    fig = go.Figure()
    
    x = np.linspace(0, 1, 100)
    
    for arm in range(len(alpha)):
        from scipy.stats import beta as beta_dist
        y = beta_dist.pdf(x, alpha[arm], beta[arm])
        
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name=f'Article {arm}',
            fill='tonexty' if arm > 0 else None
        ))
    
    fig.update_layout(
        title="Thompson Sampling: Beta Distributions",
        xaxis_title="CTR",
        yaxis_title="Probability Density",
        height=400
    )
    
    return fig


def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<p class="main-header">📰 Multi-Armed Bandit News Recommender</p>', 
                unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; color: #666;'>
    Interactive demonstration of exploration vs exploitation in recommendation systems
    </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Simulation parameters
        st.subheader("Simulation Settings")
        n_rounds = st.slider("Number of Rounds", 100, 5000, 1000, 100)
        n_simulations = st.slider("Simulations for Comparison", 1, 20, 5)
        
        st.divider()
        
        # Algorithm selection
        st.subheader("Algorithm Selection")
        use_epsilon_greedy = st.checkbox("Epsilon-Greedy", value=True)
        use_ucb = st.checkbox("UCB", value=True)
        use_thompson = st.checkbox("Thompson Sampling", value=True)
        
        st.divider()
        
        # Algorithm parameters
        st.subheader("Algorithm Parameters")
        
        if use_epsilon_greedy:
            epsilon = st.slider("Epsilon (ε)", 0.0, 1.0, 0.1, 0.01)
            st.session_state.algorithms['epsilon_greedy'].set_epsilon(epsilon)
        
        if use_ucb:
            c_param = st.slider("UCB Confidence (c)", 0.1, 5.0, 2.0, 0.1)
            st.session_state.algorithms['ucb'].set_c(c_param)
        
        st.divider()
        
        # Run simulation button
        if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
            with st.spinner("Running simulation..."):
                # Select algorithms to run
                selected_algorithms = {}
                if use_epsilon_greedy:
                    selected_algorithms['Epsilon-Greedy'] = st.session_state.algorithms['epsilon_greedy']
                if use_ucb:
                    selected_algorithms['UCB'] = st.session_state.algorithms['ucb']
                if use_thompson:
                    selected_algorithms['Thompson Sampling'] = st.session_state.algorithms['thompson']
                
                # Run simulations
                results = {}
                for name, algo in selected_algorithms.items():
                    algo.reset()
                    results[name] = run_simulation(
                        algo, 
                        st.session_state.environment, 
                        n_rounds
                    )
                
                st.session_state.simulation_results = results
                
                # Run comparison
                st.session_state.comparison_results = compare_algorithms(
                    selected_algorithms,
                    st.session_state.environment,
                    n_rounds,
                    n_simulations
                )
                
                st.success("Simulation complete!")
        
        st.divider()
        
        # Reset button
        if st.button("🔄 Reset All", use_container_width=True):
            for algo in st.session_state.algorithms.values():
                algo.reset()
            st.session_state.simulation_results = None
            st.session_state.comparison_results = None
            st.rerun()
    
    # Main content
    tabs = st.tabs([
        "📊 Overview", 
        "📈 Performance Comparison", 
        "🎯 Algorithm Details",
        "📰 Articles Info",
        "📥 Export Results"
    ])
    
    # Tab 1: Overview
    with tabs[0]:
        st.header("System Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Number of Articles",
                st.session_state.environment.n_articles
            )
        
        with col2:
            optimal_ctr = st.session_state.environment.optimal_ctr
            st.metric(
                "Optimal CTR",
                f"{optimal_ctr:.3f}"
            )
        
        with col3:
            optimal_arm = st.session_state.environment.optimal_arm
            st.metric(
                "Best Article ID",
                optimal_arm
            )
        
        st.markdown("---")
        
        # Explanation
        with st.expander("ℹ️ About Multi-Armed Bandits"):
            st.markdown("""
            ### The Multi-Armed Bandit Problem
            
            Imagine you're at a casino with multiple slot machines (bandits), each with unknown payout rates.
            You want to maximize your total winnings, but you face a dilemma:
            
            - **Exploration**: Try different machines to learn which ones pay better
            - **Exploitation**: Play the machine you currently think is best
            
            #### Algorithms Implemented:
            
            1. **Epsilon-Greedy**: 
               - Explores randomly with probability ε
               - Exploits best known option with probability (1-ε)
               - Simple but effective
            
            2. **UCB (Upper Confidence Bound)**:
               - Balances exploration and exploitation mathematically
               - Selects arms with highest upper confidence bound
               - Provides logarithmic regret guarantees
            
            3. **Thompson Sampling**:
               - Bayesian approach using Beta distributions
               - Samples from posterior distributions
               - Often performs best in practice
            
            #### In News Recommendation:
            - Each "arm" is a news article
            - "Reward" is whether the user clicks (1) or not (0)
            - Goal: Maximize total clicks while learning user preferences
            """)
    
    # Tab 2: Performance Comparison
    with tabs[1]:
        st.header("Performance Comparison")
        
        if st.session_state.simulation_results is None:
            st.info("👈 Configure settings and click 'Run Simulation' to see results")
        else:
            results = st.session_state.simulation_results
            
            # Comparison table
            if st.session_state.comparison_results is not None:
                st.subheader("📊 Summary Statistics")
                st.dataframe(
                    st.session_state.comparison_results.style.format({
                        'Avg Total Reward': '{:.2f}',
                        'Std Total Reward': '{:.2f}',
                        'Avg Final Regret': '{:.2f}',
                        'Std Final Regret': '{:.2f}',
                        'Avg CTR': '{:.3f}'
                    }),
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Regret plot
            st.subheader("📉 Cumulative Regret")
            st.plotly_chart(plot_regret_comparison(results), use_container_width=True)
            
            st.info("""
            **Regret** measures the difference between optimal performance and actual performance.
            Lower regret indicates better algorithm performance.
            """)
            
            # CTR evolution plot
            st.subheader("📈 CTR Evolution")
            st.plotly_chart(plot_ctr_evolution(results), use_container_width=True)
            
            # Arm selection frequency
            st.subheader("🎯 Arm Selection Frequency")
            st.plotly_chart(plot_arm_selection_frequency(results), use_container_width=True)
    
    # Tab 3: Algorithm Details
    with tabs[2]:
        st.header("Algorithm Details")
        
        if st.session_state.simulation_results is None:
            st.info("👈 Run simulation to see algorithm details")
        else:
            selected_algorithms = st.session_state.algorithms
            
            for name_key, algo in selected_algorithms.items():
                # Map internal names to display names
                name_map = {
                    'epsilon_greedy': 'Epsilon-Greedy',
                    'ucb': 'UCB',
                    'thompson': 'Thompson Sampling'
                }
                display_name = name_map.get(name_key, name_key)
                
                # Only show if algorithm was used in simulation
                if display_name not in st.session_state.simulation_results:
                    continue
                
                with st.expander(f"📊 {display_name}", expanded=True):
                    
                    # Metrics
                    metrics = algo.get_metrics()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Pulls", metrics['total_pulls'])
                    with col2:
                        st.metric("Total Reward", f"{metrics['total_reward']:.0f}")
                    with col3:
                        st.metric("Average CTR", f"{metrics['average_reward']:.3f}")
                    with col4:
                        if isinstance(algo, EpsilonGreedy):
                            explore_ratio = algo.get_exploration_ratio()
                            st.metric("Exploration Ratio", f"{explore_ratio:.2%}")
                    
                    # Value estimates plot
                    fig = plot_value_estimates(algo, display_name)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Thompson Sampling specific
                    if isinstance(algo, ThompsonSampling):
                        fig = plot_thompson_sampling_distributions(algo)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Confidence intervals
                        st.subheader("95% Confidence Intervals")
                        lower, upper = algo.get_confidence_intervals()
                        
                        ci_df = pd.DataFrame({
                            'Article ID': range(len(lower)),
                            'Lower Bound': lower,
                            'Estimated CTR': algo.values,
                            'Upper Bound': upper,
                            'True CTR': st.session_state.environment.true_ctrs
                        })
                        
                        st.dataframe(ci_df.style.format({
                            'Lower Bound': '{:.3f}',
                            'Estimated CTR': '{:.3f}',
                            'Upper Bound': '{:.3f}',
                            'True CTR': '{:.3f}'
                        }), use_container_width=True)
    
    # Tab 4: Articles Info
    with tabs[3]:
        st.header("📰 News Articles Information")
        
        articles_df = st.session_state.environment.get_article_info()
        
        # Highlight best article
        def highlight_best(row):
            if row['Article ID'] == st.session_state.environment.optimal_arm:
                return ['background-color: #90EE90'] * len(row)
            return [''] * len(row)
        
        styled_df = articles_df.style.format({
            'True CTR': '{:.3f}'
        }).apply(highlight_best, axis=1)
        
        st.dataframe(styled_df, use_container_width=True)
        
        st.info("🟢 Green highlight indicates the best article (highest true CTR)")
        
        # CTR distribution
        st.subheader("CTR Distribution")
        fig = px.bar(
            articles_df,
            x='Article ID',
            y='True CTR',
            color='Category',
            title='True CTR by Article',
            hover_data=['Title']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 5: Export Results
    with tabs[4]:
        st.header("📥 Export Results")
        
        if st.session_state.simulation_results is None:
            st.info("👈 Run simulation to export results")
        else:
            st.subheader("Download Simulation Data")
            
            # Prepare export data
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'configuration': {
                    'n_rounds': n_rounds,
                    'n_simulations': n_simulations,
                    'n_articles': st.session_state.environment.n_articles
                },
                'results': {}
            }
            
            # Add results for each algorithm
            for name, results in st.session_state.simulation_results.items():
                export_data['results'][name] = {
                    'total_reward': float(sum(results['rewards'])),
                    'final_regret': float(results['regret'][-1]),
                    'avg_ctr': float(np.mean(results['ctr_evolution'])),
                    'regret_history': [float(x) for x in results['regret']],
                    'ctr_history': [float(x) for x in results['ctr_evolution']]
                }
            
            # JSON export
            col1, col2 = st.columns(2)
            
            with col1:
                json_str = json.dumps(export_data, indent=2)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_str,
                    file_name=f"bandit_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                # CSV export of comparison
                if st.session_state.comparison_results is not None:
                    csv = st.session_state.comparison_results.to_csv(index=False)
                    st.download_button(
                        label="📊 Download CSV",
                        data=csv,
                        file_name=f"bandit_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            st.markdown("---")
            
            # Summary report
            st.subheader("📝 Simulation Summary")
            
            if st.session_state.comparison_results is not None:
                best_algo = st.session_state.comparison_results.loc[
                    st.session_state.comparison_results['Avg Total Reward'].idxmax()
                ]
                
                st.success(f"""
                **Best Performing Algorithm**: {best_algo['Algorithm']}
                - Average Total Reward: {best_algo['Avg Total Reward']:.2f}
                - Average CTR: {best_algo['Avg CTR']:.3f}
                - Average Final Regret: {best_algo['Avg Final Regret']:.2f}
                """)


if __name__ == "__main__":
    main()
