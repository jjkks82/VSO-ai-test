import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ─── إعداد مفتاح Gemini API ───────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyDI9Y9dzYJ4GHX280pPlNMbBfWSngiwDAE"
genai.configure(api_key=GEMINI_API_KEY)

# ─── تحديد الموديل بشكل صريح لتجاوز خطأ 404 ──────────────────────────────────
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# ─── شخصية البوت ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "أنت VSO، مساعد ذكي ومتطور. "
    "تجيب دائماً باللغة العربية بأسلوب واضح، منطقي، ومنظم. "
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

    if not user_message:
        return jsonify({"error": "الرسالة لا يمكن أن تكون فارغة."}), 400

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nالمستخدم: {user_message}\n\nVSO:"

        response = model.generate_content(full_prompt)

        reply = response.text.strip()

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"حدث خطأ أثناء المعالجة: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
