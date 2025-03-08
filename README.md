<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tuxthepenguin84/homeassistant">
    <img src="images/ai.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Home Assistant</h3>

  <p align="center">
    AI Powered Home Assistant
    <br />
    <a href="https://github.com/tuxthepenguin84/homeassistant"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/tuxthepenguin84/homeassistant/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/tuxthepenguin84/homeassistant/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#running">Running</a></li>
    <li><a href="#mobile-app">Mobile App</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

A simple Home Assistant app that uses Large Language Models & Agents to perform actions in your smart home.

Integrates with the [following model providers](https://ai.pydantic.dev/models/):

- OpenAI
- Anthropic
- Gemini
- Ollama
- Groq
- Mistral
- Cohere
- Bedrock

Perform actions like the following:

- Lights, Outlets, Plugs, Switches, etc.
- Garage Door
- Sprinkler System
- Retrieve Weather
- Its easy to customize and add your own

Example of running Home Assistant:

```
~ python3 assistant.py
> Turn the lights on in the office.
I have turned on the office lights.

~ python3 assistant.py
> Open the garage door.
The garage door is now open.

~ python3 assistant.py
> What's the weather in San Francisco today?
OK. I retrieved the weather information for San Francisco, CA. The current temperature is 52°F, with a PM2.5 of 13.2 μg/m³ and a PM10 of 17.2 μg/m³. The weather forecast for today is a high of 61.2°F and a low of 43.1°F. There is no precipitation expected. The sun will rise at 6:50 AM and set at 6:50 PM.
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [Python](https://python.org)
- [PydanticAI](https://ai.pydantic.dev)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

Home Assistant can be run in two manners, locally or hosted with an API.

#### Running Locally

- Install Pydantic-AI
  ```sh
  pip install pydantic-ai
  ```

#### Running the API with Docker

- [Install Docker](https://docs.docker.com/)

### Configuration

1. Clone the repo
   ```sh
   git clone https://github.com/tuxthepenguin84/homeassistant.git
   ```
1. Fill in API keys & Model info in `params.json`
1. Customize `agents.py`. I have provided some generic examples to help get you started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- RUNNING EXAMPLES -->

## Running

### Running Locally

- Run from terminal
  ```sh
  python3 assistant.py
  ```

### Running the API with Docker

- Build Container
  ```sh
  docker build -f Dockerfile . -t tuxthepenguin84/homeassistant:latest --no-cache
  ```
- Run Container
  ```sh
  docker compose up -d
  ```
- Send Request to API
  ```sh
  curl -s -X PUT http://localhost:5000/request -d "request=Turn the den light on."
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Mobile App -->

## Mobile App

While there is no mobile app, you can easily make one on iOS with the Shortcuts app.

- Create a new Shortcut called `Home Assistant`
- Add `Dictate text`
- Add `Get Contents of`
  - Add the URL to your API running in Docker `http://your_ip_address:5000/request`
  - Method `PUT`
  - Request Body `Form`
    - Add new field: `request "Dictacte Text"`
- Save the shortcut to your iOS home screen
- Tap the app and speak your request

<!-- ROADMAP -->

## Roadmap

TBD

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!
</a>

### Top contributors:

<a href="https://github.com/tuxthepenguin84/homeassistant/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=tuxthepenguin84/homeassistant" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->

## License

Distributed under the MIT. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Project Link: [https://github.com/tuxthepenguin84/homeassistant](https://github.com/tuxthepenguin84/homeassistant)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [Chat ai icons created by Metami septiana - Flaticon](https://www.flaticon.com/free-icons/chat-ai)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/tuxthepenguin84/homeassistant.svg?style=for-the-badge
[contributors-url]: https://github.com/tuxthepenguin84/homeassistant/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/tuxthepenguin84/homeassistant.svg?style=for-the-badge
[forks-url]: https://github.com/tuxthepenguin84/homeassistant/network/members
[stars-shield]: https://img.shields.io/github/stars/tuxthepenguin84/homeassistant.svg?style=for-the-badge
[stars-url]: https://github.com/tuxthepenguin84/homeassistant/stargazers
[issues-shield]: https://img.shields.io/github/issues/tuxthepenguin84/homeassistant.svg?style=for-the-badge
[issues-url]: https://github.com/tuxthepenguin84/homeassistant/issues
[license-shield]: https://img.shields.io/github/license/tuxthepenguin84/homeassistant.svg?style=for-the-badge
[license-url]: https://github.com/tuxthepenguin84/homeassistant/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://python.org
