 #!/usr/bin/env python3

import random

def main():
    answers = [
      "Yes - definitely",
      "It is decidedly so",
      "Without a doubt",
      "Reply hazy, try again",
      "Ask again later",
      "Better not tell you now",
      "My sources say no",
      "Outlook not so good",
      "Very doubtful"
    ]
    affirmative = ['yes','ya','ye','y','ok','go']
    negative = ['no','n','na','nah','stop','quit','exit']
    user_name = input("What is your name? ")

    while True:
      question = input(f"What would you like to ask the Magic 8-Ball(TM), {user_name}? ")
      print(f"{user_name} asks: {question}")
      answer = random.choice(answers)
      print(f"Magic 8-Ball's answer: {answer}")
      next_q = input(
              f"Ask another question? (yes/no) "
              ).lower()

      if next_q in affirmative:
        continue
      elif next_q in negative:
        print("See you next time!")
        break
      else:
        print("I didn't understand you. Try saying yes/no. I'm putting you through...")
        continue

if __name__ == "__main__":
    main()
