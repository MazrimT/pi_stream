from flask import Blueprint, render_template, request, current_app
import subprocess
import os
import signal
from flask_login import login_required

settings = Blueprint("settings", __name__)


@settings.route("/settings", methods=["POST", "GET"], endpoint="settings")
@login_required
def v_settings():

    def set_conf_from_post(key, fallback) -> None:
        if request.form.get(key):
            setattr(conf, key, request.form[key])
        else:
            setattr(conf, key, fallback)

    conf = current_app.config["stream_config"]

    # update config
    if request.method == "POST":
        set_conf_from_post("stream_key", conf.stream_key)
        set_conf_from_post("streaming_service", conf.streaming_service)
        set_conf_from_post("resolution", conf.resolution)
        set_conf_from_post("bitrate", conf.bitrate)
        set_conf_from_post("preset", conf.preset)
        set_conf_from_post("maxrate", conf.maxrate)
        set_conf_from_post("bufsize", conf.bufsize)
        set_conf_from_post("threads", conf.threads)
        set_conf_from_post("framerate", conf.framerate)
        set_conf_from_post("overlay_url", conf.overlay_url)
        set_conf_from_post("streaming", "off")


    # if starting to stream
    if conf.streaming == "on" and not conf.stream_process_id:
        commands = [
            current_app.config["PYTHON_EXECUTABLE"],
            f"{current_app.root_path}/lib/streamer.py",
            "--streaming_service",
            conf.streaming_service,
            "--stream_key",
            conf.stream_key,
            "--resolution",
            conf.resolution,
            "--bitrate",
            conf.bitrate,
            "--preset",
            conf.preset,
            "--bufsize",
            conf.bufsize,
            "--threads",
            conf.threads,
            "--framerate",
            conf.framerate,
            "--streaming",
            conf.streaming,
        ]

        streaming_process = subprocess.Popen(commands)
        current_app.logger.info(f"Starting stream, PID: {streaming_process.pid}")
        conf.stream_process_id = streaming_process.pid

    if conf.streaming == "off" and conf.stream_process_id:
        current_app.logger.info(f"Stopping stream, PID: {conf.stream_process_id}")
        os.kill(conf.stream_process_id, signal.SIGTERM)
        conf.stream_process_id = None



    return render_template(
        "settings.html",
        method=request.method,
        conf=conf,
        options=conf.options
    )
