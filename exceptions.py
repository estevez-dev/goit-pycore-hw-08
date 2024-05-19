class PhoneFormatException(Exception):
    def __init__(self):
        super().__init__('Wrong phone number format')

class ContactNotFoundException(Exception):
    def __init__(self):
        super().__init__('Contact not found')

class BirthDateIsInFutureException(Exception):
    def __init__(self):
        super().__init__('Birth date can\'t be in the future')

class DuplicateContactException(Exception):
    def __init__(self):
        super().__init__('Contact already exist')

class DuplicatePhoneException(Exception):
    def __init__(self):
        super().__init__('Phone already added')