import numpy as sarah_np
import pandas as sarah_pd
import matplotlib.pyplot as sarah_plt

sarah_dates = sarah_pd.date_range(start='2015-01-01', end='2025-01-01', freq='B')
sarah_prices = sarah_np.random.normal(loc=250, scale=25, size=len(sarah_dates)).cumsum()
sarah_returns = sarah_np.diff(sarah_prices) / sarah_prices[:-1]

sarah_stock_data = sarah_pd.DataFrame({
    'Date': sarah_dates,
    'Adj Close': sarah_prices,
    'Return': sarah_np.append([0], sarah_returns)
})
sarah_stock_data.set_index('Date', inplace=True)

sarah_plt.figure(figsize=(10, 5))
sarah_plt.subplot(2, 1, 1)
sarah_plt.plot(sarah_stock_data['Adj Close'])
sarah_plt.title('Simulated Stock Prices Over Time')
sarah_plt.subplot(2, 1, 2)
sarah_plt.plot(sarah_stock_data['Return'])
sarah_plt.title('Daily Return Percentage Change')
sarah_plt.tight_layout()
sarah_plt.savefig('simulated_stock_prices.png')
sarah_plt.close()

sarah_hmm_states = sarah_np.random.choice([0, 1], size=len(sarah_stock_data), p=[0.6, 0.4])
sarah_stock_data['Hidden State'] = sarah_hmm_states

sarah_plt.figure(figsize=(10, 6))
sarah_plt.plot(sarah_stock_data.index, sarah_stock_data['Adj Close'])
for sarah_state in range(2):
    sarah_state_data = sarah_stock_data[sarah_stock_data['Hidden State'] == sarah_state]
    sarah_plt.scatter(sarah_state_data.index, sarah_state_data['Adj Close'], label=f'State {sarah_state}')
sarah_plt.title('Stock Prices with Simulated Hidden States')
sarah_plt.legend()
sarah_plt.savefig('hidden_state_analysis.png')
sarah_plt.close()

sarah_transition_matrix = [[0.8, 0.2], [0.3, 0.7]]
print("\nTransition Matrix:\n", sarah_transition_matrix)

sarah_plt.figure(figsize=(6, 4))
sarah_plt.imshow(sarah_transition_matrix, cmap="Blues", alpha=0.5)
for i in range(len(sarah_transition_matrix)):
    for j in range(len(sarah_transition_matrix)):
        sarah_plt.text(j, i, f'{sarah_transition_matrix[i][j]:.2f}', ha='center', va='center', color='black')
sarah_plt.title("Transition Matrix Example")
sarah_plt.xticks(ticks=[0, 1], labels=['Phase A', 'Phase B'])
sarah_plt.yticks(ticks=[0, 1], labels=['Phase A', 'Phase B'])
sarah_plt.colorbar()
sarah_plt.savefig('transition_matrix.png')
sarah_plt.close()

sarah_plt.figure(figsize=(10, 6))
sarah_plt.plot(sarah_stock_data.index, sarah_stock_data['Return'])
for sarah_state in range(2):
    sarah_state_data = sarah_stock_data[sarah_stock_data['Hidden State'] == sarah_state]
    sarah_plt.scatter(sarah_state_data.index, sarah_state_data['Return'], label=f'State {sarah_state}', s=10)
sarah_plt.title('Daily Returns with Simulated Hidden States')
sarah_plt.legend()
sarah_plt.savefig('daily_returns_with_states.png')
sarah_plt.close()
