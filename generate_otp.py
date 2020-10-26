import sys
import otp

count = 1
path = None
output_format = 'text'

def option_count(option):
    global count
    option_index = sys.argv.index(option)
    count = int(sys.argv[option_index + 1])

def option_path(option):
    global path
    option_index = sys.argv.index(option)
    path = sys.argv[option_index + 1]

def option_format(option):
    global output_format
    option_index = sys.argv.index(option)
    output_format = sys.argv[option_index + 1]

options = {
        '-c': option_count,
        '-o': option_path,
        '-f': option_format
        }

if '-h' in sys.argv:
    print('generate_otp.py [-c count -o path -f format]')
    print('-c   number of one-time-pads to generate (default is 1)')
    print('-o   output file path (output to terminal if not provided)')
    print('-f   output format: text (default), html')
else:
    for option, func in options.items():
        if option in sys.argv:
            func(option)


otps = otp.OTPFactory(count)

if output_format == 'text':
    if path is None:
        print(otps)
    else:
        with open(path, 'w') as fd:
            fd.write(str(otps))
            fd.write('\n')
elif output_format == 'html':
    html = '<html>\n'
    html += '<head><title>OTP Generator</title></head>\n'
    html += '<body>\n'

    for otp in otps:
        otp = str(otp).replace('\n', '<br>')
        html += '<div>\n' + otp + '\n</div>\n<br>\n'

    html += '</body>\n'
    html += '</html>'

    if path is None:
        print(html)
    else:
        with open(path, 'w') as fd:
            fd.write(html)



