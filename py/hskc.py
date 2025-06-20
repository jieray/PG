#莫名其妙gt群分享，需要Flask环境，使用方法运行脚本后浏览器反正http://127.0.0.1:5000/hsck?格式=m3u

#!/usr/bin/env python3
from flask import Flask, request, Response
import requests
import base64
import re

app = Flask(__name__)

def base64_decode(s):
    return base64.b64decode(s).decode('utf-8', errors='ignore')

def fix_url(url_str):
    return re.sub(r'https?:\/\/.*?http', 'http', url_str, count=1)

@app.route('/hsck')
def handle():
    url = "https://ghfast.top/https://raw.githubusercontent.com/fuxkjd/hsck/main/dist/all.json"
    json_data = requests.get(url).json()

    fmt = request.args.get('格式')  

    output_lines = []

    if fmt == 'm3u':
        output_lines.append('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"')

    for item in json_data:
        title = base64_decode(item['title'])
        media = base64_decode(item['media'])
        img = base64_decode(item['thumd'])

    
        img = fix_url(img)

        if fmt == 'm3u':
         
            line = f'#EXTINF:-1 http-user-agent="your-agent" tvg-logo="{img}", {title}'
            output_lines.append(line)
            output_lines.append(media)
        else:
            output_lines.append(f"{title} , {media}")

    return Response("\n".join(output_lines), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
