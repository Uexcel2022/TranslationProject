
class Name:
    def __init__(self, name):
        self.validName = name

    @classmethod
    def Return(cls, validName):
        if validName.isalpha() and len(validName) > 2:
            return cls (validName.title())


class AgeRegex:
    def __init__(self, age):
        self.validAge = age

    @classmethod
    def ageRegex(cls, validAge):
        import re
        if match := re.fullmatch(r"^[1-9][8-9]|[2-9][0-9]|1[0-5][0-9]", validAge):
            return cls(match.group())


class PhoneNumber:
    def __init__(self, phone):
        self.validPhone = phone

    @classmethod
    def phoneNumber(cls, validPhone):
        import re
        if check := re.fullmatch("(\+234[7-9][0-1][0-9]{8}|0[7-9][0-1][0-9]{8})", validPhone):
            return cls(check.group())


class EmailAddress:
    def __init__(self, mail):
        self.validemail = mail
    @classmethod
    def MailRegex(cls, validEmail):
        validEmail = validEmail.lower()
        import re
        if check := re.fullmatch(r"^[a-z0-9]+[_.]?[a-z0-9]*[_.]?[a-z0-9]+@[a-z0-9]+\.?[a-z]*\.([a-z]{2,3})", validEmail):
            return cls(check.group())

class Code:
    def __init__(self,publicKey, privateKey, pin):
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.pin = pin

    @classmethod
    def GenerateCode(cls):
        from string import printable
        from random import randint
        publicKey = ''
        for i in range(10):
            rand = randint(10, 61)
            key = printable[rand]
            publicKey += key

        privateKey = ''
        for i in range(7):
            rand = randint(10, 61)
            key = printable[rand]
            privateKey += key

        pin = str(randint(1000, 9999))

        return cls(publicKey,privateKey, pin )


class Registration:
    def __init__(self,firstName, lastName, age, phone, mail):
        self.firstName = firstName
        self. lastName =  lastName
        self.age = age
        self.phone = phone
        self.mail = mail

    @classmethod
    def UserData(cls):
        FirstName = ''
        LastName = ''
        Age = ''
        Phone = ''
        Email = ''
        try:
            name = input("Enter firstName:").strip().title()
            obj = Name.Return(name)
            if obj is None:
                print("invalid name")
                while True:
                    name = input("Re_enter firstName Q to quit:").strip().title()
                    if name == 'Q':
                        break
                    obj = Name.Return(name)
                    if obj is None:
                        print("invalid name")
                    else:
                        FirstName += obj.validName
                        break
            else:
                FirstName += obj.validName

            if len(FirstName) >= 2:
                name = input("Enter lastName:").strip().title()
                obj1 = Name.Return(name)
                if obj1 is None:
                    print("invalid name")
                    while True:
                        name = input("Re_enter lastName or Q to quit:").strip().title()
                        if name == 'Q':
                            break
                        obj1 = Name.Return(name)
                        if obj1 is None:
                            print("invalid name")
                        else:
                            LastName += obj1.validName
                            break
                else:
                    LastName += obj1.validName

            if len(LastName) >= 2:
                age = input("Enter age:").strip()
                obj2 = AgeRegex.ageRegex(age)
                if obj2 is None:
                    print("Unexpected age value")
                    while True:
                        age = input("Re_enter age[18 - 159] or Q to Quit:").strip()
                        if age.lower() == 'q':
                            break
                        obj2 = AgeRegex.ageRegex(age)
                        if obj2 is None:
                            print("invalid age")
                        else:
                            Age += obj2.validAge
                            break
                else:
                    Age += obj2.validAge

            if len(Age) >= 2:
                nPhone = input("Enter phone number:").strip()
                obj3 = PhoneNumber.phoneNumber(nPhone)
                if obj3 is None:
                    print("invalid phone format")
                    while True:
                        nPhone = input("reenter phone or O to quit:").strip()
                        if nPhone == '0':
                            break
                        obj3 = PhoneNumber.phoneNumber(nPhone)
                        if obj3 is None:
                            print("invalid phone format")
                        else:
                            Phone += obj3.validPhone
                            break
                else:
                   Phone += obj3.validPhone

            if len(Phone) > 2:
                mail = input("Enter email:").lower().strip()
                obj4 = EmailAddress.MailRegex(mail)
                if obj4 is None:
                    print("invalid email format")
                    while True:
                        mail = input("Reenter email or Q to quit:").strip().lower()
                        if mail.lower() == 'q':
                            break
                        obj4 = EmailAddress.MailRegex(mail)
                        if obj4 is None:
                            print("invalid email format")
                        else:
                            Email += obj4.validemail
                            break
                else:
                    Email += obj4.validemail

        except KeyboardInterrupt:
            print("Process terminated.")

        else:
            if len(Email) < 2:
                print("Process cancelled.")
            else:
                import time
                print("Working on it")
                time.sleep(1)
                obj = Code.GenerateCode()
                PublicKey = obj.publicKey
                PrivateKey = obj.privateKey
                Pin = obj.pin

                Error = Insert.insert(FirstName, LastName, Phone, Age, Email, Pin, PrivateKey, PublicKey)
                if Error is None:
                    print('Registration Successful.')
                    print(f"Dear {FirstName}, \nyour longin details are:")
                    print(f"PublicKey: {PublicKey}")
                    print(f"PrivateKey: {PrivateKey}")
                    print(f"Pin: {Pin}")
                    print("You will need them for authentication.")
                else:
                    print('Error occurred.')


class Insert:
    @classmethod
    def insert(cls,FirstName, LastName, Phone, Age, Email, Pin, PrivateKey, PublicKey):
        import sqlite3
        try:

            conn = sqlite3.connect('UserData.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO UserDetail VALUES (?, ?, ?, ?, ?, ?)',
                        (FirstName, LastName, Age, Phone, Email, 0))
            cur.execute('INSERT INTO UserLog VALUES (?, ?, ? ,?)', (Phone, Pin, PrivateKey, PublicKey))
            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            return 'OperationalError'
        
    @classmethod
    def UserLogTable(cls, Phone, Pin, PrivateKey, PublicKey):
        import sqlite3
        try:
            conn = sqlite3.connect('UserData.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO UserLog VALUES (?, ?, ? ,?)', (Phone, Pin, PrivateKey, PublicKey))
            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            return 'OperationalError'


class FetchData:
    @classmethod
    def Data(cls,Phone):
        Pin = ''
        PrivateKey = ''
        PublicKey = ''
        FirstName = ''
        import sqlite3
        conn = sqlite3.connect('UserData.db')
        cur = conn.cursor()
        cur.execute(f"SELECT Phone From UserLog WHERE Phone = '{Phone}'")
        records = cur.fetchall()
        if len(records) == 0:
            print("Phone number does not exist in our record.")
        else:
            Code.GenerateCode()
            import time
            time.sleep(1)
            obj = Code.GenerateCode()
            PublicKey += obj.publicKey
            PrivateKey += obj.privateKey
            Pin += obj.pin
            print(Pin, PrivateKey, PublicKey)
            conn = sqlite3.connect('UserData.db')
            cur = conn.cursor()
            cur.execute(f"SELECT FirstName FROM UserDetail WHERE Phone = '{Phone}'")
            data = cur.fetchall()
            for items in data:
                FirstName += items[0]
            Error = Insert.UserLogTable(Phone, Pin, PrivateKey, PublicKey)
            if Error is None:
                print(f"Dear {FirstName}, \nyour longin details are:")
                print(f"PublicKey: {PublicKey}")
                print(f"PrivateKey: {PrivateKey}")
                print(f"Pin: {Pin}")
                print("You will need them for authentication.")
            else:
                print('Error occurred.')


class GenerateKey:
    @classmethod
    def Genenerate(cls):
        import time
        Quit = ''
        brake = ''
        while True:
            try:
                if brake == 'Q':
                    break
                phone = input("""Enter your phone number to generate new login details or "E" to Exit: """).strip()
                print("Working on it...")
                if phone == 'e' or phone == 'E':
                    Quit += phone.upper()
                    time.sleep(1)
                    break
                FetchData.Data(phone)
                break
            except KeyboardInterrupt:
                print("Program terminated")
                break

class Login:
    @classmethod
    def Login(cls):
        import sqlite3
        import time
        brQ = ''
        while True:
            if brQ == 'Q':
                break
            try:
                PubKy = input("""Enter your Public key to Login, N for new login details, or "Q" to Quit: """).strip()
                if len(PubKy) == 1 and PubKy.upper() == 'N':
                    GenerateKey.Genenerate()
                    continue

                elif PubKy.upper() == 'Q':
                    brQ += 'Q'
                    print('Quiting...')
                    time.sleep(0.5)
                    break
                else:
                    PrKy = input("Enter private key: ").strip()
                    print("Working on it...")
                    time.sleep(0.5)
                    validPin = ''
                    validPrKey = []
                    name = ''
                    phone = ''
                    count = 1
                    conn = sqlite3.connect('UserData.db')
                    cur = conn.cursor()
                    cur.execute(f"SELECT * FROM UserLog WHERE PublicKey = '{PubKy}'")
                    records = cur.fetchall()
                    for items in records:
                        validPin += items[1]
                        phone += items[0]
                        if items[2] == PrKy:
                            validPrKey.append(items[2])
                        else:
                            print("Invalid login details.")
                    if len(validPrKey) > 0:
                        time.sleep(0.5)
                        conn = sqlite3.connect('UserData.db')
                        cur = conn.cursor()
                        cur.execute(f"SELECT * FROM UserDetail WHERE Phone == '{phone}'")
                        records1 = cur.fetchall()
                        for items in records1:
                            name += (items[0])
                            count += int((items[5]))
                        print(f"Welcome {name},")
                        while True:
                            pin = input("Enter your pin to begin translation, N for new pin or O to quit: ").strip()
                            print("Working on it...")
                            if pin == validPin:
                                conn = sqlite3.connect('UserData.db')
                                cur = conn.cursor()
                                cur.execute(
                                    f"Update UserDetail SET LoginCount == '{count}' WHERE Phone == '{phone}'")
                                conn.commit()
                                conn.close()
                                time.sleep(1)
                                Translation.Translator()
                                brQ += 'Q'
                                break

                            elif pin.upper() == 'N':
                                GenerateKey.Genenerate()
                                break

                            elif pin == '0':
                                brQ += 'Q'
                                print('Quiting...')
                                time.sleep(0.5)
                                break
                            else:
                                print("Invalid pin.")
                                continue

            except KeyboardInterrupt:
                print('Program terminated.')
                break
            except sqlite3.OperationalError:
                print('Error occurred.')
                break



class Translation:
    @classmethod
    def Translator(cls):
        import pandas as pd
        import time
        from deep_translator import GoogleTranslator
        while True:
            try:
                try:
                    num = eval(input(
                        "From 1-3, how many languages would you like to be translated at once? or enter 0 to exit:"))
                except NameError:
                    print(f"Invalid selection")
                    continue
                except SyntaxError:
                    print("Emptiness...")
                    continue
                if num == 0:
                    print("Quiting...")
                    time.sleep(2)
                    break

                elif num > 3:
                    print("Were are sorry we can't translate more three languages at once at the moment")
                    continue

                elif num == 1:
                    source = input("""ENTER THE SOURCE LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if source == 'q':
                        print("Quiting")
                        time.sleep(2)
                        break
                    lan = input("""ENTER THE TARGET LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if lan == 'q':
                        print("Quiting")
                        time.sleep(2)
                        break
                    text = input("""ENTER THE TEXT TO BE TRANSLATED OR "Q" TO QUIT : """).lower().strip()
                    print('Working on it...')
                    if text == 'q':
                        print("Quiting")
                        time.sleep(2)
                        break

                    if len(text) == 0:
                        print("Empty text input are not allowed.")
                        time.sleep(2)
                        continue

                    if text[0].isdigit():
                        print("Unexpected value: Text does not start with digit.")
                        continue
                    if Language.languages(source) is None or Language.languages(lan) is None:
                        time.sleep(2)
                        print('We are sorry one or more of the languages are not available for translation.')
                        continue
                    else:
                        lang = {}

                        def trans(source, target, text):
                            translated = GoogleTranslator(source=source, target=target).translate(text)
                            lang[target.title()] = translated
                            return lang

                        print(trans(source, lan, text))

                        try:
                            f = open('TranslationNote.txt', 'a')
                            f.write(f"\n{source.title()}={lang}")
                            f.close()
                        except UnicodeEncodeError:
                            print("UnicodeEncodeError occurred. ")
                        except NameError:
                            print("NameError occurred")

                        Source = ([source])
                        Target = list(lang)
                        word = (list(lang.values()))
                        TranslationTable = pd.DataFrame({'Source': Source, 'Target': Target, 'Text': word})
                        TranslationTable.index = TranslationTable.index + 1
                        print(TranslationTable)
                        try:
                            TranslationTable.to_csv("TranslationTable.csv")
                        except PermissionError:
                            print('Permission denied')

                elif num == 2:
                    source1 = input("""ENTER THE SOURCE LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if source1 == 'q':
                        print("Quiting")
                        time.sleep(2)
                        break
                    lan1 = input("""ENTER THE TARGET LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if lan1 == 'q':
                        print("Quiting")
                        time.sleep(2)
                        break
                    lan2 = input("""ENTER THE TARGET LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if lan2 == 'q':
                        print("Quiting")
                        time.sleep(2)
                        break
                    text = input("""ENTER THE TEXT TO BE TRANSLATED OR "Q" TO QUIT : """).lower().strip()
                    print('Working on it...')
                    if text == 'q':
                        print("Quiting")
                        time.sleep(2)
                        break

                    if len(text) == 0:
                        print("Empty text input are not allowed.")
                        continue

                    if text[0].isdigit():
                        print("Unexpected value: Text does not start with digit.")
                        continue

                    if Language.languages(source1) is None or Language.languages(lan1) is None or \
                            Language.languages(lan2) is None:
                        time.sleep(2)
                        print('We are sorry one or more of the languages are not available for translation.')
                        continue
                    else:
                        lang2 = {}

                        def trans1(source1, target, text):
                            translated = GoogleTranslator(source=source1, target=target).translate(text)
                            lang2[target.title()] = translated
                            return lang2

                        trans1(source1, lan1, text)
                        print(trans1(source1, lan2, text))
                        try:
                            f = open('TranslationNote.txt', 'a')
                            f.write(f"\n{source1.title()}={lang2}")
                            f.close()
                        except UnicodeEncodeError:
                            print("UnicodeEncodeError occurred. ")
                        except NameError:
                            print("NameError occurred")

                        Source = ([source1, source1])
                        Target = list(lang2)
                        word = (list(lang2.values()))
                        TranslationTable = pd.DataFrame({'Source': Source, 'Target': Target, 'Text': word})
                        TranslationTable.index = TranslationTable.index + 1
                        print(TranslationTable)
                        try:
                            TranslationTable.to_csv("TranslationTable.csv")
                        except PermissionError:
                            print('Permission denied')

                elif num == 3:
                    source2 = input("""ENTER THE SOURCE LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if source2 == 'q':
                        print("Quiting...")
                        time.sleep(2)
                        break
                    lan1 = input("""ENTER THE TARGET LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if lan1 == 'q':
                        print("Quiting...")
                        time.sleep(2)
                        break
                    lan2 = input("""ENTER THE TARGET LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if lan2 == 'q':
                        print("Quiting...")
                        time.sleep(2)
                        break
                    lan3 = input("""ENTER THE TARGET LANGUAGE OR "Q" TO QUIT : """).lower().strip()
                    if lan3 == 'q':
                        print("Quiting...")
                        time.sleep(2)
                        break
                    text = input("""ENTER THE TEXT TO BE TRANSLATED OR "Q" TO QUIT : """).lower().strip()
                    print('Working on it...')
                    if text == 'q':
                        print("Quiting...")
                        time.sleep(2)
                        break

                    if len(text) == 0:
                        print("Enpty text input are not allowed.")
                        continue

                    if text[0].isdigit():
                        print("Unexpected value: Text does not start with digit.")
                        continue
                    if Language.languages(source2) is None or Language.languages(lan1) is None or \
                          Language.languages(lan2) is None or Language.languages(lan3) is None:
                        time.sleep(2)
                        print('We are sorry one or more of the languages are not available for translation.')
                        continue
                    else:
                        lang3 = {}

                        def trans3(source2, target, text):
                            translated = GoogleTranslator(source=source2, target=target).translate(text)
                            lang3[target.title()] = translated
                            return lang3

                        trans3(source2, lan1, text)
                        trans3(source2, lan2, text)
                        print(trans3(source2, lan3, text))
                        try:
                            f = open('TranslationNote.txt', 'a')
                            f.write(f"\n{source2.title()}={lang3}")
                            f.close()
                        except UnicodeEncodeError:
                            print("UnicodeEncodeError occurred. ")
                        except NameError:
                            print("NameError occurred")

                        Source = ([source2, source2, source2])
                        Target = list(lang3)
                        word = (list(lang3.values()))
                        TranslationTable = pd.DataFrame({'Source': Source, 'Target': Target, 'Text': word})
                        TranslationTable.index = TranslationTable.index + 1
                        print(TranslationTable)
                        try:
                            TranslationTable.to_csv("TranslationTable.csv")
                        except PermissionError:
                            print('Permission denied')
            except KeyboardInterrupt:
                print('Program terminated.')
                break
            except ConnectionRefusedError:
                print("No network connection")
            except ConnectionAbortedError:
                print("No network connection")
            except ConnectionError:
                print("No network connection")





class Language:
    def __int__(self,item):
        self.item = item
    @classmethod
    def languages(cls,item):
        lang = ['afrikaans' 'albanian', 'amharic', 'arabic', 'armenian', 'assamese', 'aymara', 'azerbaijani',
               'bambara', 'basque', 'belarusian', 'bengali', 'bhojpuri', 'bosnian', 'bulgarian', 'catalan', 'cebuano',
               'chichewa', 'chinese', 'chinese', 'corsican', 'croatian', 'czech', 'danish', 'dhivehi', 'dogri', 'dutch',
               'english', 'esperanto', 'estonian', 'ewe', 'filipino', 'finnish', 'french', 'frisian', 'galician',
               'georgian',
               'german', 'greek', 'guarani', 'gujarati', 'haitian', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong',
               'hungarian', 'icelandic', 'igbo', 'ilocano', 'indonesian', 'irish', 'italian', 'japanese', 'javanese',
               'kannada', 'kazakh', 'kinyarwanda', 'konkani', 'korean', 'krio', 'kurdish', 'kurdish', 'kyrgyz',
               'lao', 'latin', 'latvian', 'lingala', 'lithuanian', 'luganda', 'luxembourgish', 'macedonian', 'maithili',
               'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'meiteilon (manipuri)', 'mni-Mtei',
               'mizo',
               'mongolian', 'myanmar', 'nepali', 'norwegian', 'odia (oriya)', 'oromo', 'pashto', 'persian', 'polish',
               'portuguese', 'punjabi', 'quechua', 'romanian', 'russian', 'samoan', 'sanskrit', 'scots gaelic',
               'sepedi',
               'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish',
               'sundanese',
               'swahili', 'swedish', 'tajik', 'tamil', 'tatar', 'telugu', 'thai', 'tigrinya', 'tsonga', 'turkish',
               'turkmen',
               'twi', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba',
               'zulu']
        for x in lang:
            if x == item:
                return (x)

















