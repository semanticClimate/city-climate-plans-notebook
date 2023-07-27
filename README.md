# semanticClimate automated publication proof-of-concept

## installation

### clone repository

To clone this repository from GitHub, ensure that Git is installed on your local machine either as a command line interface (https://git-scm.com/) or through GitHub Desktop (https://desktop.github.com/).

Use either the CLI or GitHub Desktop to clone the repository into your preferred installation directory.

If using CLI, navigate in the terminal to your preferred installation directory and run:

`git clone https://github.com/SimonXIX/quarto_semanticclimate.git`

### install prerequisites (without Docker)

To install all prerequisites for running this repository on your local machine, please follow the instructions below. 

First, install Python following the instructions at https://www.python.org/downloads/

Once Python is installed, navigate to the quarto_docker directory in terminal and run:

`pip install -r requirements.txt`

This should install all the required Python modules for running the Quarto rendering process. 

Next, install the Quarto CLI following the instructions at https://quarto.org/docs/get-started/

Finally, install an environment for viewing and editing Jupyter Notebook files. This can be Visual Studio Code (https://code.visualstudio.com/), the open source fork VSCodium (https://vscodium.com/), or a dedicated Jupyter environment like JupyterLab (https://quarto.org/docs/get-started/hello/jupyter.html). 

### install prerequisites (Docker)

It's possible (though not required) to use Docker to run the environment for Jupyter Notebook running and Quarto rendering. 

This process works in Linux but does not work in macOS due to a known issue. This involves Quarto not running properly in the Docker container in macOS due to the amd64 emulation of Docker Desktop for arm64 MacOS. See discussion at https://github.com/quarto-dev/quarto-cli/discussions/3308. This shouldn't occur in any other environment running Docker.

To run in Docker, first install Docker Desktop following the instructions at https://docs.docker.com/desktop/.

Once installed, navigate in the terminal to the directory for the cloned Git repository. 

Run `docker-compose up -d --build` to start the containers. 

The jupyterlab container runs a stand-alone version of JupyterLab on http://localhost:8888. This can be used to edit any Jupyter Notebook files in the repository. The JupyterLab instance runs with the password 'jupyterlab'.

The nginx container runs Nginx webserver and displays the static site that Quarto renders. This runs at http://localhost:1337.

The quarto container starts a Ubuntu 22.04 container, installs various things like Python, downloads Quarto and installs it, and then adds Python modules like jupyter, matplotlib, and panda. It then runs in the background so Quarto can be called on to render the qmd and ipynb files into the site/book like so:

`docker exec -it quarto quarto render` 

When you're finished using the code, run `docker-compose down` to stop the containers.

## running the rendering process

The main publishing workflow uses Quarto to render the output of Jupyter Notebook files. 

You can edit the .ipynb files in whatever Jupyter environment you installed above. After editing, ensure that you run the Notebook. 

If you're running the code locally, you can then navigate to the repository directory in terminal and run: 

`quarto render`

for Quarto to render the output into an output directory, in this case, ./docs. 

To preview the published publication, navigate to ./docs/index.html and open it in a web browser. You should see the entire published site. 

When pushed to GitHub, GitHub Pages will then serve the HTML files in the ./docs directory as a website. 