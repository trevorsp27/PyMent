from venmo_api import Client, UserApi, User

# Get your access token. You will need to complete the 2FA process
# Please store it somewhere safe and use it next time
# Never commit your credentials or token to a git repository
#access_token = Client.get_access_token(username='x',
#                                        password='y',
#                                        device_id="z")
#print("My token:", access_token)

client = Client("395984c90e445fe370a656bf0c657553fd1a03e95acbf5be3717f512490561ba")




###################
# Search for users. You get a maximum of 50 results per request.
#users = client.user.search_for_users(query="Trevor")
#for user in users:
#   print(user.username)


##############

#payment_methods = client.payment.get_payment_methods()
#for payment_method in payment_methods:
#    print(payment_method.to_json())

#############

#get your own user id
myuserid = client.user.get_my_profile().id
print(myuserid)

#################

#get other peoples user id's
#users = client.user.search_for_users(query="x")
#for user in users:
#   print(user.id + " " + user.username)

###############

transactions = client.user.get_user_transactions(myuserid)
while transactions:
   for transaction in transactions:
        print(transaction) 

        #print("\n" + "=" * 15 + "\n\tNEXT PAGE\n" + "=" * 15 + "\n")
        transactions = transactions.get_next_page()

#############

#client.payment.send_money(1.00, "thanks for the 🍔", "id")

#userapi = UserApi(client)
#me = User(client)
