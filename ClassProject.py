
class FirstName:
    def __init__(self, firstName):
        self.firstName = firstName
    @classmethod
    def returnFName(cls, checkName):
        while True:
            import re
            if match := re.fullmatch(r"^[A-Za-z][A-Za-z]+", checkName):
                return cls(match.group().title())
            else:
                invalidChar = [x for x in checkName if not x.isalpha()]
                print(f"Invalid. Remove {''.join(invalidChar)} or the white space or name < 2 letters.")
                checkName = input("Enter first name or Q to quit:").title().strip()
                if checkName == 'Q':
                    return cls(checkName)


class LastName:
    def __init__(self, lastName):
        self.lastName = lastName
    @classmethod
    def returnLName(cls, checkName):
        while True:
            import re
            if match := re.fullmatch(r"^[A-Za-z][A-Za-z]+", checkName):
                return cls(match.group().title())
            else:
                invalidChar = [x for x in checkName if not x.isalpha()]
                print(f"Invalid. Remove {''.join(invalidChar)} or the white space or name < 2 letters.")
                checkName = input("Enter last name or Q to quit:").strip().title()
                if checkName == 'Q':
                    return cls(checkName)

class Email:
    def __init__(self, mail):
        self.mail = mail
    @classmethod
    def returnEmail(cls, checkEmail):
        while True:
            import re
            checkEmail = checkEmail.lower()
            if match := re.fullmatch(r"^[a-z0-9]+[_.]?[a-z0-9]+[_.]?[a-z0-9]+@[a-z0-9]+\.?[a-z]*\.([a-z]{2,3})", checkEmail):
                return cls(match.group())
            else:
                print("Invalid email format.")
                checkEmail = input("Enter email or Q to quit:").strip().lower()
                if checkEmail == 'q':
                    return cls(checkEmail)


class Age:
    def __init__(self,age):
        self.age = age
    @classmethod
    def returnAge(cls,data):
        while True:
            import re
            if match := re.fullmatch(r"^[1-9][8-9]|[2-9][0-9]|1[0-5][0-9]", data):
                return cls(match.group())
            else:
                print('18 < age > 159 or not entirely digit.')
                data = input("Enter age or 0 to quit:").strip()
                if data == '0':
                    return cls(data)

class Phone:
    def __init__(self,phone):
        self.phone = phone

    @classmethod
    def returnPhone(cls,data):
        while True:
            import re
            if match := re.fullmatch("\+234[7-9][0-1][0-9]{8}|0[7-9][0-1][0-9]{8}", data):
                return cls(match.group())
            else:
                print('Invalid Nig phone number.')
                data = input("Enter phone or 0 to quit:").strip()
                if data == '0':
                    return cls(data)

class PersonInput:
    @classmethod
    def input(cls):
        while True:
            try:
                ob1 = FirstName.returnFName(input("Enter first name:").title().strip())
                if ob1.firstName == 'Q':
                    break
                ob2 = LastName.returnLName(input("Enter last name:").title().strip())
                if ob2.lastName == 'Q':
                    break
                ob3 = Age.returnAge(input("Enter age:").strip())
                if ob3.age == '0':
                    break
                ob4 = Phone.returnPhone(input("Enter phone:").strip())
                if ob4.phone == '0':
                    break
                ob5 = Email.returnEmail(input("Enter email:").lower().strip())
                if ob5.mail == 'q':
                    break
                else:
                    import time
                    print("Processing data...")
                    time.sleep(2)
                    data = Code.GenerateCode()
                    if data.pin != 'Error!':
                        Database.PersonData(ob1.firstName, ob2.lastName, ob3.age, ob4.phone,
                                        ob5.mail,data.pin, data.privateKey, data.publicKey)
                        break
                    else: print(data.pin)
                    break
            except KeyboardInterrupt:
                print("Program terminated")
                break


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
        check = []
        for i in range(10):
            rand = randint(10, 61)
            key = printable[rand]
            publicKey += key
        check.append(publicKey)

        privateKey = ''
        for i in range(8):
            rand = randint(10, 61)
            key = printable[rand]
            privateKey += key
        check.append(privateKey)
        pin = ''
        Pin = str(randint(1000, 9999))
        pin += Pin
        check.append(pin)
        if len(check) == 3:
            return cls(publicKey,privateKey, pin )
        else: return cls('Error!', 'Error!', 'Error!')

class Database:
    @classmethod
    def PersonData(cls, firstName, lastName, age, phone, email, pin, privateKey, publicKey):
        import sqlite3
        try:
            conn = sqlite3.connect('Test.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO PersonData VALUES (?, ?, ?, ?, ?, ?)',
                        (firstName, lastName, age, phone, email, 0))
            cur.execute('INSERT INTO PersonLog VALUES (?, ?, ?, ?)',
                        (phone, pin, privateKey, publicKey))
            conn.commit()
            conn.close()

        except sqlite3.OperationalError as error:
            print(error)
        else:
            print(f"Dear {firstName},\nYour Login Details are:\nPin: {pin}\nPrivateKey: {privateKey}\n"
                  f"PublicKey: {publicKey}")
            print("Save the details.")

    @classmethod
    def personLog(cls,phone, pin, privateKey, publicKey):
        import sqlite3
        import time
        try:
            conn = sqlite3.connect('Test.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO PersonLog VALUES (?, ?, ?, ?)',
                        (phone, pin, privateKey, publicKey))
            conn.commit()
            conn.close()
        except sqlite3.OperationalError as error:
            print(error)
        else:
            records = FetchData.dataPhone(phone)
            if len(records) != 0:
                time.sleep(1)
                print(f"Dear {records[0][0]},\nYour Login Details are:\nPin: {pin}\nPrivateKey: {privateKey}\n"
                      f"PublicKey: {publicKey}")
                print("Save the details.")
            else: print('Error!')

    @classmethod
    def update(cls, data):
       import sqlite3
       try:
            count = 1
            conn = sqlite3.connect('Test.db')
            cur = conn.cursor()
            cur.execute(f"SELECT LoginCount, Phone FROM PersonData WHERE Phone = '{data}'")
            records = cur.fetchall()
            count += records[0][0]
            cur.execute(
                f"Update PersonData SET LoginCount == '{count}' WHERE Phone == '{data}'")
            conn.commit()
            conn.close()
       except sqlite3.OperationalError:
           return 'Error!'
       except IndexError:
           return 'Error!'

class FetchData:
    def __init__(self, name, phone, pin, privateKey):
        self.name = name
        self.phone = phone
        self.pin = pin
        self.privateKey = privateKey
    @classmethod
    def dataPhone(cls, data):
        import sqlite3
        try:
            conn = sqlite3.connect('Test.db')
            cur = conn.cursor()
            cur.execute(f"SELECT FirstName, Phone FROM PersonData WHERE Phone = '{data}'")
            records = cur.fetchall()
            conn.close()
        except sqlite3.OperationalError as error:
            print(error)
        else:
            return records

    @classmethod
    def dataPublickey(cls,data):
        import sqlite3
        try:
            conn = sqlite3.connect('Test.db')
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM PersonLog WHERE PublicKey = '{data}'")
            records = cur.fetchall()
            conn.close()
        except sqlite3.OperationalError as error:
            print(error)
        else:
            if len(records) != 0:
                datas = FetchData.dataPhone(records[0][0])
                if len(datas) != 0:
                    return cls(name = datas[0][0], phone = datas[0][1],
                               pin = records[0][1], privateKey = records[0][2])
                else: return
            else: return


class Generate:
    @classmethod
    def key(cls):
        import time
        while True:
            try:
                phone = input("Enter your phone number to generate new login details or E to Exit:").strip()
                print("Working on it...")
                if phone == 'e' or phone == 'E':
                    time.sleep(1)
                    break
                data = FetchData.dataPhone(phone)
                if len(data) != 0:
                   records = Code.GenerateCode()
                   if records.pin != "Error!":
                       Database.personLog(phone,records.pin, records.privateKey,records.publicKey)
                   else: print(records.pin)
                break
            except KeyboardInterrupt:
                print("Program terminated")
                break

class Login:
    @classmethod
    def login(cls):
        import time
        brQ = ''
        while True:
            if brQ == 'Q':
                break
            try:
                publicKey = input("Enter your Public key to Login, N for new login details, or Q to Quit:").strip()
                if len(publicKey) == 1 and publicKey.upper() == 'N':
                    Generate.key()
                    continue

                elif publicKey.upper() == 'Q':
                    brQ += 'Q'
                    print('Quiting...')
                    time.sleep(0.5)
                    break
                else:
                    privateKey = input("Enter private key: ").strip()
                    time.sleep(0.5)
                    records = FetchData.dataPublickey(publicKey)
                    if records is None:
                        print('Invalid public key.')
                        continue

                    elif records.privateKey != privateKey:
                        print('Invalid Private key.')
                        continue

                    else:
                        print(f"Welcome {records.name},")
                        while True:
                            pin = input("Enter your pin to begin translation, N for new pin or O to quit:").strip()
                            if pin == records.pin:
                                data = Database.update(records.phone)
                                if data is None:
                                    print('Loading...')
                                    time.sleep(1)
                                    Translation.Translator()
                                    time.sleep(1)
                                    brQ += 'Q'
                                    break
                                else: print(data)
                                break

                            elif pin.upper() == 'N':
                                Generate.key()
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
                print("Program terminated")
                break

class Language:
    def __init__(self, name):
        self.name = name
    @classmethod
    def languages(cls, name):
        while True:
            lang = ['afrikaans' 'albanian', 'amharic', 'arabic', 'armenian', 'assamese', 'aymara', 'azerbaijani',
                    'bambara', 'basque', 'belarusian', 'bengali', 'bhojpuri', 'bosnian', 'bulgarian', 'catalan',
                    'cebuano', 'chichewa', 'chinese', 'chinese', 'corsican', 'croatian', 'czech', 'danish', 'dhivehi',
                    'dogri', 'dutch', 'english', 'esperanto', 'estonian', 'ewe', 'filipino', 'finnish', 'french',
                    'frisian', 'galician', 'georgian', 'german', 'greek', 'guarani', 'gujarati', 'haitian', 'hausa',
                    'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'ilocano', 'indonesian',
                    'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'kinyarwanda', 'konkani',
                    'korean', 'krio', 'kurdish', 'kurdish', 'kyrgyz', 'lao', 'latin', 'latvian', 'lingala',
                    'lithuanian', 'luganda', 'luxembourgish', 'macedonian', 'maithili', 'malagasy', 'malay',
                    'malayalam', 'maltese', 'maori', 'marathi', 'meiteilon (manipuri)', 'mni-Mtei', 'mizo','mongolian',
                    'myanmar', 'nepali', 'norwegian', 'odia (oriya)', 'oromo', 'pashto', 'persian', 'polish',
                    'portuguese', 'punjabi', 'quechua', 'romanian', 'russian', 'samoan', 'sanskrit', 'scots gaelic',
                    'sepedi', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali',
                    'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'tatar', 'telugu', 'thai',
                    'tigrinya', 'tsonga', 'turkish','turkmen', 'twi', 'ukrainian', 'urdu', 'uyghur', 'uzbek',
                    'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']
            if name in lang:
                return cls(name.lower())
            else:
                print('We are sorry the language is not enlisted for translation presently\n'
                      'or is due to incorrect spelling.')
                name = input('Re-enter language, chose other language or  Q to quit:').lower().strip()
                if name.upper() == 'Q':
                    return cls(name.title())


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
                    source = Language.languages(input('Enter source language:').lower().strip())
                    if source.name == 'Q':
                        break
                    lan = Language.languages(input('Enter target language:').lower().strip())
                    if lan.name == 'Q':
                        break

                    word = Text.check(input('Enter text to be translated:').title().strip())
                    if word.text == 'Q':
                        continue
                    else:
                        print('Working on it...')
                        time.sleep(2)

                        lang = {}

                        def trans(source, target, text):
                            translated = GoogleTranslator(source=source, target=target).translate(text)
                            lang[target.title()] = translated.capitalize()
                            return lang

                        print(trans(source.name, lan.name, word.text))

                        try:
                            f = open('TranslationNote.txt', 'a')
                            f.write(f"\n{source.name.title()}={lang}")
                            f.close()
                        except UnicodeEncodeError:
                            print("UnicodeEncodeError occurred. ")
                        except NameError:
                            print("NameError occurred")

                        SourceText = ([word.text])
                        Target = list(lang)
                        word = (list(lang.values()))
                        TranslationTable = pd.DataFrame({f'{source.name.title()}': SourceText, 'Target': Target,
                                                         'Translated': word})
                        TranslationTable.index = TranslationTable.index + 1
                        print(TranslationTable)
                        try:
                            TranslationTable.to_csv("TranslationTable.csv")
                        except PermissionError:
                            print('Permission denied')

                elif num == 2:
                    source1 = Language.languages(input('Enter source language:').lower().strip())
                    if source1.name == 'Q':
                        break
                    lan1 = Language.languages(input('Enter target language:').lower().strip())
                    if source1.name == 'Q':
                        break
                    lan2 = Language.languages(input('Enter target language:').lower().strip())
                    if lan2.name == 'Q':
                        break
                    word = Text.check(input('Enter text to be translated.').lower().strip())
                    print('Working on it...')
                    if word.text == 'Q':
                        break

                    else:
                        lang2 = {}

                        def trans1(source1, target, text):
                            translated = GoogleTranslator(source=source1, target=target).translate(text)
                            lang2[target.title()] = translated.capitalize()
                            return lang2

                        trans1(source1.name, lan1.name, word.text)
                        print(trans1(source1.name, lan2.name, word.text))
                        try:
                            f = open('TranslationNote.txt', 'a')
                            f.write(f"\n{source1.name.title()}={lang2}")
                            f.close()
                        except UnicodeEncodeError:
                            print("UnicodeEncodeError occurred. ")
                        except NameError:
                            print("NameError occurred")

                        SourceText = ([word.text, word.text])
                        Target = list(lang2)
                        word = (list(lang2.values()))
                        TranslationTable = pd.DataFrame({f'{source1.name.title()}': SourceText, 'Target': Target, 'Translated': word})
                        TranslationTable.index = TranslationTable.index + 1
                        print(TranslationTable)
                        try:
                            TranslationTable.to_csv("TranslationTable.csv")
                        except PermissionError:
                            print('Permission denied')

                elif num == 3:
                    source2 = Language.languages(input('Enter source language:').lower().strip())
                    if source2.name == 'Q':
                        break
                    lan1 = Language.languages(input('Enter target language:').lower().strip())
                    if lan1.name == 'Q':
                        break
                    lan2 = Language.languages(input('Enter target language:').lower().strip())
                    if lan2.name == 'Q':
                        break
                    lan3 = Language.languages(input('Enter target language:').lower().strip())
                    if lan3 == 'Q':
                        break
                    word = Text.check(input('Enter text to be translated.').lower().strip())
                    print('Working on it...')
                    if word.text == 'Q':
                        break

                    else:
                        lang3 = {}

                        def trans3(source2, target, text):
                            translated = GoogleTranslator(source=source2, target=target).translate(text)
                            lang3[target.title()] = translated.capitalize()
                            return lang3

                        trans3(source2.name, lan1.name, word.text)
                        trans3(source2.name, lan2.name, word.text)
                        print(trans3(source2.name, lan3.name, word.text))
                        try:
                            f = open('TranslationNote.txt', 'a')
                            f.write(f"\n{source2.name.title()}={lang3}")
                            f.close()
                        except UnicodeEncodeError:
                            print("UnicodeEncodeError occurred. ")
                        except NameError:
                            print("NameError occurred")

                        SourceText = ([word.text, word.text, word.text])
                        Target = list(lang3)
                        word = (list(lang3.values()))
                        TranslationTable = pd.DataFrame({f'{source2.name.title()}': SourceText, 'Target': Target, 'Text': word})
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


class Text:
    def __init__(self,text):
        self.text = text
    @classmethod
    def check(cls,text):
        while True:
            if len(text) != 0 and not text[0].isdigit():
                return cls(text.capitalize())
            else:
                print("Empty text input is not allowed and text can not start with 0 digit.")
                text = input("Re-enter text or Q to quit.")
                if text.upper() == 'Q':
                    return cls(text.title())


