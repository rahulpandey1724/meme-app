# user Details list
# users = []

# Check user id exists or not
def userExists(userData,cursor):

    email = userData['email']

    sql_query = f'''
                    SELECT * FROM users;
                '''
    
    cursor.execute(sql_query)

    users = cursor.fetchall()

    print("users: ")
    print(users)

    for user in users:
        # if user exists 
        print("user found")
        if user[3] == email:
            print("user found")
            return {'response' : True, 'user' : user}
    
    # if user not exists
    return {'response' : False, 'user' : {}}

def registerUser(userData,cursor):
    
    # Check user exists or not
    checkUser = userExists(userData,cursor)

    
    if checkUser['response']:
        # user exists and Already registered
        return {'statusCode' : 503, 'message' : 'Already Register'}
    else:
        # user not exits so user is registered here
        # users.append(userData)

        sql_query = f'''
                        INSERT INTO users(name,contact,email,password) VALUES('{userData['name']}','{userData['contact']}','{userData['email']}','{userData['password']}');
                    '''
        
        cursor.execute(sql_query)

        return {'statusCode' : 200, 'message': 'Successfully received'}


def loginUser(userData,cursor):
    
    # check user exits or not
    checkUser = userExists(userData,cursor)

    # user exists
    if checkUser['response']:
        # check password and Successfully login
        if userData['password'] == checkUser['user'][4]:
            return {'statusCode' : 200, 'message' : 'Successfully Login'}
        else:
            # passworderror
            return {'statusCode' : 503, 'message' : 'PasswordError'}
    else:
        # user not exists
        return {'statusCode' : 200, 'message' : 'Not registered'}