#**INSTALLATION:**

PyGraphviz is very specific about its requirements and can be quite buggy. This currently works perfectly on Python=3.8.3. However, newer versions of Python cause issues with import-time library resolution. Additionally, the version of PyGraphviz that is supported by Google colab, has one well documented [bug](https://github.com/pygraphviz/pygraphviz/issues/162) that would prevent colored edges, thus it is recommended to run this in a local environment. 

Directions:

1. Make sure the current version of Python is `Python==3.8.3` (or create a new virtual environment)
2. Install graphviz `pip install graphviz` (or `brew install` on mac)
3. Install all other required dependences (via requirements.txt or below)
   
   ```
   pip install jupyter;
   pip install pygraphviz;
   pip install networkx;
   pip install matplotlib;
   pip install numpy;
   pip install scipy;
   pip install pillow;
   ```

Note: Due to the finicky nature of PyGraphviz, in case this does not work, several graphs should be pre-loaded for viewing in the notebook. 