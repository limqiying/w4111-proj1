# COMS4111 Introduction To Databases Project 1
Collaborators: Qi Ying Lim (ql2331) and Sourave Sarkar(ss4645). <br/>
This is a basic front-end web application that will demonstrate some functionalities of our database. 

## PostgreSQL database account

Database account number : ss5645 <br/>
We run this command : psql -U ss5645 -h 34.73.21.127 -d proj1part2

## Parts Implemented
We implemented the main page of our web server, which will allow the user to filter the items in the inventory by the name. The main page also lists other details of each item in the inventory, such as description, price and a list of available reviews.

We added an additional feature that is dedicated mainly to sellers using the UI. This is the statistics page, which will allow any seller to see some essential statistics regarding sales, such as the amount of money spent by each customer, SKU sales statistics, and shipping cost statistics.