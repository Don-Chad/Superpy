# Untitled

# **SUPER-MARK CLI: Technical Report**

In this report, I describe three technical elements of the SUPER-MARK CLI backend and speak to the development choices and considerations I made throughout the process. All in all I must say I had a lot of fun working on this. It has turned out into a lot of code - it’s hard to stop improving and adding features - but I hope this shows I learned a lot in creating my first real program.

## **1. Pendulum for Date and Time Handling**

Challenge: 

Dates proved to be very hard to work with indeed! During the development of the CLI, I faced issues with the built-in datetime module in Python due to naming conflicts between the module and other internal modules - ‘datetime.datetime’ and ‘datetime.date’. The conflicts took me a lot of time and effort to troubleshoot - mainly because the errors were not apparent and hard to pinpoint - and therefore I choose to work with another module all together - which also was a good exercise in itself. I wanted to avoid any more problems with this alltogether, so the choice for a radically different direction makes sense to me. 

Solution & Rationale: 

I chose to use the Pendulum module instead of datetime for the generation of today’s date, which also offers a  intuitive and user-friendly interface for handling date and time objects. 

## 2**. Creating unique identifiers for each product**

Challenge: 

Over time, I noticed mistakes entering into the database values. Products numbers got mixed up with other values, and just a normal number for a product seemed prone to errors. 

Solution & Rationale: 

I chose to give each bought and sold product a UUID in de bought and sold file, using the UUID module. The result is very robust; If the UUID’s match up when comparing - for example when  we are very sure that we are working/selecting the right product. 

Examples: The buy function generates a UUID for each purchased product using uuid.uuid(). 

This uuid is stored as BOUGHT_ID in the bought.csv file. The bought_id is used to uniquely identify each purchased product.

## 3**. Inventory Function with Sets**

Challenge: 

One of the main challenges in the development of the inventory function was to find an good method for selecting the right products, from both the sold and bought file. The challenge was to keep count of the available items, the items sold, and ensuring that expired items were not included in the inventory. The selecting mechanism was quite hard to get working well. 

Solution & Rationale:

To address this, I decided to use Python sets, as they enable sorting with unique elements. They allowed me to maintain a collection of unique bought_ids for the products that have been sold.

In the inventory function, I first read the data from the bought and sold CSV files. Next, I created a set called 'sold_bought_ids' that stores the unique bought_ids of the sold items. This set allows for direct checks for sold items when going through the bought items to generate the inventory report.

In summery: I made sure that only valid and unsold items were counted in the inventory. A dictionary keeps track of the quantities of each unique product.