# fit-bot

# Overview:
According to the CDC, only 28% of American adults meet the recommended exercise guidelines. Common reasons for this are lack of motivation and lack of resources/ equipment. The benefits of regular exercise range from a decreased risk of heart disease to a stronger immune system to mitigating anxiety and depression. To encourage people to work out regularly, and address some of the barriers to do so, I developed FitBot. FitBot uses a Telegram bot that will suggest the user a 20-30 minute workout every day. These will be at-home workouts that require minimal equipment. The user can reply once they've completed the workout, which can be any time of the day, and the program will keep track of their streak. The streak feature is similar to Snapchat's and aims to incentivize users to work out every day.

# Key Features: 
1. Uses Telegram's bot feature to randomly suggest a workout of a given type (cardio, strength, flexibility, etc)
2. Uses the datetime library to send a text at the same time every day, and wait for a reply
3. Streak file that will be incremented or reset depending on the user's replies

# Tools Used:
I coded this entire project using Python 3.11. I used Python's third-party telegram library to set up the application, send messages, and wait for a response. In addition, I used built-in libraries like json, datetime, and logging. The project requires a virtual environment to run. (Bot link: https://t.me/Fitness288Bot)

# How to Set Up:
The link to the bot is https://t.me/Fitness288Bot. If you have a Telegram account, click on that, and then click "Start Bot." You can start a conversation with the bot by typing /start. Then, you will need to obtain your chat id. You can do this by typing https://api.telegram.org/bot7518139033:AAH75ac4lJmvoFLigs4A23LlTuCQXQVMTj4/getUpdates in a browser, and then sending a message to the bot. The chat id will then be visible on your browser. Set CHAT_ID to this, and then you are ready to receive messages! Now, you can run polling.py or daily_message.py.

# Example Workflow:
1. At a given time (default: midnight Pacific Time), the user receives a message with a randomly selected workout.
2. Any time during the day, the user can complete the workout. Upon completion, the user must reply to the message.
3. Once the reply is received, the streak will be incremented. For first-time users, the streak will be updated from None to 1.
4. A message with the length of the current streak will be sent to the user.
5. If no reply is received for 24 hours, then the streak is reset to 0.

# Future Directions:
1. Instead of randomly selecting from a set of hardcoded workouts, I plan to pull a workout from a large database. Alternatively, using a model like OpenAI to generate a workout.
2. Allowing the user to select the type of workout (strength, cardio, flexibility), and then the bot will reply with the specific workout.

