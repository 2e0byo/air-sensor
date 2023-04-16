.PHONY: upload upload-usb wizard logs dashboard

DOCKER?=docker run
DOCKERARGS?=--rm -v "${PWD}":/config -v "$(realpath ../config)":/config/master -it --network host
USB?=--device=/dev/ttyUSB0
CONTAINER?=esphome/esphome
FILE?=sensor.yaml

upload:
	${DOCKER} ${DOCKERARGS} ${CONTAINER} run ${FILE}

upload-usb:
	${DOCKER} ${DOCKERARGS} ${USB} ${CONTAINER} run ${FILE}

wizard:
	${DOCKER} ${DOCKERARGS} ${CONTAINER} wizard ${FILE}

logs:
	${DOCKER} ${DOCKERARGS} ${CONTAINER} logs ${FILE}

dashboard:
	${DOCKER} ${DOCKERARGS} ${CONTAINER}
