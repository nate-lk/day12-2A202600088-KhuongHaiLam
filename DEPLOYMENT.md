# Deployment Information

## Public URL
https://day12-2a202600088-khuonghailam-production-0622.up.railway.app

## Platform
Railway

## Test Commands
```bash
curl -s -X POST https://day12-2a202600088-khuonghailam-production-0622.up.railway.app/ask
     -H "Content-Type: application/json" -d '{"question": "test"}'
```
```
{
    "question": "test",
    "answer": "Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic.",
    "session_id": "705d0c0a-72d6-4c4d-9cfb-d738b6a9e644",
    "timestamp": "2026-04-17T10:58:42.271212+00:00"
}
```

```bash
curl -X POST https://day12-2a202600088-khuonghailam-production-0622.up.railway.app/ask \
   2      -H "X-API-Key: YOUR_KEY" \
   3      -H "Content-Type: application/json" \
   4      -d '{"question": "What is Docker?"}'
```
```
{
    "question": "what is docker",
    "answer": "Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!",
    "session_id": "c73e332f-6a56-4344-ad2b-da07f85b7953",
    "timestamp": "2026-04-17T11:42:15.006031+00:00"
}
```

### Health Check
```bash
curl https://day12-2a202600088-khuonghailam-production-0622.up.railway.app/health

{
    "status": "ok",
    "uptime_seconds": 919.5,
    "timestamp": "2026-04-17T10:55:02.272510+00:00"
}
```

## Environment Variables Set
- `PORT`: 8000
- `REDIS_URL`: (Railway internal URL)
- `AGENT_API_KEY`: any-secure-string-here
- `ENVIRONMENT`: production
- `DAILY_BUDGET_USD`: 5.0

## Screenshots
- [Deployment dashboard](screenshots/deploy_success.png)
- [Test results](screenshots/test.png, test2.png, health.png)