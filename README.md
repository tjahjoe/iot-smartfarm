# iot-smartfarm# iot-smartfarm os windows

install node = v20.11.0
install python = 3.12.4

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
3. activate restful api
   - path iot-smartfarm
   - cd server
   - python main.py
4. activate detection and streaming
   - path iot-smartfarm
   - cd server
   - python detection.py
5. access website
   - path iot=smartfarm
   - cd src\views
   - login.html
