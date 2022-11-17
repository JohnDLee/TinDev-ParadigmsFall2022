# Paradigms FA2022 Project - TinDev
by John Lee, Mark Rumsey, and Chris Capone

### To RUN
- Navigate to `root/register/login`
- Click Sign up to register for an account.
- You will be brought back to Login if successful.

### John's Tasks
- Displaying error messages on signup.
- Login/Connecting Recruiter Profile and Candidate Profile after it's created.

### Mark's Tasks
Create Recruiter Profile
- I have created under recruiter/templates/recruiter a profile_creation.html -> use that for the view of the profile creation page.
- Use a form to fill the model (see my forms.py in register)
- in recruiter/views.py fill out the profile_creation_view function properly. See my signup_view in register for examples.
- You just need to construct an interface to fill out the form and construct the model associated with the user. Then redirect to the /recruiter/homepage/
- Also, add a logout option in the form creation step too. -> when the button is clicked, just call logout(request) and HttpsRedirect to login page.

### Chris's Tasks
Create Candidate Profile
- Literally the same things as Mark but for candidate profile. Same template is provided.

### Accessing Website
Use 
- John Lee: `http://129.74.152.125:51062/register/login`
- Mark Rumsey: `http://129.74.152.125:51090/register/login`
- Chris Capone: `http://129.74.152.125:51019/register/login`

Super User
- Username: paradigms
- Email: jlee88@nd.edu
- Password: paradigms