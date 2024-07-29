from mle_core.chat import ChatService

import asyncio
from dotenv import load_dotenv
from mle_core.chat.chat_service import ChatService

load_dotenv()


async def main():
    chat_service = ChatService(
        'openai', # or "azure" or "anthropic", 
    )

    model_params = {
        "model_name": "gpt-3.5-turbo",
        "pydantic_model": None,
        "method": "sync",
    }

    input_params = {
        "system_message": 'You are a sophisticated assistant trained to analyze sentiments and classify comments accurately.',
        "user_message": '''
            Classify the following comment as:
            category: 'in favor', 'against', or 'neutral' 
            based on the following post:
            Post: Karnataka transport department seizes 133 bike taxis in Bengaluru - Speechless!!
            Comment: Start walking guys. Walk on the road if you don't have footpath. Take metros, buses, protect your phone and wallet. If everyone starts doing this, Auto drivers will start protesting to ban walking next.
            The final output should be in the following Json format:
            {
                "category": "<category>",
                "reason": "<reason>"
            }
            Your Task:
            Analyze the given comment and classify it accordingly. Remember to format your response, as shown in the example.
        ''',
        "keywords": {
              "city": "Bangalore",
              "post": "Discussion in reddit by some user",
              "comment": "Comment placed by other users on the post",
              "category": "'in favor', 'against', or 'neutral'",
              "reason": ""
        },
    }

    output_params = {
        "response_method": 'invoke',
        "is_structured": False,
        "temperature": 0.2,
        "max_tokens": 1000
    }

    options = {
        "grammar_check": True,
        "keyword_check": False,
        "optimize_prompt": True,
        "validate_example": True,
        "validate_tests": True
    }

    tests = [
        {
            "input": {
                "post": "Government announces new cybersecurity measures to protect personal data.",
                "comment": "This is just what we needed. Privacy is paramount, and these steps are crucial for safety."
            },
            "output": {
                "category": "in favor",
                "reason": "The comment supports the government's action, highlighting the importance of privacy and safety."
            }
        },
        {
            "input": {
                "post": "New city park opens downtown to the public.",
                "comment": "Why invest in parks when we need more hospitals?"
            },
            "output": {
                "category": "against",
                "reason": "The comment criticizes the allocation of resources, suggesting that other infrastructure is more needed."
            }
        },
        {
            "input": {
                "post": "Local school district adopts new digital learning tools for classrooms.",
                "comment": "I guess this could be good, but how will they train the teachers to use these tools effectively?"
            },
            "output": {
                "category": "neutral",
                "reason": "The comment expresses uncertainty and concern about the implementation of new tools, showing neither direct support nor opposition."
            }
        }
    ]

    examples = [
        {
            "input": {
                "post": "Major tech company launches new smartphone with innovative features.",
                "comment": "All these features and still the same old battery life. Not buying it!"
            },
            "output": {
                "category": "against",
                "reason": "The comment disapproves of the new product due to its inadequate improvement in battery life."
            }
        },
        {
            "input": {
                "post": "Celebrity chef opens a new vegan restaurant in the city center.",
                "comment": "Fantastic news! More plant-based options are better for health and the environment."
            },
            "output": {
                "category": "in favor",
                "reason": "The comment applauds the opening of the restaurant, highlighting its benefits for health and the environment."
            }
        },
        {
            "input": {
                "post": "Local government plans to increase property taxes to fund educational reforms.",
                "comment": "The intention is good, but are there no other ways to fund this without burdening homeowners?"
            },
            "output": {
                "category": "neutral",
                "reason": "The comment questions the method of funding, showing concern without outright rejection or approval of the tax increase."
            }
        }
    ]

    response = chat_service.get_response(model_params, input_params, output_params,  options, tests, examples)    
    print(response)

asyncio.run(main())
