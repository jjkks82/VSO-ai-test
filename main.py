import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ─── إعداد عميل Grok ──────────────────────────────────────────────────────────
client = OpenAI(
    api_key="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",
    base_url="https://api.x.ai/v1"
)

# ─── شخصية البوت ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "أنت VSO، مساعد ذكي ومتطور ومتخصص في البرمجة والتقنية والعلوم. "
    "تجيب دائماً باللغة العربية بأسلوب واضح، منطقي، ومنظم. "
    "عند كتابة أكواد برمجية، استخدم دائماً code blocks مع تحديد لغة البرمجة. "
    "مثال: ```python\nprint('hello')\n``` "
    "نسّق إجاباتك بـ Markdown: استخدم ## للعناوين، **نص** للخط العريض، "
    "- للقوائم، والأرقام للخطوات المرتبة. "
    "إذا سألك المستخدم عن هويتك أو مصدرك، أجبه فقط أنك VSO AI. "
    "لا تذكر أي شركة أو نموذج ذكاء اصطناعي آخر تحت أي ظرف."
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"error": "الرجاء إرسال رسالة صحيحة."}), 400

    user_message = data["message"].strip()
    history      = data.get("history", [])

    if not user_message:
        return jsonify({"error": "الرسالة لا يمكن أن تكون فارغة."}), 400

    try:
        # بناء قائمة الرسائل مع السياق السابق
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in history[-12:]:
            messages.append({
                "role":    msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        messages.append({"role": "user", "content": user_message})

        # استدعاء Grok مع تفعيل التفكير العميق
        response = client.chat.completions.create(
            model="grok-3-mini",
            reasoning_effort="high",
            messages=messages,
            max_tokens=4096,
            temperature=0.7
        )

        reply   = response.choices[0].message.content.strip()
        thinking = getattr(response.choices[0].message, "reasoning_content", None)

        result = {"reply": reply}

        if thinking:
            result["thinking"] = thinking.strip()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"حدث خطأ: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
