import ClassProject
print('Welcome to One-World Translation....')
def LogIN():
    import time
    while True:
        try:
            time.sleep(1)
            options = input("""Enter "L" to login, "R" to register or "N" to get new log in details "Q" to Quit: """).upper()
            print('Working on it...')
            time.sleep(2)
            if options == 'Q':
                print('Quiting...')
                time.sleep(2)
                break
            if options == 'L':
                ClassProject.Login.login()
                time.sleep(0.5)
                continue

            elif options == 'R':
                ClassProject.PersonInput.input()
                time.sleep(0.5)
                continue

            elif options == 'N':
                ClassProject.Generate.key()
                time.sleep(0.5)
                continue
            else:
                print('No valid option selected')
        except KeyboardInterrupt:
            print('Program terminated.')
            break


LogIN()

















