import subprocess
import time

# Run the main.py script as a subprocess
process = subprocess.Popen(['python', 'main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Define a list of input values to send to the subprocess
items = ['a', 'Fracture Case', 'Snakebite case', 'dreams and nightmares', 'FAZE holo 2022 antwerp', 'G2 holo 2022 antwerp', 'ak47 anubis Field tested', 'driver gloves overtake battle scarred', 'huntsman tiger tooth facory new', 'q', 'q']
time.sleep(3)

# Loop through the input values and send them to the subprocess
for item in items:
    # Encode the input value as bytes and send it to the subprocess
    process.stdin.write(item.encode())
    # Send a newline character to simulate pressing the Enter key
    process.stdin.write(b'\n')
    # Wait for the subprocess to respond and capture its output
    output = process.stdout.readline().decode().strip()
    # Print the output to the console
    print(output)

# Close the subprocess
process.stdin.close()
process.stdout.close()
process.wait()