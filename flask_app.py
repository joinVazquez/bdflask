from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
download_links = []

@app.route('/upload_link', methods=['POST'])
def upload_link():
    link = request.json.get('link')
    timestamped_link = {'link': link, 'timestamp': datetime.now().isoformat()}
    download_links.append(timestamped_link)
    return jsonify({"status": "success"}), 200

@app.route('/get_last_link', methods=['GET'])
def get_last_link():
    if download_links:
        # Pega o link com a marca de tempo mais recente
        last_link = max(download_links, key=lambda x: x['timestamp'])['link']
    else:
        last_link = None
    return jsonify({"link": last_link}), 200

@app.route('/clear_last_link', methods=['POST'])
def clear_last_link():
    print("Requisição recebida para limpar os links. Estado atual:", download_links)
    if download_links:
        download_links.clear()
        print("Links após limpeza:", download_links)
        return jsonify({"status": "success", "message": "Last link cleared"}), 200
    return jsonify({"status": "error", "message": "No link to clear"}), 404


@app.route('/clear_downloaded_link', methods=['POST'])
def clear_downloaded_link():
    global download_links
    if download_links:
        download_links.clear()
        return jsonify({"status": "success", "message": "Download link cleared"}), 200
    return jsonify({"status": "error", "message": "No link to clear"}), 404


if __name__ == '__main__':
    app.run(port=5002)

