### Contributing

Thanks for considering a contribution!

#### Dev setup
1. Node is not required; this is a Chrome MV3 extension.
2. Python 3.9+ is required for the local server.
3. Create a venv and install deps: `pip install -r requirements.txt`.

#### Directory overview
- `background.js` – service worker, handles API calls and messaging
- `content-script.js` – finds images and draws overlays
- `options.html/js` – settings UI (API URL + optional key)
- `simple_ai_detector.py` – local Flask server that calls Hugging Face
- `docs/` – user and technical documentation

#### Guidelines
- Keep code readable; avoid one-liners that obscure logic
- Prefer early returns over deep nesting
- Add concise comments to explain the “why” of non-obvious decisions
- Update documentation when behavior, ports, or APIs change

#### Submitting changes
1. Fork and branch from `main`
2. Make your changes with clear commit messages
3. Run the local server and verify `/health`
4. Test the extension on a few pages
5. Open a PR describing the change and screenshots if UI-related


