from pwnlib.elf.elf import ELF


elf = ELF('johannes_coffe')

# Extract the flag stored in the data of the elf
print("Extracting flag..")
flag = []
for i in range(46):
    flag.append(int.from_bytes(elf.read(0x4f2680 + i, 1), 'big'))

print("Extracting the position and the signals..")
# Extract all the signals and the position to xor
positions = []
signals = []
for i in range(2653 * 46):
    signals.append(int.from_bytes(elf.read(0x4f266c - i*8, 1), 'big'))
    positions.append(int.from_bytes(elf.read(0x4f2668 - i*8, 1), 'big'))

print("Calculate the flag..")
# Calculate the flag
for i in range(len(positions)):
    if positions[i] < len(flag):
        flag[positions[i]] ^= signals[i]

print("Here it is!")
print(''.join(map(lambda x: chr(x), flag)))

