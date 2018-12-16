# Game Wire

Live URL: [https://game-wire.herokuapp.com/](https://game-wire.herokuapp.com/)

## How to install

### For development

1. First, make sure you have the following installed on your machine

    - MongoDB
    - Node.js
    - Python 3.6+
    - Yarn or npm

 (If you are using `npm`, anywhere you see `yarn`, change it to `npm`)

 Once you have the MongoDB installed, start it up. By default it should be running at `localhost` and on port `27017`.
  
   On linux or mac, you can start MongoDB using - `$ sudo mongod`

2. Then clone the repository to your local machine:

    ```bash
    $ git clone https://github.com/finnspin/remoteteam.git
    ```

3. Next, install the dependencies:

    ```bash
    $ yarn install 
    ```

4. Start up the development server:

    ```bash
    $ yarn run serve
    ```

The above command will open a server running at [http://localhost:8080](http://localhost:8080). This is the URL you will load on your browser to see how the files looks.

5. Next, change your current directory to the Python files:

    ```bash
    $ cd app
    ```

6. Create the `.env` file that contains some API keys - (Twilio, etc):

    ```bash
    $ cp .env.example .env
    ```

    Change your MongoDB and Twilio Keys to the correct API keys.

7. Install the python packages:

    ```bash
    $ pip install -r requirements.txt
    ```

8. Start up the Python server:

    ```bash
    $ flask run
    ```

This will start a server that is running at http://localhost:5000/ (You don't need to worry about this, Vue already knows about it and will connect to it automatically. You should also leave it running while you develop)

### For production

The production server uses the Python server. Currently the app is deployed to heroku.

You just need to start up the Python app located in the `app/` folder.

1. Create the `.env` file that contains some API keys - (Twilio, etc):

    ```bash
    $ cp .env.example .env
    ```

2. Change your MongoDB and Twilio Keys to the correct API keys.

3. Once the server is running, build up the Vue files:

    ```bash
    $ yarn run build
    ```

And that's it, this will create a new folder named `dist` that contains our JavaScript and CSS files optimised for production. 

## Important links
- [Twilio Programmable Chat documentation](https://media.twiliocdn.com/sdk/js/chat/releases/3.0.2/docs/index.html)
