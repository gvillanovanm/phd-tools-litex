# Setup
IMAGE 			= docker-phd-tools-litex
CONTAINER_NAME 	= docker-phd-tools-litex
HOST_PATH 		= /Users/gvillanovanm/Github/docker/docker-linux/phd/tools/phd-tools-litex
CONTAINER_PATH 	= /workspace
HOSTNAME 		= docker-phd-tools-litex

# Docker cmds
dk_run:
	docker run --platform=linux/amd64 -h $(HOSTNAME) -it --rm --name $(CONTAINER_NAME) -v $(HOST_PATH):$(CONTAINER_PATH) $(IMAGE) /bin/bash -c "cd $(CONTAINER_PATH) && /bin/bash"

dk_build:
	docker build -t $(IMAGE) .

dk_help:
	echo "open xquartz and type: xhost +gvillanovanm.local for graphical support"

# 1) run it
# 2) open xquartz and type: xhost +gvillanovanm.local 
# dk_run_eyes:
# docker run --platform=linux/amd64 -h $(HOSTNAME) -it --rm -e DISPLAY=host.docker.internal:0 -v $(HOST_PATH):$(CONTAINER_PATH) $(IMAGE) /bin/bash -c "cd $(CONTAINER_PATH) && /bin/bash"
