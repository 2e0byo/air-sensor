.PHONY: serve

PORT?=9192

serve:
	${BROWSER} "http://localhost:${PORT}" &
	python -m http.server ${PORT} -d .
