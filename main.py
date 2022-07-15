# Ameer Yousef Baraskiva Baraskiwan
import constants 
import functions
import json

#----------------------------------------------------------------------------------------------------   
def get_posts(postid = None):
    if( postid != None):
        endpoint = constants.posts+"/"+str(postid)
    else:
        endpoint = constants.posts
    payload = functions.get_payload(endpoint)
    result = functions.get(payload)
    assert result.status_code  == 200, "Failed to send request or post is not found!"
    posts = json.loads(result.text)
    if(postid != None):
        posts= [posts]
    # Validate that all posts have valid format
    valid_posts = filter(lambda p: functions.hasAllAttributes(p), posts)
    assert len(list(valid_posts)) == len(list(posts))
    return True

#----------------------------------------------------------------------------------------------------   

def post_posts(body):
    # send a post request to create a new post
    endpoint = constants.posts
    post_payload = functions.get_payload(endpoint)
    post_payload["body"] = body
    post_result = functions.post(post_payload)
    assert hasattr(post_result, "status_code")
    assert post_result.status_code == 201, "Failed to post/add a new post"
    post_resp = json.loads(str(post_result.text))
    # try to read/get the new added post
    id = post_resp["id"]
    assert id
    get_posts(id)
    #=================================
    #other way to test, test if written data = read data 
    new_endpoint = str(f"endpoint/{id}")
    payload_get = functions.get_payload(new_endpoint)
    get_result = functions.get(payload_get)
    assert hasattr(get_result, "status_code")
    assert get_result.status_code == 200
    get_resp = json.loads(str(get_result.text))
    assert post_resp["title"] == get_resp["title"]
    assert post_resp["userId"] == get_resp["userId"]
    assert post_resp["body"] == get_resp["body"]
    
#----------------------------------------------------------------------------------------------------   

def get_comments(postid): 
    endpoint = "comments?postId="+str(postid)
    payload = functions.get_payload(endpoint)
    result = functions.get(payload)
    assert result.status_code  == 200
    comments = json.loads(result.text)
    # Validate that all posts have valid format
    valid_comments = filter(lambda c: functions.hasCommentAllAttributes(c), comments)
    v = len(list(valid_comments))
    iv = len(list(comments))
    assert v !=0 , "Ivnvalid postID or no comments found for the given post"
    assert v == iv, "there is some invalid comments!" 

#----------------------------------------------------------------------------------------------------       
def delete_post(postid):
    endpoint = constants.posts
    payload = functions.get_payload(endpoint+"/"+str(postid))
    result = functions.delete(payload)
    assert result.status_code  == 200
    #try to read\get the deleted post 
    assert get_posts(postid) == False, "The post is not deleted"
    
#----------------------------------------------------------------------------------------------------   
#                                           Testing                                                 
#----------------------------------------------------------------------------------------------------   
# GET	/posts
# GET	/posts/1
# GET	/posts/1000
def test_getPosts():
    #test getting all posts
    get_posts()
    #test getting valid post
    # testing Get /posts/1
    get_posts(1)
    # testing Get /posts/1000
    get_posts(1000)

#----------------------------------------------------------------------------------------------------   
# POST	/posts

def test_postPost():
    valid_body = {
        "userId": 98877,
        "body": "We rock",
        "title": "title"
    }
    invalid_body = {
        "userId": 'invalid@!$#$%',
        "body": "23423$#@!$%",
        "title": "@234#2134#&$$"
    }
    # test posting a valid body
    post_posts(valid_body)
    #test posting an invalid body
    post_posts(invalid_body)

#----------------------------------------------------------------------------------------------------   
# GET	/comments?postId=1

def test_getComments():
    # find comments for a valid post
    get_comments(1)
    #find the comments for an invalid post
    get_comments(10000)
    #passing invalid input
    get_comments("asd")

#----------------------------------------------------------------------------------------------------   

# DELETE	/posts/1

def test_deletePost():
    #delete a valid post
    delete_post(10000)
    #delete invalid post
    delete_post(10000)
    
#----------------------------------------------------------------------------------------------------   
