### MOBILE SIGNAL API
Simplified API used to get mobile signals disponibility (2G, 3G, 4G) given a French requested address.

The precision of the API is city-level.

### Docker integration
It's possible to run this application in a Docker container to avoid having to install all its dependencies on your computer.

Swith to the "docker" branch on this repository to view it. 

### Stack
- MongoDB
- Python Flask

### Dependencies
- python3.10.12 : to install python, follow the official guide: https://www.python.org/downloads/
- mongodb: to install mongodb, follow the official mongodb tutorial https://www.mongodb.com/docs/manual/administration/install-community/ according to your OS

### Virtual environment setup:
Create venv with the following command:
```
virtualenv venv
```

Activate the venv:
```
source venv/bin/activate
```

Install the requirements into the venv:
```
pip3 install -r requirements.txt
```

### Database initialization
Launch the script create_database.py
```
python3 -m create_database.py
```

### Launch the API:
With the venv activated and the database created, launch the api with the following command:
```
python3 -m launch_signal_api
```

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




