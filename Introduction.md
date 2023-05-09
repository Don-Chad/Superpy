🍎 **WELCOME TO SUPER-MARK CLI: THE ULTIMATE EMPLOYEE GUIDE**🍎 

Dear new employee,

Welcome to the team! As a valuable member of our team, you're going to be using the revolutionary **Super-Mark CLI** (Command Line Interface), designed to make your life easier, more efficient, and a bit more fun. We are extremely proud of this CLI, and we're sure you'll love it too. 

Let's dive into the features:

🚀 **Feature Highlights:**

1. Simple yet powerful inventory management. 
2. Buying and selling products is a breeze; using short, intuitive CLI command’s. Minimal typing, maximal stocking. 
3. Tracking of revenue and profit and costs, over any time period. 
4. Visual representation of costs, revenue, and profit. 
5. Time-shifting: system Time-travel to check inventory on any date, or book products on different dates then today. 
6. FIFO (First In, First Out) selling strategy: Our inventory system is FIFO-powered. When you sell a product, the system checks for the product with the earliest purchase date and hasn't been sold yet, ensuring the product first in is sold first out.

💎 **What We're Most Proud Of:**

1. The flexibility to handle multiple product attributes
2. Robustness; this program can handle everything.
3. The ease of use for you and your colleagues - that's YOU!
4. Groovy introduction animation as your database is prepared. 

Now, let's show you about how you can use the Super-Mark CLI to make your work a breeze:

**1. Buying Products:**

To buy products, use the buy ****action, simply followed by the product name, price, expiration date. If you want to buy multiple products at once, use the multiple-buy function, by adding an amount to buy at the end.  

***python3 supermark.py buy Apple 10.00 2024-01-03
python3 supermark.py buy Apple 10.00 2024-01-03 5***

**2. Selling Products:**

Sell products with the sell action, followed by the product name, sell price, and the sell date (optional). If you want to sell multiple products at once, use the  function, simply by adding an amount at the end. You may also use ‘today’, ‘tomorrow’, or ‘yesterday’ instead of a written date. To make life even easier (time is money), you can also sell without mentioning a date, in which case today’s date is presumed. 

***python3 supermark.py sell Apple 10.00*** 
***python3 supermark.py sell Apple 10.00 2024-01-01 5
python3 supermark.py sell Apple 10.00 today***

**3. Checking Inventory:**

Easily check the inventory on any date  with the inventory action. The default is today’s date.

***python3 supermark.py inventory*** 

**4. Tracking Revenue:**

Keep an eye on the revenue for a specific period or until today with the revenue action.

***python3 supermark.py revenue 2024-01-01 2024-01-31***

**5. Analysing Profit:**

Use the profit action to check the profit for a specific period or until today (default).

***python3 supermark.py profit 2024-01-01 2024-01-31***

**6. Visualizing Costs, Revenue, and Profit:**

Get a crystal clear visual representation of your costs, revenue, and profit with the stats action or by using  —display-stats

***python3 supermark.py stats
python3 supermark.py --display-stats***

**7. Changing the system date for today:**

In case you want you need to do extensive administration work, the system’s date can be time-shifted. This will set the internal date of the system to a given date, or move it by X (amount of days). This will work on all the operations.

You can set a new internal date accordingly:

***python3 supermark.py timesshift 2024-11-01

If you want to move the internal date forwards or backwards:

***python3 supermark.py timesshift -5
python3 supermark.py timesshift +5***

Be mindful: the time-shift 4 is a permanent change, staying active until you shift it back. Shifting back is done by executing a time-shift with the negative value of the current applied time-shift value. 

Now that you're  up to date with the knowledge of the fantastic Super-Mark CLI, you're ready to conquer the supermarket world. Happy selling! 🎉
