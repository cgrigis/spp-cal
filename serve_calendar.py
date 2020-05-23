"""
Generate shift calendar for La Fève
"""
import io
import logging
import logging.config
import os
import subprocess
import tempfile

from quart import (
    Quart,
    request,
    render_template,
    send_file,
)

from gen_spp_cal import gen_calendar

logging_config = {
    "version": 1,
    "formatters": {
        "simple": {"format": "%(asctime)s [%(name)-10s] %(levelname)-10s %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


app = Quart(__name__)


@app.route("/", methods=["GET"])
async def index():
    return await render_template("index.html")

@app.route("/cal", methods=["GET"])
async def gen_cal():
    args = await request.values
    year, week_id = int(args['year']), int(args['week_id'])

    svg_data = gen_calendar(year, week_id)


    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "cal.svg"), 'w', encoding='utf-8') as f:
            f.write(svg_data)

        subprocess.run([
            "rsvg-convert",
            "--format", "pdf",
            "--output", os.path.join(tmpdirname, "cal.pdf"),
            os.path.join(tmpdirname, "cal.svg"),
            ], check=True)

        with open(os.path.join(tmpdirname, "cal.pdf"), 'rb') as f:
            pdf_data = f.read()

    response_filename = f"calendrier_spp_{year}.pdf"
    response = await send_file(io.BytesIO(pdf_data),
            mimetype="application/pdf",
            as_attachment=True,
            attachment_filename=response_filename)

    return response

@app.route("/", methods=["POST"])
async def train():
#     form = await request.get_json()

    return {"message": "Hello world"}
