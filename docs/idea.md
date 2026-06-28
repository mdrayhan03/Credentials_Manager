Project Title: Credentials Manager
Description: In our daily life we login or create many accounts in many place, most of them login via google/meta/github but some credentials need to use password and we need some other credentials, and we can't memorize all of those credentials in our memory so we write down in somewhere but managing them become nightmare. So I want to make a credentials manager which will manage my credentials more securely

Stacks:
Frontend: Flet (python + flutter)
Backend: Python
Database: Sqlite3 or Json

Workflow:
user can first login and we will cache the login for a certain time if any movement then the time will be increase and if no movement we will logout the user. For add credentials user will give title, credentials type and according to credential type other field will appear, like normal password then title, username, email, password, if ssh password then title, username, ip, ssh key if has, password etc like that
we are going to make it one codebase for all os, our main focus is windows, mac and android but we will to do for linux and ios also.

Design:
for desktop we use three part design left part is navbar, center is main page, right part is for description and more options and left right part is closeable, I want a simple easy UI
and for phone top center bottom, in top closeable navbar then main page and in the last description part we will think about that later.

        DESKTOP                             MOBILE
----------------------------             -------------
| LEFT|    CENTER    |RIGHT|             |    TOP    | 
|     |              |     |             |___________|   
|     |              |     |             |           |
|     |              |     |             |  CENTER   |
|     |              |     |             |           |
----------------------------             |___________|
                                         |  BOTTOM   |
                                         -------------

In the credentials we will give all the field copy option and we will store all the data in our db by encryption the username, email and other things also that will make more secure and our encryption key will be dynamic when the user first create account we will create a encryption key and store in db and use that key for encryption

Future Work:
now our system is local but in future we will try to make it internet. it's like we will take user gmail or a google drive public folder and two button for user to push or pull. so that if user use same account in different device so that they can sync securely
