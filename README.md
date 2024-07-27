
# XPWeb

XPWeb is a REST API interface for X-Plane using X-Plane Connect, allowing users to easily access and modify datarefs or trigger commands from any app, browser, or web app. This eliminates the need to handle complex UDP communication and packets.

## Features

- **Access X-Plane Datarefs:** Retrieve values of specified datarefs using simple REST API calls.
- **Modify X-Plane Datarefs:** Set the values of one or multiple datarefs through REST API.
- **Trigger X-Plane Commands:** Send commands to X-Plane using a straightforward REST API.

## Installation

### Prerequisites

- **X-Plane Connect:** XPWeb relies on X-Plane Connect. You need to install X-Plane Connect and set it up with your X-Plane installation. Follow the instructions on the [X-Plane Connect GitHub page](https://github.com/nasa/XPlaneConnect) to install and configure it.
- **X-Plane Version:** XPWeb supports whatever versions are supported by X-Plane Connect. It has been tested with X-Plane 11 and 12, but it should work as long as X-Plane Connect is supported.

### Using the Binary Release

1. Download the latest binary release from the [releases page](https://github.com/alireza787b/XPWeb/releases).
2. Extract the downloaded zip file.
3. Run the `main.exe` file.
4. The API server will start, and you can access the API documentation at `http://localhost:7712/docs`.

### From Source

1. Clone the repository:

    ```sh
    git clone https://github.com/alireza787b/XPWeb.git
    cd XPWeb
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:

    ```sh
    python app/main.py
    ```

## Usage

### Starting the Server

- **Binary Release:**
  Simply run `main.exe` and the server will start automatically.

- **From Source:**
  Run the application using the command: `python app/main.py`.


## Demo

We've included a demo in the `demo` folder to show how you can interact with X-Plane through a web interface and javascript. To use the demo:

1. Ensure that the XPWeb server is running.
2. X-Plane should be open, and XPlane Connect should be installed and configured correctly.
3. Open the `index.html` file in a web browser to access the demo.

- The demo allows you to send commands and set/get datarefs directly from your browser.
- The server host and port in the script.js of the demo should match those in your XPWeb `config.json` file (default is `localhost:7712`).
- You can find further instructions and download necessary files from the [XPWeb GitHub repository](https://github.com/alireza787b/XPWeb).
- The FastAPI auto-generated documentation can be accessed at `http://localhost:7712/docs` for detailed API endpoint information.


### Accessing API Documentation

Once the server is running, you can access the API documentation at `http://localhost:7712/docs`.

## API Endpoints

### Get Dataref

**Endpoint:** `/get_dataref`

**Method:** `GET`

**Description:** Fetch values of specified datarefs.

**Parameters:**
- `datarefs` (str): Comma-separated list of datarefs.

**Returns:** 
- A list of DatarefResponse objects with the dataref values and statuses.

**Examples:**

**Single Dataref Request:**

```sh
GET /get_dataref?datarefs=sim/time/zulu_time_sec
```

**Response:**

```json
[
    {
        "dataref": "sim/time/zulu_time_sec",
        "value": 36000.0,
        "status": "success"
    }
]
```

**Multiple Datarefs Request:**

```sh
GET /get_dataref?datarefs=sim/time/zulu_time_sec,sim/flightmodel/position/latitude,sim/operation/override/override_flightcontrol
```

**Response:**

```json
[
    {
        "dataref": "sim/time/zulu_time_sec",
        "value": 36000.0,
        "status": "success"
    },
    {
        "dataref": "sim/flightmodel/position/latitude",
        "value": 37.615223,
        "status": "success"
    },
    {
        "dataref": "sim/operation/override/override_flightcontrol",
        "value": 0,
        "status": "success"
    }
]
```

### Set Dataref

**Endpoint:** `/set_dataref`

**Method:** `POST`

**Description:** Set the value of one or multiple datarefs.

**Request Body:**
- `dataref` (str or list of str): Dataref(s) to set.
- `value` (number or list of number): Value(s) to set.

**Returns:**
- A SetDatarefResponse object with the status of the dataref set operation.

**Examples:**

**Single Dataref Request:**

```sh
POST /set_dataref
{
    "dataref": "sim/operation/override/override_flightcontrol",
    "value": 1
}
```

**Response:**

```json
{
    "dataref": "sim/operation/override/override_flightcontrol",
    "value": 1,
    "status": "success"
}
```

**Multiple Datarefs Request:**

```sh
POST /set_dataref
{
    "dataref": ["sim/operation/override/override_flightcontrol", "sim/time/zulu_time_sec"],
    "value": [1, 36000.0]
}
```

**Response:**

```json
{
    "dataref": ["sim/operation/override/override_flightcontrol", "sim/time/zulu_time_sec"],
    "value": [1, 36000.0],
    "status": "success"
}
```

### Send Command

**Endpoint:** `/command`

**Method:** `POST`

**Description:** Send a command to X-Plane.

**Parameters:**
- `command` (str): The command to send to X-Plane.

**Returns:**
- A CommandResponse object with the status of the command execution.

**Example:**

**Send Command Request:**

```sh
POST /command
{
    "command": "sim/operation/pause_toggle"
}
```

**Response:**

```json
{
    "command": "sim/operation/pause_toggle",
    "status": "success"
}
```

## Configuration

The configuration file `config.json` allows you to set the host and port for the server. It is located in the `app/config` directory. You can edit this file to change the server settings.

**Example `config.json`:**

```json
{
    "server": {
        "host": "0.0.0.0",
        "port": 7712
    }
}
```

## Contributing

We welcome contributions to XPWeb! If you have suggestions, bug reports, or feature requests, please open an issue on GitHub. For code contributions, please fork the repository and create a pull request.

## License

XPWeb is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for more information.

## Contact

- **GitHub:** [alireza787b](https://github.com/alireza787b)
- **LinkedIn:** [alireza787b](https://www.linkedin.com/in/alireza787b)

