1. USER TRIES TO ENTER THE APP

    A. SIGN IN (userValidity)
        ```SELECT 1 FROM USERS WHERE User_ID = %s AND Password = %s;```
            Returns 1 if the user exists with the given input user_id and password.

    B. SIGN UP (insertUser)
        ```SELECT 1 FROM USERS WHERE user_ID = %s;``` (userIDAvail)
            Checks if the user_id is available or is already in use.
        ```INSERT INTO USERS (user_ID, username_fname, username_mname, username_lname, email_address, gender, age, profile_pic, phone_number, password, user_purpose) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);```
            Inters into users all the input values in a tuple.

    C. DELETE (deleteUser)
        ```DELETE FROM USERS WHERE User_ID = 'user_id';```
            Delete the user with the given User_ID after checking if its valid. 

3. IF userPurpose=Customer

    A. Give user recommendation (dishesAvailable)
        ```SELECT DISTINCT d.Dish_ID, d.Dish_Name,r.Restaurant_Name, d.Cuisine, d.Price, AVG(f.Bitter + f.Aftertaste + f.Sweet + f.Sour + f.Spicy + f.Umami + f.Texture + f.Mouthfeel + f.Odour + f.Salty + f.Presentation + f.Sound) AS Overall_Rating FROM DISH_DETAILS d LEFT JOIN RESTAURANTS r ON d.Restaurant_ID = r.Restaurant_ID LEFT JOIN DISH_INGREDIENTS di ON d.Dish_ID = di.Dish_ID LEFT JOIN ALLERGIES a ON di.Ingredients = a.Allergens LEFT JOIN SATIETY_INDEX f ON d.Dish_ID = f.Dish_ID WHERE d.Cuisine IN {cuisine_tuple} AND d.Dish_ID NOT IN (SELECT DISTINCT di.Dish_ID FROM DISH_INGREDIENTS di LEFT JOIN ALLERGIES a ON di.Ingredients = a.Allergens WHERE a.Allergy_Name IN {allergy_tuple}) AND d.Dish_ID NOT IN (SELECT DISTINCT di.Dish_ID FROM DISH_INGREDIENTS di WHERE di.Ingredients IN {exc_ing_tuple}) AND ('{nonveg}' = 'yes' OR d.Dish_ID NOT IN (SELECT Dish_ID FROM NON_VEGETARIAN_DISH_DETAILS)) GROUP BY d.Dish_ID, d.Dish_Name, d.Cuisine, d.Price ORDER BY Overall_Rating DESC;```
            Asks for cuisine the user is interested in, the allergies they might have, and ingredients they wanna exclude from the recommendations.
            It will return dish and restaurant name, cuisine, and price for the recommended dishes.

    chosen_dish=dish the user will choose from the recommendation they will get.

    B. Based on the dish you chose, you will get the proper details of your dishes. (dishDetails)
        ```SELECT * FROM DISH_DETAILS WHERE Dish_ID = %s;```
        ```SELECT Restaurant_Name, Street, Locality, City FROM RESTAURANTS WHERE Restaurant_ID = %s;```
            And then print both the query results using python.

    C. Record feedback (recordFeedback)

        ```INSERT INTO FEEDBACK (Order_ID, User_ID, Dish_ID, Dish_Name, Bitter, Aftertaste, Texture, Sweet, Sour, Umami, Mouthfeel, Odour, Salty, Presentation, Sound, Spicy) VALUES (%s, %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d);```
            Takes the feedback from the user for the chosen dish and insert it into the database.

        ```UPDATE SATIETY_INDEX SET Bitter = (SELECT AVG(Bitter) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Aftertaste = (SELECT AVG(Aftertaste) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sweet = (SELECT AVG(Sweet) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sour = (SELECT AVG(Sour) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Spicy = (SELECT AVG(Spicy) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Umami = (SELECT AVG(Umami) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Texture = (SELECT AVG(Texture) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Mouthfeel = (SELECT AVG(Mouthfeel) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Odour = (SELECT AVG(Odour) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Salty = (SELECT AVG(Salty) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Presentation = (SELECT AVG(Presentation) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sound = (SELECT AVG(Sound) FROM FEEDBACK WHERE Dish_ID = {dish_id});```
            Correspondingly, update the satiety_index for that particular dish by taking avg of all the feedbacks of the dish.

        
4. IF userPurpose="Restaurant_Owner"

    A. insert a new restaurant tuple (insertRestaurant)
        ```INSERT INTO RESTAURANTS (Restaurant_ID, Restaurant_Name, Street, Locality, City, Email_Address, Phone_Number) VALUES (%s, %s, %s, %s, %s, %s, %s);```
            If a Restaurant_Owner want to add a new restaurant in the database, then take input from them all the details and use the insert functionality.

    B. Delete any Restaurant (deleteRestaurant)
        ```DELETE FROM RESTAURANTS WHERE Restaurant_ID = %s;```
            where %s will be the restaurant_id of the restuarant that needs to be deleted.

    C. Changes in Menu of a Restaurant

        1. Add dishes to Menu (addDish)
            ```INSERT INTO DISH_DETAILS (Dish_ID, Dish_Name, Restaurant_ID, Cuisine, Price) VALUES (%s, %s, %d, %s, %d);```
            It takes the details of the dish and adds it to the DISHES entity.

            ```INSERT INTO DISH_INGREDIENTS (Dish_ID, Ingredients) VALUES ;```
            Consecutively, add dish_ingredients for that particular dish.

        2. Delete dishes from Menu (deleteDish)
            ```DELETE FROM DISH_DETAILS WHERE Dish_ID = '%s';```
            Take input of Dish_id you want to delete, and delete it from the menu.

        3. Update the dishes from menu. (updateDish)
            -If attribute='Price'
                ```UPDATE DISH_DETAILS SET Price = %d WHERE Dish_ID = %s;```
                    Update the price for the dish whose dish_id you input.
            -If attribute='Cuisine'
                ```UPDATE DISH_DETAILS SET Cuisine = %s WHERE Dish_ID = %s;```
                    Update the cuisine for the dish whose dish_id you chose.
            -If attribute ='Ingredients'
                ```DELETE FROM DISH_INGREDIENTS WHERE Dish_ID = %d;```
                    Update the ingredients from the dish whose dish_id you chose.
                ```INSERT INTO DISH_INGREDIENTS (Dish_ID, Ingredients) VALUES ;```
                    Update Dish_Ingredients accordingly.

        
