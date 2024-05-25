from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/forward', methods=['POST'])
def forward_data():
    data = request.json
    print(f"Received data on 6005: {data}")
    id = data['details']['id']
    p = data['details']['p']
    received_data = id - p

    # 处理接收到的数据（这里简单返回数据作为示例）
    return jsonify({"status": "success", "received_data": received_data})

if __name__ == '__main__':
    app.run(port=6003)
