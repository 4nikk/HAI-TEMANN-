import os
import smtplib
import calendar
from datetime import datetime
from email.message import EmailMessage
from html import escape

from flask import Flask, request, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ganti-secret-key-ini")

OWNER_EMAIL = "anikdansafitri@gmail.com"

PAGE = r"""
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#641d35">
  <title>Untuk Sebuah Cerita — Anik</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800;900&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --blue:#244d70; --blue-soft:#eaf2f8; --maroon:#641d35;
      --maroon-dark:#481426; --green:#557b65; --green-soft:#edf4ef;
      --paper:#fffdfb; --ink:#24313b; --muted:#71808b;
      --line:#e8e5e2; --shadow:0 22px 65px rgba(42,35,39,.12);
    }
    *{box-sizing:border-box}
    body{margin:0;min-height:100vh;background:
      radial-gradient(circle at 10% 8%,rgba(36,77,112,.10),transparent 28%),
      radial-gradient(circle at 92% 88%,rgba(85,123,101,.12),transparent 26%),#f7f7f5;
      color:var(--ink);font-family:'Nunito',sans-serif;font-weight:700}
    button,input,textarea{font:inherit}
    .topline{height:7px;background:linear-gradient(90deg,var(--blue),#fff 34%,var(--maroon) 67%,var(--green))}
    .shell{width:min(940px,calc(100% - 30px));margin:34px auto 50px}
    .brand{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;color:var(--muted);font-size:12px;letter-spacing:2px;text-transform:uppercase}
    .brand strong{color:var(--maroon);letter-spacing:1px}
    .card{position:relative;overflow:hidden;background:rgba(255,253,251,.96);border:1px solid rgba(255,255,255,.9);border-radius:28px;box-shadow:var(--shadow);padding:clamp(24px,5vw,54px);min-height:560px}
    .page{display:none;animation:arrive .55s ease both}.page.active{display:block}
    @keyframes arrive{from{opacity:0;transform:translateY(13px)}to{opacity:1;transform:translateY(0)}}
    .eyebrow{color:var(--green);font-size:11px;letter-spacing:3px;text-transform:uppercase;font-weight:900}
    h1,h2{font-family:'Playfair Display',serif;color:var(--maroon);line-height:1.15;margin:12px 0}
    h1{font-size:clamp(34px,6vw,56px)} h2{font-size:clamp(29px,5vw,42px)}
    p{color:#697782;line-height:1.8;font-weight:600}
    .intro{text-align:center;max-width:680px;margin:auto}
    .food-frame{width:min(540px,100%);margin:25px auto 18px;position:relative}
    .food-frame:before{content:"";position:absolute;inset:8% 12%;border-radius:50%;background:rgba(100,29,53,.10);filter:blur(28px)}
    .food{position:relative;display:block;width:100%;aspect-ratio:735/447;object-fit:cover;border-radius:22px;box-shadow:0 18px 38px rgba(45,31,25,.2);animation:slowspin 18s linear infinite}
    @keyframes slowspin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
    .food-caption{font-size:12px;letter-spacing:2px;color:var(--green);text-transform:uppercase}
    .actions{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:28px}
    .btn{border:0;border-radius:999px;padding:14px 25px;cursor:pointer;font-weight:900;transition:.2s;display:inline-flex;align-items:center;justify-content:center;gap:9px}
    .btn:hover{transform:translateY(-2px);filter:brightness(1.06)}
    .primary{background:var(--maroon);color:white;box-shadow:0 9px 20px rgba(100,29,53,.2)}
    .secondary{background:var(--blue-soft);color:var(--blue)}
    .back{background:#f0efed;color:#6c747a}
    .calendar-wrap{max-width:490px;margin:28px auto 0;background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px;box-shadow:0 12px 30px rgba(30,40,50,.06)}
    .month{display:flex;justify-content:space-between;align-items:center;color:var(--maroon);font-size:20px;margin-bottom:18px}
    .month small{font-size:11px;color:var(--muted);letter-spacing:2px}
    .calendar{display:grid;grid-template-columns:repeat(7,1fr);gap:7px;text-align:center}
    .dayname{font-size:11px;color:var(--green);padding:8px 0}
    .date{position:relative;aspect-ratio:1;display:grid;place-items:center;color:#56636d;font-size:14px;border-radius:50%}
    .date.empty{visibility:hidden}
    .date.special{color:var(--maroon);font-weight:1000}
    .date.special:after{content:"";position:absolute;inset:3px;border:3px solid #c8323e;border-radius:48% 53% 45% 52%;transform:rotate(-13deg) scale(.2);opacity:0;animation:drawCircle 1.25s .5s ease forwards}
    @keyframes drawCircle{0%{transform:rotate(-13deg) scale(.2);opacity:0}45%{opacity:1}100%{transform:rotate(-13deg) scale(1);opacity:1}}
    .calendar-note{text-align:center;font-size:13px;color:var(--muted);margin:18px 0 0}
    .choice-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:35px auto 0;max-width:650px}
    .choice{border:1px solid var(--line);border-radius:22px;padding:28px 20px;text-align:center;background:white;cursor:pointer;transition:.22s}
    .choice:hover{transform:translateY(-5px);box-shadow:0 15px 28px rgba(30,40,50,.09);border-color:#d5c2c8}
    .choice .emoji{font-size:36px;display:block;margin-bottom:13px}
    .choice h3{margin:0;color:var(--maroon);font-size:19px}
    .choice p{font-size:13px;margin-bottom:0}
    .form-wrap{max-width:650px;margin:25px auto 0}
    .field{margin:17px 0}
    label{display:block;color:var(--blue);font-size:14px;margin-bottom:8px}
    input,textarea{width:100%;border:1.5px solid #dfe4e7;background:#fff;border-radius:13px;padding:14px 15px;outline:none;color:var(--ink);font-weight:700}
    input:focus,textarea:focus{border-color:var(--blue);box-shadow:0 0 0 4px rgba(36,77,112,.08)}
    textarea{min-height:105px;resize:vertical;line-height:1.6}
    .question{padding:17px 18px;background:#f7f8f8;border-radius:16px;margin:14px 0}
    .question label{color:var(--ink);font-weight:900}
    .hint{font-size:12px;color:var(--muted);font-weight:600;margin:7px 0 0}
    .wordcount{font-size:12px;color:var(--green);text-align:right;margin-top:6px}
    .notice{background:var(--green-soft);color:#41624e;border-radius:13px;padding:12px 14px;font-size:12px;line-height:1.6;margin:16px 0}
    .success{text-align:center;padding:50px 10px}
    .success .check{width:74px;height:74px;border-radius:50%;display:grid;place-items:center;margin:auto;background:var(--green-soft);color:var(--green);font-size:34px}
    .footer{text-align:center;color:#9aa2a7;font-size:11px;margin-top:18px;letter-spacing:1px}
    .hidden-trap{position:absolute;left:-9999px;opacity:0;height:0;width:0}
    @media(max-width:600px){.shell{margin:18px auto 30px}.card{min-height:0;border-radius:22px;padding:25px 19px}.choice-grid{grid-template-columns:1fr}.food{border-radius:15px}.brand{font-size:10px}}
  </style>
</head>
<body>
<div class="topline"></div>
<main class="shell">
  <div class="brand"><strong>✦ sebuah cerita kecil</strong><span>Untuk Anik · 2026</span></div>
  <section class="card">
    <div class="page {{ '' if result_message else 'active' }}" id="page1">
      <div class="intro">
        <div class="eyebrow">A little thing about me</div>
        <h1>Hai, selamat datang!</h1>
        <p>Sebelum melangkah lebih jauh, ada satu hal sederhana yang ingin aku tunjukkan.</p>
        <div class="food-frame"><img class="food" src="/static/tahu-tek.jpg" alt="Ilustrasi sepiring tahu tek"></div>
        <div class="food-caption">Salah satu hal favorit Anik · Tahu Tek</div>
        <p>Putar perlahan, seperti kenangan kecil yang ingin disimpan.</p>
        <div class="actions"><button class="btn primary" onclick="go(2)">Selanjutnya <span>→</span></button></div>
      </div>
    </div>

    <div class="page" id="page2">
      <div class="intro">
        <div class="eyebrow">Save the date</div>
        <h2>November yang istimewa</h2>
        <p>Ada satu tanggal yang ingin diberi tanda khusus.</p>
      </div>
      <div class="calendar-wrap">
        <div class="month"><span>November 2026</span><small>11 / 2026</small></div>
        <div class="calendar">
          {% for d in ["MIN","SEN","SEL","RAB","KAM","JUM","SAB"] %}<div class="dayname">{{ d }}</div>{% endfor %}
          {% for week in weeks %}{% for day in week %}
            {% if day == 0 %}<div class="date empty">0</div>
            {% elif day == 25 %}<div class="date special">{{ day }}</div>
            {% else %}<div class="date">{{ day }}</div>{% endif %}
          {% endfor %}{% endfor %}
        </div>
        <div class="calendar-note">✦ 25 November — tanggal yang diberi lingkaran merah ✦</div>
      </div>
      <div class="actions"><button class="btn back" onclick="go(1)">← Kembali</button><button class="btn primary" onclick="go(3)">Selanjutnya →</button></div>
    </div>

    <div class="page" id="page3">
      <div class="intro">
        <div class="eyebrow">Choose your way</div>
        <h2>Mau mengisi yang mana?</h2>
        <p>Pilih salah satu. Tidak perlu terburu-buru, isi dengan santai dan jujur, ya.</p>
      </div>
      <div class="choice-grid">
        <button class="choice" onclick="go(4)"><span class="emoji">✎</span><h3>Kuis tentang Anik</h3><p>Lima pertanyaan sederhana, jawab dengan uraianmu sendiri.</p></button>
        <button class="choice" onclick="go(5)"><span class="emoji">♡</span><h3>Pesan &amp; Kesan</h3><p>Tuliskan pesan dan kesan yang ingin kamu sampaikan.</p></button>
      </div>
      <div class="actions"><button class="btn back" onclick="go(2)">← Kembali</button></div>
    </div>

    <div class="page" id="page4">
      <div class="eyebrow">A little quiz</div><h2>Seberapa kenal kamu dengan Anik?</h2>
      <p>Jawab kelima pertanyaan berikut dengan uraian singkat.</p>
      <form class="form-wrap" method="post" action="/submit/quiz">
        <div class="field"><label for="qname">Nama kamu</label><input id="qname" name="name" required maxlength="80" placeholder="Tulis nama lengkapmu"></div>
        <div class="field"><label for="qemail">Email kamu</label><input id="qemail" name="email" type="email" required maxlength="150" placeholder="nama@email.com"><p class="hint">Email ini digunakan untuk mengirim ucapan terima kasih.</p></div>
        {% for q in questions %}
        <div class="question"><label for="q{{ loop.index }}">{{ loop.index }}. {{ q }}</label><textarea id="q{{ loop.index }}" name="answer{{ loop.index }}" required maxlength="1000" placeholder="Tulis jawabanmu di sini..."></textarea></div>
        {% endfor %}
        <input class="hidden-trap" type="text" name="website" tabindex="-1" autocomplete="off">
        <div class="notice">Dengan mengirim formulir, kamu setuju jawaban dan emailmu dikirim kepada Anik untuk keperluan halaman ini.</div>
        <div class="actions"><button type="button" class="btn back" onclick="go(3)">← Kembali</button><button class="btn primary" type="submit">Kirim jawaban ↗</button></div>
      </form>
    </div>

    <div class="page" id="page5">
      <div class="eyebrow">Words from you</div><h2>Pesan dan kesan</h2>
      <p>Setiap kata punya arti. Tulis pesan dan kesanmu dengan minimal 25 kata.</p>
      <form class="form-wrap" method="post" action="/submit/message" id="messageForm">
        <div class="field"><label for="mname">Nama kamu</label><input id="mname" name="name" required maxlength="80" placeholder="Tulis nama lengkapmu"></div>
        <div class="field"><label for="memail">Email kamu</label><input id="memail" name="email" type="email" required maxlength="150" placeholder="nama@email.com"><p class="hint">Email ini digunakan untuk mengirim ucapan terima kasih.</p></div>
        <div class="field"><label for="message">Pesan dan kesanmu</label><textarea id="message" name="message" required maxlength="5000" placeholder="Tuliskan pesan dan kesanmu di sini..."></textarea><div class="wordcount" id="wordcount">0 / 25 kata minimum</div></div>
        <input class="hidden-trap" type="text" name="website" tabindex="-1" autocomplete="off">
        <div class="notice">Dengan mengirim formulir, kamu setuju pesan dan emailmu dikirim kepada Anik untuk keperluan halaman ini.</div>
        <div class="actions"><button type="button" class="btn back" onclick="go(3)">← Kembali</button><button class="btn primary" type="submit">Kirim pesan ↗</button></div>
      </form>
    </div>

    <div class="page {{ 'active' if result_message else '' }}" id="page6">
      <div class="success"><div class="check">✓</div><h2>Terima kasih!</h2><p>{{ result_message }}</p><p class="notice">Jika email konfirmasi belum terlihat, periksa folder Spam atau Promosi.</p></div>
    </div>
  </section>
  <div class="footer">MADE WITH CARE · ANIK</div>
</main>
<script>
function go(n){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  const target=document.getElementById('page'+n);
  if(target) target.classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
}
const msg=document.getElementById('message');
if(msg){
  const count=document.getElementById('wordcount');
  const update=()=>{const words=msg.value.trim()?msg.value.trim().split(/\s+/).length:0;count.textContent=words+' / 25 kata minimum';count.style.color=words>=25?'#557b65':'#9a5b42';};
  msg.addEventListener('input',update);update();
  document.getElementById('messageForm').addEventListener('submit',e=>{
    const words=msg.value.trim()?msg.value.trim().split(/\s+/).length:0;
    if(words<25){e.preventDefault();alert('Pesan dan kesan minimal 25 kata, ya. Saat ini baru '+words+' kata.');}
  });
}
</script>
</body>
</html>
"""

QUESTIONS = [
    "Apa warna favorit Anik?",
    "Apa makanan favorit Anik?",
    "Apa gender Anik?",
    "Apa bunga favorit Anik?",
    "Siapa nama lengkap Anik yang sebenarnya?",
]

def send_email(to_address, subject, body):
    """Kirim email melalui Gmail SMTP. Kredensial dibaca dari environment variables."""
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    if not username or not password:
        raise RuntimeError("Konfigurasi email belum lengkap. Atur MAIL_USERNAME dan MAIL_PASSWORD.")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ.get("MAIL_SENDER", username)
    msg["To"] = to_address
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)

def render_page(result_message=""):
    weeks = calendar.monthcalendar(2026, 11)
    return render_template_string(PAGE, weeks=weeks, questions=QUESTIONS,
                                  result_message=result_message)

def valid_email(value):
    value = (value or "").strip()
    return len(value) <= 150 and "@" in value and "." in value.rsplit("@", 1)[-1]

def send_confirmation(email, name):
    body = (
        f"Hai {name},\n\n"
        "TERIMA KASIH SUDAH MENJADI TEMANKU SELAMA 3 TAHUN DI SMA\n\n"
        "Terima kasih sudah meluangkan waktu untuk mengisi halaman kecil ini.\n\n"
        "Salam hangat,\nAnik"
    )
    send_email(email, "Terima kasih sudah mengisi halaman Anik", body)

@app.get("/")
def home():
    return render_page()

@app.post("/submit/quiz")
def submit_quiz():
    if request.form.get("website", "").strip():
        return "Permintaan tidak dapat diproses.", 400
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    answers = [request.form.get(f"answer{i}", "").strip() for i in range(1, 6)]
    if not name or not valid_email(email) or any(not a for a in answers):
        return "Mohon lengkapi semua kolom dengan benar.", 400

    lines = ["KIRIMAN KUIS WEBSITE ANIK", "", f"Nama: {name}", f"Email: {email}", ""]
    for i, (question, answer) in enumerate(zip(QUESTIONS, answers), 1):
        lines.extend([f"{i}. {question}", answer, ""])
    try:
        send_email(OWNER_EMAIL, f"Jawaban kuis dari {name}", "\n".join(lines))
        send_confirmation(email, name)
    except Exception:
        app.logger.exception("Gagal mengirim email kuis")
        return "Maaf, pengiriman email sedang bermasalah. Silakan coba lagi nanti.", 503
    return render_page("Jawabanmu sudah dikirim kepada Anik. Terima kasih sudah ikut mengisi!")

@app.post("/submit/message")
def submit_message():
    if request.form.get("website", "").strip():
        return "Permintaan tidak dapat diproses.", 400
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    word_count = len(message.split())
    if not name or not valid_email(email) or word_count < 25:
        return "Mohon lengkapi data dan tulis pesan minimal 25 kata.", 400

    body = (
        "PESAN DAN KESAN UNTUK ANIK\n\n"
        f"Nama: {name}\nEmail: {email}\nJumlah kata: {word_count}\n\n"
        f"Pesan dan kesan:\n{message}"
    )
    try:
        send_email(OWNER_EMAIL, f"Pesan dan kesan dari {name}", body)
        send_confirmation(email, name)
    except Exception:
        app.logger.exception("Gagal mengirim email pesan dan kesan")
        return "Maaf, pengiriman email sedang bermasalah. Silakan coba lagi nanti.", 503
    return render_page("Pesan dan kesanmu sudah dikirim kepada Anik. Terima kasih atas kata-kata yang kamu tuliskan!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
