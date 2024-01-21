from flask import Flask, render_template, request, render_template_string, jsonify
import json
from google.cloud import pubsub_v1

app = Flask(__name__)

template_str ="""
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Click-Me App</title>
        <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 0;
                    background-color: #f4f4f4;
                    justify-content: center;
                }

                h1 {
                    text-align: center;
                    color: #333;
                }

                form {
                    text-align: center;
                    margin-top: 20px;
                }

                button {
                    margin-left: 100px;
                    margin-right: 100px;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                }

                button:hover {
                    background-color: #0056b3;
                }
        </style>
    </head>
    <body>
        <h1> Click any of the two buttons to generate events for GCP DataFlow Event Capture </h1>
        <form action="/click-app" method="post">
            <button type="submit" name="button_id" value="button1">Generate Event 1</button>
            <button type="submit" name="button_id" value="button2">Generate Event 2</button>
        </form>
    </body>
    </html>
    """

@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'POST':

        button_id = request.form.get('button_id')
        result = {
            'buttonID':button_id,
            'click':1
        }
        
        message_publisher(result)

        return render_template_string(template_str)
    else:
        return render_template_string(template_str)

def message_publisher(message):

    # Convert the message dictionary to a JSON string
    message_str = json.dumps(message)

    # Set up the Pub/Sub client and topic
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('business-deck', 'click-events-topic')
    
    # Publish the message to the topic
    future = publisher.publish(topic_path, message_str.encode('utf-8'))

def main(request):
    return app

# if __name__ == '__main__':
#     app.run(debug=True)