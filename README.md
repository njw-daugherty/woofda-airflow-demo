# Quick Start
If you already have recent enough versions of Docker and Docker Compose installed, and you have access to a Linux kernel, you can jump right in with the following steps. Otherwise, see [Setting Up Docker and Docker Compose](#setting-up-docker-and-docker-compose) for installing the prerequisites.

1. Clone this repository to your local file system (note: this must be a Linux file system!). The below command will clone the repository to a directory named `woofda-airflow-demo`:

    ```
    $ git clone https://github.com/njw-daugherty/woofda-airflow-demo.git
    ```

1. Navigate into the newly created directory
    ```
    $ cd woofda-airflow-demo
    ```
1. Run the following commands to make some directories that will be mounted as volumes to your Docker containers. **Do not prefex this command with `sudo`**.

    ```
    $ mkdir -p ./dags ./logs ./plugins ./output ./jars_dir 
    ```

1. Run the below command to get your current user id, and make sure the `AIRFLOW_UID` is set to this value in the `.env` file. Your user id is probably `1000`, in which case you do not need to make any changes.
    ```
    $ id -u
    ```

1. Finally, bring up all the Docker containers using Docker Compose 
    
    ```
    $ docker-compose up
    ```

The first time you run `docker-compose up`, Docker will need to build all the images from scratch. This may take a while. Subsequent calls to `docker-compose up` should proceed much more quickly.

You can follow the progress of `docker-compose up` in your terminal, where Docker Compose emits all the logs from the containers it is starting. You can tell the containers are done building by looking for the health request checks from the webserver. They will look something like this:

```
airflow-webserver_1  | 127.0.0.1 - - [19/Nov/2021:07:41:39 +0000] "GET /health HTTP/1.1" 200 187 "-" "curl/7.64.0"
airflow-webserver_1  | 127.0.0.1 - - [19/Nov/2021:07:42:09 +0000] "GET /health HTTP/1.1" 200 187 "-" "curl/7.64.0"
```
 You can verify that Airflow is ready by navigating to http://localhost:8080 in your web browser. You should see the Airflow Web UI. Sign in with the credentials below

 > **username:** airflow
 >
 > **password:** airflow

# Setting Up Docker and Docker Compose
## Using Linux on Windows 10
Apache Airflow, like many other open-source technologies, only runs on Linux. If you try to run it *natively* on Windows, it will fail. You can, however, run it using Microsoft's virtualization of the Linux kernal, [Windows Subsystem for Linux 2 (WSL2)](https://docs.microsoft.com/en-us/windows/wsl/about). Installing and configuring WSL2 is relatively straightforward; you can find instructions [here](https://docs.microsoft.com/en-us/windows/wsl/install).
## Installing Docker and Docker Compose
### Direct Installation (No Docker Desktop)
If you do not wish to use Docker Desktop (which is understandable considering how buggy and resource-intensive it is), you can follow the below instructions to install it directly into WSL2.

> **Note**: The following instructions were tested on Ubuntu 20.04. If you are using a different WSL2 distro, see the distro-specific Docker documentation for any differences: https://docs.docker.com/engine/install/

**Docker**
1. Uninstall any previously installed versions of Docker by running

    ```
    $ sudo apt-get remove docker docker-engine docker.io containerd runc
    ```

1. Run the following command to update the `apt` package index and download prerequisite packages:
    ```
    $ sudo apt-get update && sudo apt-get install ca-certificates curl gnupg lsb-release
    ```

1. Add the Docker GPG key:
    ```
     $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
     ```

1. Run the following command to configure Docker's stable repository:
    ```
    $ echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

1. Install Docker with the command
    ```
    $ sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

1. Start Docker by running
    ```
    $ sudo service docker start
    ```

1. Run the following command to verify that your installation was successful:
    ```
    $ docker run hello-world
    ```

**Docker Compose**

1. Download the current stable release of Docker Compose:
    ```
    $ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

1. Make the Docker Compose binary executable:
    ```
    $ sudo chmod +x /usr/local/bin/docker-compose
    ```

Once you've completed the installation of Docker and Docker Compose, follow the directions in the [Quickstart](#quick-start).
