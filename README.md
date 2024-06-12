# Thought for the day - Kubernetes deployment
This is an advancement from an earlier project, a flask app which outputs text from a csv to an API, found here - https://github.com/KnightBlue14/Thought_for_the_day

## Description
The project listed above is a simple flask app that can either be run independently, using a virtual Python environment, or in a Docker container, for ease of use. This project represents the next stage of development - using a container orchestration service to deploy and update, potentially, multiple instances of one image from a central controller, in this case kubernetes. Here, the service is run on an AWS EC2 instance, allowing it to be run separately from your primary machine, and accessible over the internet, though incurring a small cost. While AWS does have a free tier, the installation process this project uses requires at least 2 CPUs and more than 2GB of RAM, which is not on the free tier. While there are machines that are low cost and meet these requirements, be aware that you will be charged. You can also install kubernetes locally, which will largely have the same process, but some steps won't apply to you. In either case, this project will use a Linux operating system (Amazon Linux), so keep an eye out for any OS-specific commands.

## Technologies used
* Python - As with the original project, Python is used for app development, though it does not matter much for kubernetes, apart from a single step in configuration.
* Docker - Much more relevant is Docker, as kubernetes is a container orchestration services. In this instance, it pulls the Docker image from a public repository, and then deploys it within a cluster. Some familiarity with Docker beforehand would be beneficial to understanding what is happening, though I will also explain where I can
* Kubernetes - the orchestration service in question.
## How to use
Most of the files used here are the same, and can be found in the earlier project, but I will repeat them here for full clarity. If you already have these files, or your own versions, move to the 'Next steps' section

### App.py
This file contains the settings for the application. As it is, it includes two endpoints, a homepage to confirm that the app is running, and the page for the posting of quotes. If you wish to add any more, simply add a block beginning with '@app.get("/{endpoint_name}")', then write a function for what you want to appear at the endpoint.

### ThoughtfortheDay.py
This is the script that webscrapes the three pages on Lexicanum for the quotes used, which can be found here (https://wh40k.lexicanum.com/wiki/Thought_for_the_day). There is a large block of if statements, covering additional information that is not needed, mostly sources and admin information that use the same element type as the quotes. There is also another block that tries to print the quote, then adds it to a list if successful, which is needed as some quotes featured characters that python was unable to print, and would break the application.

### thought_for_the_day.csv
The collection of quotes used in the app. Even after the filters mentioned in the script, some editing was still needed, so if you redownload them be sure to check for any broken or misplaced lines.

If you are not interested in Docker, these are all you need. Just place the files in a directory, create a virtual environment, install flask WITHIN the environment, then use the command 'flask run' (or 'python -m flask run'). If you are, you will aslo need the following files -

### requirements.txt
The needed modules for the app, covering flask and it's dependencies

### Dockerfile
The blueprint for your container. This can be left alone, unless you change the default port used by your flask application, in which case you will need to change EXPOSE from 5000 to your port. Other than that, just have everything in the same folder, use the command -
```
docker build -t {image-name} .
```
If everything is properly configured, it will then build the container. From there, using Docker Desktop, run the image. Under 'Optional settings', you will need to select a port so that your machine can access the container (i.e. 5000).

## Next steps
Once your image has been built, and you can confirm it is working, you will need to send it to a repository, such as Dockerhub. To do this, you first need to create a free Dockerhub account. When you do, you will name your account. This is the name of your repository.

Then, you will need to tag your image using the command
```
docker {image_name} tag {repository_name}/{image_name}:{tag}
```
In this case, I use knightblue/thoughtfortheday:1.1, which will come up soon.

Then, push the image to the repository, with
```
docker push {repository_name}/{image_name}:{tag}
```
If you reload your dockerhub page, the image should appear, with the version tag, and can now be pulled by any docker instance on any machine

Following this, there is one more file you will need to configure kubernetes

### thought_deploy.yaml
This file tells kubernetes how to deploy your application, and is split into two parts.

The first half concerns the flask deployment, and mostly concerns metadata, which can be left alone, apart from a few lines -
* replicas (line 8) - this determines how many instances of your app will be deployed, be it 1, 3, 10, however many you need. This is mainly for redundancy purposes, but will use more resources from your system, so I would advise it be left at 1.
* image (line 19) - this will be the image that kubernetes uses to build the container, and will pull it from the listed repository. If you have your own version of the app, you will need to change the targeted image. Just use the details you entered to build your image earlier
* containerPort (line 21) - The port within the Docker container that the application will use. Unless you have a aprticular use case, this can be left alone

The second half covers the flask service. The only things you need to be aware of are the port and targetPort variables. For convenience, I would suggest leaving them be. If you want to change them, I'd recommend making them the same, provided your machine doesn't have anything running on that port already.

## Installing Minikube
Minikube is a utility that allows you to quickly set up kubernetes as a container, which can then deploy more containers within the cluster. This does mean that there are a couple more steps to get it working, but means that everything is in one place and can run on its own.

Depending on your OS, you can find instructions for installation here -
https://minikube.sigs.k8s.io/docs/start/

That done, use the command 
```
minikube start --driver docker
```
or --driver=docker, again, depending on your OS

## Deploying the app
Once minikube is set up and your files prepared, you can deploy them via kubectl


When you start, you will be in the `default` namespace, namespaces being where the cluster will store resources between projects. For convenience, I'd suggest setting up your own. To do this, type
```
kubectl create namespace {name}
```
Then navigate to it with
```
kubectl config set-context --current --namespace={name}
```
To get back, just replace {name} with `default`


To upload your files to the cluster, use 
```
kubectl apply -f {filename}
```
for your config file, in this case thought_deploy.yaml

## EC2 deployment

Once applied, the app will be running on a node under kubernetes. Normally, it's activity would be restricetd to that node, and we could not interact with it. With the Load Balancer service, which is set up in the config file, the local machine can now interact with it on a port (i.e. 127.0.0.1:5000). If you are running this on your local machine, you are done. However, this was run on an EC2 instance, so there is one more step.

Right now, you will not be able to access your app because it is still restricted to the machine. We will need to use port forwarding to make it accessible.

First, confirm that the port you have in mind will accept traffic over the internet, in this case port 5000. Then, to be sure your app is running, use the command
```
minikube service thoughtoftheday-service --url
```
which will output a url. Then, use
```
curl {URL}
```
If an error is not reported, that will mean that your app is working. Finally, use
```
kubectl port-forward svc/thoughtoftheday-service 5000:5000 --address 0.0.0.0 &
```
This will route activity from port 5000 of your machine to port 5000 of the cluster. If you are using AWS, then your instance will have an autoassigned public IP, in the Details tab. Use that IP, specifying port 5000, and you will reach the homepage. From there, use the commands you have specified in the app file to navigate. As you load each URL, you will find that the command line prints a message in the form of 'handling connection for {port number}'. Just use CTRL+C to exit and commands again, the service will still run
