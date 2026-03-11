import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode

# --- Configuration via Environment Variables ---
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_DIR = os.environ.get("LOG_DIR", "logs")
QR_DIR = os.environ.get("QR_DIR", "qr_codes")
QR_FILL_COLOR = os.environ.get("QR_FILL_COLOR", "black")
QR_BACK_COLOR = os.environ.get("QR_BACK_COLOR", "white")

# --- Setup Logging ---
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
log_filename = Path(LOG_DIR) / f"qr_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def generate_qr_code(url: str, output_dir: str = QR_DIR) -> str:
    """
    Generate a QR code for the given URL and save it to the output directory.

    Args:
        url: The URL to encode in the QR code.
        output_dir: Directory where the QR code image will be saved.

    Returns:
        The file path of the saved QR code image.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
    filename = f"qr_{safe_name}_{timestamp}.png"
    filepath = Path(output_dir) / filename

    logger.info(f"Generating QR code for URL: {url}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=QR_FILL_COLOR, back_color=QR_BACK_COLOR)
    img.save(filepath)

    logger.info(f"QR code saved to: {filepath}")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="QR Code Generator")
    parser.add_argument(
        "--url",
        type=str,
        default="http://github.com/djnv34",
        help="The URL to encode into a QR code.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=QR_DIR,
        help="Directory to save the generated QR code images.",
    )
    args = parser.parse_args()

    logger.info("=== QR Code Generator Started ===")
    logger.info(f"URL: {args.url}")
    logger.info(f"Output Directory: {args.output_dir}")
    logger.info(f"Fill Color: {QR_FILL_COLOR} | Background Color: {QR_BACK_COLOR}")

    try:
        output_path = generate_qr_code(args.url, args.output_dir)
        logger.info(f"Success! QR code generated at: {output_path}")
    except Exception as e:
        logger.error(f"Failed to generate QR code: {e}", exc_info=True)
        sys.exit(1)

    logger.info("=== QR Code Generator Finished ===")


if __name__ == "__main__":
    main()
