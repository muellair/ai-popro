
## Bullet points 

- changing 'code' folder to 'src' due to name-overlapping with the python module. Otherwise, a workaround for all imports from inside our 'code' folder would be necessary
### Scraping

- ran into HTTP error 429 on destatis website, occurred across devices in browser too, with VPN


### Issues i had
- Genesis website sometime down (in browser and from different devices/networks, too)
- docker-compose: evaluate.py needs train_nn.py
- warning for docker compose: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
- tensorflow "error" which actuall isnt problematic
- codebase_aipopro image: compressed size: 1GB: took long to push
    - busybox does not offer enough functionality for easy usage of python 
