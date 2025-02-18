# iot-smartfarm# iot-smartfarm os windows

install node = v20.11.0, python = 3.12.4, atlasmongodb

# usage steps
1. install tailwind
   - path iot-smartfarm
   - cd ..
   - npm install tailwindcss @tailwindcss/cli
2. install server lib
   - path iot-smartfarm
   - cd server
   - python -m venv iot-smartfarm
   - # open cmd
   - iot-smartfarm\Scripts\activate
   - pip install -r requirements.txt
3. connect to mongodb atlas
4. activate restful api
   - path iot-smartfarm
   - cd server
   - python main.py
5. activate detection and streaming
   - path iot-smartfarm
   - cd server
   - python detection.py
6. access website
   - path iot=smartfarm
   - cd src\views
   - login.html
