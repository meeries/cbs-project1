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


## Flaw 2 Broken Access Control:
https://github.com/meeries/cbs-project1/blob/ff0fd04357f81ba145619d7303a83c14ac5c3be9/tasks/views.py#L19

### Description
Broken access control is a security vulnerability, where an application fails to properly restrict access to resources or actions based on the user's identity and permissions. This makes it possible for a user to access or modify data, that they are not supposed to be able to.
For example, the application might use a URL with an ID parameter (```/task/<task_id>``` in this project). When proper access restrictions are not in place, the user can modify the URL by placing any number on ```<task_id>``` and gaining access to viewing tasks that are not theirs.

### Fix
This vulnerability can be fixed by adding checks that ensure that the resource (task) the user is trying to access, actually belongs to them. If the user trying to view the task, is not the user that created it, they get redirected to the list of tasks. The fix can be implemented by removing the current function body of ```def task_detail(request, task_id):``` and replacing it with the function body provided in the commented-out code.

https://github.com/meeries/cbs-project1/blob/80913b684321b25e602c18abd2d6087c3b04689a/tasks/views.py#L19


## Flaw 3: (SQL) Injection
https://github.com/meeries/cbs-project1/blob/6c899d806484b5a13cc2539c4c324e23ce247115/tasks/views.py#L42

### Description
Injection vulnerabilities occur when an application doesn't process data provided by the user properly, making it possible for users to introduce harmful input that then gets interpreted by the web application, when it shouldn't be. A common example of this (and the one demonstrated in this project) is SQL injection, where user input gets directly inserted to an SQL query for execution. The user can then introduce malicious SQL code, which will be executed by the application, possibly causing serious damage. For example, in this project, the flawed deleting of a task is done with ```f"DELETE FROM tasks_task WHERE id = {task_id}"```, where ```task_id``` comes from URL ```http://127.0.0.1:8000/task/{task_id}/delete/```. Now the user can manipulate the URL by adding, for example ```DROP TABLES```, causing serious damage.

### Fix
Instead of using a raw SQL query to delete a task, we can use Object-relational mapping (ORM) to escape unwanted or dangerous input. Django has it's own ORM, which lets us query the database safely without having to write raw SQL. 

https://github.com/meeries/cbs-project1/blob/6c899d806484b5a13cc2539c4c324e23ce247115/tasks/views.py#L49

## Flaw 4: Cryptographic failures
https://github.com/meeries/cbs-project1/blob/d83dc6fb165ccd8cd731a48a42478015cdd22675/taskapp/settings.py#L24
https://github.com/meeries/cbs-project1/blob/d83dc6fb165ccd8cd731a48a42478015cdd22675/taskapp/settings.py#L30

### Description
Cryptographic failures are security failures that occur when sensitive data is not properly protected. This can lead to malicious users having access to other users' sensitive information, such as passwords or secret keys. An example of this is hardcoding a ```SECRET_KEY``` to the applications code (in this project, ```settings.py```), leaving it vulnerable to attackers if they have access to the code. Another cryptographic failure flaw in this app is hardcoding ```DEBUG = True```. This can allow a malicious user to gain access to vulnerable information.

### Fix
Instead of hardcoding the ```SECRET_KEY``` in ```settings.py```, we can create an ```.env``` file, that includes the ```SECRET_KEY``` we want to use. This file is added to the ```.gitignore```file, so it doesn't get committed to the repository, and thus get exposed to anyone who has access to the repository. We also change ```DEBUG = True``` to ```DEBUG = False```

Fix for ```SECRET_KEY```:
https://github.com/meeries/cbs-project1/blob/d83dc6fb165ccd8cd731a48a42478015cdd22675/taskapp/settings.py#L26

Fix for ```DEBUG = True```:
https://github.com/meeries/cbs-project1/blob/d83dc6fb165ccd8cd731a48a42478015cdd22675/taskapp/settings.py#L32

## Flaw 5: Security misconfiguration
https://github.com/meeries/cbs-project1/blob/c5444765fb942156da8add7c7de2e713615f1f43/taskapp/settings.py#L30

### Description
Security misconfiguration vulnerabilities occur when security settings are improperly applied or overlooked, leaving a system vulnerable to attacks. These misconfigurations may lead to unauthorized access, data breaches, or disruptions. In this project, the flaw can be seen in that in file ```settings.py```, we have ```DEBUG = True```, due to which we receive very detailed error messages, for example when trying to view a task that doesn't exist. These error messages reveal sensitive information, that can be exploited.

### Fix
This flaw can be fixed by changing ```DEBUG = True``` to ```DEBUG = False```. This way, there are no detailed error messages when there is an issue with the application.
https://github.com/meeries/cbs-project1/blob/c5444765fb942156da8add7c7de2e713615f1f43/taskapp/settings.py#L32

## Flaw 6: Identification and Authentication Failures
https://github.com/meeries/cbs-project1/blob/e592e83ba8fc4003866c6479967471953a26eb2a/taskapp/settings.py#L94

### Description
Identification and authentication failures are vulnerabilities in the way an application verifies and manages users' identities. These vulnerabilities can allow malicious users to gain unauthorized access to another user's data, for example. There are many ways these vulnerabilities can manifest in an application, like allowing weak passwords, storing passwords unsafely or improper session management.
In this project, this flaw can be seen in that there are no requirements to what type of password can be created. Thus, a user can choose a weak password, that can be easy to guess or crack, via brute force attacks or credential stuffing.

### Fix
The fix provided for this flaw is including password validators, that ensure the password a user chooses fills the required criteria. Django has built-in password validators, that are used in the fix for this flaw. These validators check that the password has at least 8 characters, and is not some of the most common passwords, like "password" or "12345678".

https://github.com/meeries/cbs-project1/blob/6780d1df1f486aee8b2f91004cd2f2dadecac08a/taskapp/settings.py#L95
