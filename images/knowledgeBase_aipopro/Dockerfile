FROM busybox

# Create target directory
RUN mkdir -p /knowledgeBase

# Copy models
COPY learningBase/currentAiSolution.keras /knowledgeBase/
COPY learningBase/currentOlsSolution.pkl /knowledgeBase/

# Copy README
COPY README.md /knowledgeBase/

CMD [sh]

