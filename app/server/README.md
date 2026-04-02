# ITC-OS Presence Server

A Flask-based Python server that tracks Linux users currently logged into the server and exposes a REST API for the course website frontend.

## Requirements

- Python 3.12+
- Linux server where students SSH in
- `flask` and `flask-cors` (see `requirements.txt`)

## Quick Start

```bash
# On the Linux server, from the project root:
cd app/server
pip3 install -r requirements.txt
python3 app.py
```

The server starts on `http://0.0.0.0:5000` by default.

### Options

```bash
python3 app.py --port 8080        # custom port
python3 app.py --host 127.0.0.1   # localhost only (behind reverse proxy)
```

## API Endpoints

| Endpoint | Description |
| --- | --- |
| `GET /api/users` | Currently logged-in users (parsed `who` output) |
| `GET /api/who` | Raw `who` command output |
| `GET /api/last?n=20` | Recent login history from `last` |
| `GET /api/health` | Server health check |

### Example: `/api/users`

```json
{
  "users": [
    {
      "username": "student01",
      "terminal": "pts/0",
      "loginTime": "2026-03-26 10:00",
      "host": "192.168.1.5"
    }
  ],
  "count": 1,
  "timestamp": "2026-03-26T10:30:00Z"
}
```

## Running as a systemd Service

Create `/etc/systemd/system/itc-os-presence.service`:

```ini
[Unit]
Description=ITC-OS Presence Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/ITC-OS-2026/server
ExecStartPre=/usr/bin/pip3 install --quiet -r requirements.txt
ExecStart=/usr/bin/python3 app.py --host 0.0.0.0 --port 5000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable itc-os-presence
sudo systemctl start itc-os-presence
```

## Running Behind Nginx (Recommended)

If you want HTTPS or to serve on port 80/443 alongside other services:

```nginx
server {
    listen 443 ssl;
    server_name your-server.example.com;

    # SSL config...

    # Proxy API requests to the presence server
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Serve static files directly (optional, faster than Python)
    location / {
        root /path/to/ITC-OS-2026;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

## CORS

By default, the server allows all origins (`*`). For production, edit the `CORS_ORIGIN` variable in `app.py` to restrict to your GitHub Pages domain:

```python
CORS_ORIGIN = "https://rathpiseyalpha.github.io"
```

## Frontend Configuration

In `app/js/config.js`, set the server URL:

```javascript
server: {
    url: 'https://your-server.example.com',   // or http://server-ip:5000
    pollInterval: 10000  // poll every 10 seconds
}
```
