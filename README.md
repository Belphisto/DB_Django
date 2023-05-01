# DB_Django

Implemented tasks:

1. Development of a database in SQLLite that mimics a bookstore database:
- The main page displays a list of all books from the database. Near each element there are buttons for changing and deleting data about the current book, there is also an "Add new element" button on the page.
- Implemented changing information about the book and adding a new one on separate pages.
- Implemented the output of the catalog of books in the format "N items per page" with the ability to navigate.

2. Authorization and registration of users:
- Implemented a separate table in the database to store data about users with their role (regular user / authorized / administrator).
- Implemented pages and process for registering and authorizing users on the site.
- Differentiated access to content depending on the role of the user: an unauthorized user can only view the list of books; an authorized user can view the list and add new books; administrator can view, add, edit and delete.

3. Working with sessions and cookies:
- A page has been created with the user's personal account, where he can change his data.
- For each item in the catalog on the main page there is a button "Add to cart".
- It is possible to add an item to the cart and create a new page to view your cart.
- Implemented automatic calculation of the cost of all items in the cart.
- Implemented the ability to place an order based on the user's current shopping cart.
- A page has been implemented to view all your orders, indicating the composition, date and cost of each order.

4. Working with data validation "on the fly" using JavaScript:
- On the registration page, the implementation of on-the-fly input data validation using JavaScript: checking for correctness of the input data (valid email address, password of at least 6 characters), the field is also checked by means of an AJAX request to the server.
- On the output page of the catalog of all books, the ability to filter the contents by any criterion is implemented.

5. Working with site testing on Selenium: automatic verification of all the above stages of working with the site.
