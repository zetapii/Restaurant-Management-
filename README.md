## The Database
The following relations are present in the database:
* Restaurant
* Billings
* Customer
* Expenditure
* Menu
* Order_Details
* Order_Items
* Staff

## The Interface
### Functionalities
* The python program can handle all valid insertions, updates and deletions into the database relations.
* In case of invalid input, a suitable error is thrown.
* There is provision to view the current state of any relation.
* In addition to basic retrievals, updates and deletions, some queries are supported:
	* Query to obtain the most profitable month for any restaurant
	* Query to obtain the total profit earned by a restaurant
	* Getting the history of orders by a customer across all the restaurant outlets.
	* Most selling dish of a given restaurant

### Instructions to Run
* A new user is required to first create the database schema. This can be done by opening the MySQL server, and running the ```create_db.sql```.
* Then the user can run the database interface program by running ```python3 main.py```.
* The user will be prompted to enter the MySQL username, password and the port number of the MySQL server.

