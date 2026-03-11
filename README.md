# QR Code Generator

A Python app that generates QR codes from URLs, containerized with Docker.

## Setup

Clone the repo and make sure Docker is installed.

## Build and Run

Build the image:
```
docker build -t qr-code-generator-app .
```

Run the container:
```
docker run -d --name qr-generator -v $(pwd)/qr_codes:/app/qr_codes qr-code-generator-app
```

Run with a custom URL:
```
docker run -d --name qr-generator -v $(pwd)/qr_codes:/app/qr_codes qr-code-generator-app --url http://www.njit.edu
```

View logs:
```
docker logs qr-generator
```

Stop and remove the container:
```
docker stop qr-generator
docker rm qr-generator
```

## Environment Variables

- LOG_LEVEL - logging level (default: INFO)
- LOG_DIR - where logs are saved (default: logs)
- QR_DIR - where QR images are saved (default: qr_codes)
- QR_FILL_COLOR - QR code color (default: black)
- QR_BACK_COLOR - background color (default: white)

## Dependencies

- qrcode[pil]
- Pillow