# cbs-project1
LINK: https://github.com/meeries/csb-project1

This project was done with Python and Django, using the [OWASP 2021](https://owasp.org/www-project-top-ten/) list for flaws.

## Starting the app

1. Clone this repository
2. Navigate to the directory that has file ```manage.py``` and run command ```python3 manage.py runserver```
3. Execute the migrations by running commands ```python3 manage.py makemigrations```
   and ```python3 manage.py migrate```
4. Open the address shown in the terminal, and log in with username: ```username``` and password: ```password```

## Flaws and their fixes:

## Flaw 1: CSRF (Cross-site request forgery)
https://github.com/meeries/cbs-project1/blob/b937cedd5089da948cd96f96facddac11d71a135/tasks/views.py#L17
https://github.com/meeries/cbs-project1/blob/b937cedd5089da948cd96f96facddac11d71a135/tasks/templates/tasks/add_task.html#L11

### Description
CSRF is a security vulnerability, where an attacker tricks a user's browser into making illegitimate requests to a website or web application, where the user is authenticated. Because the server trusts the authenticated user's browser, it believes the requests to be legitimate, even when they are in fact unauthorized. The attacker can, for example, change users' data, without the user's knowledge.

### Fix
CSRF attacks can be prevented by introducing a CSRF token, that is generated by the server and difficult (if not impossible) to guess. When a user submits a form or makes a request, the server ensures that the token matches the one stored for the user. Nowadays, most frameworks, including Django, provide defences for CSRF attacks. So, to introduce this flaw, I added ```@csrf_exempt``` to bypass Django's defence. This flaw can be fixed by removing this, and thus enabling Django's CSRF protection.

Fix in tasks/views.py: https://github.com/meeries/cbs-project1/blob/b937cedd5089da948cd96f96facddac11d71a135/tasks/views.py#L16

Fix in tasks/templates/tasks/add_task.html form: https://github.com/meeries/cbs-project1/blob/b937cedd5089da948cd96f96facddac11d71a135/tasks/templates/tasks/add_task.html#L12


## Flaw 2 Broken Access Control:[
https://github.com/meeries/cbs-project1/blob/ff0fd04357f81ba145619d7303a83c14ac5c3be9/tasks/views.py#L19

### Description
Broken access control is a security vulnerability, where an application fails to properly restrict access to resources or actions based on the user's identity and permissions. This makes it possible for a user to access or modify data, that they are not supposed to be able to.
For example, the application might use a URL with an ID parameter (```/task/<task_id>``` in this project). When proper access restrictions are not in place, the user can modify the URL by placing any number on ```<task_id>``` and gaining access to viewing tasks that are not theirs.

### Fix
This vulnerability can be fixed by adding checks that ensure that the resource (task) the user is trying to access, actually belongs to them. If the user trying to view the task, is not the user that created it, they get redirected to the list of tasks. The fix can be implemented by removing the current function body of ```def task_detail(request, task_id):``` and replacing it with the function body provided in the commented-out code.

https://github.com/meeries/cbs-project1/blob/80913b684321b25e602c18abd2d6087c3b04689a/tasks/views.py#L19


## Flaw 3: 
link
### Description
### Fix

## Flaw 4: 
link
### Description
### Fix

## Flaw 5: 
link
### Description
### Fix

## Flaw 6: 
link
### Description
### Fix
