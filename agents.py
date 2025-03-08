import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import requests
import sys
from typing import Union


# Alignment Agent
class Command(BaseModel):
  cmd: str = Field(description="""The command to run on the linux command line""")

class Services(BaseModel):
  service: str = Field(description="""Type of service (camera, garage, lights, plugs, sprinklers, etc)""")
  device: str = Field(description="""Name of the device""")
  action: str = Field(description="""Action to take on the device (on, off, start, stop, health, status,
                      light color, light temperature, etc). It could also be a preset for a camera to apply""")

class Weather(BaseModel):
  city: str
  state: str

class NoOp(BaseModel):
  None

Response = Union[Command, Services, Weather, NoOp]

alignment_agent = Agent(
  result_type = Response,
  system_prompt = ("""You are a friendly home assistant and your job is to help
                   perform automation tasks for the user. The user is going
                   to ask you to perform tasks and you need to match it with
                   the lists below. There are multiple device types and
                   different device types can perform different functions."""),
  model_settings = {'temperature': 0.0},
  retries = 0
)

@alignment_agent.system_prompt
def ha_command() -> str:
  return """If the user asks you to run a command, provide the exact command needed
  to perform the action for the user on the Linux command line."""

@alignment_agent.system_prompt
def ha_services(ctx: RunContext[str]) -> str:
  return f"Here are the available services with the devices and actions they can perform:{ctx.deps}"

@alignment_agent.system_prompt
def ha_weather() -> str:
  return """The user may ask you about the weather and provide a location."""

@alignment_agent.result_validator
def validate_result(ctx: RunContext[str], result: Response) -> Response:
  if isinstance(result, Command):
    return result
  elif isinstance(result, Services):
    service = result.service
    device = result.device
    action = result.action
    all_services = ctx.deps['services']
    service_name = all_services[service]
    devices = service_name['devices']
    actions = service_name['actions']
    if service in all_services and device in devices and action in actions:
      return result
    return NoOp()
  elif isinstance(result, Weather):
    return result
  return NoOp()


# Action Agent
action_agent = Agent(
  result_type = str,
  system_prompt = ("""You are a friendly home assistant and your job is to
                   help perform automation tasks for the user. Take the
                   user input and apply it to only one of the tools
                   below it best aligns with. Do not run any of the tools
                   or functions twice. Describe in detail any actions you
                   performed. If you run the command function just print
                   the command in single quotes with no addtional details
                   or descriptions."""),
  model_settings = {'temperature': 0.0},
  retries = 0
)


# Command
@action_agent.tool_plain
def show_command(cmd: str) -> str:
  """Print out a command"""
  return cmd


# Service Camera
@action_agent.tool_plain
def apply_camera_preset(device: str, action: str) -> str:
  """Apply a specific preset to a camera, move the camera to a specific view"""
  camera_def = {
    'camera-nursery': 'cam1.mydomain.com'
  }
  preset_def = {
    'room': '1',
    'privacy': '2',
    'crib': '3',
    'closet': '4',
    'window': '5',
    'floor': '6'
  }
  passed_camera = camera_def[device]
  passed_preset = preset_def[action]
  url = f"http://{passed_camera}/cgi-bin/ptz.cgi?action=start&channel=0&code=GotoPreset&arg1=1&arg2={passed_preset}&arg3=0"
  r = requests.get(url)
  return device, action, r.status_code, r.text


# Service Garage
@action_agent.tool_plain
def garage_door(device: str, action: str) -> str:
  """Open or close the garage door as well as get health and status
  of the garage door service"""
  url = f"https://garagedoor.mydomain.com/{action}"
  if action == 'close' or action == 'open':
    passed_action = requests.put(url)
  elif action == 'health' or action == 'status':
    passed_action = requests.get(url)
  return device, action, passed_action.status_code, passed_action.text


# Service Bulbs Lights or Plugs On/Off
@action_agent.tool_plain
def turn_bulbs_lights_or_plugs_on_off(device: str, action: str) -> str:
  """Turn bulbs, lights, or plugs on or off."""
  r = requests.put(f"https://iot.mydomain.com/power{action}/{device}")
  return device, action, r.status_code, r.text


# Service Lights Brightness
@action_agent.tool_plain
def adjust_light_brightness(device: str, action: str) -> str:
  """Adjust light brightness ['dim', 'mid', 'bright']."""
  brightness = {
    'dim': 20,
    'mid': 50,
    'bright': 100,
    'default': 20
  }
  new_device_state = {
    'devicename': device,
    'requestedbrightness': brightness[action]
  }
  r = requests.put('https://iot.mydomain.com/brightness', data=new_device_state)
  return device, action, r.status_code, r.text


# Service Lights Temperature
@action_agent.tool_plain
def adjust_light_temperature(device: str, action: str) -> str:
  """Adjust light temperature ['warm', 'sunlight', 'cool']."""
  temperature = {
    'warm': 3000,
    'sunlight': 4800,
    'cool': 6500,
    'default': 3000
  }
  new_device_state = {
    'devicename': device,
    'requestedtemperature': temperature[action]
  }
  r = requests.put('https://iot.mydomain.com/temperature', data=new_device_state)
  return device, action, r.status_code, r.text


# Service Lights Color
@action_agent.tool_plain
def adjust_light_color(device: str, action: str) -> str:
  """Adjust light color ['red', 'orange', 'yellow', 'green', 'aqua', 'blue', 'purple']."""
  hue = {
    'red': 0,
    'orange': 10,
    'yellow': 40,
    'green': 120,
    'aqua': 180,
    'blue': 240,
    'purple': 300
  }
  new_device_state = {
    'devicename': device,
    'requested_hue': hue[action],
    'requested_saturation': 100,
    'requested_value': 100
  }
  r = requests.put('https://iot.mydomain.com/hsv', data=new_device_state)
  return device, action, r.status_code, r.text


# Service Sprinklers
@action_agent.tool_plain
def sprinkler_system(device: str, action: str) -> str:
  """Perform various actions on the sprinkler system, start, stop,
  perform a rain delay, get the health, and status."""
  zone_def = {
    'front-bed': '1',
    'front-lawn': '2',
    'side-fence': '3',
    'back-fence': '4',
    'back-garden': '5'
  }
  if device not in zone_def and action == 'start':
    return device, action, 400, 'bad request'
  base_url = 'https://sprinkles.mydomain.com/'
  url = f"{base_url}{action}"
  if action in ['health', 'status']:
    passed_action = requests.get(url)
  elif action in ['deleteraindelay']:
    passed_action = requests.delete(url = f"{base_url}raindelay")
  elif action in ['getraindelay']:
    passed_action = requests.get(url = f"{base_url}raindelay")
  elif action in ['putraindelay']:
    passed_action = requests.patch(url = f"{base_url}raindelay")
  elif action in ['start']:
    passed_action = requests.put(url = f"{base_url}runadhoc/{zone_def['device']}")
  elif action in ['stop']:
    passed_action = requests.delete(url)
  return device, action, passed_action.status_code, passed_action.text


# Weather
@action_agent.tool_plain
def get_weather(city: str, state: str) -> str:
  """Get the current weather and air quailty index based on city and state"""
  script_dir = os.path.dirname(os.path.abspath(__file__))
  git_dir = os.path.dirname(script_dir)
  sys.path.insert(1, os.path.join(git_dir, 'weather'))
  import weather
  return weather.main(city, state, False)