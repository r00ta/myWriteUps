# Johannes' coffee cup

Requirements: 

- `python3`
- `pip`
- other system packages listed here http://docs.pwntools.com/en/latest/install.html

## Reverse 

The application register an handler for the signals from `1` to `64`: the handler xors the user's input with the signal code depending with an offset controlled by a global variable. 

![Screenshot from 2022-10-28 19-17-24](https://user-images.githubusercontent.com/18282531/198697418-186c296a-5334-45b4-bb9a-8dddc9ca8a78.png)


The application reads the signal to be raised and updates the global offset at every loop. After `2653*46` loops, the application `memcmp` the xored user's input with a fixed string stored in the memory. 

![Screenshot from 2022-10-28 19-23-22](https://user-images.githubusercontent.com/18282531/198697425-3ea46937-ec93-4c58-8b85-c269be0ebc97.png)

## Solution 

```
pip install --upgrade pwntools
```

Here's the static solution 

```python
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
```

Run it!

```bash
python crack.py
```

Finally

```bash
Extracting flag..
Extracting the position and the signals..
Calculate the flag..
Here it is!
RH_CTF{Th1s_i5_4_V3rY_w311_hIdd3N_s3cr37_info}
```
