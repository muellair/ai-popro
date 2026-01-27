
## Bullet points 

- changing 'code' folder to 'src' due to name-overlapping with the python module. Otherwise, a workaround for all imports from inside our 'code' folder would be necessary
### Scraping

- ran into HTTP error 429 on destatis website, occurred across devices in browser too, with VPN

 ### training
 - Für optimierung des Modells müsste eine Zeitreihe von 3 Jahren über alle 16 Bundesländer gleichzeitig als input gegeben werde. Aktuell weiß das modell nicht um welches Bundesland es sich handelt, die Populationen entwickeln sich aber unterschiedlich und es lernt so nur den 'mittelwert' der verteilungen aller Bundesländer.
 

### Issues i had
- Genesis website sometime down (in browser and from different devices/networks, too)
- docker-compose: evaluate.py needs train_nn.py
- warning for docker compose: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
- tensorflow "error" which actuall isnt problematic
- codebase_aipopro image: compressed size: 1GB: took long to push
    - busybox does not offer enough functionality for easy usage of python 
