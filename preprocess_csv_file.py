import sys

skipped = 0

with open(sys.argv[1], 'rb') as input:
    with open(f'preprocessed_{sys.argv[1]}', 'wb') as output:
        buf = input.read(1)

        while buf:
            if buf[0] == 0x1e:
                output.write(b' ')
            if buf[0] == 0x19 or buf[0] == 0x17:
                skipped += 1
            else:
                output.write(buf)
            buf = input.read(1)

print(f'{skipped} characters skipped')
