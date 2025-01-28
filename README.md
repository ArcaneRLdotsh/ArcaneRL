# ArcaneRL

<p align="center">
  <a href="https://arcanerl.sh">
    <img src="https://pbs.twimg.com/profile_banners/1884311837576974338/1738090250/1500x500" alt="ArcaneRL Banner" />
  </a>
</p>

<p align="center"><i>Open-source framework that gives you AI Agents that help you navigate decision-making, get personalized goals, and execute them</i></p>

<p align="center">
<a href="https://github.com/topoteretes/ArcaneRL/fork" target="blank">
<img src="https://img.shields.io/github/forks/topoteretes/ArcaneRL?style=for-the-badge" alt="ArcaneRL forks"/>
</a>

<a href="https://github.com/topoteretes/ArcaneRL/stargazers" target="blank">
<img src="https://img.shields.io/github/stars/topoteretes/ArcaneRL?style=for-the-badge" alt="ArcaneRL stars"/>
</a>
<a href="https://github.com/topoteretes/ArcaneRL/pulls" target="blank">
<img src="https://img.shields.io/github/issues-pr/topoteretes/ArcaneRL?style=for-the-badge" alt="ArcaneRL pull-requests"/>
</a>
<a href='https://github.com/topoteretes/ArcaneRL/releases'>
<img src='https://img.shields.io/github/release/topoteretes/ArcaneRL?&label=Latest&style=for-the-badge'>
</a>
</p>

<p align="center"><b>Share ArcaneRL Repository</b></p>

<p align="center">
<a href="https://twitter.com/intent/tweet?text=Check%20this%20GitHub%20repository%20out.%20ArcaneRL%20-%20Let%27s%20you%20easily%20build,%20manage%20and%20run%20useful%20autonomous%20AI%20agents.&url=https://github.com/topoteretes/ArcaneRL&hashtags=ArcaneRL,AGI,Autonomics,future" target="blank">
<img src="https://img.shields.io/twitter/follow/arcanerldotsh?label=Share Repo on Twitter&style=social" alt="Follow arcanerldotsh"/></a> 
<a href="https://t.me/share/url?text=Check%20this%20GitHub%20repository%20out.%20ArcaneRL%20-%20Let%27s%20you%20easily%20build,%20manage%20and%20run%20useful%20autonomous%20AI%20agents.&url=https://github.com/topoteretes/ArcaneRL" target="_blank"><img src="https://img.shields.io/twitter/url?label=Telegram&logo=Telegram&style=social&url=https://github.com/topoteretes/ArcaneRL" alt="Share on Telegram"/></a>
<a href="https://api.whatsapp.com/send?text=Check%20this%20GitHub%20repository%20out.%20ArcaneRL%20-%20Let's%20you%20easily%20build,%20manage%20and%20run%20useful%20autonomous%20AI%20agents.%20https://github.com/topoteretes/ArcaneRL"><img src="https://img.shields.io/twitter/url?label=whatsapp&logo=whatsapp&style=social&url=https://github.com/topoteretes/ArcaneRL" /></a> <a href="https://www.reddit.com/submit?url=https://github.com/topoteretes/ArcaneRL&title=Check%20this%20GitHub%20repository%20out.%20ArcaneRL%20-%20Let's%20you%20easily%20build,%20manage%20and%20run%20useful%20autonomous%20AI%20agents.">
<img src="https://img.shields.io/twitter/url?label=Reddit&logo=Reddit&style=social&url=https://github.com/topoteretes/ArcaneRL" alt="Share on Reddit"/>
</a> <a href="mailto:?subject=Check%20this%20GitHub%20repository%20out.&body=ArcaneRL%20-%20Let%27s%20you%20easily%20build,%20manage%20and%20run%20useful%20autonomous%20AI%20agents.%3A%0Ahttps://github.com/topoteretes/ArcaneRL" target="_blank"><img src="https://img.shields.io/twitter/url?label=Gmail&logo=Gmail&style=social&url=https://github.com/topoteretes/ArcaneRL"/></a> <a href="https://www.buymeacoffee.com/arcanerl" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="23" width="100" style="border-radius:1px"></a>
</p>

<hr>

## We took all the work we did with PromethAI into our new product, ArcaneRL -> check it out [here](https://github.com/topoteretes/ArcaneRL)

## What is it

ArcaneRL is a Python-based AGI project that recommends choices based on a user's goals and preferences and can modify its recommendations based on user feedback.

Our focus is currently on food, but the system is extendible to any area.

## 💡 Features

- Optimized for Autonomous Agents
- Personalized for each user
- Introduces decision trees to help user navigate and decide on a solution
- Runs asynchronously
- For App builds, check out this repo [ArcaneRL-GUI](https://github.com/topoteretes/ArcaneRL-Mobile)
- Supports automating tasks and executing decisions
- Multiple Vector DBs supported through Langchain 
- Low latency
- Easy to use
- Easy to deploy

## 💻 Demo

<p align="center">
  <a href="https://arcanerl.sh">
    <img  src="https://promethai-public-assets.s3.eu-west-1.amazonaws.com/product_demo-min.gif"  width="25%" height="50%"/>
  </a>
</p>

## 🛣 Architecture
<p align="center">
  <img src="assets/PromethAI_infra.png" alt="ArcaneRL Architecture" width="50%" height="50%">
</p>

## 🛣 Roadmap
<p align="center">
  <img src="assets/roadmap.png" alt="ArcaneRL Roadmap" width="50%" height="50%">
</p>

## ⚙️ Setting up

1. Download the repo using `git clone https://github.com/topoteretes/ArcaneRL.git` in your terminal or directly from the GitHub page in zip format.
2. Navigate to the directory using `cd ArcaneRL` and create a copy of `.env.template` and name it `.env`.
3. Enter your unique OpenAI API Key, Google key, Custom search engine ID without any quotes or spaces in `.env` file. Follow the links below to get your keys:

| Keys                        | Accessing the keys                                                                                                                                                                                                |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **OpenAI API Key**          | Sign up and create an API key at [OpenAI Developer](https://beta.openai.com/signup/)                                                                                                                              |
| **Pinecone API Key**        | Sign up and create an API key at [Pinecone.io](https://www.pinecone.io/)                                                                                                                                          |
| **Google API key**          | Create a project in the [Google Cloud Console](https://console.cloud.google.com/) and enable the API you need (for example: Google Custom Search JSON API). Then, create an API key in the "Credentials" section. |
| **Custom search engine ID** | Visit [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/) to create a custom search engine for your application and obtain the search engine ID.                              |

4. Ensure that Docker and Docker Compose are installed in your system, if not, Install it from [here](https://docs.docker.com/get-docker/). 
5. Once you have Docker Desktop running, run command : `docker-compose up arcanerl --build` in ArcaneRL directory. Open your browser and go to `localhost:3000` to see ArcaneRL running.

## Resources
Papers like ["Generative Agents: Interactive Simulacra of Human Behavior"](https://arxiv.org/abs/2304.03442)

## Quick start 
Make sure to add your credentials in the .env file. Launch the app with:

```docker-compose build arcanerl && docker-compose up arcanerl```

## How it Works
Here is what happens every time the AI is queried by the user:
1. AI vectorizes the query and stores it in a Pinecone Vector Database
2. AI looks inside its memory and finds memories and past queries that are relevant to the current query
3. AI thinks about what action to take
4. AI stores the thought from Step 3
5. Based on the thought from Step 3 and relevant memories from Step 2, AI generates an output
6. AI stores the current query and its answer in its Pinecone vector database memory

## How to use
```
docker-compose build arcanerl
```
Access the API by doing CURL requests, example: 
```
curl -X POST "http://0.0.0.0:8000/data-request" -H "Content-Type: application/json" --data-raw 

```
## Example of available endpoint

The available endpoint:
```
POST request to '/recipe-request' endpoint that takes a JSON payload containing 'user_id', 'session_id', 'factors' keys, and returns a JSON response with a 'response' key.

```
All endpoints receive a payload in JSON format and return a response in JSON format.

Example of curl requests
```
curl --location --request POST 'http://0.0.0.0:8000/recipe-request' \
--header 'Content-Type: application/json' \
--data-raw '{
  "payload": {
    "user_id": "659",
    "session_id": "459",
    "model_speed":"slow",
    "prompt":"I would like a healthy chicken meal over 125$"
    
  }
}'
```

# 🔰 Notice

ArcaneRL is a work in progress, delivered to you without any guarantees, whether explicit or implied. By choosing to use this application, you consent to take on any associated risks, including data loss, system failure, or any other complications that may arise.

The creators and contributors of ArcaneRL disclaim any responsibility or liability for any potential losses, damages, or any other adverse effects resulting from your use of this software. The onus is solely on you for any decisions or actions you take based on the information given by ArcaneRL.

Please be aware that usage of the GPT-4 language model could incur significant costs due to its token consumption. By using this software, you acknowledge and agree to monitor your own token usage and manage the associated costs. We strongly suggest routinely checking your OpenAI API usage and implementing necessary limits or alerts to avoid unexpected fees.

Given its experimental nature, ArcaneRL may generate content or perform actions that do not align with real-world business norms or legal obligations. It falls on you to ensure that any actions or decisions based on this software’s output adhere to all relevant laws, regulations, and ethical standards. The creators and contributors of this project will not be held accountable for any fallout from using this software.

By utilizing ArcaneRL, you agree to protect, defend, and absolve the creators, contributors, and any affiliated parties from any claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys' fees) that arise from your use of this software or your violation of these terms.

# 📝 License

MIT License

# Credits: 
Teenage AGI -> https://github.com/seanpixel/Teenage-AGI  
Baby AGI -> https://github.com/yoheinakajima/babyagi
