import agents
import argparse
import asyncio
import itertools
import json
import logging
import os
from pathlib import Path
import providers
import sys


# Load Home Assistant Configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
ha_file = os.path.join(script_dir, 'ha.json')
ha_config = json.load(open(Path(ha_file)))


# Functions
async def prompt(input_prompt, parsed_args):
  parsed_model = parsed_args.model
  parsed_provider = parsed_args.provider

  # Get Model
  model = getattr(providers, parsed_provider)(model=parsed_model)

  # Send prompt to Alignment Agent
  alignment_response = await agents.alignment_agent.run(input_prompt, deps = ha_config, model = model)
  logging.info(alignment_response.all_messages())

  # Send Alignment Agent response to Action Agent
  action_response = await agents.action_agent.run(str(alignment_response.data), model = model)
  logging.info(action_response.all_messages())
  return action_response.data


async def main(user_input=None, log_level='disabled', model=None, provider='gemini'):
  # Arg Parser
  arg_parser = argparse.ArgumentParser(description='Home Assistant')
  arg_parser.add_argument('--logging', help='Log level', choices=['debug', 'info', 'warning', 'error', 'critical', 'disabled'], default=log_level)
  arg_parser.add_argument('--model', help='Override model in params.json', choices=providers.get_models(), default=model)
  arg_parser.add_argument('--provider', help='Model provider', choices=list(itertools.chain(*providers.get_providers())), default=provider)
  parsed_args = arg_parser.parse_args()
  parsed_logging = parsed_args.logging

  # Logging Config
  if parsed_logging == 'disabled':
    logging.disable()
  else:
    logging.basicConfig(
      format="{asctime} - {levelname} - {message}",
      style="{",
      datefmt="%Y-%m-%d %H:%M:%S",
      level=getattr(logging, parsed_logging.upper()),
    )
    logging.info(parsed_args)
  try:
    if not user_input:
      while True:
        input_prompt = input('> ')
        if input_prompt in ['exit', 'q', 'quit']:
          sys.exit(0)
        response = await prompt(input_prompt, parsed_args)
        print(response)
    else:
      response = await prompt(user_input, parsed_args)
      return response
  except KeyboardInterrupt:
    sys.exit(0)


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  main_loop = loop.run_until_complete(main())


#prompt('Move the nursery camera to point to the crib.')
#prompt('What is the command to get the uptime of the system?')
#prompt('Turn the the lights off in the office.')
#prompt('Turn the bedroom lights off.')
#prompt('Turn off all the lights.')
#prompt('Open the garage door.')
#prompt('What is the weather in San Francisco, CA?')
#prompt('Turn the front-bed sprinkler system on.')