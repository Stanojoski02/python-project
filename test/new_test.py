#There is no finished just an idea
with open("emails.txt","r")as d:
    data = d.readlines()
    a = 0
    old_text = ""
    for i in data:
        a=0
        text = ""
        if "From:" in i or "Von:" in i:
            print(i.strip().replace("   ",""))
        if "An:" in i or "To:" in i:
            print(i.strip().replace("  ",""))
        for j in data:
            if "An:" in j or "To:" in j:
                a+=1
            if a<2:
                text += f"{j}"
        a+=1
        print("______________________")
        print(text.replace(old_text,""))
        old_text = text

    print("______________________")
    print(text)

