### MOBILE SIGNAL API - DOCKER INTEGRATION
Simplified API used to get mobile signals disponibility (2G, 3G, 4G) given a French requested address.

The precision of the API is city-level.

### Application Stack
- MongoDB
- Python Flask

### Docker integration
It's possible to run this application in a Docker container to avoid having to install all its dependencies on your computer.

The docker-compose.yml file will create the following services:
- db: the mongo database (non exposed) used with the signal api
- create_db: a service that runs a python script once to send data to the database. At the end of the script te service is stopped
- signal_api: the main api container

To lanch the services, run the following command next to the docker-compose.yml file:
```
docker-compose up
```

The first time you run the docker compose, you will see the following message on your terminal:
```
mobile_signal_api-create_db-1 exited with code 0
```
Meaning that the create_db script send the data correctly to the database and the api is ready to be used.

If you stop all the services and restart them with 
```
docker-compose up
```
You will encounter the following message:
```
mobile_signal_api-create_db-1 exited with code 1
```
This is normal because the script was not able to send the data again to the database since it was already sent before.

### Test the API
To test the API, go to the following address:

http://localhost:5000/?q=requested_address

Where requested_address is the request and should be a french address.
The request format is much like the one used on https://adresse.data.gouv.fr/api-doc/adresse, since the API used in this project passes by the 'adresse api' to filter the inserted address.

### Requests examples:
#### > EX 1: A precise request

Request: http://localhost:5000/?q=rue+victor+hugo+brest

Response:
``` json
{
    "29019 Brest": {
        "Bouygues Telecom": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "Free mobile": {
            "2G": false,
            "3G": true,
            "4G": true
        },
        "Orange": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "SFR": {
            "2G": true,
            "3G": true,
            "4G": true
        }
    }
}
```

#### > EX 2: A less precise request

Request: http://localhost:5000/?q=rue+victor+hugo

Response:
``` json
{
    "33063 Bordeaux": {
        "Bouygues Telecom": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "Free mobile": {
            "2G": false,
            "3G": true,
            "4G": true
        },
        "Orange": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "SFR": {
            "2G": true,
            "3G": true,
            "4G": true
        }
    },
    "37261 Tours": {
        "Bouygues Telecom": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "Free mobile": {
            "2G": false,
            "3G": true,
            "4G": true
        },
        "Orange": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "SFR": {
            "2G": true,
            "3G": true,
            "4G": true
        }
    },
    "49007 Angers": {
        "Bouygues Telecom": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "Free mobile": {
            "2G": false,
            "3G": true,
            "4G": true
        },
        "Orange": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "SFR": {
            "2G": true,
            "3G": true,
            "4G": true
        }
    },
    "76351 Le Havre": {
        "Bouygues Telecom": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "Free mobile": {
            "2G": false,
            "3G": true,
            "4G": true
        },
        "Orange": {
            "2G": true,
            "3G": true,
            "4G": true
        },
        "SFR": {
            "2G": true,
            "3G": true,
            "4G": true
        }
    },
    "97209 Fort-de-France": {
        "message": "city_code 97209 not found in the database"
    }
}
```

#### > EX 3: An invalid request

Request: http://localhost:5000/?q=iadsjasdipa

Response:
``` json
{
    "message": "The requested address was not found."
}
```




