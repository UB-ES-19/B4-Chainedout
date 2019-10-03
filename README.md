![alt Chainedout](https://raw.githubusercontent.com/UB-ES-19/B4-Chainedout/master/repo_logo.png "Chainedout")
# Chainedout - Tasks

## Sprint I
<details>
<summary>Show Sprint I </summary>

### Time: 46h
Start Project: 4h

Learning:
- From scratch: 3h
- Remember: 5h

Register:
- Frontend: 4h
- Backend: 10h

Log in:
- Frontend: 4h
- Backend: 4h

Log out:
- Frontend: 2h
- Backend: 2h

Lading page:
- Frontend: 10h
- Backend: 2h

### User Story I: Register
- As a guest user, I want to register so that I can browse and find a job from the website list.
- As a guest user, I want to register so that I can offer a job and list it on the website list.
- As a guest user, I want to register so that I can meet people.
- As a guest user, I want to register so that I can find a course or formation.
- As a guest user, I want to register so that I can take a look at user's profiles.

### Issues
FrontEnd:
- Home Page: Header, Register button, Footer.
- Register Page: Form (back to Home Page).

Backend:
- User Model.
- Database (sqlite by default).
- Files: views, urls

### User Story II: Login
As a registered user i want to be able to log into my account so that i can access all website functionalities
As an admin user i want to be able to log into my account so that i can administrate website
### Issues
FrontEnd:
- Home page : Add login button
- Login Page: Form login (back to previous page)

Backend:
- Active session control
- Files: urls, views

### User Story III: Logout
As a logged user i want to be able to log off my account so that i can finish my session
### Issues
FrontEnd:
- Home page : Add logout button (back to previous page)

Backend:
- Kill active session, logout method
- Files: urls, views

### User Story IV: Landing Page
As a user i want to be able to access a home page so that i can navigate through the website.
### Issues
FrontEnd:
- Home Page

Backend:
- Files: urls, views

## TODO
<summary>Show pending Publish and Sharing</summary>

### User Story V: Publish and Sharing
### Issues
FrontEnd:
- N

Backend:
- Files: urls, views

</details>

## Sprint II
<detail open>
<summary>Show Sprint II</summary>

### Time: 46h

Landing page:
- Frontend: 6h

Profile page:
- Frontend: 12h
- Backend: 12h

Following/Friendship: 
- Frontend: 6h
- Backend: 10h

### User Story IV: Landing page

As a user I want to be able to filter categories from the landing page so that i can access to different posts/publicity
As a user I want to be able to search people, jobs or courses so that i can participate with people
As a company I want to be able to post a job to the webpage

### Issues

Frontend:
- Filter
- Search bar
- Posting job option

Backend: 
- ?

### User Story V: Profile page

As a registered user I want to be able to insert my information to my profile page so that I can share my information to others
As a registered user I want to see the preview of my personal profile page so that I can manage it as I prefer
As a registered user I want to be able to see others profiles so that i can met new people with common interests

### Issues
Frontend:
- Page where a user can insert his personal information
- Own profile page preview
- Others user profile page

Backend:
- Save the information inserted by user

### User Story VI: Friendship/Followers

As a registered user I want to be able to have access to a list with all my friends so that I can contact them easier
As a registered user I want to be able to add another user to my Friend list so that I can contact them in a future
As a registered user I want to be able to follow people so that i can be updated from all his activities
As a registered user I want to be able to receive the invitations to become friends so that I can decide whether accept it or not
As a registered user I want to be able to see the people who follow my activities so that I can know who is interested in me

### Issues

Frontend:
- Friends list
- Followers list

Backend:
- Friendlist model
- Follower model
- Notifications for friends request

</detail>
