from collections import UserDict
from exceptions import PhoneFormatException, DuplicateContactException, DuplicatePhoneException, BirthDateIsInFutureException
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        if value.isnumeric() and len(value) == 10:
            super().__init__(value)
        else:
            raise PhoneFormatException()

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, '%d.%m.%Y')

            if date <= datetime.now():
                super().__init__(date)
            else:
                raise BirthDateIsInFutureException()
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')
    
    def __str__(self):
        return str(self.value.strftime('%d.%m.%Y'))

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if self.find_phone(phone) != None:
            raise DuplicatePhoneException
        
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def remove_phone(self, phone):
        self.phones = list(filter(lambda p : p.value != phone, self.phones))

    def find_phone(self, query):
        return next((p for p in self.phones if p.value == query), None)

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def __str__(self):
        phones_part = ', has no phones'
        birthday_part = ', birthday not set'

        if len(self.phones) > 0:
            phones_part = f', phones: {'; '.join(p.value for p in self.phones)}'

        if self.birthday != None:
            birthday_part = f', {self.birthday.strftime('%d.%m.%Y')}'
        
        return f'Contact name: {self.name.value}{phones_part}{birthday_part}'

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if record.name in self.data:
            raise DuplicateContactException
        
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]

        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()

        result = []

        for _, contact in self.data.items():
            if contact.birthday == None:
                continue

            # беремо дату народження
            birth_date = contact.birthday.value.date()

            # створюємо дату дня народження цього року
            birthday_this_year = datetime(year = today.year, month = birth_date.month, day = birth_date.day).date()

            # якщо день народження вже минув, беремо день народження у наступному році
            if birthday_this_year < today:
                birthday_this_year = datetime(today.year + 1, birth_date.month, birth_date.day).date()

            # знаходимо різницю сьогоднішньої дати та дати наступного дня народження
            left = birthday_this_year - today

            # Якщо припадає на найближчий тиждень
            if (left.days <= 7):
                week_no = birthday_this_year.weekday()
                
                # Якщо припадає на вихідні - переносимо на найближчий понеділок
                if week_no >= 5:
                    birthday_this_year = birthday_this_year + timedelta(days = 6 - week_no)

                result.append({'name': contact.name.value, 'congratulation_date': birthday_this_year})

        return result

