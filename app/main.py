from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from app.db import init_db, SessionLocal, Conversation, Message
from app.prompts import SYSTEM_PROMPT
from app.llm import chat_llm
from app.tools import get_last_k_messages, get_order_status, get_product_info, get_warranty_policy
import json, re
import traceback

app = FastAPI(title="Synapsis Chatbot")

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    user_id: Optional[int] = 1
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    answer: str

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/conversations")
def new_conversation(user_id: Optional[int] = 1):
    with SessionLocal() as s:
        conv = Conversation(user_id=user_id)
        s.add(conv); s.commit(); s.refresh(conv)
        return {"conversation_id": conv.id}

@app.get("/conversations/{cid}/messages")
def get_messages(cid:int):
    with SessionLocal() as s:
        msgs = s.query(Message).filter(Message.conversation_id==cid)\
                .order_by(Message.created_at.asc()).all()
        return [{"role":m.role,"content":m.content,"ts":m.created_at.isoformat()} for m in msgs]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        #Memastikan pesan tidak kosong
        if not req.conversation_id:
            with SessionLocal() as s:
                conv = Conversation(user_id=req.user_id); s.add(conv); s.commit(); s.refresh(conv)
                req.conversation_id = conv.id

        #Menyimpan pesan user
        with SessionLocal() as s:
            s.add(Message(conversation_id=req.conversation_id, role="user", content=req.message))
            s.commit()

        # konteks memory (3 interaksi terakhir)
        history = get_last_k_messages(req.conversation_id, k=3)
        msgs = [{"role":"system","content":SYSTEM_PROMPT}]
        for m in history:
            msgs.append({"role":m.role,"content":m.content})
        msgs.append({"role":"system","content":"Gunakan format planner bila perlu tool."})
        msgs.append({"role":"user","content":req.message})

        # panggil LLM
        raw = chat_llm(msgs)
        content = raw["message"]["content"].strip()

        # Validation apakah LLM meminta tool
        tool_match = re.search(r'\{.*"tool"\s*:\s*".*"\s*,\s*"arguments"\s*:\s*\{.*\}\s*\}', content)
        if tool_match:
            try:
                tool_json = json.loads(tool_match.group(0))
                tool = tool_json.get("tool")
                args = tool_json.get("arguments", {})
                observation = None

                if tool == "order_status":
                    observation = get_order_status(args.get("order_id",""))
                    if not observation:
                        final = "Maaf, saya tidak menemukan pesanan tersebut. Pastikan ID benar."
                    else:
                        final = (f"Status pesanan {observation['id']}: {observation['status']} "
                                f"(kurir {observation['courier']}, resi {observation['tracking_number']}). "
                                f"Produk: {observation['name']}. Terakhir update: {observation['last_update']}.")
                elif tool == "product_info":
                    p = get_product_info(args.get("product_id",""))
                    if not p:
                        final = "Produk tidak ditemukan. Coba cek kembali ID produk."
                    else:
                        final = f"{p['name']} - Fitur:{p['features']}"
                elif tool == "warranty_policy":
                    policy = get_warranty_policy(args.get("product_id", ""))
                    if not policy:
                        final = "Produk tidak ditemukan, jadi saya tidak bisa menampilkan kebijakan garansinya."
                    else:
                        p = get_product_info(args.get("product_id", ""))
                        final = f"Kebijakan garansi untuk produk {p['name']}: {policy}"
                else:
                    final = "Maaf, tool tidak dikenali."

            except Exception:
                final = "Format permintaan tool tidak valid."
        else:
            final = content

        # simpan jawaban bot
        with SessionLocal() as s:
            s.add(Message(conversation_id=req.conversation_id, role="assistant", content=final))
            s.commit()

        return ChatResponse(conversation_id=req.conversation_id, answer=final)
    
    except Exception as e:
        print("🔥 ERROR:", e)
        traceback.print_exc()
        return ChatResponse(conversation_id=req.conversation_id, answer="Terjadi error di server.")