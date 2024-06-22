from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd
import os
import socket
import psutil
import uuid

app = Flask(__name__)

# Define CSV files
user_log_file = 'user_log.csv'
network_log_file = 'network_log.csv'

# Ensure the log files exist
if not os.path.exists(user_log_file):
    user_df = pd.DataFrame(columns=['username', 'password', 'login_time', 'logout_time', 'ip_address', 'mac_address'])
    user_df.to_csv(user_log_file, index=False)

if not os.path.exists(network_log_file):
    network_df = pd.DataFrame(columns=['username', 'ip_address', 'mac_address', 'bytes_sent', 'bytes_recv'])
    network_df.to_csv(network_log_file, index=False)

# Helper function to get MAC address
def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
    return mac

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ip_address = request.remote_addr
    mac_address = get_mac_address()

    # Append to user log CSV
    user_df = pd.read_csv(user_log_file)
    new_user_row = pd.DataFrame([{
        'username': username,
        'password': password,
        'login_time': login_time,
        'logout_time': '',
        'ip_address': ip_address,
        'mac_address': mac_address
    }])
    user_df = pd.concat([user_df, new_user_row], ignore_index=True)
    user_df.to_csv(user_log_file, index=False)

    return jsonify({'message': 'Login successful', 'login_time': login_time})

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    username = data['username']

    logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_df = pd.read_csv(user_log_file)

    # Update logout time
    user_df.loc[user_df['username'] == username, 'logout_time'] = logout_time
    user_df.to_csv(user_log_file, index=False)

    # Record network statistics
    ip_address = request.remote_addr
    mac_address = get_mac_address()
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv

    network_df = pd.read_csv(network_log_file)
    new_network_row = pd.DataFrame([{
        'username': username,
        'ip_address': ip_address,
        'mac_address': mac_address,
        'bytes_sent': bytes_sent,
        'bytes_recv': bytes_recv
    }])
    network_df = pd.concat([network_df, new_network_row], ignore_index=True)
    network_df.to_csv(network_log_file, index=False)

    login_time = user_df.loc[user_df['username'] == username, 'login_time'].values[0]

    log_data = {
        'username': username,
        'ip_address': ip_address,
        'mac_address': mac_address,
        'login_time': login_time,
        'logout_time': logout_time,
        'bytes_sent': bytes_sent,
        'bytes_recv': bytes_recv
    }

    return jsonify({'message': 'Logout successful', 'log_data': log_data})

if __name__ == '__main__':
    app.run(debug=True)
