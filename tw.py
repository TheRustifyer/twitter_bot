import tweepy
import time

#Setting the credentials to log in to Twitter API

auth = tweepy.OAuthHandler('i9U2yMP9d9sQrD79czQaNWwRs', 'Aw8H1HAxQqDZoN744jkxAtxroMjM6KiXXMxXhMcFQ6svjrz5Dw')
auth.set_access_token('1294915515975114752-8jguMYr3LijKaTpALd5rMhhoJZb5W5', 'UxNbPBHqHVwSBMRbwxUyCR0wr4If1muwaqHzSG7RUS3y0')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


#Cheking correct access to the platform

try:
    
    api.verify_credentials()
    
    print('· Authentication OK, you have know gain access to the API.\n')

except:
    
    print('· Error during authentication. Check the end date of your tokens.\n')



# Decorators....................................................................

def performance(func):

	def wrapper(*args, **kwargs):

		t1 = time.time()
		result = func(*args, **kwargs)
		t2 = time.time()
		
		print(f'\nThis operation has been completed in {t2 - t1} seconds.\n')
		
		return result

	return wrapper

# End of decorators..............................................................



# Generator to manually handle the rate limit of TW API..........................

def limit_handled(cursor):

	while True:

		try:
		
			yield next(cursor)

		except tweepy.RateLimitError:

			time.sleep(1)
		
		except StopIteration:
			
			print()
			print('**********')

			return

#................................................................................


	# 1st --> Getting a list of users based on a query search
	
	#Function to format the output of the search function

def output_format(*args):

	print('Those are the results for the designed search: \n')

	for number, dictionary in enumerate(*args):

		if number == 0:

			print(f"\nUsers with more than 10 and less than 100 followers: \n")

		elif number == 1:

			print(f"Users with more than 100 and less than 1000 followers: \n")

		elif number == 2:

			print(f"\nUsers with more than 1000 followers:\n")

		else:

			print(f"\nAqui o teu primo añadeu un diccionario antes de tempo\n")


		if dictionary:

			for key, value in dictionary.items():

				print(f'Usuario => {key}')
		else:

			print(f'No users found with this criteria.\n')


	# Func to follow users based on the previous search

def follow_searched(data_array, data_decision):

	if data_decision:

		for dictionary in data_array:

			for user_name, user in dictionary.items():

				if not user.following:

					api.create_friendship(user.id)

					time.sleep(1/3600 )

					print (f'{user_name} has been followed!')

				else:

					print (f"{user_name} it's already been followed!")

	return f'Work done succesfully!' if data_decision else f'No one was followed!'


	#Function to search users based on a query

@performance #Decorator to measure the performance of this function
def search_users(query, number_of_results_users):

	targeted_users_low = {}
	targeted_users_intermediate = {}
	targeted_users_high = {}

	for target_user in tweepy.Cursor(api.search_users, q=query).items(number_of_results_users):

		if target_user.followers_count > 10 and target_user.followers_count <= 99:
			# targeted_users_low[target_user.screen_name] = target_user.id
			targeted_users_low[target_user.screen_name] = target_user

		if target_user.followers_count >= 100 and target_user.followers_count <= 999:
			# targeted_users_intermediate[target_user.screen_name] = target_user.id
			targeted_users_intermediate[target_user.screen_name] = target_user

		if target_user.followers_count >= 1000:
			# targeted_users_high[target_user.screen_name] = target_user.id
			targeted_users_high[target_user.screen_name] = target_user


		#Saving dicts on a list for EZ use the data when be required
	users_data_array = [targeted_users_low,targeted_users_intermediate,targeted_users_high]

		#Calling the function to format the data output!
	output_format(users_data_array)


		#Second part of the function, the part will determine if AUTO FOLLOW USERS will be called
	print('\nDo you want to follow the searched users?\n')

	follow_user_decision = input('Press [Y / n]:\n')

	if follow_user_decision == 'Y' or follow_user_decision == 'y':

		follow_user_decision == True

		follow_searched(users_data_array, follow_user_decision)

	elif follow_user_decision == 'N' or follow_user_decision == 'n':

		follow_user_decision == False

	else:

		return f'Leaving the program!'


	# 2nd --> Getting a list of users based on a query search

@performance #Decorator to measure the performance of this function
def tweet_threatment(hashtag, n_items):
	
		#Function to format empty returned data
	checker = lambda x: "· Data not availiable ·" if x in [0, None, "", False] else x

		#Formating the requested hashtag	
	hashtag_format = lambda x: ', '.join(["#" + json_elements.get('text') for json_elements in x])

		#All the requested data will be saved here, to easily access desired data when be necesary...
	tweets_mined = tweepy.Cursor(api.search, q=f'#{hashtag}',count=n_items, tweet_mode="extended").items(n_items)

	for tweet in tweets_mined:
		
		print("·Name:", checker(tweet.author.name))
		print(f"·Screen-name: @{checker(tweet.author.screen_name)}")
		print("·Tweeted on created:", checker(tweet.created_at)) #Maybe implement option format date

		if 'retweeted_status' in tweet._json:
			
			print("·Last ReTweet:", checker(tweet.retweeted_status.full_text))
		
		else:
			
			print("·Last Tweet:", checker(tweet.full_text))

		print("·Hashtags: ", hashtag_format(tweet.entities['hashtags']))#Check if we can print all the hastags in the _json as in TW/RT

		print("·Likes: ", checker(tweet.favorite_count))
		print("·RTs: ", checker(tweet.retweet_count))
		print("·Location:", checker(tweet.user.location))
		print("·Time-zone:", checker(tweet.user.time_zone))
		#Deprecated print("Geo:", checker(tweet.geo)
		print("·Place:", checker(tweet.place))
		print("·Language:", checker(tweet.lang).capitalize())
		print("·Source:", checker(tweet.source))
		print("\r\n","*"*20,"\r\n")


#<<<<<<<<<<<<<<<<<<<<<<<<<<<--------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
###Bot sections. This is part of the code where is supposed to be mantained by the 'bot'


	# Here is where we mantain Twitter data for our bot to work with. 

def followers_data():
		
	# All of your followers
	data_followers = tweepy.Cursor(api.followers).items()

	# All of the followed accounts
	data_following = tweepy.Cursor(api.friends).items()

	return data_followers, data_following


	# Function for manage the follow back action

@performance
def auto_follow_back(followers, following, fav_rt=False, interest_list=[]):

	# Users that follows you but u don't them.
	
	follow_back_count = 0

	for follow_back_user in followers:
		
		# Follow back action
		if not follow_back_user.following:

			api.create_friendship(follow_back_user.id)

			follow_back_count += 1

			print(f'U have follow back a new follower, {follow_back_user.screen_name}')
			
			#Ahora escollemos un TW e RT + fav // Puede escalarse en otra versión a una función para reutilizar

			if fav_rt: #Para a seguinte versión, separar esto...

				for tweet in api.user_timeline(follow_back_user.id):

					if any(word.lower() in tweet.text.lower() for word in interest_list):
						
						try:

							tweet.favorite()

						except tweepy.TweepError as error:

							print(error.reason)

						try:

							tweet.retweet()

						except tweepy.TweepError as error:

							print(error.reason)

					print(f'A tweet of {follow_back_user.screen_name} has been RETWETEED!' + '\r\n' +  
						f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}')


	return (f"\nThere's no one new to follow back. Try again later!" if follow_back_count == 0 else f'\n A total of {follow_back_count} users have been followed back!')


	#Function to unfollow people that you follow but they don't follow you

@performance
def unfollow_followed(followers, following):

	# ID's followers list

	followers_id = [follower.id for follower in followers]

	unfollowed_counter = 0

	for user_who_follow in following:

		if not user_who_follow.id in followers_id:

			api.destroy_friendship(user_who_follow.id)

			unfollowed_counter += 1

			print(f'U have unfollow {user_who_follow.screen_name}!')

	return f"\nAll of your users are in love with you. Good job!" if unfollowed_counter == 0 else f'\n A total of {unfollowed_counter} users have been unfollowed!'




#<<<<<<<<<<<<<<-------------------------------------------------------->>>>>>>>>>>>>>>>>


if __name__ == '__main__':

	print('''Hey there. Welcome to the BRION TWITTER BOT V1. Before anything, thanks for choosing me! But let's gonna do some funny things...\n
	First of all, do you wanna search for something in Twitter before launch the bot?:\n''')

	while True:

		data_decision = input('Press [Y / n]:\n')

		if data_decision == 'Y' or data_decision == 'y':

			while True:

				print('\nWant to search for an @user or a #Hastag?')
				data_decision_2 = input('Press [1] for @user or [2] for #Hastag.\n')

				if data_decision_2 == '1':

					entrance_query = input('\nIntroduce a user to find (No @ needed): \n')
					number_of_users = int(input('\nHow many results you want to look for?\n'))

					if entrance_query and number_of_users < 1000:

						#Function search_users_call
						print('\nJust wait while we perform the task...')
						print(search_users(entrance_query, number_of_users))
						
						break

					else:

						print('Fields can not be empty. Please, insert something to find for... and a number of results between 1 and 1000.\n')

					

				elif data_decision_2 == '2':

					hastag = input('\nIntroduce a hastag to find: \n')
					number_of_hastags = int(input('\nHow many results you want to look for? (Less than 20)\n'))

					if hastag and number_of_hastags <= 20:

						print('\nJust wait while we perform the task...\n\n')
						tweet_threatment(hastag, number_of_hastags)
						
						#Exportar tweets a .odt
						break

					elif number_of_hastags > 20:

						print('''In order to not overload the TWITTER server, 
							for this task, we can just search for 20 or less Hastags...''')

					else:

						print('Fields can not be empty. Please, insert something to find for... and a number of results between 1 and 20.')

				else:

					print('\nUse one of the designed options please...\n')

		
		elif data_decision == 'N' or data_decision == 'n':

			pass
			#Sitio dónde hacer las llamadas al bot.
			#Este es el else de Y/N

			while True:
				
				print('\nSo...')
				user_bot_decision = input('\nPress [1] for auto Follow Back people or [2] for Unfollow users who do not follow you..\n')

				# Gonna launch and manage the funcion who takes care about follow back users!
				if user_bot_decision == '1':

					#Calling the function who grabs data from the API
					data_followers, data_following = followers_data()

					print('\nIf we find some interesting TWEET based on a few keywords, would you like to hit FAV button and RT?\n')
					print('\n As an advice, thought that this action usually increment your popularity ratio on TWTTER.\n')
					use_rt_fav = input('Press [Y / n]:\n')

					if use_rt_fav == 'Y' or use_rt_fav == 'y':

						use_rt_fav = True

						keyword_1 = input('\nIntroduce the first keyword\n')
						keyword_2 = input('\nIntroduce the second keyword\n')
						keyword_3 = input('\nIntroduce the third keyword\n')

						array_of_keywords = [keyword_1, keyword_2, keyword_3]

						print(auto_follow_back(data_followers, data_following, use_rt_fav, array_of_keywords))

						break

					else:

						print(auto_follow_back(data_followers, data_following))

						break


				# Gonna launch and manage the funcion who takes care about unfollow users!
				elif user_bot_decision == '2':

					#Calling the function who grabs data from the API
					data_followers, data_following = followers_data()
					
					print('\nThis action will unfollow ALL users who do not follow you... Are you completly sure?\n')
				
					user_sure_unfollow = input('Press [Y / n]:\n')

					if user_sure_unfollow == 'Y' or user_sure_unfollow == 'y':

						print(unfollow_followed(data_followers, data_following))

						break
					
					else:

						print('\nAny action has been performed over your account.\n')

						break

				else:
					
					print('\nUse one of the designed options please...\n')

		print('\nCompleted program. If you wanna do something more, just run the program again.\n')
		print('See you next time!')
		break
		
		# Else from the main WHILE
	else:

		print('\nUse one of the designed options please...\n')


