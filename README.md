# iYYU Chatbot

## Handige links
- [Mattermost](https://iyyu-infra.cloud.mattermost.com/)
- [ZOOM meetings link](https://us05web.zoom.us/j/87397737329?pwd=ZC9pYjBwTXV1QXYrdndZTXVMa2FNdz09)

## Reden van het project

Dit project is opgezet om een chatbot te ontwikkelen voor iYYU, gericht op privacy gerelateerde vragen. De chatbot maakt gebruik van machine learning en intent recognition om gebruikers vragen over privacy statements, legal statements en privacy settings te beantwoorden.

## Doel van het project

Het doel van deze chatbot is om gebruikers van iYYU een gemakkelijke en snelle manier te bieden om antwoorden te krijgen op hun privacy gerelateerde vragen. Door gebruik te maken van machine learning en intent recognition, kan de chatbot snel en nauwkeurig antwoorden geven op vragen over privacy statements en legal statements, terwijl de vragen over privacy settings handmatig worden beantwoord door de vooraf opgestelde antwoorden.

## Aanpak 

Voor de ontwikkeling van deze chatbot hebben we gebruikgemaakt van Python. We hebben de bibliotheek nltk gebruikt voor intent recognition en het ChatGPT-3 model voor het beantwoorden van vragen over privacy statements en legal statements.

De vragen van gebruikers zijn verdeeld in drie groepen: privacy statements, legal statements en privacy settings. Vragen over privacy statements en legal statements worden geanalyseerd en vervolgens doorgestuurd naar het ChatGPT model om te worden beantwoord. Vragen over privacy settings worden handmatig beantwoord door middel van vooraf opgestelde antwoorden.

Om de chatbot te trainen, hebben we gebruik gemaakt van een dataset van privacy gerelateerde vragen en antwoorden. We hebben deze dataset gebruikt de intent recognition te trainen. Het ChatGPT-3 model is een pre-trained language model waardoor wij zelf geen data nodig hebben. Dit omdat dit voor ons de beste optie was, aangezien wij op kleine schaal niet een beter model kunnen maken.

Een probleem waar we tijdens het project tegenaan liepen is de hoeveelheid data. Om een model goed te trainen, heb je veel data nodig. We hebben wel een beetje data van de privacy statements van iYYU zelf, maar dit is niet genoeg om een chatbot te bouwen die aan onze eisen voldoet. We hebben vervolgens gekeken naar verschillende manieren om ons trainingsdata te verrijken, maar vonden het lastig om voldoende data te vinden die relevant was voor onze specifieke situatie. Uiteindelijk hebben we besloten om gebruik te maken van een model zoals ChatGPT om zelf data te genereren die we konden gebruiken om onze chatbot te trainen

## Old flowchart
![Flowchart v1](https://github.com/lukasvdgaag/iYYU/assets/22807647/fe3541d3-db57-4e2c-ad3b-a02942659819)
[Klik hier voor de link naar deze flowchart](https://lucid.app/lucidchart/2d995a9f-6e3d-465e-9da7-dba8b7ee99fb/edit?viewport_loc=-1460%2C1146%2C3343%2C1773%2C0_0&invitationId=inv_a6d11154-4962-4771-8de0-915ad78b4006)

## New flowchart
![Flowchart v2](https://github.com/lukasvdgaag/iYYU/assets/83826673/ae2cf532-9b0f-428f-aa44-a11567e50550)
[Klik hier voor de link naar deze flowchart](https://lucid.app/lucidchart/2d995a9f-6e3d-465e-9da7-dba8b7ee99fb/edit?viewport_loc=-1460%2C1146%2C3343%2C1773%2C0_0&invitationId=inv_a6d11154-4962-4771-8de0-915ad78b4006)

