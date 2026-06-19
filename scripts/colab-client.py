#!/usr/bin/env python3
"""
Colab Remote Client — interact with a Jupyter Lab server running on Colab
via Cloudflare Tunnel, from the command line or programmatically.

Usage:
    python3 colab-client.py --url https://xxx.trycloudflare.com --token mytoken

    # List notebooks
    python3 colab-client.py --url <url> --token <token> ls

    # Upload and run a notebook
    python3 colab-client.py --url <url> --token <token> run notebook.ipynb

    # Create a new notebook
    python3 colab-client.py --url <url> --token <token> create my-notebook

    # Execute a single Python snippet
    python3 colab-client.py --url <url> --token <token> exec "print('hello')"
"""

import argparse
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

import requests


class JupyterClient:
    """Interact with a remote Jupyter Lab server via its REST API."""

    def __init__(self, base_url: str, token: str, verify: bool = True):
        self.base = base_url.rstrip("/")
        self.token = token
        self.verify = verify
        self.headers = {"Authorization": f"Token {token}"}
        self._session = requests.Session()

    def _req(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base}{path}"
        headers = kwargs.pop("headers", {})
        headers.update(self.headers)
        r = self._session.request(
            method, url, headers=headers, verify=self.verify, **kwargs
        )
        r.raise_for_status()
        return r

    # ── Contents API ──────────────────────────────────────────

    def list_contents(self, path: str = "/") -> list:
        """List files and directories in the given path."""
        r = self._req("GET", f"/api/contents/{path.lstrip('/')}")
        data = r.json()
        if isinstance(data, dict) and "content" in data:
            return data["content"]
        return data if isinstance(data, list) else [data]

    def get_notebook(self, path: str) -> dict:
        """Fetch a notebook as a parsed JSON object."""
        r = self._req("GET", f"/api/contents/{path.lstrip('/')}")
        return r.json()

    def save_notebook(self, path: str, notebook: dict) -> dict:
        """Save a notebook JSON object to the server."""
        r = self._req("PUT", f"/api/contents/{path.lstrip('/')}", json={
            "type": "notebook",
            "content": notebook,
            "format": "json",
        })
        return r.json()

    def create_notebook(self, path: str) -> dict:
        """Create a new empty notebook at the given path."""
        r = self._req("POST", "/api/contents", json={
            "type": "notebook",
            "path": path,
        })
        return r.json()

    def upload_file(self, local_path: str, remote_dir: str = "/") -> dict:
        """Upload a local file to the Colab server."""
        name = os.path.basename(local_path)
        remote_path = f"{remote_dir.rstrip('/')}/{name}"
        with open(local_path, "rb") as f:
            r = self._session.put(
                f"{self.base}/api/contents/{remote_path.lstrip('/')}",
                headers=self.headers,
                data={"type": "file", "format": "base64", "content": f.read()},
                verify=self.verify,
            )
        r.raise_for_status()
        return r.json()

    # ── Kernel API ────────────────────────────────────────────

    def start_kernel(self, kernel_name: str = "python3") -> str:
        """Start a new kernel and return its ID."""
        r = self._req("POST", "/api/kernels", json={"name": kernel_name})
        return r.json()["id"]

    def stop_kernel(self, kernel_id: str):
        """Stop/delete a kernel."""
        self._req("DELETE", f"/api/kernels/{kernel_id}")

    def list_kernels(self) -> list:
        """List running kernels."""
        r = self._req("GET", "/api/kernels")
        return r.json()

    def execute_code(self, code: str, kernel_id: str = None,
                     timeout: int = 120) -> dict:
        """
        Execute Python code on a kernel and wait for the result.
        If no kernel_id is given, starts a temporary kernel.
        Returns {'text': '...', 'success': bool, 'execution_count': int}
        """
        import websocket  # pip install websocket-client

        own_kernel = kernel_id is None
        if own_kernel:
            kernel_id = self.start_kernel()

        # Get websocket URL (same origin, upgrade protocol)
        ws_url = self.base.replace("https://", "wss://").replace("http://", "ws://")
        ws_url = f"{ws_url}/api/kernels/{kernel_id}/channels"

        ws = websocket.create_connection(
            ws_url,
            header=self.headers,
            timeout=30,
            skip_verify=not self.verify,
        )

        # Send execute request
        msg_id = str(uuid.uuid4())
        ws.send(json.dumps({
            "header": {
                "msg_id": msg_id,
                "msg_type": "execute_request",
                "username": "",
                "session": str(uuid.uuid4()),
            },
            "parent_header": {},
            "metadata": {},
            "content": {
                "code": code,
                "silent": False,
                "store_history": True,
                "user_expressions": {},
                "allow_stdin": False,
                "stop_on_error": True,
            },
        }))

        # Collect output
        output_text = ""
        success = True
        exec_count = None
        start = time.time()

        try:
            while time.time() - start < timeout:
                ws.settimeout(timeout - (time.time() - start))
                raw = ws.recv()
                if not raw:
                    continue
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                msg_type = msg.get("msg_type", "")
                content = msg.get("content", {})

                if msg_type == "execute_reply":
                    success = content.get("status") == "ok"
                    exec_count = content.get("execution_count")
                    if not success:
                        output_text += f"\nERROR: {content.get('ename')}: {content.get('evalue')}\n"
                    break

                elif msg_type == "stream":
                    output_text += content.get("text", "")

                elif msg_type == "display_data":
                    output_text += content.get("data", {}).get("text/plain", "")

                elif msg_type == "execute_result":
                    exec_count = content.get("execution_count")
                    output_text += content.get("data", {}).get("text/plain", "")

                elif msg_type == "error":
                    success = False
                    output_text += "\n".join(content.get("traceback", []))

        except Exception as e:
            output_text += f"\n<TIMEOUT or WS error: {e}>"
        finally:
            ws.close()
            if own_kernel:
                self.stop_kernel(kernel_id)

        return {"text": output_text.strip(), "success": success, "execution_count": exec_count}

    # ── Session API ───────────────────────────────────────────

    def list_sessions(self) -> list:
        """List active notebook sessions."""
        r = self._req("GET", "/api/sessions")
        return r.json()

    def create_session(self, notebook_path: str, kernel_name: str = "python3") -> dict:
        """Create a session for an existing notebook."""
        path = notebook_path.lstrip("/")
        r = self._req("POST", "/api/sessions", json={
            "path": path,
            "type": "notebook",
            "name": os.path.basename(path),
            "kernel": {"name": kernel_name},
        })
        return r.json()


# ── CLI ──────────────────────────────────────────────────────

def cmd_ls(client: JupyterClient, args):
    path = args.path or "/"
    items = client.list_contents(path)
    for item in items:
        typ = "📄" if item["type"] == "notebook" else "📁" if item["type"] == "directory" else "📎"
        print(f"  {typ} {item['name']:40} {'→ ' + item.get('mimetype', '') if item['type'] == 'file' else ''}")


def cmd_create(client: JupyterClient, args):
    path = args.path if args.path.endswith(".ipynb") else f"{args.path}.ipynb"
    result = client.create_notebook(path)
    print(f"✅ Created notebook: {result['path']}")


def cmd_exec(client: JupyterClient, args):
    result = client.execute_code(args.code, kernel_id=args.kernel,
                                 timeout=args.timeout)
    if result["text"]:
        print(result["text"])
    if result["success"]:
        print(f"\n✅ Executed (count={result['execution_count']})")
    else:
        print(f"\n❌ Execution failed")
        sys.exit(1)


def cmd_run(client: JupyterClient, args):
    """Upload a local .ipynb notebook and execute it via papermill-style API."""
    if not args.notebook.endswith(".ipynb"):
        print("❌ Must be a .ipynb file")
        sys.exit(1)

    name = os.path.basename(args.notebook)
    remote_path = f"/{name}"

    # Upload notebook
    with open(args.notebook) as f:
        nb = json.load(f)
    client.save_notebook(remote_path, nb)
    print(f"📤 Uploaded notebook to {remote_path}")

    # Create session (starts kernel)
    session = client.create_session(remote_path)
    kernel_id = session["kernel"]["id"]
    print(f"🧠 Kernel started: {kernel_id}")

    # Execute all code cells
    for i, cell in enumerate(nb.get("cells", [])):
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell.get("source", []))
        if not source.strip():
            continue
        print(f"  ▶️  Executing cell {i}...")
        result = client.execute_code(source, kernel_id=kernel_id,
                                     timeout=args.timeout)
        # Update cell with output
        cell["outputs"] = [{"output_type": "stream", "name": "stdout",
                           "text": result["text"]}]
        cell["execution_count"] = result["execution_count"]
        if not result["success"]:
            print(f"  ❌ Cell {i} failed:")
            print(result["text"])
            break

    # Save executed notebook
    client.save_notebook(remote_path, nb)
    print(f"\n💾 Executed notebook saved to {remote_path}")

    # Cleanup
    client.stop_kernel(kernel_id)


def main():
    parser = argparse.ArgumentParser(
        description="Remote Colab Jupyter Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  ls [path]       List files/notebooks on the Colab server
  create <path>   Create a new empty notebook
  exec <code>     Execute Python code and return output
  run <file>      Upload and execute a .ipynb notebook
        """,
    )
    parser.add_argument("--url", help="Colab server URL (https://xxx.trycloudflare.com)")
    parser.add_argument("--token", default="colab-finetune", help="Jupyter token")
    parser.add_argument("--timeout", type=int, default=180, help="Execution timeout per cell")

    sub = parser.add_subparsers(dest="command")

    # ls
    p_ls = sub.add_parser("ls")
    p_ls.add_argument("path", nargs="?", default="/", help="Path to list")

    # create
    p_cr = sub.add_parser("create")
    p_cr.add_argument("path", help="Notebook path/name")

    # exec
    p_ex = sub.add_parser("exec")
    p_ex.add_argument("code", help="Python code to execute")
    p_ex.add_argument("--kernel", help="Existing kernel ID (optional)")

    # run
    p_run = sub.add_parser("run")
    p_run.add_argument("notebook", help="Local .ipynb file to upload and execute")
    p_run.add_argument("--kernel", help="Existing kernel ID (optional)")

    args = parser.parse_args()

    if not args.url:
        # Try from env var
        args.url = os.environ.get("COLAB_URL")
    if not args.url:
        print("❌ Provide --url or set COLAB_URL environment variable")
        sys.exit(1)

    client = JupyterClient(args.url, args.token)

    if args.command == "ls":
        cmd_ls(client, args)
    elif args.command == "create":
        cmd_create(client, args)
    elif args.command == "exec":
        cmd_exec(client, args)
    elif args.command == "run":
        cmd_run(client, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
