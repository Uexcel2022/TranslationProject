
class FirstName:
    def __init__(self, firstName):
        while True:
            import re
            if checkName1 := re.fullmatch(r"^[A-Za-z][A-Za-z]+", firstName):
                self.firstName = checkName1.group().title()
                break
            else:
                v = [x for x in firstName if not x.isalpha()]
                self.firstName = f"Invalid. Remove {''.join(v)} or the white space or name < 2 letters."
                print(self.firstName)
                firstName = input("first name:").strip()
                self.firstName = firstName

    def returnFName(self):
        return self.firstName


class LastName:
    def __init__(self, lastName):
        while True:
            import re
            if checkName1 := re.fullmatch(r"^[A-Za-z][A-Za-z]+", lastName):
                self.lastName = checkName1.group().title()
                break
            else:
                v = [x for x in lastName if not x.isalpha()]
                self.lastName = f"Invalid. Remove {''.join(v)} or the white space or name < 2 letters."
                print(self.lastName)
                lastName = input(" last name:").strip().title()
                self.lastName = lastName

    def returnLName(self):
        return self.lastName


class Email:
    def __init__(self, mail):
        while True:
            import re
            mail = mail.lower()
            if check2 := re.fullmatch(r"^[a-z0-9]+[_.]?[a-z0-9]+[_.]?[a-z0-9]+@[a-z0-9]+\.?[a-z]*\.([a-z]{2,3})",mail):
                self.mail = check2.group()
                break
            else:
                self.mail = check2
                print("invalid email format")
                mail = input("Email:").strip().lower()
                self.mail = mail

    def returnEmail(self):
        return self.mail


class Age:
    def __init__(self,age):
        while True:
            import re
            if match := re.fullmatch(r"^[1-9][8-9]|[2-9][0-9]|1[0-5][0-9]", age):
                self.age = match.group()
                break
            else:
                self.age = '18 < age > 159 or not entirely digit.'
                print(self.age)
                age = input("Age:").strip()
                self.age = age

    def returnAge(self):
        return self.age


class Phone:
    def __init__(self,phone):
        while True:
            import re
            if match := re.fullmatch("\+234[7-9][0-1][0-9]{8}|0[7-9][0-1][0-9]{8}", phone):
                self.phone = match.group()
                break
            else:
                self.phone = 'Invalid Nig phone number.'
                print(self.phone)
                phone = input("Phone:").strip()
                self.phone = phone

    def returnPhone(self):
        return self.phone


class PersonInput:
    @classmethod
    def input(cls):
        ob1 = FirstName(input("first name:").strip())
        ob2 = LastName(input(" last name:").strip())
        ob3 = Age(input("Age:").strip())
        ob4 = Phone(input("Phone:").strip())
        ob5 = Email(input("Email:").strip())
        # print(f"{ob1.returnFName()} {ob2.returnLName()} {ob3.returnAge()} {ob4.returnPhone()} {ob5.returnEmail()}")
        import time
        print("Processing data...")
        time.sleep(2)
        data = Code.GenerateCode()
        Database.PersonData(ob1.returnFName(), ob2.returnLName(), ob3.returnAge(), ob4.returnPhone(),
                            ob5.returnEmail(),data.pin, data.privateKey, data.publicKey)


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
                data = FetchData.dataPhone(phone)
                if len(data) != 0:
                   records = Code.GenerateCode()
                   Database.personLog(phone,records.pin, records.privateKey,records.publicKey)
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

            publicKey = input("""Enter your Public key to Login, N for new login details, or "Q" to Quit: """).strip()
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
                        pin = input("Enter your pin to begin translation, N for new pin or O to quit: ").strip()
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
                        TranslationTable = pd.DataFrame({f'{source.name.title()}': SourceText, 'Target': Target, 'Translated': word})
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
                print("Empty text input are not allowed and text can not start with 0 digit.")
                text = input("Re-enter text or Q to quit.")
                if text.upper() == 'Q':
                    return cls(text.title())


