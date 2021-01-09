import clearbit

clearbit.key = 'API_KEY'

#the following could be used to enrich the database with some extra informantion about the user_registration
#the functions could be run right after the user registers and results could populate some fields
# I could not get it to return any meaningfull data,outside of their given example, perhaps you need to be a payed user.

response = clearbit.Enrichment.find(email='alex@clearbit.com', stream=True)
# respons should return a json with info about company, title ...
