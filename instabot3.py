import requests, urllib
from paralleldots import set_api_key, get_api_key, sentiment
import matplotlib.pyplot as plt
a=[]
APP_ACCESS_TOKEN = "2170149923.5a5863d.94363ab14ad940019bfbc7a0cb8cfa3b"
BASE_URL ='https://api.instagram.com/v1/'


set_api_key("SDxXFqDsFdEFNq1DsJEvcIYpkkxca1XdlLsrdiULJn0")
get_api_key()
Positive_sentiments = 0
Negative_sentiments = 0
Neutral_sentiments = 0

#defing the self info
def self_info():
    request_url=(BASE_URL + "users/self/?access_token=%s") % (APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username:%s' % (user_info['data']['username'])
            print 'No. of followers:%s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts:%s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


#defing user id
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()



def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url :%s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username:%s' % (user_info['data']['username'])
            print 'No. of followers:%s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following:%s' % (user_info['data']['counts']['follows'])
            print 'No. of posts:%s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


#defing get own post
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name= own_media['data'][0]['id'] + ".jpeg"
            image_url =  own_media['data'][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print"your image has been downloaded"
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


#defing the user post
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + ".jpeg"
            image_url = user_media['data'][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)

        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


#defing like a post
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


#defing the comment
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"



def get_the_comments(insta_username):
    post_id = get_post_id(insta_username)
    print "Get request URL:" + ((BASE_URL + "media/%s/comments?access_token=%s") % (post_id, APP_ACCESS_TOKEN))
    comments = requests.get((BASE_URL + "media/%s/comments?access_token=%s") % (post_id, APP_ACCESS_TOKEN)).json()
    for i, d in enumerate(comments["data"]):
        print d["text"]
        a.append(d["text"])
    return a






#defing pie chart
def pie_chart():
    insta_username = raw_input("Enter the username: \n")
    give_comments = get_the_comments(insta_username)
    for i in give_comments:
        sentiments = sentiment(str(i))
        print sentiments["sentiment"]
        if (sentiments["sentiment"] > 0.75):
            print "Positive sentiments"
            global Positive_sentiments
            Positive_sentiments = Positive_sentiments + 1
        elif (0.25 < sentiments["sentiment"] <= 0.75):
            print "Neutral Sentiments"
            global Neutral_sentiments
            Neutral_sentiments = Neutral_sentiments + 1
        else:
            print "Negative Sentiments"
            global Negative_sentiments
            Negative_sentiments = Negative_sentiments + 1

    labels = 'Positive Sentiments', 'Negative Sentiments', 'Neutral Sentiments'
    sizes = [Positive_sentiments,Neutral_sentiments ,Negative_sentiments ]
    explode = (0.1, 0.1, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()



def start_bot():
    while True:
        print '\n'
        print "Hey! Welcome to instaBot!\nHere are your menu options:\n" \
              "a.Get your own details\nb.Get details of a user by username\n" \
              "c.Get your recent post\nd.Get recent post of any user\ne.like a post\nf.comment on a post\n" \
              "g. Get the list of comments\nh. Sentimental"
        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice== "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "g":
            insta_username= raw_input("Enter the username of the user: ")
            get_the_comments(insta_username)
        elif choice == "h":
            pie_chart()



start_bot()