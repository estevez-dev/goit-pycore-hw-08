import sys
from entities import AddressBook, Record
from exceptions import PhoneFormatException, DuplicateContactException, DuplicatePhoneException, BirthDateIsInFutureException, ContactNotFoundException

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return 'Not enough arguments'
        except IndexError:
            return 'Not enough arguments'
        except (PhoneFormatException, DuplicateContactException, DuplicatePhoneException, BirthDateIsInFutureException, ContactNotFoundException) as e:
            return e

    return inner

@input_error
def add_contact(args, contacts: AddressBook):
    name, phone, *_ = args

    record = contacts.find(name)

    if record == None:
        record = Record(name)

    record.add_phone(phone)

    contacts.add_record(record)
    
    return 'Contact added.'

@input_error
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone, *_ = args
    
    record = contacts.find(name)

    if not record:
        raise ContactNotFoundException
    
    record.edit_phone(old_phone, new_phone)
    
    return 'Contact updated.'

@input_error
def get_phone(args, contacts: AddressBook):
    name, *_ = args

    record = contacts.find(name)

    if not record:
        raise ContactNotFoundException

    return ', '.join(str(p) for p in record.phones)

@input_error
def add_birthday(args, contacts: AddressBook):
    name, birthday, *_ = args

    record = contacts.find(name)

    if not record:
        raise ContactNotFoundException

    record.add_birthday(birthday)

    return f'Birthday added for {name}'

@input_error
def get_birthday(args, contacts: AddressBook):
    name, *_ = args

    record = contacts.find(name)

    if not record:
        raise ContactNotFoundException
    
    if record.birthday == None:
        return f'Birthday for {name} was not set yet'

    return f'{name} was born on {record.birthday}'

@input_error
def birthdays(_, contacts: AddressBook):
    if len(contacts) == 0:
        return 'Contacts are empty.'
    
    birthdays = contacts.get_upcoming_birthdays()

    if not len(birthdays):
        return 'No upcoming birthdays'

    result = ''
    
    for birthday in birthdays:
        result += f'{birthday['name']} awaits for congratulations on {birthday['congratulation_date'].strftime('%d.%m.%Y')}\n'
    
    return result.removesuffix('\n')


@input_error
def list(_, contacts: AddressBook):
    if len(contacts) == 0:
        return 'Contacts are empty.'
    
    result = ''
    
    for name in contacts:
        result += f'{contacts.find(name)}\n'

    return result.removesuffix('\n')

def main():
    contacts = AddressBook.load_data()

    print('Welcome to the assistant bot!')

    while True:
        user_input = input('Enter a command: ')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:

            AddressBook.save_data(contacts)
            
            print('Good bye!')

            quit()
        
        elif command in ['hello', 'hi']:
            
            print('How can I help you?')
        
        elif command == 'add':
            
            print(add_contact(args, contacts))
        
        elif command == 'change':
            
            print(change_contact(args, contacts))

        elif command == 'phone':
            
            print(get_phone(args, contacts))

        elif command == 'all':
            
            print(list(None, contacts))

        elif command == 'add-birthday':
            
            print(add_birthday(args, contacts))

        elif command == 'show-birthday':
            
            print(get_birthday(args, contacts))

        elif command == 'birthdays':
            
            print(birthdays(args, contacts))
        
        else:
            print('Invalid command.')
    

if __name__ == '__main__':
    main()