# Black-Scholes Option Pricing and Implied Volatility Calculator

This project is a web application for calculating option prices using the Black-Scholes-Merton model and implied volatility using the Newton-Raphson method. The application is built using Python with a web framework, and it provides a user-friendly interface for inputting parameters and viewing results.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7+
- Flask
- SciPy

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/fallender5/BS-and-IV-calculator.git
    cd BS-and-IV-calculator
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. You will see the homepage where you can select between calculating option prices or implied volatility.
3. Enter the required parameters and click on the "Calculate" button to get the results.


## Features

- **Black-Scholes-Merton Model:** Calculate call and put option prices.
- **Implied Volatility Calculation:** Compute implied volatility using the Newton-Raphson method.
- **User-Friendly Interface:** Simple web interface for input and output.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


