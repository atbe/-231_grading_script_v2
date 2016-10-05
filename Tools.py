def print_menu(options,menuName):
    print("\nChoose from the options below: [{}]\n".format(menuName))
    counter = 1
    for option in options:
        line = "    {}.....{}".format(counter,option)
        print(line)
        counter += 1
    print("\n    X.....Quit {}".format(menuName))
    options = [option.lower().strip() for option in options]
    choice_nums = [str(num) for num in range(1, len(options) + 1)]
    choice_nums.append("x")
    choice = input("\nWhat is your selection?: ").lower()
    while (choice not in choice_nums):
        print("Not a valid option. Please try again.")
        choice = input("\nWhat is your selection?: ").lower()
    return choice


