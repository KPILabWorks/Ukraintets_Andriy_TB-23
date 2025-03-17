# 4. Байєсівський аналіз споживання
# Реалізуйте байєсівську регресію для моделювання залежностей між погодними умовами та енергоспоживанням. Порівняйте отримані висновки з результатами, отриманими за допомогою класичної лінійної регресії.

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.optimize import minimize

N = 100
temperature = np.random.uniform(-10, 35, N)  # Температура від -10 до 35°C
energy_consumption = 50 - 1.5 * temperature + np.random.normal(0, 5, N)  # Лінійна залежність + шум

# Візуалізація вхідних даних
plt.scatter(temperature, energy_consumption, alpha=0.6, label="Observed Data")
plt.xlabel("Temperature (°C)")
plt.ylabel("Energy Consumption (kWh)")
plt.legend()
plt.show()

# Лінійна регресія
X = temperature.reshape(-1, 1)
lin_reg = LinearRegression().fit(X, energy_consumption)
beta_hat = [lin_reg.intercept_, lin_reg.coef_[0]]  # Оцінки параметрів

# Передбачення та похибка для класичної регресії
y_pred_classic = lin_reg.predict(X)
mse_classic = mean_squared_error(energy_consumption, y_pred_classic)

# Байєсівська регресія
# Апріорні розподіли: N(0, 10) для β0 та β1
prior_mu = [0, 0]
prior_sigma = [10, 10]

# Функція логарифма апостеріорного розподілу
def log_posterior(beta, X, y, sigma=5):
    beta0, beta1 = beta
    prior_prob = stats.norm(prior_mu[0], prior_sigma[0]).logpdf(beta0) + \
                 stats.norm(prior_mu[1], prior_sigma[1]).logpdf(beta1)
    likelihood = np.sum(stats.norm(beta0 + beta1 * X.flatten(), sigma).logpdf(y))
    return prior_prob + likelihood

# Оптимізація MAP (максимальна апостеріорна оцінка)
result = minimize(lambda b: -log_posterior(b, X, energy_consumption), x0=[0, 0])
beta_map = result.x

# Передбачення та похибка для байєсівської регресії
y_pred_bayes = beta_map[0] + beta_map[1] * X.flatten()
mse_bayes = mean_squared_error(energy_consumption, y_pred_bayes)

print(f"Класична регресія: β0 = {beta_hat[0]:.2f}, β1 = {beta_hat[1]:.2f}, MSE = {mse_classic:.2f}")
print(f"Байєсівська (MAP) регресія: β0 = {beta_map[0]:.2f}, β1 = {beta_map[1]:.2f}, MSE = {mse_bayes:.2f}")

# Візуалізація результатів
x_range = np.linspace(-10, 35, 100)
y_classic = beta_hat[0] + beta_hat[1] * x_range
y_bayes = beta_map[0] + beta_map[1] * x_range

plt.scatter(temperature, energy_consumption, alpha=0.5, label="Observed Data")
plt.plot(x_range, y_classic, label=f"Classic Regression (MSE={mse_classic:.2f})", color="red", linestyle="dashed")
plt.plot(x_range, y_bayes, label=f"Bayesian Regression (MSE={mse_bayes:.2f})", color="green")
plt.xlabel("Temperature (°C)")
plt.ylabel("Energy Consumption (kWh)")
plt.legend()
plt.show()

plt.figure(figsize=(10, 4))
plt.bar(["β0 (Intercept)", "β1 (Slope)"], [beta_hat[0], beta_hat[1]], alpha=0.6, label="Classic Regression", color="red")
plt.bar(["β0 (Intercept)", "β1 (Slope)"], [beta_map[0], beta_map[1]], alpha=0.6, label="Bayesian Regression", color="green")
plt.ylabel("Coefficient Value")
plt.legend()
plt.title("Comparison of Regression Coefficients")
plt.show()
