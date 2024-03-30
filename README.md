QRKot - a service for voluntary donations and fundraising for the needs of animals.

FastAPI - FastAPIUser - SQLAlchemy - API
_______________________________________________________________________________________________________________________________________________


<img width="758" alt="Снимок экрана 2024-03-30 в 11 06 38" src="https://github.com/zubkovoleg01/QRKot/assets/120819704/511dfd5e-aa4b-4d69-a0da-d0b5a2d7c401">


_______________________________________________________________________________________________________________________________________________

● You can open, close, or edit a new collection in the Fund.

● The user can make a donation with a comment.

● Donations to projects are received on the principle of First In, First Out.

● Any user can see a list of all projects, including the required and already deposited amounts.


_______________________________________________________________________________________________________________________________________________

Deployment Instructions

● Clone the repository

git clone https://github.com/zubkovoleg01/QRKot.git

● Navigate to the project directory

cd QRKot

● Create and activate a virtual environment:

python3 -m venv venv

source venv/bin/activate

or for Windows users

source env/Scripts/activate

● Install dependencies from the requirements.txt file:

python3 -m pip install --upgrade pip

pip install -r requirements.txt


● Run project: 

uvicorn app.main:app
