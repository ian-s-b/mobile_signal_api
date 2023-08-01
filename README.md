### MOBILE SIGNAL API
Simplified API used to get 

### Stack
- MongoDB
- Python Flask

### Dependencies
- python3.10
- requirements.txt for python
- mongodb

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
python3 -m launch_signal_api.py

### To test the API, go to the following address:
http://localhost:5000/?q=address

Where address is the request and should be a french address.
The request format is much like the one used on https://adresse.data.gouv.fr/api-doc/adresse, since it passes by this api to filter the inserted address.


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




