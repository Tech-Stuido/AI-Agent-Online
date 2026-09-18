from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

LLAMA_URL = "http://127.0.0.1:8081/v1/chat/completions"

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MB AI</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#0b0b0f;color:white;font-family:Arial;height:100vh;display:flex;flex-direction:column}
header{padding:18px 22px;border-bottom:1px solid #292932;font-size:21px;font-weight:bold}
#chat{flex:1;overflow:auto;padding:20px}
.msg{max-width:850px;margin:12px auto;padding:14px 17px;border-radius:14px;white-space:pre-wrap;line-height:1.5}
.user{background:#252530}
.ai{background:#15151c;border:1px solid #292932}
.bottom{padding:15px;border-top:1px solid #292932}
.box{max-width:850px;margin:auto;display:flex;gap:10px}
textarea{flex:1;height:52px;resize:none;background:#15151b;color:white;border:1px solid #33333d;border-radius:12px;padding:14px;font-size:15px}
button{width:55px;border:0;border-radius:12px;background:white;color:black;font-size:20px}
</style>
</head>
<body>
<header>MB AI</header>
<div id="chat"></div>
<div class="bottom">
<div class="box">
<textarea id="input" placeholder="Message MB AI..." onkeydown="key(event)"></textarea>
<button onclick="send()">↑</button>
</div>
</div>
<script>
let messages=[];
function add(role,text){
 let d=document.createElement("div");
 d.className="msg "+(role=="user"?"user":"ai");
 d.textContent=text;
 document.getElementById("chat").appendChild(d);
 document.getElementById("chat").scrollTop=999999;
}
async function send(){
 let i=document.getElementById("input"),t=i.value.trim();
 if(!t)return;
 i.value="";
 messages.push({role:"user",content:t});
 add("user",t);
 add("assistant","Thinking...");
 try{
  let r=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({messages})});
  let d=await r.json();
  document.getElementById("chat").lastChild.remove();
  if(d.reply){messages.push({role:"assistant",content:d.reply});add("assistant",d.reply)}
  else add("assistant","Error: "+(d.error||"Unknown error"));
 }catch(e){
  document.getElementById("chat").lastChild.remove();
  add("assistant","AI server is not running.");
 }
}
function key(e){if(e.key=="Enter"&&!e.shiftKey){e.preventDefault();send()}}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/chat",methods=["POST"])
def chat():
    data=request.get_json()
    try:
        r=requests.post(
            LLAMA_URL,
            json={
                "messages":[
                    {"role":"system","content":"You are MB AI, a helpful concise local AI running on a Raspberry Pi."},
                    *data["messages"][-10:]
                ],
                "temperature":0.7,
                "max_tokens":256,
                "stream":False
            },
            timeout=180
        )
        r.raise_for_status()
        return jsonify({"reply":r.json()["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error":str(e)}),500

app.run(host="0.0.0.0",port=8080)
