## HOMEWORK 1

import random

print("Welcome to Pao Ying Chub challenge!!")
print()

# declare score
user_score = 0
computer_score = 0

while user_score < 5 and computer_score < 5:
  options = ["R", "P", "S"]
  # get hand from user and computer
  user_hand = input("Choose R, P, S ").upper()
  print(f"User choose: {user_hand}")
  computer_hand = random.choice(options)
  print(f"Computer choose: {computer_hand}")

  # check invalid option before looping
  if user_hand not in options:
    print("Invalid choice. Please choose " + ",".join(options))

  else:
    #while user_score or computer_score < 5:
    if user_hand == computer_hand:
      print("Tie !!")
    elif (user_hand == "R" and computer_hand == "S") or \
    (user_hand == "S" and computer_hand == "P") or \
    (user_hand == "P" and computer_hand == "R"):
      print("Congrat! You won!!")
      user_score += 1
    else:
      print("You lose!! Try again")
      computer_score += 1

  # summary the score
  print(f"Your score is {user_score}")
  print(f"Computer score is {computer_score}")

if user_score > computer_score:
  print(f"Congratulation! You win with score {user_score} to {computer_score}")
else:
  print(
      f"You lose with score {user_score} to {computer_score}. Try again next time"
  )
