# COMS4111 Introduction To Databases Project 1
Collaborators: Qi Ying Lim (ql2331) and Sourave Sarkar(ss4645). <br/>
This is a basic front-end web application that will demonstrate some functionalities of our database. 

## PostgreSQL database account

Database account number : ss5645 <br/>
We run this command : psql -U ss5645 -h 34.73.21.127 -d proj1part2

## Parts Implemented

# MAIN PAGE
We implemented the main page of our web server, which will allow the user to filter the items in the inventory by the name. The main page also lists other details of each item in the inventory, such as description, price and a list of available reviews. 

Also the user can select each of the items and see all its reviews and ratings. Which is analogus to a Amazon Review page.

We did not end up implementing the features where a user can update his or her database, or where a user can select his/her address and receive the tracking information, by advise of the TAs, who encouraged more "SELECT" statements that will produce interesting information regarding our database.

# STATISTICS PAGE
Therefore, in the spirit of adding more SELECT statements, We added an additional feature that is dedicated mainly to sellers using the UI. This is the statistics page, which will allow any seller to see some essential statistics regarding sales, such as the amount of money spent by each customer, SKU sales statistics, and shipping cost statistics.

The First statistics is the amount spent by each customer. It can be filtered by minimum spent amount. It is important as finding top spending customers are crucial.

The second is SKU level sale and rating analytics. It is important as it helps to find out popular items both rating wise and sell wise.

The third is Shipping cost analytics. Again we can filter by to zip code and minimum cost. This helps to analyze which areas expensive to ship items.

## Interesting Database Operations

We believe that our main page is interesting, as it lists all the available products available that is in stock. That is, inventory that has 0 quantity in stock will not be displayed. Also, mimicks commercial shopping websites where the users are allowed to filter by ratings, for example, to narrow their search. These rating filter inputs are used as a threshold for the average rating for any particular product, and only products that match the search criteria is displayed. Moreover, the user can select particular items to view more details about the item, such as a list of specific reviews. 
