

## API

### `compute_portvals`
```python
def compute_portvals(
    orders_file="./orders/orders.csv",
    start_val=1000000,
    commission=9.95,
    impact=0.005,
):
```
- **Input**:
  - `orders_file`: Path to CSV file with columns: `Date`, `Symbol`, `Order` (`BUY`/`SELL`), `Shares`.
  - `start_val`: Initial portfolio value (default: `1,000,000`).
  - `commission`: Fixed commission per trade (default: `9.95`).
  - `impact`: Market impact per trade (default: `0.005`).
- **Output**: `pandas.DataFrame` with daily portfolio values.

---

## Implementation

### Order Processing
1. **Read Orders**:
   ```python
   orders_df = pd.read_csv(orders_file, parse_dates=True, index_col='Date')
   ```
2. **Fetch Prices**:
   ```python
   prices = get_data(symbols, pd.date_range(start_date, end_date))
   ```

### Portfolio Calculation
1. **Transaction Costs**:
   - **Buy**: 
     \[
     \text{cost} = \text{shares} \times \text{price} \times (1 + \text{impact}) + \text{commission}
     \]
   - **Sell**: 
     \[
     \text{cost} = \text{shares} \times \text{price} \times (1 - \text{impact}) - \text{commission}
     \]
2. **Portfolio Value**:
   \[
   \text{portvals} = \sum (\text{prices} \times \text{holdings}) + \text{cash}
   \]

---

## Example Usage

```python
# Compute portfolio values
portvals = compute_portvals(orders_file="./orders/orders.csv", start_val=1000000)

# Test code
test_code()
```

---

## Performance Metrics

### Sharpe Ratio
\[
\text{Sharpe Ratio} = \sqrt{252} \times \frac{\text{avg daily return}}{\text{std of daily returns}}
\]

### Cumulative Return
\[
\text{Cumulative Return} = \frac{\text{final portfolio value}}{\text{initial portfolio value}} - 1
\]

### Daily Returns
\[
\text{Daily Returns} = \frac{\text{portvals}_t}{\text{portvals}_{t-1}} - 1
\]

---

## Dependencies
- **Python 3.x**
- **pandas**, **numpy**
- **util.py**
