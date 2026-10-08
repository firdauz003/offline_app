import random

# Generate a random 4-digit number
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

    # Correct guess
    if guess == secret_num:
        print("\nYou've become a Mastermind!")
        print(f"It took you only {attempts} tries.")
        break

    # Convert numbers to strings for digit comparison
    guess_str = str(guess)
    secret_str = str(secret_num)

    count = 0
    correct = ['X'] * 4

    # Check each digit
    for i in range(4):
        if guess_str[i] == secret_str[i]:
            count += 1
            correct[i] = guess_str[i]

    print(f"\nNot quite the number. You did get {count} digit(s) correct.")

    if count > 0:
        print("Correctly placed digits:")
        print(" ".join(correct))

    print()