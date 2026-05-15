package com.rrobotjang.apigateway;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InterviewWebController {

    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    public String home() {
        return """
            <!doctype html>
            <html lang=\"en\">
            <head>
              <meta charset=\"UTF-8\" />
              <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
              <title>AI Interview Practice</title>
              <style>
                body { font-family: Arial, sans-serif; margin: 0; background: #0b1020; color: #e8ecff; }
                .wrap { max-width: 900px; margin: 40px auto; padding: 24px; }
                .card { background: #151c33; border-radius: 14px; padding: 20px; margin-bottom: 16px; }
                button { background:#5b8cff;color:white;border:0;padding:10px 14px;border-radius:8px;cursor:pointer; }
                input, textarea { width:100%;padding:10px;border-radius:8px;border:1px solid #334; background:#0f1530;color:#fff; }
                .muted { color:#aab3d8; font-size: 14px; }
              </style>
            </head>
            <body>
            <div class=\"wrap\">
              <h1>🚀 AI Interview Practice (Live Scaffold)</h1>
              <p class=\"muted\">Gateway UI for immediate mock interview practice.</p>

              <div class=\"card\">
                <h3>1) Get JWT Token</h3>
                <input id=\"username\" placeholder=\"username\" value=\"candidate\" />
                <button onclick=\"login()\">Login</button>
                <pre id=\"tokenBox\" class=\"muted\"></pre>
              </div>

              <div class=\"card\">
                <h3>2) Validate Token</h3>
                <button onclick=\"validateToken()\">Validate /api/auth/validate</button>
                <pre id=\"validateBox\" class=\"muted\"></pre>
              </div>

              <div class=\"card\">
                <h3>3) Mock Interview Question</h3>
                <p id=\"q\">Tell me about a time you designed a scalable API under pressure.</p>
                <textarea id=\"answer\" rows=\"5\" placeholder=\"Type your answer in English...\"></textarea>
                <button onclick=\"scoreAnswer()\">Get AI-style Feedback (local rubric)</button>
                <pre id=\"feedback\" class=\"muted\"></pre>
              </div>
            </div>
            <script>
            let token = '';
            async function login(){
              const username = document.getElementById('username').value;
              const r = await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username})});
              const j = await r.json(); token = j.token || '';
              document.getElementById('tokenBox').textContent = token ? 'Bearer ' + token : JSON.stringify(j,null,2);
            }
            async function validateToken(){
              const r = await fetch('/api/auth/validate',{headers:{'Authorization':'Bearer '+token}});
              const t = await r.text();
              document.getElementById('validateBox').textContent = r.status + ' ' + t;
            }
            function scoreAnswer(){
              const a = document.getElementById('answer').value.trim();
              const words = a ? a.split(/\s+/).length : 0;
              const hasTradeoff = /(trade-?off|latency|throughput|consistency|availability)/i.test(a);
              const hasStructure = /(first|second|finally|because|therefore)/i.test(a);
              const score = Math.min(100, (words>60?40:words>30?30:15)+(hasTradeoff?30:10)+(hasStructure?20:5)+10);
              document.getElementById('feedback').textContent =
                `Score: ${score}/100\n- Length: ${words} words\n- Tradeoff terms: ${hasTradeoff?'good':'add tradeoff keywords'}\n- Structure: ${hasStructure?'clear':'use structured flow'}\nTip: mention metrics, bottlenecks, and failure handling.`;
            }
            </script>
            </body></html>
            """;
    }
}
