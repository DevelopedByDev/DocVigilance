

# DocVigilance - Doctor Alertness Monitoring App

![DocVigilance Demo](demo.gif)

## Setup

Before running the application, ensure you have the required Python packages installed. You can install them using `pip` as follows:

```bash
pip install -r requirements.txt
```

## Usage

To run the DocVigilance app, execute the following command:

```bash
streamlit run app.py
```

This will start a local web server and open the app in your default web browser. You can then interact with the app to monitor a doctor's alertness by detecting handshaking and eye fatigue.

## Description

DocVigilance is a Streamlit web application designed to assist doctors in maintaining their alertness during long shifts. The app leverages computer vision and machine learning technologies to monitor doctors' hand movements and detect signs of eye fatigue.

### Features

- **Handshaking Detection**: The app uses the Mediapipe library to detect handshaking motions. It can identify when a doctor's hand is shaking due to fatigue or other factors.

- **Eye Fatigue Detection**: DocVigilance also employs computer vision techniques to detect signs of eye fatigue. It monitors the doctor's eyes and provides alerts if it detects drowsiness or excessive blinking.

- **Real-time Monitoring**: The app offers real-time monitoring, providing immediate feedback to doctors to help them stay alert and focused on their tasks.

### How it Works

DocVigilance utilizes the following key libraries and technologies:

- **Streamlit**: The user interface is built using Streamlit, which makes it easy to create interactive web applications in Python.

- **Streamlit-WebRTC**: This extension enables real-time video streaming for monitoring doctors' movements and eyes.

- **OpenCV-Python**: OpenCV is used for image and video processing, allowing us to analyze video feeds for handshaking and eye fatigue.

- **Mediapipe**: Mediapipe provides pre-trained machine learning models for hand and face tracking, making it a powerful tool for detecting hand movements and eye fatigue.

## Build Docker Image

To build the DocVigilance app in Docker.

```bash
docker build -t streamlit .
docker images
```

This will build the image in local.

## Run Docker Image

To run the DocVigilance app in Docker.

```bash
docker run -p 8080:8080 streamlit
```

To view your app, users can browse to ```http://0.0.0.0:8080`` or ```http://localhost:8080```

## Testing Local
Chrome do not allow camera access when visiting unsecured website.

To ignore Chrome’s secure origin policy, follow these steps. Navigate to ```chrome://flags/#unsafely-treat-insecure-origin-as-secure``` in Chrome.

Find and enable the Insecure origins treated as secure section (see below). Add any addresses you want to ignore the secure origin policy for. Remember to include the port number too (if required). Save and restart Chrome.

## Google Cloud Cli
```
sudo apt-get install apt-transport-https ca-certificates gnupg curl sudo

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

sudo apt-get update && sudo apt-get install google-cloud-cli

gcloud init
```

## Deployment

```
gcloud builds submit --tag gcr.io/docvigilance/docvigilance
```

## Issues

Need Turned Server
https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice

## Contributing

We welcome contributions to improve and enhance the functionality of DocVigilance. If you'd like to contribute, please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to thank the open-source community for their contributions to the libraries and tools that make this app possible.

References:
https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe
https://medium.com/mlearning-ai/live-webcam-with-streamlit-f32bf68945a4

