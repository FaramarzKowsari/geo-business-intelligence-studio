from __future__ import annotations

import http.client
import multiprocessing
import os
import socket
import sys
import threading
import time
import webbrowser


def find_available_port(start: int = 8765, attempts: int = 25) -> int:
    requested = os.getenv("GEOBUSINESS_PORT")
    if requested:
        return int(requested)
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("No available local port was found.")


def wait_until_ready(port: int, attempts: int = 120) -> bool:
    for _ in range(attempts):
        try:
            connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
            connection.request("GET", "/api/health")
            response = connection.getresponse()
            response.read()
            connection.close()
            if 200 <= response.status < 400:
                return True
        except OSError:
            pass
        time.sleep(0.25)
    return False


def show_error(message: str) -> None:
    try:
        import tkinter.messagebox

        tkinter.messagebox.showerror("GeoBusiness Intelligence Studio", message)
    except Exception:
        print(message, file=sys.stderr)


def prepare_environment(port: int) -> None:
    os.environ.setdefault("APP_ENV", "desktop")
    os.environ.setdefault(
        "APP_CONTACT_EMAIL",
        "https://github.com/FaramarzKowsari/geo-business-intelligence-studio",
    )
    os.environ["APP_HOST"] = "127.0.0.1"
    os.environ["APP_PORT"] = str(port)


def run_headless(port: int) -> None:
    import uvicorn

    from app.main import app

    uvicorn.run(app, host="127.0.0.1", port=port, workers=1, log_level="warning")


def run_desktop_controller(port: int) -> None:
    import tkinter as tk
    from tkinter import ttk

    import uvicorn

    from app.main import app

    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    if not wait_until_ready(port):
        server.should_exit = True
        raise RuntimeError("The local web server did not become ready.")

    url = f"http://127.0.0.1:{port}"
    if os.getenv("GEOBUSINESS_NO_BROWSER", "").casefold() not in {"1", "true", "yes"}:
        webbrowser.open(url)

    root = tk.Tk()
    root.title("GeoBusiness Intelligence Studio")
    root.geometry("520x245")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=24)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="GeoBusiness Intelligence Studio", font=("Segoe UI", 17, "bold")).pack(
        anchor="w"
    )
    ttk.Label(
        frame,
        text=(
            "The application is running locally and is available only on this computer. "
            "Keep this window open while using the browser dashboard."
        ),
        wraplength=465,
        justify="left",
    ).pack(anchor="w", pady=(12, 8))
    ttk.Label(frame, text=url, font=("Consolas", 10)).pack(anchor="w", pady=(0, 18))

    buttons = ttk.Frame(frame)
    buttons.pack(fill="x")
    ttk.Button(buttons, text="Open dashboard", command=lambda: webbrowser.open(url)).pack(
        side="left"
    )

    def stop() -> None:
        server.should_exit = True
        root.after(100, root.destroy)

    ttk.Button(buttons, text="Stop application", command=stop).pack(side="right")
    root.protocol("WM_DELETE_WINDOW", stop)
    root.mainloop()
    server.should_exit = True
    server_thread.join(timeout=5)


def main() -> None:
    try:
        port = find_available_port()
        prepare_environment(port)
        if os.getenv("GEOBUSINESS_NO_UI", "").casefold() in {"1", "true", "yes"}:
            run_headless(port)
        else:
            run_desktop_controller(port)
    except Exception as exc:
        show_error(f"The application could not start.\n\n{exc}")
        raise


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
