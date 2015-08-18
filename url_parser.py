data = raw_input("Input>")

code = {'40' : '@'}

def url_parser(data):
    data = data.split("%")
    print data
    output = []
    output.append(data.pop(0))
    for elem in data:
        if elem[:2] in code:
            print elem[:2]
            elem = code[elem[:2]] + elem[2:]
        output.append(elem)
    return "".join(output)

print url_parser(data)
