import sys, secrets

otp_count = 1

if len(sys.argv) > 1:
    otp_count = int(sys.argv[1])

def get_random_group(length=5, rand_below=10):
    numbers = []
    for x in range(length):
        numbers.append(str(secrets.randbelow(rand_below)))
    return ''.join(numbers)

def get_random_line(length=10):
    groups = []
    for x in range(length):
        groups.append(get_random_group())
    return ' '.join(groups)

def get_random_block(length=5):
    lines = []
    for x in range(length):
        lines.append(get_random_line())
    return '\n'.join(lines)

def get_otp(count):
    blocks = []
    for x in range(count):
        blocks.append(get_random_block())
    return '\n\n'.join(blocks)

print(get_otp(otp_count))
