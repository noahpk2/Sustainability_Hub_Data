<h1> Sustainability Hub - Containerized Databases </h1>



pre-requisites:
1. I'm using anaconda to manage my python environment- but you can use whatever you want.
2. cd to ./src , run setup.sh to install the necessary packages and tools
3. run start.py to set up and start the containerized databases




This repository serves two purposes: 
1. To test langchain retrieval on geospatial data gathered from the colorado geo portal 
2. To serve as a base for constructing training data for a clone of "GeoLM", a language model trained on geospatial data. 


notes:
- this won't work with the proprietary .gdb format, yet. Need to install the esri api into GDAL, which is only compatible with x86_64 architecture.
    - potential solution: another container containing the esri api, and a script to convert .gdb
