1. USER TRIES TO ENTER THE APP

    A. SIGN IN (userValidity)<br>
        ```SELECT 1 FROM USERS WHERE User_ID = %s AND Password = %s;```
            Returns 1 if the user exists with the given input user_id and password.

    B. SIGN UP (insertUser)<br>
        ```SELECT 1 FROM USERS WHERE user_ID = %s;``` (userIDAvail)
            Checks if the user_id is available or is already in use.<br>
        ```INSERT INTO USERS (user_ID, username_fname, username_mname, username_lname, email_address, gender, age, profile_pic, phone_number, password, user_purpose) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);```
            Insert into users all the input values in a tuple.

    C. DELETE (deleteUser)<br>
        ```DELETE FROM USERS WHERE User_ID = 'user_id';```
            Delete the user with the given User_ID after checking if its valid. 

2. IF userPurpose=Customer

    A. Give user recommendation (dishesAvailable)<br>
        ```SELECT DISTINCT d.Dish_ID, d.Dish_Name,r.Restaurant_Name, d.Cuisine, d.Price, AVG(f.Bitter + f.Aftertaste + f.Sweet + f.Sour + f.Spicy + f.Umami + f.Texture + f.Mouthfeel + f.Odour + f.Salty + f.Presentation + f.Sound) AS Overall_Rating FROM DISH_DETAILS d LEFT JOIN RESTAURANTS r ON d.Restaurant_ID = r.Restaurant_ID LEFT JOIN DISH_INGREDIENTS di ON d.Dish_ID = di.Dish_ID LEFT JOIN ALLERGIES a ON di.Ingredients = a.Allergens LEFT JOIN SATIETY_INDEX f ON d.Dish_ID = f.Dish_ID WHERE d.Cuisine IN {cuisine_tuple} AND d.Dish_ID NOT IN (SELECT DISTINCT di.Dish_ID FROM DISH_INGREDIENTS di LEFT JOIN ALLERGIES a ON di.Ingredients = a.Allergens WHERE a.Allergy_Name IN {allergy_tuple}) AND d.Dish_ID NOT IN (SELECT DISTINCT di.Dish_ID FROM DISH_INGREDIENTS di WHERE di.Ingredients IN {exc_ing_tuple}) AND ('{nonveg}' = 'yes' OR d.Dish_ID NOT IN (SELECT Dish_ID FROM NON_VEGETARIAN_DISH_DETAILS)) GROUP BY d.Dish_ID, d.Dish_Name, d.Cuisine, d.Price ORDER BY Overall_Rating DESC;```<br>
            Asks for cuisine the user is interested in, the allergies they might have, and ingredients they wanna exclude from the recommendations.
            It will return dish and restaurant name, cuisine, and price for the recommended dishes.

    B. Based on the dish you chose, you will get the proper details of your dishes. (dishDetails)<br>
        ```SELECT * FROM DISH_DETAILS WHERE Dish_ID = %s;```<br>
        ```SELECT Restaurant_Name, Street, Locality, City FROM RESTAURANTS WHERE Restaurant_ID = %s;```<br>
            And then print both the query results using python.

    C. Record feedback (recordFeedback)<br>
        ```INSERT INTO FEEDBACK (Order_ID, User_ID, Dish_ID, Dish_Name, Bitter, Aftertaste, Texture, Sweet, Sour, Umami, Mouthfeel, Odour, Salty, Presentation, Sound, Spicy) VALUES (%s, %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d);```
            Takes the feedback from the user for the chosen dish and insert it into the database.<br>
        ```UPDATE SATIETY_INDEX SET Bitter = (SELECT AVG(Bitter) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Aftertaste = (SELECT AVG(Aftertaste) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sweet = (SELECT AVG(Sweet) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sour = (SELECT AVG(Sour) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Spicy = (SELECT AVG(Spicy) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Umami = (SELECT AVG(Umami) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Texture = (SELECT AVG(Texture) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Mouthfeel = (SELECT AVG(Mouthfeel) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Odour = (SELECT AVG(Odour) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Salty = (SELECT AVG(Salty) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Presentation = (SELECT AVG(Presentation) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sound = (SELECT AVG(Sound) FROM FEEDBACK WHERE Dish_ID = {dish_id});```
            Correspondingly, update the satiety_index for that particular dish by taking avg of all the feedbacks of the dish.

        
3. IF userPurpose="Restaurant_Owner"<br>

    A. insert a new restaurant tuple (insertRestaurant)<br>
        ```INSERT INTO RESTAURANTS (Restaurant_ID, Restaurant_Name, Street, Locality, City, Email_Address, Phone_Number) VALUES (%s, %s, %s, %s, %s, %s, %s);```<br>
            If a Restaurant_Owner want to add a new restaurant in the database, then take input from them all the details and use the insert functionality.

    B. Delete any Restaurant (deleteRestaurant)<br>
        ```DELETE FROM RESTAURANTS WHERE Restaurant_ID = %s;```<br>
            where %s will be the restaurant_id of the restuarant that needs to be deleted.

    C. Changes in Menu of a Restaurant<br>
        1. Add dishes to Menu (addDish)<br>
            ```INSERT INTO DISH_DETAILS (Dish_ID, Dish_Name, Restaurant_ID, Cuisine, Price) VALUES (%s, %s, %d, %s, %d);```<br>
            It takes the details of the dish and adds it to the DISHES entity.<br>
            ```INSERT INTO DISH_INGREDIENTS (Dish_ID, Ingredients) VALUES ;```<br>
            Consecutively, add dish_ingredients for that particular dish.
        2. Delete dishes from Menu (deleteDish)<br>
            ```DELETE FROM DISH_DETAILS WHERE Dish_ID = '%s';```<br>
            Take input of Dish_id you want to delete, and delete it from the menu.
        3. Update the dishes from menu. (updateDish)<br>
            *If attribute='Price'<br>
                ```UPDATE DISH_DETAILS SET Price = %d WHERE Dish_ID = %s;```<br>
                    Update the price for the dish whose dish_id you input.
            -If attribute='Cuisine'<br>
                ```UPDATE DISH_DETAILS SET Cuisine = %s WHERE Dish_ID = %s;```<br>
                    Update the cuisine for the dish whose dish_id you chose.
            -If attribute ='Ingredients'<br>
                ```DELETE FROM DISH_INGREDIENTS WHERE Dish_ID = %d;```
                    Update the ingredients from the dish whose dish_id you chose.<br>
                ```INSERT INTO DISH_INGREDIENTS (Dish_ID, Ingredients) VALUES ;```
                    Update Dish_Ingredients accordingly.

        
