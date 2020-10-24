import secrets


class OTP:
    def __init__(self, length=250, group_size=5, otp=None):
        self.length = length
        self.group_size = group_size
        self.numbers = []
        self.pad = ''
        self.new = True

        # force length to a multiple of the group size
        if self.length % (self.group_size * 10) != 0:
            self.length += (self.group_size * 10) - (self.length % (self.group_size * 10))

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
        # add the otp id to the beginning of the ciphertext (used for
        # decryption with printed otp's)
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
        # remove formatting characters
        numbers = otp
        numbers = numbers.replace(' ', '')
        numbers = numbers.replace('\n', '')
        print(numbers)
        # convert string to list of single digit numbers
        numbers = [int(x) for x in numbers]
        self.numbers = numbers

    def __get_random_numbers(self):
        for i in range(self.length):
            # get a random number below 10 (0-9)
            self.numbers.append(secrets.randbelow(10))

    # construct a readable text block of the otp
    def __build_pad(self):
        for i in range(len(self.numbers)):
            # create text lines by inserting line breaks
            if i != 0 and i % (self.group_size*10) == 0 and i != len(self.numbers)-1:
                self.pad += '\n'
            # create groups by inserting spaces
            elif i != 0 and i % self.group_size == 0 and i != len(self.numbers)-1:
                self.pad += ' '
            self.pad += str(self.numbers[i])

    def __repr__(self):
        return self.pad


class MultipleUseException (Exception):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)
