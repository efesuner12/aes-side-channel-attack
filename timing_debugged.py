import random
from random import randrange
import subprocess

# seed rng
random.seed(0)

# number of timing measurements
# you'll need about 3500 to recover the key
N = 3500

# These will hold timings and plaintexts after measurement
plaintexts = []
timings = []

print("Measuring...")

# Test value
for i in range(0, N):
    pt = random.getrandbits(128)
    pt_hex = "{0:0{1}x}".format(pt, 32)

    (stat, output) = subprocess.getstatusoutput("./aes " + pt_hex)

    if(stat != 0):
        print("aes failed! Make sure the file is in the same directory and executable (chmod +x)")
        exit()

    parts = output.split(", ")

    if len(parts) != 3:
        print("Did not get expected format!")
        exit()

    # parse out the timing
    timing = int(parts[2])

    # and store for current trace
    plaintexts.append(pt)
    timings.append(timing)

    if i % 10 == 0:
        print("Measurement " + str(i) + " = " + str(timing))

print("Done.")

print("Recovering key...")

# The AES SBox, you'll need it
sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

#### DO NOT CHANGE ANYTHING ABOVE THIS LINE ###
#### ADD YOUR SOLUTION BELOW THIS LINE ########
####
#### This script should only print the recovered key as hex

## Write the hexadecimal plaintexts and timings into a file for debugging
with open("debug.txt", "w") as f:
    for i in range(0, len(plaintexts)):
        pt_hex = "{0:0{1}x}".format(plaintexts[i], 32)
        f.write(f"{pt_hex} : {timings[i]}\n")

from datetime import datetime

start_time = datetime.now()

key = ""

# Loop to access the plaintexts byte-by-byte
# Byte zero of the plaintexts will give byte zero
## of the encryption key
for x in range(15, -1, -1):

    # Dictionary to store key candidate : score
    key_candidate_scores = {}

    # Run the loop for each key candidate k
    ## from 0 to 127 (0 to 0xFF)
    for k in range(0, 256):

        # Cration of the timing lists based on the MSbit of the SBOX result
        msbit_zero = []
        msbit_one = []

        # Each plaintext will be iterated byte-by-byte simultaneously
        ## for the calculation of the hypothetical SBOX result
        # For instance - each plaintext's byte 0 will be accessed 
        ## and below operations will be done for all k
        ## then it'll move on to byte 1 then to byte 2 ... then to byte 15
        for i in range(0, len(plaintexts)):
            
            # Get the byte of the plaintext
            pt_byte = (plaintexts[i] >> (x*8)) & 0xff
            pt_byte_hex = hex(pt_byte)
            print(f"\Byte {15-x} of plaintext {i} = {pt_byte} or {pt_byte_hex}")
            
            # Get the recorded runtime of the plaintext
            runtime = timings[i]
            print(f"Runtime of plaintext {i} = {runtime}")

            print(f"Key candidate = {k} or {hex(k)}")

            # XOR the plaintext byte and the key byte
            xor_result = pt_byte ^ k
            print(f"XOR result = {xor_result} or {hex(xor_result)}")

            # Perform the SBOX operation
            sbox_result = sbox[xor_result]
            print(f"SBOX result = {sbox_result} or {hex(sbox_result)}")

            # Get the MSbit of the SBOX result
            sbox_result_binary = format(sbox_result, '08b')
            print(f"SBOX result in binary = {sbox_result_binary}")

            sbox_result_byte = int(sbox_result_binary[0])
            print(f"Most significant bit of the SBOX result = {sbox_result_byte}")

            # Group the timing of the plaintext
            if sbox_result_byte == 1:
                msbit_one.append(runtime)
                print("Appended to msbit_one")
            elif sbox_result_byte == 0:
                msbit_zero.append(runtime)
                print("Appended to msbit_zero")

        # Calculate the average of the lists for each key candidate k
        msbit_zero_average = sum(msbit_zero) / len(msbit_zero)
        print(f"\nAverage of msbit_zero for key candidate {hex(k)} = {msbit_zero_average}")

        msbit_one_average = sum(msbit_one) / len(msbit_one)
        print(f"Average of msbit_one for key candidate {hex(k)} = {msbit_one_average}")

        # Substract the averages to get a single score for each key candidate k
        key_candidate_score = msbit_one_average - msbit_zero_average
        print(f"Score of key candidate {hex(k)} = {key_candidate_score}")

        # Add the key candidate and the associated score to the dic
        key_candidate_scores[hex(k)] = key_candidate_score

    print(f"\nSCORES = {key_candidate_scores}")

    # Find the key candidate with the highest score which will be 
    ## the key byte
    max_key = max(key_candidate_scores, key=key_candidate_scores.get)
    print(f"AES-128 key byte {15-x} = {max_key}")
    print(key_candidate_scores[max_key])
    key += max_key

    can_continue = input("Press any key to continue...")

print(key)

end_time = datetime.now()
print(f"Operation completed in {end_time - start_time}")
