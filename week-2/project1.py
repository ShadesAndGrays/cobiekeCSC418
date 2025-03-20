import os
import cv2
# program relies of a file structred approach
# profile format firstname_lastname.jpg (case sensitive) 
# Prof. Enase Okonedo  (Username = enase) (password = 7 len(Okonedo)  )

root_dir = os.path.abspath(os.curdir) 
profile_directory = "img/profile" # all profiles are stored here

class Profile:
    def __init__(self,img):
        self.file_name=img
        name=img.split(".")[0]
        self.username  = name.split("_")[0]
        self.password  = len(name.split("_")[1])


def profile_exists(username,profiles):
    for i in profiles:
        if i.username == username:
            return True
    return False

def authenticate(username,password):
    # initialize a list of profile of all users
    profiles = [Profile(x) for x in os.listdir(f"{root_dir}/{profile_directory}")] 

    # check if username exsits
    if not profile_exists(username,profiles):
        print('profile does not exist')
        return None

    #check if password is valid
    for i in profiles:
        if i.password == password and i.username == username:
            return i
    print('incorrect password')
    return None

def display_user(profile:Profile):
    path = f"img/profile/{profile.file_name}"
    image = cv2.imread(path)
    msg = f"profile: {profile.username}"
    print("displaying ",msg)
    cv2.imshow(f"{profile.username}",image)
    cv2.waitKey(0)

def main():
    print("Welcome to UMCFR")
    username = input("Username: ")
    password = -1
    try:
        password = int(input("Password: "))
    except:
        print("invalid password")
        return

    if profile := authenticate(username,password) :
        display_user(profile)
        pass

main()
