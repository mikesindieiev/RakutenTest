# API for brakeman scanner

API for brakeman scanner. API is written in Python3 with Flask. It has only one endpiont / with 2 methods: GET and POST. Both methods does not requiere authentication now. Maybe will be implemented in the future.

**GET** method will return the scan result and if it not exist on the server, then it will return 404 error code.

**POST** method requires JSON payload to run the scan.

Find the Swagger documentation here: <https://mikesindieiev.github.io/test_api/>

When **POST** request received, API will trigger git command to clone the fresh code, run the scanner against that code and save the report insite the working dir. To retrieve that report user should send **GET** request without body (body is ignored in the request processing flow)

## Setup

To run the container with API, run the following command:

`> docker run -it -p 80:80 mikesindieiev/api-scanner`

Running container will bound to localhost ip address and expose 80 port with API

-----

This container slightly different from Dockerfile description. It was created by commiting chnages to presidentbeef/brakeman

To modify the image, edit Dockerfile and build new version of the image with following command:

`docker build -t mikesindieiev/api-scanner .`

## Testing

To test the API use [Postman colletion](API_scanner.postman_collection.json)

### Happy path

**GET** Get report

Shold return report in JSON format. If report is missing on the server, then return 404 http code and info message in the JSON object

**POST** Run scan

Requires application/json header, and payload with JSON object.

```{
    "source_code_url": "https://github.com/manojbinjola/ruby-project",
    "lang": "ruby",
    "scanner_name": "brakeman"
}
```

This method should trigger the scan against `source_code_url` repository and save the report into working directory

### Unhappy path

**POST** Missing field request

If JSON object from **POST** method from happy path is missing one field, then API should return 400 http code and message which field is missing

**POST** Empty body request

If JSON object from **POST** method from happy path is missing all filds, then API should return 400 http code and message that no data was received

