* Python version: 3
* Required packaged: sleep, requests and flask

> Be sure that the server is running before running the client because we did not manage the case where the server is down.

> By default, we put `192.168.1.2` as server ip and `5000` as server port. These values can be set in the home page of the client by clicking on the `Server config` button.

* To run the client:

```shell
$ python3 client.py
```

the application will runs on `http://localhost:3001/`