### API Specification

#### Endpoint
- Method: `POST`
- Path: `/classify`
- Content-Type: `application/json`
- Base URL (default dev): `http://localhost:5001`

#### Request Body
```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

#### Success Response (200)
```json
{
  "label": "ai",        // "ai" | "real"
  "confidence": 0.87     // number in [0,1]
}
```

#### Error Responses
- `400` → invalid payload or unreachable image
```json
{ "error": "imageUrl is required" }
```
- `500` → internal error
```json
{ "error": "<message>" }
```

#### Example cURL (dev)
```bash
curl -s -X POST http://localhost:5001/classify \
  -H 'Content-Type: application/json' \
  -d '{"imageUrl": "https://picsum.photos/600"}'
```

#### Auth (Optional)
- Header: `Authorization: Bearer <API_KEY>`
- Configure `apiKey` in the extension options page

#### Health
- `GET /health` returns `{ status, api_key_configured, api_key_length }`
