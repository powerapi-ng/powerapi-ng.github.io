# powerapi-ng.github.io
PowerAPI website use [MKDocs](https://www.mkdocs.org/). 

You can push your changes on `master` branch to deploy them on the website. 

## Local development  

When redacting changes for this documentation, you may want to visualize the 
output the way it will be presented in the final website once compiled.  

One way to do so is to:  

1. Install the necessary packages : mkdocs, mkdocs-material, mkdocs-material-extensions  
This can be done with: `pip install mkdocs mkdocs-material mkdocs-material-extensions`  

2. Have a local copy of this repository (taking care of *checkout-ing* the right ref)  

3. From the CLI, have this particular repository as PWD  

4. Use mkdocs in order to serve locally (default on http://localhost:8000)  
This can be done with: `mkdocs serve -o`  

5. Check the URL it serves to, targets will be rebuild on modifications in the 
current directory or in any nested elements (use -W to add paths to be considered for hot reloading)  
