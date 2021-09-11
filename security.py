from user import User


users = [
    User(1,'pans','ppp')
]

# username_mapping = { 'pans': {
# 'id' : 1,
# 'username' : 'pans'
# 'password' :  'ppp'
# }
# }

username_mapping ={u.username: u for u in users}
#assigning key value pairs above
userid_mapping = {u.id: u for u in users}

# userid_mapping = { 1:{
# 'id' : 1,
# 'username' : 'pans'
# 'password' :  'ppp'
# }
# }


def authenticate(username, password):
        user = username_mapping.get(username, None)
        #default value is none if there is no username key then return none
        if user and user.password == password:
            #if user and safe_str_cmp(user.password, password):
            return user


def identity(payload):
    #Here payload is the content of the JWT token
    user_id = payload['identity']
    #Extract user id from the payload
    return userid_mapping.get(user_id, None)
    #None as a default
