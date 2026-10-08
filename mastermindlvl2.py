# mastermindlvl2.py
import random

secret_num = random.randrange(1000, 10000)

attempts = 0

print("Welcome to Mastermind!")
print("Try to guess the 4-digit number.\n")

while True:

    try:
        guess = int(input("Guess the 4-digit number: "))

        if guess < 1000 or guess > 9999:
            print("Please enter a valid 4-digit number.\n")
            continue

    except ValueError:
        print("Please enter numeric digits only.\n")
        continue

    attempts += 1

    if guess == secret_num:
        print("\nYou've become a Mastermind!")
        print(f"It took you only {attempts} tries.")
        break

    guess_str = str(guess)
    secret_str = str(secret_num)

    count = 0

    for i in range(4):
        if guess_str[i] == secret_str[i]:
            count += 1

    print(
        f"\nNot quite the number. "
        f"You got {count} digit(s) correct.\n"
    )