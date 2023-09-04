
def parse_srec_line(line):
    record_type = line[0:2]
    data_length = int(line[2:4], 16)
    address = line[4:8]
    data = bytearray(line[8:-2])
    checksum = line[-2:]

    return {
        "record_type": record_type,
        "data_length": data_length,
        "address": address,
        "data": data,
        "checksum": checksum
    }


with open(r'Arquivos WPS\rl_application.mot', 'rb') as srec:
    records = []
    within_range = False

    for line in srec:
        line = line.strip()
        record = parse_srec_line(line)
        records.append(record)

print(records)
