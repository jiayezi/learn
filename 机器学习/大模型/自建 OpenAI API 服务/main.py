import json
import uuid
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Literal, Optional
from model import generate_reply, generate_stream

app = FastAPI()

# OpenAI 接口兼容格式
class Message(BaseModel):
    role: Literal["user", "system", "assistant"]
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 1
    stream: Optional[bool] = False

@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "local",
                "object": "model",
                "owned_by": "local-user",
            }
        ]
    }

@app.post("/v1/chat/completions")
def chat_completions(request: ChatRequest):
    # 转换为 chat template 格式
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    if request.stream:
        def stream_generator():
            for chunk in generate_stream(messages, request.max_tokens, request.temperature):
                data = {
                    "id": f"chatcmpl-{uuid.uuid4().hex}",
                    "object": "chat.completion.chunk",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {
                                "content": chunk
                            },
                            "finish_reason": None
                        }
                    ]
                }
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

            # 结束标志
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_generator(), media_type="text/event-stream")

    else:
        reply = generate_reply(messages, request.max_tokens, request.temperature)
        return {
            "id": f"chatcmpl-{uuid.uuid4().hex}",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": reply
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
