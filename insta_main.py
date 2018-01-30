import requests

app_access_token = '4870715640.a48e759.874aba351e5147eca8a9d36b9688f494'
base_url = 'https://api.instagram.com/v1/'


#*********************************************Prints information of the user's account - self*******************************************
def self_info():
    request_url = (base_url + 'users/self/?access_token=%s') % app_access_token
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        print "User Name: %s" % user_info['data']['username']
        print "Full Name: %s" % user_info['data']['full_name']
        print "Bio shared: %s" % user_info['data']['bio']
        print "Count of Media shared: %s" % user_info['data']['counts']['media']
        print "Count of followers of the user: %s" % user_info['data']['counts']['follows']
        print "Count of people user follows: %s" % user_info['data']['counts']['followed_by']
    else:
        print "Status code 200 not received!"


self_info()
