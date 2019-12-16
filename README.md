# CoCo Houndify Connector

CoCo Houndify connector is a [Flask](http://flask.palletsprojects.com/en/1.1.x/ "Flask") application which allows you to expose your [Houndify](https://www.houndify.com/ "houndify") bots as a components at the [CoCo marketplace](https://marketplace.conversationalcomponents.com/ "CoCo marketplace").

### Deployment Flow:

1. Create new client on Houndify.
2. Create JSON file for component with client's key and ID.
3. Place the key JSON at the following directory at the CoCo Houndify Connector source:
`/HoundifyManager/components` - Each file represent a component which can be accessed through an http call to` https://<host>/api/exchange/<file name - no extension>/<session ID>`
4. Map the 3 commands from Houndify client at the config.py file(Create new
record for your component):
	- **Done Action** - Action which will be triggered when the bot/`component` achived it's goal.
	- **Failed Action** - Action which will be triggered when the bot/`component` will not complete it's goad.
	- **Out Of Context** - Action which will be triggered when the conversation went out of context.
5. Upload the Flask app to a cloud service(Google app engine is recommende - yaml file included.)




#### 1. Create new client on Houndify.

 ![Create a new client.](/Screenshots/1CreateClient.png)

### 2,3. Create config for the component and place it at the components directory.
 ![Create component config.](/Screenshots/2ComponentConfig.png)

### 4. Map client commands to component states at config.py.

config.py:
'''
    ACTIONS_MAPPING_CONFIG = {
        "default": {
            "COMPLETE_ACTION": "InformationCommand",
            "FAILED_ACTION": "ErrorCommand",
            "OUT_OF_CONTEXT_ACTION": "NoResultCommand"
        },
        "weather": {
            "COMPLETE_ACTION": "InformationCommand",
            "FAILED_ACTION": "ErrorCommand",
            "OUT_OF_CONTEXT_ACTION": "NoResultCommand"
        }
    }
'''

#### 5. Upload the Flask app to a cloud service.

 Open bash, configure gcloud tools and then run the following command:

    `gcloud app deploy`


