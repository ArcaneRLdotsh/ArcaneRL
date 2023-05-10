from langchain.prompts import PromptTemplate
from concurrent.futures import ThreadPoolExecutor
import pinecone
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import openai
import re
import datetime
from jinja2 import Template
from dotenv import load_dotenv
import time
from langchain.llms.openai import OpenAI
from langchain import LLMChain
from langchain.schema import  Document

#from heuristic_experience_orchestrator.prompt_template_modification import PromptTemplate
# from langchain.retrievers import TimeWeightedVectorStoreRetriever
import os
from food_scrapers import wolt_tool
import json
from langchain.tools import GooglePlacesTool


# redis imports for cache

from langchain.cache import RedisSemanticCache
import langchain
import redis



# nltk.download('punkt')
import subprocess

# database_url = os.environ.get('DATABASE_URL')
# import nltk
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
from langchain.llms import Replicate

import os




class Agent():
    load_dotenv()
    OPENAI_MODEL = os.getenv("OPENAI_MODEL") or "gpt-3.5-turbo"
    GPLACES_API_KEY = os.getenv("GPLACES_API_KEY", "")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_API_ENV = os.getenv("PINECONE_API_ENV", "")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
    REDIS_HOST = os.getenv("REDIS_HOST", "promethai-dev-backend-redis-repl-gr.60qtmk.ng.0001.euw1.cache.amazonaws.com")

    def __init__(self, table_name=None, user_id: Optional[str] = "user123", session_id: Optional[str] = None) -> None:
        self.table_name = table_name
        self.user_id = user_id
        self.session_id = session_id
        self.memory = None
        self.thought_id_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # Timestamp with millisecond precision
        self.last_message = ""
        self.llm = OpenAI(temperature=0.0,max_tokens = 1000, openai_api_key = self.OPENAI_API_KEY)
        self.replicate_llm = Replicate(model="replicate/vicuna-13b:a68b84083b703ab3d5fbf31b6e25f16be2988e4c3e21fe79c2ff1c18b99e61c1", api_token=self.REPLICATE_API_TOKEN)
        self.verbose: bool = True
        self.openai_model = "gpt-3.5-turbo"
        self.openai_temperature = 0.0
        self.index = "my-agent"

        # use any OPENAI embedding provider
        from langchain.embeddings import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings(openai_api_key=self.OPENAI_API_KEY)
        from langchain.cache import RedisCache
        from redis import Redis
        langchain.llm_cache = RedisCache(redis_=Redis(host=self.REDIS_HOST, port=6379, db=0))
        # langchain.llm_cache = RedisSemanticCache(
        #     embedding=embeddings,
        #     redis_url=redis_url
        # )

    def test_replicate(self):
        start_time = time.time()
        bb = self.replicate_llm("""             Help me choose what food choice, order, restaurant or a recipe to eat or make for my next meal.     
                There are 'health', 'time', 'cost' factors I want to consider.
                
                For 'health', I want the meal to be '85' points on a scale of 1 to 100 points.
                
                For 'time', I want the meal to be '75' points on a scale of 1 to 100 points.
                
                For 'cost', I want the meal to be '50' points on a scale of 1 to 100 points.
                
                Instructions and ingredients should be detailed.  Result type can be Recipe, but not Meal
                Answer with a result in a correct  python dictionary that is properly formatted that contains the following keys and must have  values
                "Result type",  "body" which should contain "title", "rating", "prep_time", "cook_time", "description", "ingredients", "instructions" 
                The values in JSON should not repeat
                """)
        time.sleep(15)
        end_time = time.time()

        execution_time = end_time - start_time
        print("Execution time: ", execution_time, " seconds")
        return print(bb)
    def set_user_session(self, user_id: str, session_id: str) -> None:
        self.user_id = user_id
        self.session_id = session_id

    def get_ada_embedding(self, text):
        text = text.replace("\n", " ")
        return openai.Embedding.create(input=[text], model="text-embedding-ada-002",api_key =OPENAI_API_KEY)[
            "data"
        ][0]["embedding"]

    def init_pinecone(self, index_name):
            load_dotenv()
            PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
            PINECONE_API_ENV = os.getenv("PINECONE_API_ENV", "")
            pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
            return pinecone.Index(index_name)
    def _update_memories(self, observation: str, namespace: str):
        # Fetch related characteristics
        memory = self.init_pinecone(index_name=self.index)

        vector = self.get_ada_embedding(observation)
        upsert_response = memory.upsert(
            vectors=[
                {
                    'id': f"thought-{self.thought_id_timestamp}",
                    'values': vector,
                    'metadata':
                        {"thought_string": observation, "user_id": self.user_id
                         }
                }],
            namespace=namespace,
        )
        return upsert_response

    def _fetch_memories(self, observation: str, namespace:str) -> List[Document]:
          #"""Fetch related characteristics, preferences or dislikes for a user."""
        query_embedding = self.get_ada_embedding(observation)
        memory = self.init_pinecone(index_name=self.index)
        memory.query(query_embedding, top_k=1, include_metadata=True, namespace=namespace,
                          filter={'user_id': {'$eq': self.user_id}})
    #     return self.memory_retriever.get_relevant_documents(observation)
    def _compute_agent_summary(self, model_speed:str):
        """Computes summary for a person"""
        prompt = PromptTemplate.from_template(
            "How would you summarize {name}'s core characteristics given the"
            + " following statements:\n"
            + "{relevant_characteristics}"
            + "{relevant_preferences}"
            + "{relevant_dislikes}"
            + "Do not embellish."
            + "\n\nSummary: "
        )
        self.init_pinecone(index_name=self.index)
        # The agent seeks to think about their core characteristics.
        relevant_characteristics = self._fetch_memories(f"Users core characteristics", namespace="TRAITS")
        relevant_preferences = self._fetch_memories(f"Users core preferences", namespace="PREFERENCES")
        relevant_dislikes = self._fetch_memories(f"Users core dislikes", namespace="DISLIKES")
        if model_speed =='fast':
            output = self.replicate_llm(prompt)
            return output

        else:
            chain = LLMChain(llm=self.llm, prompt=prompt, verbose=self.verbose)
            return chain.run(name= self.user_id, relevant_characteristics=relevant_characteristics, relevant_preferences=relevant_preferences, relevant_dislikes=relevant_dislikes).strip()



    def update_agent_preferences(self, preferences:str):
        """Serves to update agents preferences so that they can be used in summary"""

        prompt = """ The {name} has following {past_preference} and the new {preferences}
                Update user preferences and return a list of preferences
            Do not embellish.
            Summary: """
        self.init_pinecone(index_name=self.index)
        past_preference = self._fetch_memories(f"Users core preferences", namespace="PREFERENCES")
        prompt = PromptTemplate(input_variables=["name", "past_preference", "preferences"], template=prompt)
        prompt = prompt.format(name=self.user_id, past_preference= past_preference, preferences=preferences)
        return self._update_memories(prompt, namespace="PREFERENCES")

    def update_agent_taboos(self, dislikes:str):
        """Serves to update agents taboos so that they can be used in summary"""
        prompt =""" The {name} has following {past_dislikes} and the new {dislikes}
                Update user taboos and return a list of taboos
            Do not embellish.
            Summary: """
        self.init_pinecone(index_name=self.index)
        past_dislikes = self._fetch_memories(f"Users core dislikes", namespace="DISLIKES")
        prompt = PromptTemplate(input_variables=["name", "past_dislikes", "dislikes"], template=prompt)
        prompt = prompt.format(name=self.user_id, past_dislikes= past_dislikes, dislikes=dislikes)
        return self._update_memories(prompt, namespace="DISLIKES")


    def update_agent_traits(self, traits:str):
        """Serves to update agent traits so that they can be used in summary"""
        prompt =""" The {name} has following {past_traits} and the new {traits}
                Update user traits and return a list of traits
            Do not embellish.
            Summary: """
        self.init_pinecone(index_name=self.index)
        past_traits = self._fetch_memories(f"Users core dislikes", namespace="TRAITS")
        prompt = PromptTemplate(input_variables=["name", "past_traits", "traits"], template=prompt)
        prompt = prompt.format(name=self.user_id, past_traits= past_traits, traits=traits)
        return self._update_memories(prompt, namespace="TRAITS")


    def update_agent_summary(self):
        """Serves to update agent traits so that they can be used in summary"""
        summary = self._compute_agent_summary()
        return self._update_memories(summary, namespace="SUMMARY")

    def task_identification(self, goals:str):
        """Serves to update agent traits so that they can be used in summary"""
        self.init_pinecone(index_name=self.index)
        agent_summary = self._fetch_memories(f"Users core summary", namespace="SUMMARY")
        complete_query = str(agent_summary) + goals
        complete_query = PromptTemplate.from_template(complete_query)
        print("HERE IS THE COMPLETE QUERY", complete_query)
        from heuristic_experience_orchestrator.task_identification import TaskIdentificationChain
        chain = TaskIdentificationChain.from_llm(llm=self.llm, task_description="none",  value="Decomposition", verbose=self.verbose)

        chain_output = chain.run(name= self.user_id).strip()
        return chain_output


    def solution_generation(self, factors:dict, model_speed:str):
        """Generates a solution choice"""
        import time

        start_time = time.time()
        prompt = """
                Help me choose what food choice, order, restaurant or a recipe to eat or make for my next meal.     
                There are {% for factor, value in factors.items() %}'{{ factor }}'{% if not loop.last %}, {% endif %}{% endfor %} factors I want to consider.
                {% for factor, value in factors.items() %}
                For '{{ factor }}', I want the meal to be '{{ value }}' points on a scale of 1 to 100 points{% if not loop.last %}.{% else %}.{% endif %}
                {% endfor %}
                Instructions and ingredients should be detailed.  Result type can be Recipe, but not Meal
                Answer with a result in a correct  python dictionary that is properly formatted that contains the following keys and must have  values
                "Result type" should be "Solution proposal,  "body" which should contain "proposal" and the value of the proposal that should be order, restaurant or a recipe
        """
        self.init_pinecone(index_name=self.index)
        agent_summary = self._fetch_memories(f"Users core summary", namespace="SUMMARY")
        template = Template(prompt)
        output = template.render(factors=factors)
        complete_query = str(agent_summary) + output
        # complete_query =  output
        complete_query = PromptTemplate.from_template(complete_query)

        if model_speed =='fast':
            output = self.replicate_llm(output)
            json_data = json.dumps(output)
            return json_data
        else:
            chain = LLMChain(llm=self.llm, prompt=complete_query, verbose=self.verbose)
            chain_result = chain.run(prompt=complete_query, name=self.user_id).strip()
            end_time = time.time()

            execution_time = end_time - start_time
            print("Execution time: ", execution_time, " seconds")
            json_data = json.dumps(chain_result)
            return json_data
    def recipe_generation(self, factors:dict, model_speed:str):
        """Generates a recipe solution in json"""
        import time

        start_time = time.time()
        prompt = """
                Help me choose what recipe to eat or make for my next meal.     
                There are {% for factor, value in factors.items() %}'{{ factor }}'{% if not loop.last %}, {% endif %}{% endfor %} factors I want to consider.
                {% for factor, value in factors.items() %}
                For '{{ factor }}', I want the meal to be '{{ value }}' points on a scale of 1 to 100 points{% if not loop.last %}.{% else %}.{% endif %}
                {% endfor %}
                Instructions and ingredients should be detailed.
                Answer with a result in a correct  python dictionary that is properly formatted that contains the following keys and must have  values
                "Result type" should be "Recipe",  "body" which should contain "title", "rating", "prep_time", "cook_time", "description", "ingredients", "instructions"
        """
        self.init_pinecone(index_name=self.index)
        agent_summary = self._fetch_memories(f"Users core summary", namespace="SUMMARY")
        template = Template(prompt)
        output = template.render(factors=factors)
        complete_query = str(agent_summary) + output
        # complete_query =  output
        complete_query = PromptTemplate.from_template(complete_query)

        if model_speed =='fast':
            output = self.replicate_llm(output)
            json_data = json.dumps(output)
            return json_data
        else:
            chain = LLMChain(llm=self.llm, prompt=complete_query, verbose=self.verbose)
            chain_result = chain.run(prompt=complete_query, name=self.user_id).strip()
            end_time = time.time()

            execution_time = end_time - start_time
            print("Execution time: ", execution_time, " seconds")
            json_data = json.dumps(chain_result)
            return json_data

    def goal_generation(self, factors: dict, model_speed:str):
        """Serves to optimize agent goals"""

        prompt = """
              Based on all the history and information of this user, suggest mind map that would have four decision points that are personal to him that he should apply to optimize his decision choices related to food. The cuisine should be one of the points, and goal should contain one or maximum two words
              Answer a condensed JSON with no whitespaces. The structure should only contain a list of goals under field "goals". After the JSON output, don't explain or write anything.
            """

        self.init_pinecone(index_name=self.index)
        agent_summary = self._fetch_memories(f"Users core summary", namespace="SUMMARY")
        template = Template(prompt)
        output = template.render(factors=factors)
        print("HERE IS THE AGENT SUMMARY", agent_summary)
        print("HERE IS THE TEMPLATE", output)
        complete_query = str(agent_summary) + output
        complete_query = PromptTemplate.from_template(complete_query)
        if model_speed =='fast':
            output = self.replicate_llm(output)
            return output
        else:
            chain = LLMChain(llm=self.llm,  prompt=complete_query, verbose=self.verbose)
            chain_result = chain.run(prompt=complete_query).strip()
            print("RESULT IS ", chain_result)
            return chain_result

    def sub_goal_generation(self, factors: dict, model_speed:str):
        """Serves to generate sub goals for the user and drill down into it"""

        prompt = """
            Based on all the history and information of this user, GOALS PROVIDED HERE  {% for factor in factors %} '{{ factor['name'] }}'{% if not loop.last %}, {% endif %}{% endfor %} 
             provide a mind map representation of the secondary nodes that can be used to narrow down the choice better. Each of the results should have 4 sub nodes.
            Answer a condensed JSON with no whitespaces. The strucuture should only contain the list of subgoal items under field "sub_goals".
            Every subgoal should have a "goal_name" refers to the goal and the list of subgoals with "name" and a "amount" should be shown as a range from 0 to 100, with a value chosen explicilty and shown based on the personal preferences of the user.  
            After the JSON output, don't explain or write anything
            """

        self.init_pinecone(index_name=self.index)
        agent_summary = self._fetch_memories(f"Users core summary", namespace="SUMMARY")
        template = Template(prompt)
        output = template.render(factors=factors)
        print("HERE IS THE AGENT SUMMARY", agent_summary)
        print("HERE IS THE TEMPLATE", output)
        complete_query = str(agent_summary) + output
        complete_query = PromptTemplate.from_template(complete_query)
        if model_speed =='fast':
            output = self.replicate_llm(output)
            return output
        else:
            chain = LLMChain(llm=self.llm,  prompt=complete_query, verbose=self.verbose)
            chain_result = chain.run( prompt=complete_query).strip()
            print("RESULT IS ", chain_result)
            return chain_result

    def extract_info(self, s):
        lines = s.split('\n')
        name = lines[0]
        address = lines[1].replace('Address: ', '')
        phone = lines[2].replace('Phone: ', '')
        website = lines[3].replace('Website: ', '')
        return {
            'name': name,
            'address': address,
            'phone': phone,
            'website': website,
        }
    def restaurant_generation(self, factors: dict, model_speed:str):
        """Serves to suggest a restaurant to the agent"""

        prompt = """
              Based on the following factors, There are {% for factor, value in factors.items() %}'{{ factor }}'{% if not loop.last %}, {% endif %}{% endfor %} factors I want to consider.
                {% for factor, value in factors.items() %}
                For '{{ factor }}', I want the meal to be '{{ value }}' points on a scale of 1 to 100 points{% if not loop.last %}.{% else %}.{% endif %}
                {% endfor %}
                Determine the type of restaurant you should offer to a customer. Make the recomendation very short and to a point, as if it is something you would type on google maps
            """

        self.init_pinecone(index_name=self.index)
        agent_summary = self._fetch_memories(f"Users core summary", namespace="SUMMARY")
        template = Template(prompt)
        output = template.render(factors=factors)
        complete_query = str(agent_summary) + output
        # print('HERE IS THE COMPLETE QUERY', complete_query)
        complete_query = PromptTemplate.from_template(complete_query)
        chain = LLMChain(llm=self.llm, prompt=complete_query, verbose=self.verbose)
        chain_result = chain.run(prompt=complete_query).strip()
        GPLACES_API_KEY = self.GPLACES_API_KEY
        places = GooglePlacesTool()
        output = places.run(chain_result)
        restaurants = re.split(r'\d+\.', output)[1:3]
        # Create a list of dictionaries for each restaurant
        restaurant_list = [self.extract_info(r) for r in restaurants]
        print('HERE IS THE OUTPUT', restaurant_list)
        return restaurant_list
    async def run_wolt_tool(self, zipcode, chain_result):
        from food_scrapers import  wolt_tool
        return wolt_tool.main(zipcode, chain_result)
    async def delivery_generation(self, factors: dict, zipcode:str, model_speed:str):
        """Serves to optimize agent delivery recommendations"""

        prompt = """
              Based on the following factors, There are {% for factor, value in factors.items() %}'{{ factor }}'{% if not loop.last %}, {% endif %}{% endfor %} factors I want to consider.
                {% for factor, value in factors.items() %}
                For '{{ factor }}', I want the meal to be '{{ value }}' points on a scale of 1 to 100 points{% if not loop.last %}.{% else %}.{% endif %}
                {% endfor %}
                Determine the type of food you would want to recommend to the user, that is commonly ordered online. It should be like burger or pizza or something you search on food delivery app. 
                The response should be very short
            """

        self.init_pinecone(index_name=self.index)
        agent_summary = self._fetch_memories(f"Users core summary", namespace="SUMMARY")
        template = Template(prompt)
        output = template.render(factors=factors)
        complete_query = str(agent_summary) + output
        complete_query = PromptTemplate.from_template(complete_query)
        chain = LLMChain(llm=self.llm, prompt=complete_query, verbose=self.verbose)
        chain_result = chain.run(prompt=complete_query).strip()
        print("HERE IS THE PROMPT", chain_result)
        import asyncio
        from food_scrapers import wolt_tool
        # with ThreadPoolExecutor() as executor:
        #     loop = asyncio.get_running_loop()
        output = await wolt_tool.main( zipcode, chain_result)
        return output

    def solution_evaluation_test(self):
        """Serves to update agent traits so that they can be used in summary"""
        return


    def solution_implementation(self):
        """Serves to update agent traits so that they can be used in summary"""
        return

    # checker_chain = LLMSummarizationCheckerChain(llm=llm, verbose=True, max_checks=2)
    # text = """
    # Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
    # • In 2023, The JWST spotted a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
    # • The telescope captured images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
    # • JWST took the very first pictures of a planet outside of our own solar system. These distant worlds are called "exoplanets." Exo means "from outside."
    # These discoveries can spark a child's imagination about the infinite wonders of the universe."""
    # checker_chain.run(text)


if __name__ == "__main__":
    agent = Agent()
    agent.goal_optimization(factors={}, model_speed="slow")
    # agent._update_memories("lazy, stupid and hungry", "TRAITS")
    #agent.task_identification("I need your help choosing what to eat for my next meal. ")
    # agent.solution_generation( {    'health': 85,
    # 'time': 75,
    # 'cost': 50}, model_speed="slow")