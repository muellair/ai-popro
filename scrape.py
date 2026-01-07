import pathlib
import requests
import json
import zipfile
import io

url = "https://www-genesis.destatis.de/genesisGONLINE/api/rest/tables/12411-0010/download/csv/de"

payload = {"variableBlocks":{"v1":{"mainAttributes":[{"attribute":"1990-12-31","isDocumentary":False},{"attribute":"1991-12-31","isDocumentary":False},{"attribute":"1992-12-31","isDocumentary":False},{"attribute":"1993-12-31","isDocumentary":False},{"attribute":"1994-12-31","isDocumentary":False},{"attribute":"1995-12-31","isDocumentary":False},{"attribute":"1996-12-31","isDocumentary":False},{"attribute":"1997-12-31","isDocumentary":False},{"attribute":"1998-12-31","isDocumentary":False},{"attribute":"1999-12-31","isDocumentary":False},{"attribute":"2000-12-31","isDocumentary":False},{"attribute":"2001-12-31","isDocumentary":False},{"attribute":"2002-12-31","isDocumentary":False},{"attribute":"2003-12-31","isDocumentary":False},{"attribute":"2004-12-31","isDocumentary":False},{"attribute":"2005-12-31","isDocumentary":False},{"attribute":"2006-12-31","isDocumentary":False},{"attribute":"2007-12-31","isDocumentary":False},{"attribute":"2008-12-31","isDocumentary":False},{"attribute":"2009-12-31","isDocumentary":False},{"attribute":"2010-12-31","isDocumentary":False},{"attribute":"2011-12-31","isDocumentary":False},{"attribute":"2012-12-31","isDocumentary":False},{"attribute":"2013-12-31","isDocumentary":False},{"attribute":"2014-12-31","isDocumentary":False},{"attribute":"2015-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2016-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2017-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2018-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2019-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2020-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2021-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2022-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2023-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"2024-12-31","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False}],"mainVariable":"STAG","showVariable":"LIKE_GENESIS","showVariableValue":["LABEL"],"labelOverwrite":{"de":"Stichtag","en":"Reference date","wiki":False},"idOverwrite":"STAG","sorting":{"direction":"ASC","sortBy":"NONE","sortLanguage":"NONE"},"lockSelection":False,"showAsInterline":False,"isHidden":False},"v2":{"mainAttributes":[{"attribute":"08","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"09","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"11","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"12","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"04","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"02","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"06","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"13","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"03","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"05","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"07","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"10","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"14","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"15","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"01","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False},{"attribute":"16","childVariable":None,"childAttributes":[],"isHidden":False,"isDocumentary":False}],"mainVariable":"DLAND","showVariable":"LIKE_GENESIS","showVariableValue":["LABEL"],"labelOverwrite":{"de":"Bundesländer","en":"Länder","wiki":False},"idOverwrite":"DLAND","sorting":{"direction":"ASC","sortBy":"LABEL","sortLanguage":"DE"},"lockSelection":False,"showAsInterline":False,"isHidden":False}},"contentBlocks":{"c1":{"content":"BEVSTD","functions":["QMU"],"possibleFunctions":[],"functionDecimalDigits":{"QMU":0},"labelOverwrite":{"de":"Bevölkerungsstand","en":"Population","wiki":False},"idOverwrite":552354,"lockSelection":True,"showAsInterline":False,"isHidden":False}},"statisticBlocks":{"s1":{"statisticCode":"12411","showAsInterline":False,"isHidden":False}},"tableStructure":{"filter":[{"blockCode":"s1","blockType":"STATISTIC","childBlocks":[{"blockCode":"c1","blockType":"CONTENT","childBlocks":[],"possibleBlocks":[]}],"possibleBlocks":[]}],"colTitle":[{"blockCode":"v1","blockType":"VARIABLE","childBlocks":[],"possibleBlocks":[]}],"rowTitle":[{"blockCode":"v2","blockType":"VARIABLE","childBlocks":[],"possibleBlocks":[]}]},"displayOption":{"showQualityInCells":True,"hideEmptyCols":False,"hideEmptyRows":False,"lockTranspose":False,"lockStructureModification":False,"fixFirstColumn":False}}

headers = {
    "Host": "www-genesis.destatis.de",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www-genesis.destatis.de/",
    "Content-Type": "application/json",
    # "Content-Length": "5494",
    "Origin": "https://www-genesis.destatis.de",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    zip_file_path = pathlib.Path("data/dataset.zip")
    zip_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(zip_file_path, "wb") as f:
        f.write(response.content)
    print(f"ZIP saved to {zip_file_path}")

    csv_directory_path = zip_file_path.parent / "raw"
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(csv_directory_path)
    print(f"CSV extracted to {csv_directory_path}")
else:
    print("Request failed:", response.status_code, response.text)
