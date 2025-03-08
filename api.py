# Modules
import assistant
import os
from quart import Quart, request
from quart_cors import cors

app = Quart(__name__)
app = cors(app)

@app.route('/request', methods=['PUT'])
async def handle_request():
  user_request = (await request.form)['request']
  response = await assistant.main(user_request, logging, model, provider)
  return response, 200

@app.route('/status', methods=['GET'])
async def handle_status():
  return 'ready', 200

@app.route('/health', methods=['GET'])
async def handle_health():
  return 'up', 200

if __name__ == '__main__':
  logging = os.environ.get('LOGGING', 'info')
  model = os.environ.get('MODEL', '')
  provider = os.environ.get('PROVIDER', 'gemini')
  app.run(host='0.0.0.0', port=5000, debug=False)