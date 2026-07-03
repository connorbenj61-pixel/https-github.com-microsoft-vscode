import json
from pathlib import Path
import webbrowser


HTML_TEMPLATE = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Pyodide Preview - {name}</title>
  </head>
  <body>
    <h3>Pyodide Preview: {name}</h3>
    <pre id="output"></pre>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
    <script>
      async function main() {{
        const pyodide = await loadPyodide();
        const code = {code_json};
        try {{
          await pyodide.runPythonAsync(code);
        }} catch (e) {{
          document.getElementById('output').textContent = 'Error: ' + e;
        }}
      }}
      main();
    </script>
  </body>
</html>
"""


def publish_to_browser(script_path: Path, out_dir: Path | None = None, open_browser: bool = True) -> Path:
    """Create an HTML file that runs the given Python script using Pyodide in the browser.

    Returns the path to the generated HTML file.
    """
    script_path = Path(script_path)
    if out_dir is None:
        out_dir = script_path.parent / 'dist' / 'web'
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    name = script_path.stem
    code = script_path.read_text(encoding='utf-8')
    # JSON-encode the code so it's safe to embed in JS
    code_json = json.dumps(code)

    html = HTML_TEMPLATE.format(name=name, code_json=code_json)

    out_path = out_dir / f"{name}.html"
    out_path.write_text(html, encoding='utf-8')

    print(f"Published {script_path} to {out_path}")
    if open_browser:
        webbrowser.open(out_path.as_uri())
    return out_path


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Publish Python script to browser via Pyodide')
    parser.add_argument('script', help='Path to Python script')
    parser.add_argument('--no-open', dest='open_browser', action='store_false', help="Don't open browser")
    args = parser.parse_args()
    publish_to_browser(Path(args.script), open_browser=args.open_browser)
