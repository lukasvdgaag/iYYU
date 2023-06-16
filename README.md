# 1 - Benodigdheden  

Om de chatbot te kunnen installeren en gebruiken, moet je voldoen aan de volgende eisen: 

- **Systeemvereisten**  
  - Besturingssysteem: Windows 10+, macOS of Linux
  - Minimaal 4 GB RAM-geheugen
  - Voldoende opslagruimte voor het project en eventuele gegevens
- **Python-installatie**
  - Python 3.10 of hoger geïnstalleerd op je systeem
  - Je kunt Python downloaden op de [Officiële Python-website](https://www.python.org/downloads/)
- **Externe libraries en afhankelijkheden**  
  - Pandas
  - Jupyther
  - Torch
  - Gradio
  - Toktoken
  - Openai
  - Dotenv

Dit project heeft mogelijk extra afhankelijkheden, afhankelijk van de specifieke implementatie. Zorg ervoor dat je aan alle benodigdheden voldoet voordat je verdergaat met de installatie en het verdere gebruik van de chatbot.  
 
We raden aan om gebruik te maken van Visual Studio Code, aangezien dit een integratie heeft met jupyter notebooks. Dit maakt het gemakkelijker om code te schrijven, lezen of uit te voeren. De rest van deze handleiding zal op basis zijn van VSCode.  

# 2 - Clonen van het project en OpenAI Key  

**Clonen van het project**
Om het chatbot-project te gebruiken, moet je eerst het project klonen naar je lokale device. Voer de volgende stappen uit in VSCode om het project te clonen. 
1. Open VSCode op je computer.
2. Ga naar de github repository van het project in je browser.
3. Klik op “Code” op de repositorypagina en kopieer de HTTPS- of SSH-URL van het project.
4. Open VScode op je machine.
5. Ga naar het menu "View" bovenaan het scherm en selecteer "Command Palette" of gebruik de sneltoets Ctrl + Shift + P (Windows/Linux) of Cmd + Shift + P (Mac).
6. Typ "Git: Clone" in de zoekbalk van het Command Palette en selecteer de optie "Git: Clone" wanneer deze verschijnt. Druk op Enter.
7. In het pop-upvenster "Clone Repository" plak je de gekopieerde URL van het GitHub-project in het invoerveld "Repository URL".
8. Kies een lokale map op je machine waarin je het project wilt opslaan door op "Browse" te klikken naast het invoerveld "Clone Repository".
9. Klik op de knop "Clone" om het kloonproces te starten.  

VSCode zal nu het project klonen en opslaan in een lokale map. Op dit moment is het mogelijk om gebruik te maken van het project. 

**OpenAI key**

Om gebruik te maken van de functionaliteit van ChatGPT, is het nodig op een API-key te verkrijgen van OpenAI. Voor het veilig opslaan van deze API-key, maken we gebruik van dotenv. 

Voer deze stappen uit om dotenv te gebruiken

1. Ga naar de OpenAI-website en registreer je voor een API-key als je dat nog niet hebt. 
2. Maak in de hoofdmap van het gekloonde project een nieuw bestand aan met de naam `.env` (let op de punt voor de bestandsnaam)
3. Open het `.env` bestand en voeg hier de volgende regel aan toe aan het bestand: 
`OPENAI_API_KEY=JOUW_API_KEY`
Vervang “JOUW_API_KEY” door de API-key die je hebt ontvangen van OpenAI. 
4. Sla het `.env` bestand op

Nu wordt de API-key veilig opgeslagen in het `.env` bestand en kan deze worden opgevraagd door de code in het project.

Let op: Zorg ervoor dat je het .env-bestand niet deelt of uploadt naar een openbare repository, omdat dit gevoelige informatie bevat.  

# 2 - Belangrijke bestanden

De chatbot bevat verschillende bestanden en mappen die een belangrijke rol spelen bij het functioneren van de chatbot. Hieronder vind je een overzicht van de belangrijkste bestanden en hun functies: 



* `main.ipynb`: Dit bestand bevat de hoofdcode van de chatbot. In dit bestand komt alle code uit de rest van de bestanden samen. 
* `gpt.py`: In dit bestand zit alle logica voor het gebruik van ChatGPT. Het bevat de integratie van ChatGPT-API, definieert functies voor het genereren van reacties en verwerkt de communicatie met de ChatGPT-service. 
* `intent_model.py`: In dit bestand zit de logica voor het intent model. Het bevat een functie waarin het model getraind kan worden, en een functie waar de intent kan worden berekend aan de hand van de vraag van de gebruiker. Ook zit hier een functie in om het model mee te evalueren. 
* `settings.py`: Dit bestand bevat alle logica wat betreft gebruikersinstellingen. Hierin wordt alle logica afgehandelt voor het wijzigen van gebruikersgegevens en het voorspellen van het privacy level van de gebruiker aan de hand van een paar opgestelde vragen.
* `ner.py`: Dit bestand bevat alle informatie van het Named Entity Recognition model. Dit wordt gebruikt voor om het type instelling en de nieuwe waarde af te leiden uit de vraag van de gebruiker. 
* `/trained_models` In deze folder worden alle getrainde modellen opgeslagen. Deze folder is opgedeeld in drie sub-folders die voor de getrainde modellen zijn. 
* `/training_data` Deze folder bevat de data voor het trainen van de models. In deze folder zitten drie andere folders die voor een specifiek model gelden. 


# 3 - Gebruik van de data

Deze chatbot wordt geleverd met demo-data die gebruikt kan worden om de functionaliteiten van de chatbot te verkennen. De demo-gegevens zijn te vinden in de `/training-data` folder. Deze folder is opgedeeld in drie bestanden voor de drie verschillende modellen. 



* `gpt` In deze folder staan twee bestanden genaamd `legal.txt` en `privacy.txt. Dit moeten de privacy- en legalstatements van iYYU voorstellen. 
* `intents` In deze folder staat het `intent_recognition.json` bestand. Deze bestaat uit een array van json objecten met daarin de train vragen, intent naam, categorie, responses, test vragen etc. Verdere uitleg hierover is te vinden in het hoofdstuk “Architectuur”. 
* `ner` In deze folder staat een bestand genaamd `ner_data.json`. In dit bestand staat de data om het NER Keyword Recognition model mee te trainen. Verdere uitleg over de data staat in het hoofdstuk “Architectuur” 

Nogmaals zijn de demogegevens bedoeld voor demonstratie- en testdoeleinden. Als je jouw eigen dataset wilt gebruiken, kun je de bovenstaande bestanden vervangen met je eigen dataset. Zorg ervoor dat je het formaat van de bestanden behoudt.

Het gebruik van aangapaste datasets biedt de mogelijkheid om de chatbot aan te passen aan specifieke scenarios of vereisten. Zorg ervoor dat de dataset zo groot en correct mogelijk is. Dit zorgt voor een beter presterend model. 


# 4 - Runnen van het project

Om de chatbot te kunnen runnen, voer je de onderstaande stappen uit: 



1. Open het bestand `main.ipynb` in Visual Studio Code. 
2. Zorg dat je de benodigde Python libraries hebt gedownload. Zie “Benodigdheden”. 
3. Voer de codecellen in het `main.ipynb` bestand uit van boven naar beneden. Dit omvat ook het importeren van de vereiste libraries, trainen van modellen en het instellen van de chatbot visuals. 
4. Het trainen van de modellen wordt automatisch uitgevoerd wanneer je de code uitvoert. Dit proces kan enige tijd in beslag nemen, afhankelijk van de grootte van de trainingsdata. 
5. Na het trainen van de modellen, wordt de chatbot automatisch gestart in de laatste codecel. De chatbot maakt gebruik van de visuele weergave van Gradio App.
6. In de Gradio App is het nu mogelijk om de chatbot vragen te stellen. 

Als je geen gebruik wilt maken van de visuele weergave van Gradio, voer dan de bovenstaande stappen 1-4 uit. Vervolgens is het mogelijk om gebruik te maken van de volgende functies voor het berekenen van de intents en antwoorden: 

`intent, confidence = intentmodel.get_intent(user_question)` Deze functie geef je de vraag van de gebruiker mee. De functie bepaalt de intent en geeft de intent en confidence score terug.

`response = gpt.answer_question(question=user_question)`. Deze functie genereert een antwoord op je vraag via ChatGPT aan de hand van de berekende context.


# 5 - Foutafhandelingen

Tijdens het gebruik van de chatbot kunnen er verschillende fouten of problemen optreden. Hieronder staan enkele veelvoorkomende foutmeldingen en mogelijke oplossingen:

**Foutmelding: "API-sleutel ontbreekt"**

Mogelijke oorzaak: De vereiste API-sleutel is niet correct geconfigureerd of ontbreekt.

Oplossing: Controleer of je de juiste API-sleutel hebt verstrekt en of deze correct is geconfigureerd in het configuratiebestand. Zorg ervoor dat je de API-sleutel op de juiste manier invoert, zonder extra spaties of typfouten.

**Foutmelding: "Verbinding mislukt"**

Mogelijke oorzaak: Er is een probleem met de internetverbinding of de server waarmee de chatbot communiceert.

Oplossing: Controleer je internetverbinding om ervoor te zorgen dat deze stabiel is. Als de fout zich blijft voordoen, kan er mogelijk een probleem zijn met de server. Probeer het later opnieuw of neem contact op met de technische ondersteuning voor verdere assistentie.
