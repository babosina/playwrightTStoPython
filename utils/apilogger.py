import json


class APILogger:

    def __init__(self):
        self._recent_logs: list[dict] = []

    def log_request(self, method: str, url: str, headers: dict[str, str], body: dict | None = None, *args):
        log_entry = {
            "method": method,
            "url": url,
            "headers": headers
        }
        if body is not None:
            log_entry["body"] = body

        self._recent_logs.append({
            "type": "Request Details",
            "data": log_entry
        })

    def log_response(self, status_code: int, body: dict | None = None, *args):
        log_entry = {
            "status_code": status_code
        }
        if body is not None:
            log_entry["body"] = body

        self._recent_logs.append({
            "type": "Response Details",
            "data": log_entry
        })

    def get_recent_logs(self):
        return "\n\n".join([
            f"====={log['type']}=====\n{json.dumps(log['data'], indent=2)}"
            for log in self._recent_logs
        ])
