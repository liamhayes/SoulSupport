from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import cohere
from cohere.responses.classify import Example
from LocalWeather import local_weather

co = cohere.Client('Ny9KNHwWiLPRlXjwnsIxnlZPCiBriaqYM21RXFJO')

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    incomingMessage = request.values.get('Body', None)
    incomingMessage = str(" " if incomingMessage is None else incomingMessage)
    incomingMessage = incomingMessage.lower()
    # Add a message

    text = incomingMessage
    inputs=[text]
    if 'recipes' in incomingMessage:
        if( 'dinner' in incomingMessage):
            resp.message("Here is a great site for dinner recipes: https://www.allrecipes.com/recipes/17562/dinner/")
        elif('lunch' in incomingMessage):
            resp.message("Here are some lunch ideas: https://www.allrecipes.com/recipes/17561/lunch/")
        elif('breakfast' in incomingMessage):
            resp.message("Here are some breakfast ideas: https://www.allrecipes.com/recipes/78/breakfast-and-brunch/")
    elif incomingMessage.isdigit():
        weatherInfo = local_weather(incomingMessage)
        if 'Rain' in weatherInfo[0]:
            resp.message("It's raining outside, maybe take a mental health day and watch your favorite show?") 
        elif 'Sun' or "scattered" in weatherInfo[0] and int(weatherInfo[1]) > 60:
            resp.message("It's warm & sunny outside, how about going for a walk?") 
        elif int(weatherInfo[1]) < 50:
            resp.message("It's a little cold outside, make sure to bundle up for your daily walk!") 
    elif 'depressed' or 'hurt' in incomingMessage:
        resp.message("There is help available, please set up an appointment at: https://ucc.vt.edu/about/appointments.html \n or call 988 to speak to somebody") 
    else:
        # Sentiment Analysis

        print("IN SENTIMENT")
        # Sentiment Analysis
        examples=[
          Example("Im feeling good", "positive"), 
          Example("I have lots of energy", "positive"), 
          Example("I ate a lot for dinner", "positive"), 
          Example("I have been sleeing a lot", "positive"), 
          Example("I slept great", "positive"), 
          Example("I worked out today!", "positive"), 
          Example("I went for a walk today!", "positive"),
          Example("Im grateful for my family and friends", "positive"),
          Example("I got out of bed", "positive"),
          Example("my mom", "positive"),
          Example("my day is awesome", "positive"),
          Example("love", "positive"),
          Example("happy", "positive"),
          Example("joy", "positive"),
          Example("amazing", "positive"),
          Example("steller", "positive"),
          Example("beautiful", "positive"),
          Example("I did all my work", "positive"),
          Example("Just relaxing and painting", "positive"),
          Example("Listening to music", "positive"),
          Example("Hang out with friends", "positive"),
          Example("My day is terrible", "negative"), 
          Example("I havent eaten at all today", "negative"),
          Example("I didnt get out of bed", "negative"),
          Example("I dont look forward to anything", "negative"),
          Example("work is killing me", "negative"),
          Example("I dont enjoy my old hobbies anymore", "negative"),
          Example("I'm not grateful for anything", "negative"),
          Example("I feel empty", "negative"),
          Example("bad", "negative"), 
          Example("not the best", "negative"),
          Example("I dont have anything to look forward to", "negative"),
          Example("terrorism", "negative"),
          Example("Bad", "negative"),
          Example("stressed", "negative"),
          Example("Die", "negative"),
          Example("negative", "negative"),
          Example("hate", "negative"),
          Example("ugly", "negative"),
          Example("mean", "negative"),
          Example("terrible", "negative"),
          Example("im drained", "negative"),
          Example("Im having a horrible day", "negative")
        ]

        response = co.classify(
          model='large',
          inputs = inputs,
          examples = examples,
        )

        WholeClassification = ''.join(str(x) for x in response.classifications)
        classification = WholeClassification.removeprefix("Classification<prediction:")
        mood = classification[:10]
        mood = mood[2:]
        confidence = classification[:30]
        confidence = float(confidence[25:])

        if (confidence < 0.70):
            mood = "neutral"

        # Debug print statements
        # ----------------------

        # Response Generation
        prompt = f"""  
        This program generates a message based off your response to a mental health question.

        Mood: positive  
        That's great to hear!
        --  
        Mood: positive  
        I'm so happy for you!
        --  
        Mood: positive  
        Keep the good vibes going!
        --
        Mood: positive  
        I hope your day continues to be amazing.
        --
        Mood: positive  
        You deserve to have a good day.
        --
        Mood: neutral  
        Sometimes neutral days can be a good thing, it's a break from the highs and lows.
        --
        Mood: neutral  
        Remember, it's okay to have a quiet day once in a while.
        --
        Mood: neutral  
        Neutral days can be a chance to relax and recharge before a more exciting day comes along.
        --
        Mood: negative  
        Remember that bad days are temporary and tomorrow is a new day.
        --
        Mood: negative  
        You're strong enough to get through this.
        --
        Mood: negative  
        Take care of yourself today, and remember that things will get better.
        --
        Mood: negative  
        It's okay to have a bad day, we all have them. Just know that you're not alone.
        --  
        """

        prompt = prompt + "Mood: " + mood

        response = co.generate(  
            model='command-xlarge-nightly',  
            prompt = prompt,  
            max_tokens = 40,  
            temperature = 2,  
            stop_sequences=["--"])

        answer = response.generations[0].text
        answer = answer.strip("-")
        print(answer)
        resp.message(answer)


    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)