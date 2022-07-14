# Ameer Yousef Baraskiva Baraskiwan

import requests
import constants


def hasAllAttributes(post):  
    x = str(post['id']) and str(post['userId']) and str(post['title']) and str(post['body'])
    return x

def hasCommentAllAttributes(post):  
    x = str(post['postId']) and str(post['id']) and str(post['name']) and str(post['email']) and str(post['body'])
    return x

def get_payload(endpoint):
    return {
        "url": constants.domain + endpoint,
        "headers": constants.headers
    }

def get(payload):
    return requests.get(payload["url"], headers=payload["headers"])

def post(payload):
    return requests.post(payload["url"], json=payload["body"], headers=payload["headers"])


def delete(payload):
    return requests.delete(payload["url"], headers=payload["headers"])

def checkPostId(postid):
    if (str(type(postid)) != "<class 'int'>"): 
        raise Exception("postid should be an int")