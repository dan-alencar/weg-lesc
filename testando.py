
# Original S-record lines in bytes format
line1 = b'S1130070000000000000000000000000000000007C'
line2 = 'S10700C0EFFFF8044E'

print(line2)

if len(line2) < 32:
    for i in range(32-len(line2)):
        line2 = line2+'F'

print(line2)
print(len(line2))
