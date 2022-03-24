# Project Proposal

### goals 
The main use of this website will be to find diffrent cocktail recipies.

A user will be able to search up the name of a drink and will get back a list of all related drinks.

A user can also search up an ingidient and get back a list off all drinks with that ingridient.

Clicking a drink will bring you to a informational page about the drink.
##### this page will include
 

- a picture of the drink
- instructions to make
- ingridients list
- Similar drinks based on ingridients
Clicking on any ingridient will show you other drinks that contain it

Here is a link to the API i will be using
https://www.thecocktaildb.com/api.php

A user will also be able to register an account.
They can use this account to save drinks to their "Make Later" list which they can go view whenever they are logged in.
When a user clicks a drink they can see how many other users have also saved that drink and this could possibly be used to rank drinks by populatiry on the website

I also want to create a comment feature where users can comment on drinks and leave reviews


### DataBase
The database for this project will have 3 tables.
#### Users
Users will store all user information like username and password.
password will be stored as a hashed string and will be validated using bcrypt.
#### Posts
posts and users will have a many to many relationship
posts will store post id,
user id,
and post text.

#### user_drinks
Will store a user id and a drink id for any drink that was saved by the user.




