import sys
from time import sleep
from pypresence import Presence

# if argument --help or -h is passed, print help
if len(sys.argv) > 1:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("""---------------------------- Discord RPC ----------------------------
Você pode especificar as configurações no arquivo config.txt, ou passá-las como argumentos.
python3 discord-rpc.py [arguments]
ARGUMENTS:
-id --clientId <clientId>      id da aplicação (obrigatório)
-t1 --text1 <text>             texto que aparecerá no primeiro campo
-t2 --text2 <text>             texto que aparecerá no segundo campo
-li --large-image <imageKey>   nome da imagem maior
-lt --large-text <imageText>   texto que aparecerá quando o mouse estiver sobre a imagem maior
-si --small-image <imageKey>   nome da imagem menor
-st --small-text <imageText>   texto que aparecerá quando o mouse estiver sobre a imagem menor
-s --start <startTimestamp>    timestamp de início
-e --end <endTimestamp>        timestamp final
-b1 --button1URL <buttonURL>   URL do botão 1
-bt1 --buttonText <buttonText> texto do botão 1
-b2 --button2URL <buttonURL>   URL do botão 2
-bt2 --buttonText <buttonText> texto do botão 2
"""
        )
        sys.exit()

clientId = ""
text1 = ""
text2 = ""
largeImageKey = ""
largeImageText = ""
smallImageKey = ""
smallImageText = ""
startTimestamp = ""
endTimestamp = ""
button1URL = ""
button1Text = ""
button2URL = ""
button2Text = ""

# read the properties from the config.txt file. if the file doesn't exist, create it
try:
    with open("config.txt", "r") as f:
        for line in f:

            if line.startswith("clientId"):
                clientId = line.split("=")[1].strip()

            elif line.startswith("text1"):
                text1 = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("text2"):
                text2 = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("largeImageKey"):
                largeImageKey = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("largeImageText"):
                largeImageText = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("smallImageKey"):
                smallImageKey = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("smallImageText"):
                smallImageText = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("startTimestamp"):
                startTimestamp = line.split("=")[1].strip()

            elif line.startswith("endTimestamp"):
                endTimestamp = line.split("=")[1].strip()

            elif line.startswith("button1URL"):
                button1URL = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("button1Text"):
                button1Text = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("button2URL"):
                button2URL = "=".join(line.split("=")[1:]).strip()

            elif line.startswith("button2Text"):
                button2Text = "=".join(line.split("=")[1:]).strip()

except FileNotFoundError:
    # only create the file if there are no arguments
    if len(sys.argv) == 1:
        with open("config.txt", "w") as f:
            f.write(
                """clientId=
text1=
text2=
largeImageKey=
largeImageText=
smallImageKey=
smallImageText=
startTimestamp=
endTimestamp=
button1URL=
button1Text=
button2URL=
button2Text=
"""
            )
        print("Arquivo de configuração criado com sucesso! Preencha-o e execute novamente.")
        input()
        exit()

# read the properties from the arguments, overriding the config.txt file
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):

        if sys.argv[i] == "-id" or sys.argv[i] == "--clientId":
            clientId = sys.argv[i + 1]

        elif sys.argv[i] == "-t1" or sys.argv[i] == "--text1":
            text1 = " ".join(sys.argv[i + 1 :]).split("-")[0].strip()

        elif sys.argv[i] == "-t2" or sys.argv[i] == "--text2":
            text2 = " ".join(sys.argv[i + 1 :]).split("-")[0].strip()

        elif sys.argv[i] == "-li" or sys.argv[i] == "--large-image":
            largeImageKey = sys.argv[i + 1]

        elif sys.argv[i] == "-lt" or sys.argv[i] == "--large-text":
            largeImageText = " ".join(sys.argv[i + 1 :]).split("-")[0].strip()

        elif sys.argv[i] == "-si" or sys.argv[i] == "--small-image":
            smallImageKey = sys.argv[i + 1]

        elif sys.argv[i] == "-st" or sys.argv[i] == "--small-text":
            smallImageText = " ".join(sys.argv[i + 1 :]).split("-")[0].strip()

        elif sys.argv[i] == "-s" or sys.argv[i] == "--start":
            startTimestamp = sys.argv[i + 1]

        elif sys.argv[i] == "-e" or sys.argv[i] == "--end":
            endTimestamp = sys.argv[i + 1]

        elif sys.argv[i] == "-b1" or sys.argv[i] == "--button1URL":
            button1URL = sys.argv[i + 1]

        elif sys.argv[i] == "-bt1" or sys.argv[i] == "--button1Text":
            button1Text = " ".join(sys.argv[i + 1 :]).split("-")[0].strip()

        elif sys.argv[i] == "-b2" or sys.argv[i] == "--button2URL":
            button2URL = sys.argv[i + 1]

        elif sys.argv[i] == "-bt2" or sys.argv[i] == "--button2Text":
            button2Text = " ".join(sys.argv[i + 1 :]).split("-")[0].strip()

# if the clientId is not set, exit the program
if clientId == "":
    print("é necessário definir o ID de uma aplicação no arquivo config.txt ou informar com -id <clientId>")
    input()
    exit()

RPC = Presence(clientId)
RPC.connect()

buttonsArray = []

if button1URL != "" and button1Text != "":
    buttonsArray.append({"label": button1Text, "url": button1URL})

if button2URL != "":
    buttonsArray.append({"label": button2Text, "url": button2URL})

def updatePresence():
    RPC.update(
        details=text1 if text1 != "" else None,
        state=text2 if text2 != "" else None,
        large_image=largeImageKey if largeImageKey != "" else None,
        large_text=largeImageText if largeImageText != "" else None,
        small_image=smallImageKey if smallImageKey != "" else None,
        small_text=smallImageText if smallImageText != "" else None,
        start=int(startTimestamp) if startTimestamp != "" else None,
        end=int(endTimestamp) if endTimestamp != "" else None,
        buttons=buttonsArray if len(buttonsArray) > 0 else None,
    )

updatePresence()

print("Status do discord atualizado!")
print("Para manter o status ativo, mantenha o programa aberto")

while True:
    try:
        sleep(30)
        updatePresence()
    except KeyboardInterrupt:
        print("Saindo...")
        exit()