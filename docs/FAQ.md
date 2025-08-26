### FAQ

#### Do I need to be technical to use this?
No. Follow the Quickstart in the README. You’ll copy–paste a key, start the server, and click “Analyze.”

#### What does the badge mean?
Each image gets a label: “AI-generated” or “Real,” with a confidence score (0–100%). It’s an estimate, not a guarantee.

#### Is my data uploaded anywhere?
The local server downloads the image from its original URL to analyze it, then calls the Hugging Face Inference API. The extension itself never uploads your images; it only sends the image URL to your local server. See Ethical Considerations in `docs/ML-Approach.md`.

#### It says “Analyzing…” for too long.
The extension has built-in timeouts. If you still see delays, the model may be warming up or the image host is slow. Try again or refresh the page.

#### Accuracy isn’t great. What can I do?
This repo ships with a general model for demonstration. For best results, we recommend swapping in a stronger detector or fine-tuning a model on your own examples. See `docs/Roadmap.md`.

#### Can I use another API instead of Hugging Face?
Yes. Any server that exposes a compatible `/classify` endpoint will work. Update the API URL in the extension settings.

#### Is there a cost?
Hugging Face may charge for API usage depending on your plan. Check your account for details.


