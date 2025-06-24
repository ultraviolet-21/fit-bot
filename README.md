# fitness-bot

# Overview:
[statistic] The Fitness Bot is a Telegram bot that will suggest the user a 20-30 minute workout every day. The user can reply once they've completed the workout, and the program will keep track of their streak.

# Key Features: 
1. Uses Telegram's bot feature to randomly suggest a workout of a given type (cardio, strength, flexibility, etc)
2. Uses the datetime library to send a text at the same time every day, and wait for a reply
3. Streak file that will be incremented or reset depending on the user's replies

# Tools Used:
I coded this entire project using Python 3.11. I used Python's third-party telegram library to set up the application, send messages, and wait for a response. In addition, I used built-in libraries like json, datetime, and logging. The project requires a virtual environment to run.

# Example Workflow:
1. At a given time (default: midnight Pacific Time), the user receives a message with a randomly selected workout.
2. Any time during the day, the user can complete the workout. Upon completion, the user must reply to the message.
3. Once the reply is received, the streak will be incremented. For first-time users, the streak will be updated from None to 1.
4. A message with the length of the current streak will be sent to the user.
5. If no reply is received for 24 hours, then the streak is reset to 0.

[add conclusion/ future directions]
