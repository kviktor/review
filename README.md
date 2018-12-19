
# Review API

## Requirements
The application requires Python 3.6 or newer to run. To install the additional Python packages run the following command (preferably in a virtualenv but it's not required)
```
$ pip install -r requirements/local.txt
```

## Application setup

First you need to create the database with
```
$ ./manage.py migrate
```

Then you can start the development web server
```
$ ./manage.py [::]:8000
```
To verify that it's working navigate to
[http://localhost:8000/docs/](http://localhost:8000/docs/).

## Data setup
To load some initial data into the database run
```
$ ./manage.py loaddata initial
```
This will create a 2 users with 1-1 review each:
 - `kviktor` with the password `test` and token `113902b2d38fc43172d6f52c69f7f56343572f52`
 - `test` with the password `test` and token `375815b84b11cf2858b0bf182ae6eb32335985cf`

## Testing
To run the tests use the following command
```
./manage.py test --settings=review.settings.test
```
Coverage can be checked with
```
$ coverage run manage.py test --settings=review.settings.test
$ coverage report
```


## Documentation
The API documentation is available at [http://localhost:8000/docs/](http://localhost:8000/docs/).

In order to reach any of the API endpoints you need to set the `Authorization` header to `Token your_token`. This can be found or created in the Django admin available at [http://localhost:8000/admin/](http://localhost:8000/admin/).

## Examples
The example below creates a new review, lists all available reviews and retrieves one (you might need to install `curl`˙first). 
```
$ curl -X POST -H "Authorization: Token 375815b84b11cf2858b0bf182ae6eb32335985cf" -H "Content-Type: application/json" http://localhost:8000/api/v1/reviews/ --data '{"title": "a", "company_name": "b", "rating": 5, "summary": "cc"}'
$ curl -H "Authorization: Token 375815b84b11cf2858b0bf182ae6eb32335985cf" -H "Content-Type: application/json" http://localhost:8000/api/v1/reviews/
$ curl -H "Authorization: Token 375815b84b11cf2858b0bf182ae6eb32335985cf" -H "Content-Type: application/json" http://localhost:8000/api/v1/reviews/2/
```

More examples can be found in the [documentation](http://localhost:8000/docs/).

