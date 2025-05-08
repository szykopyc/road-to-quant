![Python](https://img.shields.io/badge/python-3.11-blue)
# road-to-quant
This repo documents my journey into quantitative finance through small, focused projects inspired by concepts taught in *Quantitative Portfolio Management* by Michael Isichenko.

## Backstory
Although I don't come from a quantitative background, I am deeply drawn to quant finance because:
- It uses data to forecast asset prices.
- It allows me to apply my programming skills in a meaningful way.
- It represents a challenging intellectual pursuit.

On the 2nd May 2025, I bought the book *Quantitative Portfolio Management* by Michael Isichenko to begin structured learning on this journey. My earlier interest in quant finance led me to explore topics like CAPM, mean-variance optimization, and risk metrics, but mostly through self-guided experimentation in Python. While my initial understanding was limited, the tools I built — especially Drapt Analytics, an in-progress portfolio analytics tool, which can be found [here](https://github.com/szykopyc/drapt-analytics.git) — proved to be both functional and personally rewarding.


This time, my goal is to approach quant finance with both theory and practical implementation. Even if I don't end up working as a quant, I believe that intellectual curiosity is always a valuable pursuit.

Szymon Kopycinski
[LinkedIn](https://www.linkedin.com/in/szymonkopycinski)

## Chapters
- **Chapter 1: Market Data**
    - This chapter explored the different types of data, corporate actions and their adjustments, and linear vs log returns.
    - The mini-projects include 2 notebooks, one showing adjustment for corporate actions, and one for the difference between linear and log returns.
- **Chapter 2: Forecasting**
    - This chapter has so far explored data used for forecasts (e.g., event-based predictors, macroeconomic data, alternative data), as well as technical forecasts (e.g., mean reversion, momentum).
    - So far, the mini-projects are a notebook visualising mean-reversion, including noise, residuals, market beta, as well as a simple momentum trading strategy with a backtester. Unsurprisingly, the momentum trading strategy had a negative Sharpe Ratio.
    - This chapter is still being read, further mini-projects will be added.

## Future Plans
- Finish reading Chapter 2, complete any further projects.

## Technologies
- Python 3.11
- Pandas, NumPy, Matplotlib, yfinance
- Jupyter Notebook
- Git

## Setup Instructions
1. Clone the repo: `git clone https://github.com/szykopyc/road-to-quant.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run scripts using Jupyter Notebook or Python where applicable:
    - Example: `jupyter notebook adjusting_for_corporate_actions.ipynb`

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute it with proper attribution.