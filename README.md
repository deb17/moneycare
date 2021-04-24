# MoneyCare - An expense tracker

MoneyCare is a comprehensive personal expense tracker app. It has been built
entirely with the Python Flask framework and its several extensions. Its features
include a dashboard to visualize expenditure. Managing expenses is easy with
intuitive forms and listings. There is a 'budget' section where the user can plan
his expenditure for the year, and check whether targets have been met. There is a 
search feature to find expense transactions by different criteria. It uses
the Whoosh search engine to perform searches against the transaction description
or comments.

Among other things,

- The app enables social login via Google and Twitter.

- It provides a REST api to access and search the expenses. Check out the docs
at https://moneycare.pythonanywhere.com/api/docs .

- It has an admin section, provided by Flask-Admin. You can check out the code
in the 'admin' blueprint.

- The app includes integration with Sentry for error logging and with New Relic
for performance monitoring.


Check out the webapp at https://moneycare.pythonanywhere.com . Use demo username
`testuser` and password `pass123` to login.
