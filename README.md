
[![CircleCI](https://circleci.com/gh/BigZeta/datapages.ai/tree/feature%2Fbuild-script-SYNOPTIC-190.svg?style=svg&circle-token=b870be8aec7230a1f7b460085e9a38ed6d24240e)](https://circleci.com/gh/BigZeta/synopticone/tree/feature%2Fbuild-script-SYNOPTIC-190)

# Introduction

Django application for the DataPages.ai MVP.

The Django application uses Wagtail as a core application to implement the CMS for the system.

It is possible to have CMS based pages, as well as non-CMS pages, so we have the flexibility to work either way. CMS pages can be simple, with as many items on the page handled by a database model as needed, or as few. In the simplest case, the page would just be named page in the CMS, that results in a custom template that is 100% hand-configured, and no content is from the CMS

# Steps to setup the project from scratch

## Prerequisites

1. git
2. docker and docker-compose 17+
3. npm

## Installation

Clone the repo and the project-editor-scaffold apps into your working directory

    git clone git@github.com:BigZeta/datapages.git synopticone

Checkout the develop branch of the repository (or some other desired branch)

    git checkout develop

Copy the local versions of environment and django config.

    dc datapages
    cp env.local.example .env.local
    cp local_config-example.py local_config.py

If running django local, with a remote postgres and remote smtpd, you need to add a line to your .env.local
to setup the database url

    DATABASE_URL=postgresql://datasheet_user:<password>@0.0.0.0:5441/datasheetai

The hostname of 0.0.0.0 and port of 5441 are based on the docker-compose.yml file, so compare to that if anything changes.
    
There are also a couple of other environment settings that are required to be setup. All of these can be done manually, as below:

    export DJANGO_ROOT_PATH=./datashseet_ai

To make life easier, I have a "godev" file that can be sourced into the shell (I assume you are using bash). None of this applies if you are on windows, as far as I know.

I find that typing 'docker-compose' a lot is tedious. If you are on a Unix like system (*nix or Mac, not windows), you can set a shell alias also. The rest of this document will use 'dc' instead of docker-compose. If you are on windows, go ahead and type out the full name.
    
    alias dc='docker-compose'
    
First, lets build the containers. This step can be long the fisrt time as it must download all of the required files, build the containers, do pip installs, etc.

    docker-compose build
    
Now you can start the docker containers. The first time postgres starts it must create a database, do I tend to start it by itself fisrt. 

    dc up -d postgres
    
Check to see that it is running, and dump the logs for fun and learning

    docker ps
    dc logs postgres
    
The ps command should show that postgres is running, and the logs command should show you a few output values, including some stuff about creating a database.

The next thing we need to do is create a database. Database backups are mounted to the local path at ./database/backups.
If you were given a database file, put that file there. Assume you were given a file named "backup_2016_07_21T16_30_50.sql". Put that file in the backups directory, and run the following commands. Use the name of the file you were actually given if it is different.

    dc exec postgres restore backup_2016_07_21T16_30_50.sql

Now, you can start the rest of the containers. docker-compose up will bring all of the containers that are not running up, which will include django and smtpd

    dc up -d
    
Now, use ps to check the status again, and the django logs

    docker ps

#### Last Step - build SASS files

The frontend assets are built using gulp. I have a special container that runs gulp in watch mode so that any changes are detected and written. This gulp task has been added to the dev.yml, so no further steps are required. 

### Live Testing

At this point, you should be running. Point a browser at http://localhost:8001/ and enjoy.

All of the source files in the repo are mapped to the containers, so any changes on the source files will be reflected immediately in the Django site.
    
## Cleanup

If you want to re-set everything then you need to do the following

- shut down all docker containers
- remove any associated volumes

Keep in mind that if you have *other* projects using docker, the following steps need to be modified as they clean up all containers and volumes.

First, shut down any running containers. Use docker ps to verify.

    dc down
    
The postgres container willl create the database in a volume. If you want to completely reset the postgres container, you must remove this volume. You can list volumes like this:

    docker volume ls
    
> DRIVER              VOLUME NAME
local               synopticonebuild_postgres_data_dev
   
I want to remove the volumes for the postgres_data.

    docker volume rm synopticonebuild_postgres_data_dev
    
Now, check your volumes again, and that one should be gone. You can now re-build everything from scratch.



# Environment setup

Here we define the system requirements to run the application in development.

The easiest way to get setup is to use the Docker configuration. This requires that  you setup and learn Docker but then everything else is easier.

## Docker Configuration

Docker is a container system. It has some similarities to a virtual machine, but it is not a VM. Docker containers are based on a linux operating system, and you can think of them as "operating system versions". They layer on top of an existing system, and then add custom files, data, and applications that are unique to just that container. 

Changes to files in the container are completely isolated to changes to files in other containers, or the operating system itself. Container can be configured to access some files or directories from the operating system. This is how container can be made to share data with other containers. They can also communicate via networking, so a PGSQL container can open a database networking port for access by another container or the operating system.

Since containers work on Linux, they don't quite work on Native OSX and Windows. There are however some beta capabilities to make this work, so it is getting easier. Currently, both OSX and windows require virtual machines tha run Linux to be installed. These virtual machines then host containers within them.

I use Docker to avoid having to install PostGreSQL on each system. If you happen to have a copy of PGSQL installed, then yo could use that instead, but if not, running with a Docker container is a good alternative as in the long run, it is easier to configure.d


# Local Environment Setup

I don't recommend this setup, but here are a few notes for if you want to try and get this all configured from scratch. 

### Python 3.6+

Development requires a current Python 3.6+ configuration. The development is using the latest Python 3.6+ so that we may take advantage of all of the new capabilities of Python 3.

#### Install Python on OSX

This is pretty easy. Go to https://www.python.org/downloads/, and download the latest Python 3.6+ version. Run the installer, and you will be ready to start.

### NodeJS

We use NodeJS to compile the scss files, build javascript libraries and
generally build tools and features. Some of these are re-built locally
when they change, and will also be built on the production system when
deployed. In order to work on the local system you need to have nodejs
and the various modules installed.

#### Install on OSX

Go to the main nodejs website:

    https://nodejs.org/en/
    
Installed the latest 6.x version of the tool. If you already have an
older copy installed, please update to the latest (just to avoid any
issues between versions). Check your current version with this command
at the terminal:

    node --version
    
When you download nodejs, it will download a system package. You can
double-click this package to install the tool.

##### NPM Preferences and configuration

I prefer to keep my global NPM modules out of /usr/local/*. So, I
update my prefix to be a new directory in my home, ie.. /Users/kutenai/npm-global.

To update the configuration for yourself:

    npm config set prefix ~/npm-global
    
Check your config values with:
        
    npm config list
    
With the prefix set, you will install new node values into that
npm-global location. Now, you need to update your path to include that
path. Edit your ~/.bashrc or ~/.bash_profile to include something like this:

    export PATH=/Users/kutenai/npm-global/bin:$PATH
    
There may be some variations for your system. On my system my ~/.profile
loads ~/.bashrc, but on some systems, your terminal shell startup might
vary. We can work together if there is some variation on your system.

#### Global NPM Modules
 
You will want to install the following npm modules globally so they are
readily available.

    npm install -g babel bower browserify express grunt gulp 
    npm install -g jasmine jsx karma mocha uglifyjs webpack

