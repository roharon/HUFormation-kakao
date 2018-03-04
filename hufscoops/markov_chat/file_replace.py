import settings

def make_json():

    f = open(settings.beforeParse,"r")
    lines=f.readlines()
    f.close()
    file=open(settings.Parsed,"w")
    total = ""
    for line in lines:

        if (':' not in line) or ('http:/' or 'www') in line:
            continue
        elif ("님이 들어왔습니다." or "님이 나갔습니다.") in line:
            continue

        line = line[line.find(' : ')+2:-1]
        line+='\n'
        file.write(line)
        print(line)
    file.close()

