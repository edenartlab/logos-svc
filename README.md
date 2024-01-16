# logos-svc

Run

    `rye run uvicorn app.server:app --reload`

Send a command to the server


    curl -X POST 'http://localhost:5050/tasks/create' \
    -H 'x-api-key: YOUR_API_KEY' \
    -H 'x-api-secret: YOUR_API_SECRET' \
    -H 'Content-Type: application/json' \
    -d '{
    "generatorName": "monologue",
        "config": {
            "characterId": "6577e5d5c77b37642c252423",
            "prompt": "who are you?"
        }
    }'



Tests

    `rye run pytest -s tests`

