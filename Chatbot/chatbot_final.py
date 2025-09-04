import tkinter as tk
import re

# -------- Bot Logic -------- #
main_topics = {
    "emergency": ["call ambulance", "nearest er"],
    "doctors": ["cardiologist", "pediatrician", "orthopedics", "general physician"],
    "appointment": ["book today", "book tomorrow", "cancel"],
    "prescription": ["new prescription", "refill", "view history"],
    "report": ["blood test", "x-ray", "mri"],
    "payment": ["bill summary", "make payment", "insurance claim", "refund request"]
}

sub_topic_responses = {
    "emergency": {
        "call ambulance": "🚑 Dialing 112… Help is on the way!",
        "nearest er": "🏥 Nearest ER: City Hospital, Sector 12. Open 24/7."
    },
    "doctors": {
        "cardiologist": "🫀 Dr. Mehta is available Mon/Wed/Fri 2:30–4:30 PM.",
        "pediatrician": "🧒 Dr. Neha is available Tue/Thu/Sat 1:30–5:30 PM.",
        "orthopedics": "🦴 Dr. Raj is available Daily 10:00–3:00 PM.",
        "general physician": "🩺 Dr. Preeti is available Daily 12:30–4:00 PM."
    },
    "appointment": {
        "book today": "✅ Appointment booked for today at 4 PM.",
        "book tomorrow": "✅ Appointment booked for tomorrow at 11 AM.",
        "cancel": "❌ Appointment successfully cancelled."
    },
    "prescription": {
        "new prescription": "📝 Please visit your doctor for a new prescription.",
        "refill": "💊 Refill request submitted. Your medication will be ready soon.",
        "view history": "📋 View prescriptions under Health Profile > History."
    },
    "report": {
        "blood test": "🧪 Blood test report will be available within 24 hours.",
        "x-ray": "📸 X-Ray reports are available in Diagnostics > My Reports.",
        "mri": "🔍 MRI results will be emailed within 48 hours."
    },
    "payment": {
        "bill summary": "📋 View current charges in Payment > Bill Summary.",
        "make payment": "💳 Pay via UPI, card, or hospital wallet in Payment > Make Payment.",
        "insurance claim": "🛡️ Begin insurance-related payments via Payment > Insurance Claim.",
        "refund request": "🔄 Refunds for overcharges/cancellations: Payment > Refund Request."
    }
}

current_topic = None

def chatbot_response(user_input):
    global current_topic
    user_input = user_input.lower()

    if user_input in ["yes", "yeah", "yep", "sure", "another", "continue"]:
        current_topics = None
        return "Great! 😊 Choose a topic below:", list(main_topics.keys())

    if user_input in ["no", "nope", "nah"]:
        current_topic = None
        return "It was a pleasure assisting you! 😊 Type 'yes' for help again.", []

    if re.search(r"(hi+|hello+|hey+|hlo+)", user_input):
        current_topic = None
        return "Welcome to HealthCare Assistant 🏥\nChoose a topic below:", list(main_topics.keys())

    for topic in main_topics:
        if topic in user_input:
            current_topic = topic
            return f"What do you need help with in {topic.title()}?", main_topics[topic]

    if current_topic:
        for sub in main_topics[current_topic]:
            if re.search(rf"\b{sub}\b", user_input):
                response = sub_topic_responses[current_topic][sub]
                current_topic = None
                return response + "\nWould you like help with another topic?", ["yes", "no"]
        return f"Sorry... I didn’t catch that. Try choosing one below.", main_topics[current_topic]

    return "I’m not sure I understood that 🧐 Try saying 'Hello' to begin again.", []

# -------- GUI Setup -------- #
def add_message(text, sender="bot", options=None):
    outer = tk.Frame(chat_frame, bg="#f2f6fc")
    bubble = tk.Frame(outer, bg="#c8e6c9" if sender=="user" else "#e1f5fe", pady=6, padx=8)

    label = tk.Label(bubble, text=text, wraplength=400, justify="left",
                     font=("Segoe UI", 10), bg=bubble["bg"])
    label.pack(anchor="w")

    if sender == "bot" and options:
        option_frame = tk.Frame(bubble, bg=bubble["bg"])
        option_frame.pack(anchor="w", pady=(6,0))
        for opt in options:
            btn = tk.Button(option_frame, text=opt.title(), font=("Segoe UI", 9),
                            bg="#006699", fg="white", bd=0, relief=tk.RAISED,
                            activebackground="#007fbf",
                            command=lambda val=opt: send_message(val))
            btn.pack(side=tk.LEFT, padx=4)

    # Align bubble within outer frame
    if sender == "user":
        bubble.pack(anchor="e")
        outer.pack(anchor="e", fill="x", pady=4, padx=(200,10))
    else:
        bubble.pack(anchor="w")
        outer.pack(anchor="w", fill="x", pady=4, padx=(10,200))

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def send_message(text=None):
    user_input = text or entry.get()
    if not user_input.strip():
        return
    entry.delete(0, tk.END)
    add_message(f"You: {user_input}", "user")

    response, options = chatbot_response(user_input)
    add_message(f"Bot: {response}", "bot", options)

root = tk.Tk()
root.title("HealthCare Chatbot 🏥")
root.geometry("720x620")
root.configure(bg="#f2f6fc")

entry_frame = tk.Frame(root, bg="#f2f6fc")
entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5,10))

entry = tk.Entry(entry_frame, font=("Segoe UI", 11), bg="white", relief=tk.SOLID)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10), ipady=8)
entry.bind("<Return>", lambda e: send_message())

send_btn = tk.Button(entry_frame, text="Send", font=("Segoe UI", 10, "bold"),
                     bg="#006699", fg="white", activebackground="#0099cc",
                     relief=tk.RAISED, bd=0, command=send_message)
send_btn.pack(side=tk.RIGHT, ipadx=10, ipady=5)

canvas = tk.Canvas(root, bg="#f2f6fc", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
chat_frame = tk.Frame(canvas, bg="#f2f6fc")

canvas.create_window((0,0), window=chat_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0))
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Initial welcome message
welcome, options = chatbot_response("hello")
add_message(f"Bot: {welcome}", "bot", options)

root.mainloop()