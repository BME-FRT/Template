import os
import sys
from datetime import datetime

lang = sys.argv[1]

languages = ["US", "HUN"]

if not languages.__contains__(lang):
    raise(ValueError)

dt_format1 = '%Y.%m.%d.%H:%M:%S'
dt_format2 = '%m.%d.%Y %I:%M:%S %p'
dt_format3 = '%d.%m.%Y %H:%M:%S'
dt_format4 = '%y.%m.%d %H:%M:%S'

dir = os.getcwd()
files = os.listdir(dir)
txts = []
for f in files:
    if f.endswith(".txt"):
        txts.append(f)
        reader = open(f'{dir}/{f}', 'r')
        writer = open(f'{dir}/{f}.rewrite', 'w')
        for line in reader:
            if line.startswith("frmTimeStamp"):
                line = line.replace("\"", "").replace(". ", ".").replace("frmTimeStamp=", "").replace("\n", "").replace("/", ".").replace("-", ".")
                try:
                    dt = datetime.strptime(line, dt_format1)
                except ValueError as v:
                    try:
                        dt = datetime.strptime(line, dt_format2)
                    except ValueError as v:
                        try:
                            dt = datetime.strptime(line, dt_format3)
                        except ValueError as v:
                            try:
                                dt = datetime.strptime(line, dt_format4)
                            except ValueError as v:
                                raise (ValueError)
                if lang == "US":
                    writer.write(dt.strftime('frmTimeStamp=%m/%d/%Y %I:%M:%S %p\n'))
                elif lang == "HUN":
                    writer.write(dt.strftime('frmTimeStamp=%Y. %m. %d. %H:%M:%S\n'))
            else:
                writer.write(line)
        reader.close()
        writer.close()
        os.remove(f'{dir}/{f}')
        os.rename(f'{dir}/{f}.rewrite', f'{dir}/{f}')