import sys
from time import sleep
from pypresence import Presence

# if argument --help or -h is passed, print help
if len(sys.argv) > 1:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(
            """---------------------------- Discord RPC ----------------------------
Você pode especificar as configurações no arquivo config.txt, ou passá-las como argumentos.
python3 discord-rpc.py [arguments]
ARGUMENTS:
-id --clientId <clientId>     id da aplicação (obrigatório)
-t1 --text1 <text>            texto que aparecerá no primeiro campo
-t2 --text2 <text>            texto que aparecerá no segundo campo
-li --large-image <imageKey>  nome da imagem maior
-lt --large-text <imageText>  texto que aparecerá quando o mouse estiver sobre a imagem maior
-si --small-image <imageKey>  nome da imagem menor
-st --small-text <imageText>  texto que aparecerá quando o mouse estiver sobre a imagem menor
-s --start <startTimestamp>   timestamp de início
-e --end <endTimestamp>       timestamp final
-url --buttonURL <buttonURL>  URL do botão
-bt --buttonText <buttonText> texto do botão"""
        )
        sys.exit()

# if there not a config.txt file, create one then write the default values
try:
    open("config.txt")
except:
    file = open("config.txt", "w")
    file.write(
        """clientId=
text1=
text2=
largeImageKey=
largeImageText=
smallImageKey=
smallImageText=
startTimestamp=
endTimestamp=
buttonURL=
buttonText="""
    )
    file.close()
    print("Arquivo config.txt criado\nPor favor, preencha as informações e reinicie o programa")
    input()
    exit()

clientId = ""
text1 = ""
text2 = ""
largeImageKey = ""
largeImageText = ""
smallImageKey = ""
smallImageText = ""
startTimestamp = ""
endTimestamp = ""
buttonURL = ""
buttonText = ""

# read the properties from the config.txt file
with open("config.txt", "r") as f:
    for line in f:
        if line.startswith("clientId"):
            clientId = line.split("=")[1].strip()
        elif line.startswith("text1"):
            text1 = line.split("=")[1].strip()
        elif line.startswith("text2"):
            text2 = line.split("=")[1].strip()
        elif line.startswith("largeImageKey"):
            largeImageKey = line.split("=")[1].strip()
        elif line.startswith("largeImageText"):
            largeImageText = line.split("=")[1].strip()
        elif line.startswith("smallImageKey"):
            smallImageKey = line.split("=")[1].strip()
        elif line.startswith("smallImageText"):
            smallImageText = line.split("=")[1].strip()
        elif line.startswith("startTimestamp"):
            startTimestamp = line.split("=")[1].strip()
        elif line.startswith("endTimestamp"):
            endTimestamp = line.split("=")[1].strip()
        elif line.startswith("buttonURL"):
            buttonURL = line.split("=")[1].strip()
        elif line.startswith("buttonText"):
            buttonText = line.split("=")[1].strip()

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
        elif sys.argv[i] == "-url" or sys.argv[i] == "--buttonURL":
            buttonURL = sys.argv[i + 1]
        elif sys.argv[i] == "-bt" or sys.argv[i] == "--buttonText":
            buttonText = " ".join(sys.argv[i + 1 :]).split("-")[0].strip()

# if the clientId is not set, exit the program
if clientId == "":
    print("é necessário definir o ID de uma aplicação no arquivo config.txt ou informar com -id <clientId>")
    input()
    exit()

RPC = Presence(clientId)
RPC.connect()

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
        buttons=[{"label": buttonText, "url": buttonURL}]
        if buttonText != "" and buttonURL != ""
        else None,
    )

updatePresence()

print("Status do discord atualizado!")
print("Para manter o status ativo, mantenha o programa aberto")

while True:
    sleep(30)
    updatePresence()