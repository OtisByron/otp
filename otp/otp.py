import secrets

# Module for generating and using one-time-pads (otp)

# Object to genereate an otp of specified length, or load a given otp.
# Random numbers are generated using the cryptographically secure secrets
# module. Functions to encrypt and decrypt text are available. Encryption
# is as follows (decryption is the reverse/opposite process):
#  
# 1. Convert text to all uppercase characters (keeps ordinal values to 2 digits)
# 2. Convert each character to its UTF-8 ordinal value
# 3. Subtract 10 from the ordinal value (ensures ciphertext is always 2 digits)
# 4. Subtract OTP values from 'ordinal' values (skipping the first group, the ID)
# 5. Prepend the OTP ID (the first group) to the beginning of the ciphertext
#
class OTP:
    def __init__(self, length=225, group_size=5, otp=None):
        self.length = length
        self.group_size = group_size
        self.width = group_size * 15
        self.numbers = []
        self.pad = ''
        self.new = True

        # force length to a multiple of the group size
        if self.length % self.width != 0:
            self.length += self.width - (self.length % self.width)

        # load otp if provided, otherwise generate otp
        if otp is not None:
            self.__load_pad(otp)
        else:
            self.__get_random_numbers()
            self.__build_pad()

        # set the otp id to the first group
        self.id = self.pad[:self.group_size]

    def encrypt(self, msg):
        # error if the message is longer than the otp
        if len(msg) > self.length:
            raise ValueError('Message is longer than one-time-pad.')
        if not self.new:
            raise MultipleUseException('One-time-pad already used for encryption.')

        # convert to uppercase to keep ordinal values two digits
        msg = msg.upper()
        # convert characters to ordinal values, offseting by 10 to keep
        # ciphertext values two digits
        code = [(ord(c) - 10) for c in msg]
        ciphertext = []
        # generate ciphertext values based on ordinal values and otp,
        # accounding for otp id group)
        for i in range(len(code)):
            ciphertext.append(code[i] - self.numbers[i + len(self.id)])
        ciphertext = [str(c) for c in ciphertext]
        # prepend the otp id to the beginning of the ciphertext (used
        # for decryption with printed otp's)
        ciphertext =  self.id + ''.join(ciphertext)
        self.new = False
        return ciphertext

    def decrypt(self, ciphertext):
        # remove the otp id from the beginning of the ciphertext
        ciphertext = ciphertext[self.group_size:]
        code = []
        # steps of two because code values are two digits
        for i in range(0, len(ciphertext), 2):
            # capture both code digits
            c = int(ciphertext[i] + ciphertext[i+1])
            # decode using otp, accounting for for-loop step size and
            # otp id group
            c += self.numbers[int(i/2) + len(self.id)]
            # adjust for offset (see comments in encrypt() function)
            code.append(c + 10)
        msg = ''
        for i in range(len(code)):
            # convert ordinal values to characters
            msg += chr(code[i])
        return msg

    def __load_pad(self, otp):
        self.pad = otp
        self.numbers = otp
        # determine group size
        self.group_size = self.numbers.find(' ')
        # remove space characters
        self.numbers = self.numbers.replace(' ', '')
        # determine line width
        self.width = self.numbers.find('\n')
        # remove line break characters
        self.numbers = self.numbers.replace('\n', '')
        # convert string to list of single digit numbers
        self.numbers = [int(x) for x in self.numbers]
        # determine total length
        self.length = len(self.numbers)

    def __get_random_numbers(self):
        for i in range(self.length):
            # get a random number below 10 (0-9)
            self.numbers.append(secrets.randbelow(10))

    # construct a readable text block of the otp
    def __build_pad(self):
        for i in range(len(self.numbers)):
            # create text lines by inserting line breaks
            if i != 0 and i % self.width == 0 and i != len(self.numbers)-1:
                self.pad += '\n'
            # create groups by inserting spaces
            elif i != 0 and i % self.group_size == 0 and i != len(self.numbers)-1:
                self.pad += ' '
            self.pad += str(self.numbers[i])

    def __repr__(self):
        return self.pad


# Generate the specified quantity of otps.
# Generated otps are available as a text block (using built-in functions
# repr, str, print), a list (OTPFactory.otps attribute), or as a generator
# object (using a for statement).
#
# example:
#
# for otp in otp.OTPFactory(5):
#   print(otp, end='\n\n')
#
class OTPFactory:
    def __init__(self, count, length=225, group_size=5):
        self.count = count
        self.otps = []
        self.iterator = None

        # generate otps
        for i in range(self.count):
            self.otps.append(OTP(length, group_size))

    def __iter__(self):
        # create an iterator object from the list of otps
        self.iterator = iter(self.otps)
        return self.iterator

    def __next__(self):
        # if an iterator object has been created, return the next item
        if not self.iterator is None:
            return next(self.iterator)

    # construct a readable text block of the otps
    def __repr__(self):
        text = ''
        for i in range(len(self.otps)):
            # do not add line breaks after the last otp
            if i == (len(self.otps) - 1):
                text += str(self.otps[i])
            else:
                text += str(self.otps[i]) + '\n\n'

        return text


# exception used by OTP object
# raised when an OTP object is used to encrypt more than once
class MultipleUseException (Exception):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)
