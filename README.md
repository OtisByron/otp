# otp

A module to generate and use (encrypt and decrypt text) one-time-pads (otps).

Module usage examples:

    import otp
    
    # generate a new otp and encrypt a message
    pad = otp.OTP()
    print(pad)
    pad.encrypt('hello world!')
  
    # import an existing pad and decrypt a message
    imported_pad = '18513 16841 ...'
    imported_pad = otp.OTP(otp=imported_pad)
    imported_pad.decrypt('3781673584197...')
    
    # generate multiple otps using an otp factory
    otps = otp.OTPFactory(10)
    print(otps)
    for otp in otps:
      # do something useful with each otp
      

There is also a *generate_otp.py* script for easily generating and formatting otps.

Command line options:
* -h &nbsp;&nbsp;&nbsp; print script help
* -c &nbsp;&nbsp;&nbsp; number of otps to genereate (default is one)
* -o &nbsp;&nbsp;&nbsp; output file path (print to terminal if not included)
* -f &nbsp;&nbsp;&nbsp; format output as text (default, normal line breaks) or html (complete page, for viewing and printing from a browser)

Script usage examples:
    
    # generate a single otp in the terminal
    python3 generate_otp.py
    # generate 5 otps, formatted as text, and save them to /home/pi/otp
    python3 generate_otp.py -c 5 -o /home/pi/otp
    # generate 14 otps, formatted as html, and save everything to /home/pi/otp.html
    # this is a good option for filling a single page with otps for printing
    python3 generate_otp.py -c 14 -f html -o /home/pi/otp.html
