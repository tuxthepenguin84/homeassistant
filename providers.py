import json
import os
from pathlib import Path
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.providers.openai import OpenAIProvider
import sys


# Functions
def get_models():
  models = []
  providers_json = import_params()['providers']
  for provider in providers_json:
    models.append(providers_json[provider]['model_name'])
  return models


def get_providers():
  providers_json = import_params()['providers']
  cloud_providers = []
  for provider in providers_json:
    if providers_json[provider]['type'] == 'cloud':
      cloud_providers.append(provider)
  local_providers = []
  for provider in providers_json:
    if providers_json[provider]['type'] == 'local':
      local_providers.append(provider)
  return cloud_providers, local_providers


def import_params(json_file='params.json'):
  script_dir = os.path.dirname(os.path.abspath(__file__))
  params_file = os.path.join(script_dir, json_file)
  params_json = json.load(open(Path(params_file)))
  if params_json is None:
    print(f'Unable to import {params_file} data')
    sys.exit(1)
  return params_json


# Providers
def ollama(model = None):
  providers_json = import_params()['providers']
  if model:
    model_name = model
  else:
    model_name = providers_json['ollama']['model_name']
  return OpenAIModel(
    model_name = model_name,
    provider = OpenAIProvider(
      base_url = providers_json['ollama']['base_url']
    )
  )


def openai(model = None):
  providers_json = import_params()['providers']
  if model:
    model_name = model
  else:
    model_name = providers_json['openai']['model_name']
  return OpenAIModel(
    model_name = model_name,
    provider = OpenAIProvider(
      api_key = providers_json['openai']['api_key']
    )
  )


def gemini(model = None):
  providers_json = import_params()['providers']
  if model:
    model_name = model
  else:
    model_name = providers_json['gemini']['model_name']
  return GeminiModel(
    model_name = model_name,
    provider = GoogleGLAProvider(
      api_key = providers_json['gemini']['api_key']
    )
  )