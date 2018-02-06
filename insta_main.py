import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

app_access_token = '4870715640.a48e759.874aba351e5147eca8a9d36b9688f494'
base_url = 'https://api.instagram.com/v1/'

print "Welcome to InstaBot!"


# *********************************************Prints information of the user's account - self*******************************************
def self_info():
    request_url = (base_url + 'users/self/?access_token=%s') % app_access_token
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if 'data' in user_info:
            print "User Name: %s" % user_info['data']['username']
            print "Full Name: %s" % user_info['data']['full_name']
            print "Bio shared: %s" % user_info['data']['bio']
            print "Count of Media shared: %s" % user_info['data']['counts']['media']
            print "Count of followers of the user: %s" % user_info['data']['counts']['follows']
            print "Count of people user follows: %s" % user_info['data']['counts']['followed_by']
        else:
            print "User doesn't exist."
    else:
        print "Status code 200 not received!"


#**********************************************************Retrieve user's user_id**************************************************
def get_user_id(user_name):
    request_url = (base_url + 'users/search?q=%s&access_token=%s') % (user_name, app_access_token)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if 'data' in user_info:
            return user_info['data'][0]['id']
        else:
            print "User does not exist."
            return None
    else:
        print "Status code 200 not received!"
        exit()


#*******************************************************Retrieve a user's information************************************************
def get_user_info(user_name):
    user_id = get_user_id(user_name)
    if user_id is None:
        print 'User does not exist!'
        exit()
    request_url = (base_url + 'users/%s?access_token=%s') % (user_id, app_access_token)
    print "GET REQUEST URL: %s" % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "Username: %s" % user_info['data']['username']
            print "No. of followers: %s" % user_info['data']['counts']['followed_by']
            print "No. of people you are following: %s" % user_info['data']['counts']['follows']
            print "No. of posts: %s" % user_info['data']['counts']['media']
        else:
            print "User does not exist."
    else:
        print "Status code 200 not received!"


# *********************************************Retrieve posts on the user's account - self****************************************
def get_own_post():
    request_url = (base_url + 'users/self/media/recent/?access_token=%s') % app_access_token
    print 'GET request url : %s' % request_url
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']) > 0:
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# *********************************************Retrieve posts on the user's account*************************************************
def get_user_post(username):
    user_id = get_user_id(username)
    if user_id is None:
        print 'User does not exist!'
        exit()
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % request_url
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return user_media['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
        return None


# *****************************************************Function for liking posts****************************************************
def like_a_post(username):
    media_id = get_user_post(username)
    request_url = (base_url + 'media/%s/likes') % media_id
    payload = {"access_token": app_access_token}
    print 'POST request url : %s' % request_url
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


# *****************************************************Function for deleting negatie comments****************************************************
def delete_negative_comment(username):
    media_id = get_user_post(username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, app_access_token)
    print 'GET request url : %s' % request_url
    print "@@@@"
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']) > 0:
            for comment in comment_info['data']:
                comment_text = comment['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    comment_id = comment['id']
                    delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % media_id, comment_id, app_access_token
                    print "DELETE request url : %s" % delete_url
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!'
                    else:
                        print 'Could not delete the comment'
        else:
            print 'No comments found'
    else:
        print 'Status code other than 200 received!'
    print "No negative comments."


# *********************************************Start bot function-This is where it all begins****************************************
def start_bot():
    while True:
        print "Here are your menu options:"
        print "1.Get your own details"
        print "2.Get details of a user by username"
        print "3.Get your own recent post"
        print "4.Get the recent post of a user by username"
        print "5.Like recent post of a user"
        print "6.Delete negative comment for a user"
        print "7.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "1":
            self_info()
        elif choice == "2":
            user_name = raw_input("Enter the username of the user: ")
            get_user_info(user_name)
        elif choice == "3":
            get_own_post()
        elif choice == "4":
            username = raw_input("Enter the username of the user: ")
            get_user_post(username)
        elif choice == "5":
            user_name = raw_input("Enter the username of the user: ")
            like_a_post(user_name)
        elif choice == "6":
            user_name = raw_input("Enter the username of the user: ")
            delete_negative_comment(user_name)
        elif choice == "7":
            exit()
        else:
            print "Wrong choice!"


start_bot()
