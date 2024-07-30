# Development Container for Python 3

This README provides instructions on how to set up and use a development container for Python 3 with VS Code. The development container is defined using a `Dockerfile` and a `.devcontainer.json` configuration file.

## Prerequisites

- [Docker](https://www.docker.com/get-started): Ensure Docker is installed and running on your machine.
- [Visual Studio Code](https://code.visualstudio.com/): Make sure you have VS Code installed.
- [Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers): Install this extension in VS Code.

## .devcontainer.json Configuration

The `.devcontainer.json` file defines the configuration for the development container:

```json
{
    "name": "Python 3",
    "build": {
        "dockerfile": "Dockerfile",
        "context": "."
    },
    "customizations": {
        "vscode": {
            "settings": {
                "python.pythonPath": "/usr/local/bin/python"
            },
            "extensions": [
                "ms-python.python"
            ]
        }
    },
    //"postCreateCommand": "pip install -r requirements.txt",
    "remoteUser": "root"
}
```

Explanation
``` json
    "name": The name of the development container.
    "build": Specifies the Docker build context and the Dockerfile to use.
        "dockerfile": The Dockerfile that defines the container image.
        "context": The build context, usually the root of your project.
    "customizations": VS Code-specific settings and extensions.
        "vscode": Customizations for VS Code.
            "settings": Custom settings for VS Code, such as the path to the Python interpreter.
            "extensions": A list of VS Code extensions to install in the container. In this case, the Python extension.
    "postCreateCommand": A command to run after the container is created. This is currently commented out but would install Python dependencies if uncommented.
    "remoteUser": The user to use inside the container. Here, it is set to root.
```

Setting Up the Development Container

    Open the Project in VS Code: Open your project folder in VS Code.
    Open the Command Palette: Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (macOS) to open the Command Palette.
    Run Remote-Containers Command: Type Remote-Containers: Reopen in Container and select it.
    Wait for the Container to Build and Start: VS Code will use the .devcontainer.json and Dockerfile to build and start the container. This may take a few minutes.
    Develop in the Container: Once the container is running, you can develop your application inside the container with all dependencies and settings configured.