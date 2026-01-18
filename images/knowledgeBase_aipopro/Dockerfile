FROM busybox

RUN mkdir -p /knowledgeBase

COPY learningBase/currentAiSolution.keras /knowledgeBase/
COPY learningBase/currentOlsSolution.pkl /knowledgeBase/
COPY images/knowledgeBase_aipopro/Readme.md /knowledgeBase/

CMD ["sh", "-c", "mkdir -p /tmp && cp -r /knowledgeBase /tmp/"]
# CMD ["sh"]
