from flask import Flask, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# Only using pins that are not used for other functionalities like SPI or I2C
usable_pins = [4,17,18,27,22,23,24,25,5,6,12,13,16,19,20,21]

GPIO.setmode(GPIO.BCM)
for pin in usable_pins:
    # Set pin to output
    GPIO.setup(pin, GPIO.OUT)
    # Default pin to 0
    GPIO.output(pin, False)

@app.route('/<hex_value>', methods=['GET'])
def set_bits(hex_value):
    try:
        # Read parameter and convert to int
        value = int(hex_value, 16)
    except ValueError:
        return jsonify({'error': 'Invalid hex value'}), 400

    # Check if length is correct
    if value < 0 or value > 0xFFFF:
        return jsonify({'error': 'Value must be a 16-bit hex (0000–FFFF)'}), 400

    # Set outputs
    for i in range(16):
        GPIO.output(usable_pins[i], bool((value >> i) & 1))

    # Send Response
    return jsonify({
        'message': f'Set GPIOs to {bin(value)}',
        'hex': f'{value:04X}',
        'dec': value
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
