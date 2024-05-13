Here's a script that encapsulates the steps outlined above:

```bash
#!/bin/bash

# Step 1: Install Python
# If Python is not installed, download and install it from https://www.python.org/downloads/

# Step 2: Create a Virtual Environment
python3 -m venv env

# Step 3: Activate the Virtual Environment
source env/bin/activate

# Step 4: Install Required Libraries
pip install pandas numpy scikit-learn yfinance TA-Lib

# Step 5: Create a Python File
touch trading_bot.py

# Step 6: Copy the Code
# Open trading_bot.py in your preferred text editor and paste the Python code provided

# Step 7: Run the Script
python trading_bot.py

# Step 8: Deactivate the Virtual Environment (Optional)
deactivate
```

Save this script as `setup_trading_bot.sh` in your project directory. Then, open Terminal, navigate to your project directory, and run the following command to make the script executable:

```bash
chmod +x setup_trading_bot.sh
```

Now you can run the script by executing:

```bash
./setup_trading_bot.sh
```

This script automates the setup process, making it easier to get started with the trading bot in a new Python project on macOS. Remember to customize the `trading_bot.py` file with the Python code provided earlier.