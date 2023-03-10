# Krautuvele-back-end

Krautuvele back-end with Python and Flask

How to run this project:

1. Fork it

2. Create virtual environment
   $python -m venv venv

3. Activate virtual environment
   $source venv/Scripts/activate

4. Install packages from requirements.txt file
   $pip install -r requirements.txt

5. Create .env.local file and write secret key and database URI
   export FLASK_SECRET_KEY=<some key>
   export FLASK_SQLALCHEMY_DATABASE_URI=mysql://<database connection>

   To run on local machine, mysql server is needed. With mysql server running, use this for connection:
   export FLASK_SQLALCHEMY_DATABASE_URI=mysql://root:<password>@localhost:3306/defaultdb

   A dump of database is available on request.

6. Activate local environment variables
   $source .env.local

7. Run project by running run.py file
