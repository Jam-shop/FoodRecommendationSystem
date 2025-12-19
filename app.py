import pymysql
from tabulate import tabulate

db=pymysql.connect(host='localhost',
                           user='nilanjana',
                           password='Ni07-De10',
                           database='food_rec_sys')
cursor = db.cursor()


def get_next_primary_key(table_name, column_name, prefix):
    try:
        query = f"SELECT MAX({column_name}) AS max_key FROM {table_name};"
        cursor.execute(query)
        max_key = cursor.fetchall()[0][0]
        
        if max_key:
            next_number = str(int(max_key[1:]) + 1)
        else:
            next_number = str(101)

        return f"{prefix}{next_number}"
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def userValidity(userID, password):
    try:
        q = "SELECT User_ID FROM USERS WHERE User_ID = %s AND Password = %s;"
        cursor.execute(q, (userID, password))
        result = cursor.fetchall()
        return result

    except Exception as e:
        db.rollback()
        print("Failed to validate\n>>>>>>> ", e)
        return None


def userIDAvail(userID):
    try:
        q = "SELECT User_ID FROM USERS WHERE User_ID = %s;"
        cursor.execute(q, (userID,))
        result = cursor.fetchall()
        return result
    
    except Exception as e:
        db.rollback()
        print("Failed to check availability\n>>>>>>> ", e)
        return None


def insertUser():
    try:
        while True:
            user_id = input("Choose a User ID: ").strip()
            if userIDAvail(user_id):
                print("This User ID has been taken. Choose another one.")
            else:
                break
        print("\nEnter your details:")
        username_fname = input("First name: ").strip()
        username_mname = input("Middle name: ").strip()
        username_lname = input("Last name: ").strip()
        email_address = input("Email address: ").strip()
        gender = input("Gender (Male/Female/Others/Prefer not to say): ").strip()
        dob = input("Date of Birth (YYYY-MM-DD): ").strip()
        profile_pic = input("Profile picture: ").strip()
        phone_number = input("Phone number: ").strip()
        user_purpose = input("User purpose (Customer/Restaurant Owner): ").strip()

        password = input("Set a password: ").strip()

        q = "INSERT INTO USERS (User_ID, User_Name_FName, User_Name_MInit, User_Name_LName, Email_Address, Gender, DOB, Profile_Picture, Phone_Number, Password, User_Purpose) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        value = (user_id, username_fname, username_mname, username_lname, email_address, gender.replace(" ", "_"), dob, profile_pic, phone_number, password, user_purpose.capitalize().replace(" ", "_"))
        cursor.execute(q, value)
        db.commit()
        return user_id


    except Exception as e:
        db.rollback()
        print("Failed to insert into database\n>>>>>>> ", e)
        return None


def deleteUser():
    try:
        user_id = input("Enter your User ID: ")
        q = "DELETE FROM USERS WHERE User_ID = %s;"
        cursor.execute(q, (user_id,))
        db.commit()
        print("Sorry to see you go :(")
        return user_id

    except Exception as e:
        db.rollback()
        print("Failed to delete from the database\n>>>>>>> ", e)
        return None


def dishesAvailable():
    try:
        print("\nWhat do you want to eat today?\n\n1.  North_Indian\n2.  South_Indian\n3.  Chinese\n4.  Japanese\n5.  Korean\n6.  Thai\n7.  Italian\n8.  Mediterranean\n9.  Mexican\n10. Continental\n11. Fast_food\n12. Turkish\n13. Fusion\n")

        cuisine = input("\nEnter the cuisines (1-13) you want to choose by seperating them with a comma: ").split(",")
        cuisine_tuple = tuple(cuisine)
        allergy = input("Any allergies? (Seperate them with a comma): ").split(",")
        allergy_tuple = tuple(allergy)
        exc_ing = input("Any ingredients you want to exclude? (Seperate them with a comma): ").split(",")
        exc_ing_tuple = tuple(exc_ing)
        nonveg = input("Do you want us to include Non-vegetarian dishes? (yes/no): ").strip().lower()
        if len(cuisine_tuple) == 1:
            cuisine_tuple = f"('{cuisine_tuple[0]}')"
        else:
            cuisine_tuple = str(cuisine_tuple)

        if len(allergy_tuple) == 1:
            allergy_tuple = f"('{allergy_tuple[0]}')"
        else:
            allergy_tuple = str(allergy_tuple)

        if len(exc_ing_tuple) == 1:
            exc_ing_tuple = f"('{exc_ing_tuple[0]}')"
        else:
            exc_ing_tuple = str(exc_ing_tuple)


        q = f"SELECT DISTINCT d.Dish_ID, d.Dish_Name,r.Restaurant_Name, d.Cuisine, d.Price, AVG(f.Bitter + f.Aftertaste + f.Sweet + f.Sour + f.Spicy + f.Umami + f.Texture + f.Mouthfeel + f.Odour + f.Salty + f.Presentation + f.Sound) AS Overall_Rating FROM DISH_DETAILS d LEFT JOIN RESTAURANTS r ON d.Restaurant_ID = r.Restaurant_ID LEFT JOIN DISH_INGREDIENTS di ON d.Dish_ID = di.Dish_ID LEFT JOIN ALLERGIES a ON di.Ingredients = a.Allergens LEFT JOIN SATIETY_INDEX f ON d.Dish_ID = f.Dish_ID WHERE d.Cuisine IN {cuisine_tuple} AND d.Dish_ID NOT IN (SELECT DISTINCT di.Dish_ID FROM DISH_INGREDIENTS di LEFT JOIN ALLERGIES a ON di.Ingredients = a.Allergens WHERE a.Allergy_Name IN {allergy_tuple}) AND d.Dish_ID NOT IN (SELECT DISTINCT di.Dish_ID FROM DISH_INGREDIENTS di WHERE di.Ingredients IN {exc_ing_tuple}) AND ('{nonveg}' = 'yes' OR d.Dish_ID NOT IN (SELECT Dish_ID FROM NON_VEGETARIAN_DISH_DETAILS)) GROUP BY d.Dish_ID, d.Dish_Name, d.Cuisine, d.Price ORDER BY Overall_Rating DESC;"
        cursor.execute(q)
        result = cursor.fetchall()
        return result
    
    except Exception as e:
        db.rollback()
        print("Failed to retrieve data from the database\n>>>>>>> ", e)
        return None


def dishDetails(dish_id):
    try:
        print("\n\nHere's more detail about the dish you chose:")
        q = "SELECT * FROM DISH_DETAILS WHERE Dish_ID = %s;"
        cursor.execute(q, (dish_id,))
        results = cursor.fetchall()
        r = "SELECT Restaurant_Name, Street, Locality, City FROM RESTAURANTS WHERE Restaurant_ID = %s;"
        cursor.execute(r, (results[2],))
        rest_results = cursor.fetchall()
        print(f"\nDish ID: {results[0]}\nDish Name: {results[1]}\nRestaurant Name: {rest_results[0]}\nRestaurant Address: {rest_results[1]}, {rest_results[2]}, {rest_results[3]}\nCuisine: {results[3]}\nPrice: {results[4]}\n")
        return None
    
    except Exception as e:
        db.rollback()
        print("Failed to retrieve data from the database\n>>>>>>> ", e)
        return None


def recordFeedback(user_id, dish_id):
    try:
        print("Charles Boyle, our messiah, would like your opinion on the food we recommended to you based on the following parameters.")
        Bitter = input("Bitter (on a scale of 1 to 10): ")
        Aftertaste = input("Aftertaste (on a scale of 1 to 10): ")
        Texture = input("Texture (on a scale of 1 to 10): ")
        Sweet = input("Sweetness (on a scale of 1 to 10): ")
        Sour = input("Sourness (on a scale of 1 to 10): ")
        Umami = input("Umami (on a scale of 1 to 10): ")
        Mouthfeel = input("Mouthfeel (on a scale of 1 to 10): ")
        Odour = input("Odour (on a scale of 1 to 10): ")
        Salty = input("Salty (on a scale of 1 to 10): ")
        Presentation = input("Presentation (on a scale of 1 to 10): ")
        Sound = input("Sound (on a scale of 1 to 10): ")
        Spicy = input("Spicy (on a scale of 1 to 10): ")
        order_id = get_next_primary_key("FEEDBACK", "Order_ID", "O")
        if not order_id:
            print("Failed to generate primary key.")
            return
        
        cursor.execute("SELECT Dish_Name FROM DISH_DETAILS WHERE Dish_ID = %s;", dish_id)
        dish_name = cursor.fetchall()[0][0]
        
        q1 = "INSERT INTO FEEDBACK (Order_ID, User_ID, Dish_ID, Dish_Name, Bitter, Aftertaste, Texture, Sweet, Sour, Umami, Mouthfeel, Odour, Salty, Presentation, Sound, Spicy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        value = (order_id, user_id, dish_id, dish_name, Bitter, Aftertaste, Texture, Sweet, Sour, Umami, Mouthfeel, Odour, Salty, Presentation, Sound, Spicy)
        cursor.execute(q1, value)
        result = cursor.fetchall()

        q2 = f"UPDATE SATIETY_INDEX SET Bitter = (SELECT AVG(Bitter) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Aftertaste = (SELECT AVG(Aftertaste) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sweet = (SELECT AVG(Sweet) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sour = (SELECT AVG(Sour) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Spicy = (SELECT AVG(Spicy) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Umami = (SELECT AVG(Umami) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Texture = (SELECT AVG(Texture) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Mouthfeel = (SELECT AVG(Mouthfeel) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Odour = (SELECT AVG(Odour) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Salty = (SELECT AVG(Salty) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Presentation = (SELECT AVG(Presentation) FROM FEEDBACK WHERE Dish_ID = {dish_id}), Sound = (SELECT AVG(Sound) FROM FEEDBACK WHERE Dish_ID = {dish_id});"
        cursor.execute(q2)
        db.commit()
        return result
    
    except Exception as e:
        db.rollback()
        print("Failed to insert data into the database\n>>>>>>> ", e)
        return None

def insertRestaurant():
    try:
        print("Enter details of the new restaurant:")
        rest_name = input("Restaurant name: ").strip()
        street = input("Address Line 1 (Street): ").strip()
        locality = input("Address Line 2 (Locality): ").strip()
        city = input("Address Line 3 (City): ").strip()
        email_address = input("Email Address: ").strip()
        phone_number = input("Phone number: ").strip()
        rest_id = get_next_primary_key("RESTAURANTS", "Restaurant_ID", "R")
        if not rest_id:
            print("Failed to generate primary key.")
            return

        q = "INSERT INTO RESTAURANTS (Restaurant_ID, Restaurant_Name, Street, Locality, City, Email_Address, Phone_Number) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        values = (rest_id, rest_name, street, locality, city, email_address, phone_number)
        cursor.execute(q, values)
        db.commit()

        cursor.execute("SELECT Restaurant_ID FROM RESTAURANTS WHERE Restaurant_Name = %s AND Phone_Number = %s", (rest_name, phone_number))
        rest_id = cursor.fetchall()[0][0]
        return rest_id

    except Exception as e:
        db.rollback()
        print("Failed to insert data into the database\n>>>>>>> ", e)
        return None


def deleteRestaurant():
    try:
        rest_id = input("Enter the Restaurant ID of the restaurant you want to remove: ")
        q = "DELETE FROM RESTAURANTS WHERE Restaurant_ID = %s;"
        cursor.execute(q, rest_id)
        db.commit()
        print("Sorry to see you go :(")
        print("\n" + "-"*100 + "\n")
        return None

    except Exception as e:
        db.rollback()
        print("Failed to delete from the database\n>>>>>>> ", e)
        return None


def addDish(rest_id):
    try:
        print("\nEnter details of the new dish: ")
        dish_name = input("Enter dish name: ")
        cuisine = input("Enter the cuisine: ")
        price = input("Enter price of the dish: ")
        ingredients = input("Enter ingredients: ").split(",")
        dish_id = get_next_primary_key("DISH_DETAILS", "Dish_ID", "D")
        if not dish_id:
            print("Failed to generate primary key.")
            return

        q1 = "INSERT INTO DISH_DETAILS (Dish_ID, Dish_Name, Restaurant_ID, Cuisine, Price) VALUES (%s, %s, %s, %s, %s);"
        values = (dish_id, dish_name, rest_id, cuisine, price)
        cursor.execute(q1, values)
        db.commit()

        q2 = "INSERT INTO DISH_INGREDIENTS (Dish_ID, Ingredients) VALUES ;"
        ingredient_list_qvalue = []
        for i in range(len(ingredients)-1):
            ingredient_list_qvalue.extend(dish_id, ingredients[i])
            q2 += "(%s, %s), "

        ingredient_list_qvalue.extend(dish_id, ingredients[-1])
        q2 += "(%s, %s);"

        cursor.execute(q2, tuple(ingredient_list_qvalue))
        db.commit()
        return dish_id
    
    except Exception as e:
        db.rollback()
        print("Failed to insert into the database\n>>>>>>> ", e)
        return None
    

def deleteDish():
    try:
        dish_id = input("Enter Dish ID of the dish you want to remove: ")
        q = "DELETE FROM DISH_DETAILS WHERE Dish_ID = '%s';"
        cursor.execute(q, dish_id)
        db.commit()
        return None

    except Exception as e:
        db.rollback()
        print("Failed to delete from the database\n>>>>>>> ", e)
        return None


def updateDish(dish_id, attr, new_value):
    try:
        if attr == "Price":
            q = "UPDATE DISH_DETAILS SET Price = %s WHERE Dish_ID = %s;"
            cursor.execute(q, (dish_id, new_value))
            db.commit()
        elif attr == "Cuisine":
            q = "UPDATE DISH_DETAILS SET Cuisine = %s WHERE Dish_ID = %s;"
            cursor.execute(q, (dish_id, new_value))
            db.commit()
        elif attr == "Ingredients":
            q1 = "DELETE FROM DISH_INGREDIENTS WHERE Dish_ID = %s;"
            cursor.execute(q1, (dish_id,))
            db.commit()

            q2 = "INSERT INTO DISH_INGREDIENTS (Dish_ID, Ingredients) VALUES ;"
            ingredient_list_qvalue = []
            for i in range(len(new_value)-1):
                ingredient_list_qvalue.extend(dish_id, new_value[i])
                q2 += "(%s, %s), "

            ingredient_list_qvalue.extend(dish_id, new_value[-1])
            q2 += "(%s, %s);"

            cursor.execute(q2, tuple(ingredient_list_qvalue))
            db.commit()
        return None
    
    except Exception as e:
        db.rollback()
        print("Failed to update the database\n>>>>>>> ", e)
        return None





print("\n" + "-"*100)
print("Welcome to Charles Boyle's Food Recommendation System")
print("-"*100 + "\n")

#--------------------------------------------------------------------------------------------------------------------------------
# SIGN IN/ SIGN UP
print("\nDiscover dishes tailored to your taste in your vicinity!\n\nDo you have an account?\n1. Yes! I would like to SIGN IN.\n2. No! I would like to SIGN UP.\n3. I do but I want to DELETE it.\n")

acc_choice = input("Enter your choice (1/2/3): ").strip()
user_id = ""
if acc_choice == "1":
    user_id = input("User ID: ").strip()
    password = input("Password: ")
    user_valid = userValidity(user_id, password)
    while not user_valid:
        print("Wrong User ID/Password. Try again!")
        user_id = input("User ID: ").strip()
        password = input("Password: ")
        user_valid = userValidity(user_id, password)

elif acc_choice == "2":
    user_id = insertUser()

elif acc_choice == "3":
    user_id = deleteUser()
    exit()

cursor.execute("select User_Purpose from USERS where User_ID = %s", (user_id,))
userPurpose = cursor.fetchall()[0][0]
print(userPurpose)
print("\n" + "-"*100 + "\n")

if userPurpose == "Customer":
    #--------------------------------------------------------------------------------------------------------------------------------
    # OPTIONS AND RECS
    again = "yes"
    while again == "yes":
        dishes_available = dishesAvailable()
        print(dishes_available)

        if dishes_available is None or dishes_available == ():
            print("Boyle says you're picky. Maybe you should reconsider your choices.")
            again = input("Do you want to try shifting around your choices? (yes/no): ").strip().lower()

        else:
            again = "no"
            print(tabulate(dishes_available, headers = ['Dish ID', 'Dish name', 'Restaurant', 'Cuisine', 'Price', 'Overall_Rating']))

    chosen_dish = input("What's your choice? (Enter Dish ID): ").strip()

    dishDetails(chosen_dish)
    print("\n" + "-"*100 + "\n")

    #--------------------------------------------------------------------------------------------------------------------------------
    # FEEDBACK
    

    recordFeedback(user_id, chosen_dish)

    print("Thanks for the feedback! Hope we'll see you again sometime soon!")
    exit()



elif userPurpose == "Restaurant_Owner":
    print("\nWhat would you like to do today?\n1. Add a new restaurant\n2. Remove a restaurant\n3. Update menu of a restaurant\n4. View feedback for restaurants\n")
    ro_choice = input("Enter your choice(1-4): ")
    rest_id = None
    if ro_choice == "1":
        #--------------------------------------------------------------------------------------------------------------------------------
        # ADD RESTAURANTS
        rest_id = insertRestaurant()
        print("The Restaurant ID of your new restaurant is " + rest_id)
        print("\n" + "-"*100 + "\n")
        ro_choice = "3"
        
    elif ro_choice == "2":
        #--------------------------------------------------------------------------------------------------------------------------------
        # DELETE RESTAURANTS
        deleteRestaurant()
        print("\n" + "-"*100 + "\n")

        exit()

    if ro_choice == "3":
        #--------------------------------------------------------------------------------------------------------------------------------
        # CHANGES IN MENU
        if not rest_id:
            rest_id = input("Enter Restaurant ID of the restaurant whose menu you want to update: ")

        print("\nWhich of the following operations do you want to do?\n1. Add dishes to the menu\n2. Remove dishes from the menu\n3. Update dish details\n")
        dish_choice = input("Enter your choice (1-3): ")
        if dish_choice == "1":
            repeat = "yes"

            while repeat == "yes":
                dish_id = addDish(rest_id)
                print("The Dish ID of the new dish is " + dish_id)
                repeat = input("Do you want to add more dishes? (yes/no): ").lower()
            
            print("\n" + "-"*100 + "\n")            
            exit()

        elif dish_choice == "2":
            repeat = "yes"

            while repeat == "yes":
                deleteDish()
                repeat = input("Do you want to remove more dishes? (yes/no): ").lower()
            
            print("\n" + "-"*100 + "\n")
            exit()
        
        elif dish_choice == "3":
            repeat = "yes"
            while repeat == "yes":
                dish_id = input("Enter Dish ID of the dish whose details you want to modify: ")
                repeat_updation = "yes"
                while repeat_updation == "yes":
                    print("Which component of the menu do you want to modify?\n1. Price\n2. Ingredients\n3. Cuisine")
                    detail_update_choice = input("Enter your choice (1-3): ")
                    if detail_update_choice == "1":
                        new_price = input("\nEnter the updated price: ")
                        updateDish(dish_id, "Price", new_price)
                    elif detail_update_choice == "2":
                        new_ingredients = eval(input("\nEnter the updated ingredient list: "))
                        updateDish(dish_id, "Ingredients", new_ingredients)
                    elif detail_update_choice == "3":
                        new_cuisine = input("\nEnter the updated cuisine: ")
                        updateDish(dish_id, "Cuisine", new_cuisine)

                    repeat_updation = input("Do you want to update any other detail of this dish? (yes/no): ").lower()
                repeat = input("Do you want to update the details of another dish? (yes/no): ").lower()
            
            print("\n" + "-"*100 + "\n")
            exit()
                    
print("\n" + "-"*100 + "\n")

