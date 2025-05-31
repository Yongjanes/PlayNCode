import re
import os
import subprocess
import sys
# import ast

# Updated Convention Dictionary
convention = {
    "bh": {
        "const" : "",
        "setup": "pinMode({pin}, OUTPUT);",
        "loop": "digitalWrite({pin}, HIGH);"
    },
    "bl": {
        "const" : "",
        "setup": "pinMode({pin}, OUTPUT);",
        "loop": "digitalWrite({pin}, LOW);"
    },
    # "bp": {
    #     "const": "int buttonState_{pin} = 0;",  # Declare button state variable
    #     "setup": "pinMode({pin}, INPUT);",    # Button pin
    #     "loop": "buttonState_{pin} = digitalRead({pin});"
    # },
    "ifbp": {
        "const": "int buttonState_{pin} = 0;",  # Declare button state variable
        "setup": "pinMode({pin}, INPUT);",
        "loop": "if (buttonState_{pin} == {state}){"  # Button state check
    },
    "wt": {
        "const" : "",
        "setup": "",
        "loop": "delay({milliseconds});"  # Delay (wait)
    },
    "fr": {
        "const" : "",
        "setup": "",
        "loop": "for (int {var} = 0; {var} < {range}; {var}++){"
    },
    "br": {
        "const" : "",
        "setup": "",
        "loop": "break;"
    },
    "cn": {
        "const" : "",
        "setup": "",
        "loop": "continue;"
    },
    "e": "}"
    
}

# Initialize setup and loop code blocks
const_code =""
setup_code = ""
loop_code = ""

# Track used pins for buttons and bulbs
used_pins = {'buttons': set(), 'bulbs': set(), 'servo':set(), 'buzzer': set()}

# Input string (example)
# input_string = input("Enter : ")
#reading String from file string.txt
# f = open("string.txt","r")
# input_string = f.read()
# f.close
dom_text = sys.argv[1]
# print(dom_text)
string = dom_text  # Initialize an empty string

# Assuming arrwithIdandTop is a list of lists or tuples
# for i in range(len(dom_text)):
#     if not dom_text:
#         continue
#     else:
#         string += str(dom_text[i][1]) + str(dom_text[i][2])

input_string = string
# print(string)

# Updated Regex to match commands with following digits
regex = re.compile(r'(fr(\d+))|(bh(\d+))|(bl(\d+))|(ifbp(\d+))|(wt(\d+))|(cb(\d+))|(s)|(e)|(mtr(\d+)rt(\d+))|(ifld(\d+))|(bzh(\d+))|(bzl(\d+))|(bz(\d+)cta4)|(bz(\d+)ctb4)|(bz(\d+)ctc4)|(bz(\d+)ctd4)|(bz(\d+)cte4)|(bz(\d+)ctf4)|(bz(\d+)ctg4)')

# Variable to keep track of nested loop variables
loop_variable_counter = 0
indentation_level = 0

def add_indent(code, level):
    """ Helper function to add indentation to generated code. """
    return '    ' * level + code

for match in regex.finditer(input_string):
    if match.group(3):  # 'bh' (Bulb high)
        pin = match.group(4)
        if (pin in used_pins['buttons']) or (pin in used_pins['servo']) or (pin in used_pins['buzzer']):
            raise ValueError(f"Pin {pin} cannot be used for a bulb, it is already assigned to another component.")
        used_pins['bulbs'].add(pin)
        setup_code += convention['bh']['setup'].format(pin=pin) + "\n"
        loop_code += add_indent(convention['bh']['loop'].format(pin=pin), indentation_level) + "\n"
        pin = ''
        const_code += convention["bh"]["const"]


    elif match.group(5):  # 'bl' (Bulb low)
        pin = match.group(6)
        if (pin in used_pins['buttons']) or (pin in used_pins['servo']) or (pin in used_pins['buzzer']):
            raise ValueError(f"Pin {pin} cannot be used for a bulb, it is already assigned to another component.")
        used_pins['bulbs'].add(pin)
        setup_code += convention['bl']['setup'].format(pin=pin) + "\n"
        loop_code += add_indent(convention['bl']['loop'].format(pin=pin), indentation_level) + "\n"
        pin = ''
        const_code += convention["bl"]["const"]

    # elif match.group(6):  # 'bp' (Button press)
    #     pin = match.group(6)
    #     if pin in used_pins['bulbs']:
    #         raise ValueError(f"Pin {pin} cannot be used for a button, it is already assigned to a bulb.")
    #     used_pins['buttons'].add(pin)
    #     setup_code += convention['bp']['setup'].format(pin=pin) + "\n"
    #     loop_code += add_indent(convention['bp']['loop'].format(pin=pin), indentation_level) + "\n"
    #     pin = ''

    elif match.group(7):  # 'ifbp' (Button press with condition)
        pin = match.group(8)
        if (pin in used_pins['bulbs']) or (pin in used_pins['servo']) or (pin in used_pins['buzzer']):
            raise ValueError(f"Pin {pin} cannot be used for a button, it is already assigned to another component.")
        used_pins['buttons'].add(pin)
        state = "HIGH"  # Button state check default to HIGH
        loop_code += add_indent(convention['ifbp']['loop'].format(pin=pin, state=state), indentation_level) + "\n"
        const_code += convention["ifbp"]["const"].format(pin=pin, state=state)
        setup_code += convention["ifbp"]["setup"].format(pin=pin, state=state)
        pin = ''

    elif match.group(9):  # 'wt' (Wait)
        milliseconds = match.group(10)
        loop_code += add_indent(convention['wt']['loop'].format(milliseconds=milliseconds), indentation_level) + "\n"
        const_code += convention["wt"]["const"]

    elif match.group(1):  # 'fr' (For loop)
        range_value = match.group(2)
        loop_variable_counter += 1
        var_name = f"i{loop_variable_counter}"  # Unique variable for each loop
        loop_code += add_indent(convention['fr']['loop'].format(var=var_name, range=range_value), indentation_level) + "\n"
        indentation_level += 1  # Increase indentation for loop body
        const_code += convention["fr"]["const"]

    elif match.group(13):  # 's' (Start block)
        loop_code += add_indent(convention['s'], indentation_level) + "\n"
        indentation_level += 1  # Increase indentation for block

    elif match.group(14):  # 'e' (End block)
        indentation_level -= 1  # Decrease indentation for end of block
        loop_code += add_indent(convention['e'], indentation_level) + "\n"
    
    elif match.group(15):  # 'mtr' (Servo Motor)
        pin = match.group(16)
        print(match.group(15))
        print(match.group(16))
        print(match.group(17))
        if ((pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['buzzer'])):
            raise ValueError(f"Pin {pin} cannot be used for a servo, it is already assigned to another component.")
        deg = match.group(17)
        if (f"Servo myServo{pin};" not in const_code):
            const_code += f"Servo myServo{pin};" + '\n'
        setup_code += f"myServo{pin}.attach({pin});" + '\n'
        loop_code += f"myServo.write({deg});" + '\n'
    
    elif match.group(18):  # 'ifld' (Ultrasonic Sensor)
        pass

    elif match.group(20):  # 'bzh' (Buzzer)
        pin = match.group(21)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += f'pinMode({pin}, OUTPUT);'
        loop_code += f'digitalWrite({pin}, HIGH);'
    
    elif match.group(22):  # 'bzl' (Buzzer)
        pin = match.group(23)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += f'pinMode({pin}, OUTPUT);'
        loop_code += f'digitalWrite({pin}, LOW);'
    
    elif match.group(24):  # 'bzTone' (Buzzer Tone)
        pin = match.group(25)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += ''
        loop_code += f'tone({pin}, 440);'
    
    elif match.group(26):  # 'bzTone' (Buzzer Tone)
        pin = match.group(27)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += ''
        loop_code += f'tone({pin}, 493);'

    elif match.group(28):  # 'bzTone' (Buzzer Tone)
        pin = match.group(29)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += ''
        loop_code += f'tone({pin}, 261);'

    elif match.group(30):  # 'bzTone' (Buzzer Tone)
        pin = match.group(31)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += ''
        loop_code += f'tone({pin}, 294);'
    
    elif match.group(32):  # 'bzTone' (Buzzer Tone)
        pin = match.group(33)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += ''
        loop_code += f'tone({pin}, 329);'

    elif match.group(34):  # 'bzTone' (Buzzer Tone)
        pin = match.group(35)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += ''
        loop_code += f'tone({pin}, 349);'
    
    elif match.group(36):  # 'bzTone' (Buzzer Tone)
        pin = match.group(37)
        if (pin in used_pins['buttons']) or (pin in used_pins['bulbs']) or (pin in used_pins['servo']):
            raise ValueError(f"Pin {pin} cannot be used for a Buzzer, it is already assigned to another component.")
        const_code += ''
        setup_code += ''
        loop_code += f'tone({pin}, 392);'

    




# Generate final Arduino code
generated_code = f"""
{const_code}
void setup() {{
{setup_code}
}}

void loop() {{
{loop_code}
}}
"""

print(generated_code)

# file = open(r"C:\Users\User\OneDrive\Downloads\Arduino\libraries\Servo\examples\Sweep\Sweep.ino", "w")
# file.write(generated_code)
# file.flush()
# file.close()


# def fetch_arduino_code(filename):
#     if not os.path.isfile(filename):
#         print(f"Error: File '{filename}' does not exist.")
#         return None
#     with open(filename, 'r') as f:
#         code = f.read()
#     print(f"Arduino code read from {filename}")
#     return code

# # def upload_arduino_code(filename, port, board_type):
# #     try:
# #         os.system(r"arduino-cli upload -p COM4 --fqbn arduino:avr:uno C:\Users\prohi\Downloads\test\test.ino")  C:\Users\prohi\Downloads\arduino-cli_1.0.4_Windows_64bit\
# #     except:
# #         print(f"Error during compilation or upload:")

# def upload_arduino_code(file_path, board, port):
#     try:
#         # Compile the Arduino code
#         # os.system("ch")
#         subprocess.run(['arduino-cli.exe', 'compile', '--fqbn', board, file_path], check=True)
#         print("compilation done")
        
#         # Upload the Arduino code to the specified port
#         subprocess.run(['arduino-cli.exe', 'upload', '-p', port, '--fqbn', board, file_path], check=True)

#         print("Upload successful!")
#     except subprocess.CalledProcessError as e:
#         print("An error occurred:", e)


# filename = r"C:\Program Files\WindowsApps\ArduinoLLC.ArduinoIDE_1.8.57.0_x86__mdqgnx93n4wtt\libraries\Servo\examples\Sweep\Sweep.ino"
# board_type = "arduino:avr:uno"
# port = "COM4"
# upload_arduino_code(filename, board_type, port)
# # arduino_code = fetch_arduino_code(filename)
# # if arduino_code:
# #     upload_arduino_code(filename, board_type, port)
# # else:
# #     print("Skipping upload as Arduino code could not be fetched.")




try:
    # Compile the Arduino sketch
    os.system(r'arduino-cli compile --fqbn arduino:avr:uno C:\Users\User\Documents\Arduino\Blink')
    print("Done compilation")
    
    # Upload the compiled sketch to the Arduino board
    os.system(r'arduino-cli upload -p COM3 --fqbn arduino:avr:uno C:\Users\User\Documents\Arduino\Blink')
    print("Done uploading")
    
except Exception as e:
    print(f"Uploading stopped due to an error: {e}")
