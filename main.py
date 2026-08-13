import os
import sys

if sys.platform.startswith('linux'):
    os.environ.setdefault(
        'QTWEBENGINE_CHROMIUM_FLAGS',
        '--disable-gpu --no-sandbox --disable-gpu-compositing',
    )

import webview

from orphan_tl_cleaner.gui import Api, build_html


def main():
    api = Api()
    html = build_html()

    window = webview.create_window(
        "Limpiador de TLs Hu\u00e9rfanas",
        html=html,
        js_api=api,
        width=1000,
        height=700,
        resizable=True,
    )

    api.window = window
    webview.start(gui='qt')


if __name__ == '__main__':
    main()
