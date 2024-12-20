# Multi-Strategy Multi-Account Trade Execution Engine

This project is a multi-strategy, multi-account trade execution engine designed to work with Alpaca. The engine is capable of executing various trading strategies across multiple accounts and can be expanded to support other brokers in the future. It is developed to be easily deployed to a linux server.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Scripts](#scripts)
- [APIs](#apis)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

### Directories and Files

- **alpaca_api/**: Contains the Alpaca API integration functions.
- **historical_data/**: Manages historical data fetching and updating.
- **postgresql/**: Contains the Flask application, database models, and PostgreSQL management scripts.
- **schedulers/**: Scheduler scripts for different trading strategies.
- **systems/**: Implementation of various trading strategies.
- **crontab**: Crontab configuration for scheduling tasks.
- **maintenance.sh**: Script for system maintenance.
- **run_schedulers.sh**: Script to run all schedulers.
- **requirements.txt**: Python dependencies.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    - Copy the [.env](http://_vscodecontentref_/23) files in [alpaca_api](http://_vscodecontentref_/24) and [postgresql](http://_vscodecontentref_/25) directories and fill in the required values.

## Configuration

### Alpaca API

- Configure your Alpaca API keys in [.env](http://_vscodecontentref_/26):
    ```env
    API_PUBLIC=your_public_key
    API_SECRET=your_secret_key
    ```

### PostgreSQL

- Configure your PostgreSQL database in [.env](http://_vscodecontentref_/27):
    ```env
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    DB_NAME=your_db_name
    ```

## Usage

### Running the Flask Application

1. Navigate to the [postgresql](http://_vscodecontentref_/28) directory:
    ```sh
    cd postgresql
    ```

2. Run the Flask application:
    ```sh
    python flaskapp.py
    ```

### Running the Schedulers

1. Run the [run_schedulers.sh](http://_vscodecontentref_/29) script to start all schedulers:
    ```sh
    bash run_schedulers.sh
    ```

### Maintenance

1. Run the [maintenance.sh](http://_vscodecontentref_/30) script for system maintenance:
    ```sh
    bash maintenance.sh
    ```

## Scripts

### [run_schedulers.sh](http://_vscodecontentref_/31)

This script starts all the scheduler scripts in separate `tmux` sessions.

### [maintenance.sh](http://_vscodecontentref_/32)

This script performs system maintenance tasks such as terminating `tmux` sessions, cleaning up the system, and rebooting.

## APIs

### Flask Application

The Flask application provides an interface to manage user accounts and their API keys.

- **Endpoint**: `/manage`
- **Methods**: `GET`, `POST`
- **Form Fields**:
    - [email](http://_vscodecontentref_/33): User's email.
    - [api_public](http://_vscodecontentref_/34): Alpaca Public API key.
    - [api_secret](http://_vscodecontentref_/35): Alpaca Secret API key.
    - [stop_strategy](http://_vscodecontentref_/36): Checkbox to stop the strategy.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE(LICENSE) file for details.