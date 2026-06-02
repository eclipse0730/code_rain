from __future__ import annotations

import argparse
import os
import random
import sys
import time
from pathlib import Path

RESET = "\033[0m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GRAY = "\033[90m"

AI_CODE = """
import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "neural-edge-lab/hypercode-vision-v4"

class RealtimeInferenceEngine:
    def __init__(self, model_name: str, device: str = "cuda"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        ).to(device)
        self.model.eval()

    @torch.no_grad()
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.72,
            top_p=0.91,
            do_sample=True,
            repetition_penalty=1.08,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

def normalize_tensor(x: torch.Tensor) -> torch.Tensor:
    mean = x.mean(dim=-1, keepdim=True)
    std = x.std(dim=-1, keepdim=True).clamp(min=1e-6)
    return (x - mean) / std

def run_pipeline():
    engine = RealtimeInferenceEngine(MODEL_NAME)
    prompts = [
        "Design a real-time analytics pipeline for financial market data.",
        "Optimize GPU inference latency for edge notebooks.",
        "Generate secure Python code for encrypted local storage."
    ]

    for idx, prompt in enumerate(prompts):
        print(f"[task:{idx:03d}] {prompt}")
        result = engine.generate(prompt)
        score = np.random.normal(loc=0.87, scale=0.03)
        print(f"[confidence] {score:.4f}")
        print(result[:900])

if __name__ == "__main__":
    run_pipeline()
"""

CYBER_CODE = """
package main

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
    "net/http"
    "sync"
    "time"
)

type PacketTrace struct {
    SourceIP    string
    TargetIP    string
    Signature   string
    RiskScore   float64
    CapturedAt  time.Time
}

type ThreatScanner struct {
    mutex  sync.RWMutex
    cache  map[string]PacketTrace
}

func NewThreatScanner() *ThreatScanner {
    return &ThreatScanner{
        cache: make(map[string]PacketTrace),
    }
}

func fingerprint(payload []byte) string {
    hash := sha256.Sum256(payload)
    return hex.EncodeToString(hash[:])
}

func (s *ThreatScanner) Analyze(source string, target string, payload []byte) PacketTrace {
    sig := fingerprint(payload)
    risk := 0.42

    if len(payload) > 2048 {
        risk += 0.18
    }
    if payload[0]%7 == 0 {
        risk += 0.29
    }

    trace := PacketTrace{
        SourceIP:   source,
        TargetIP:   target,
        Signature:  sig,
        RiskScore:  risk,
        CapturedAt: time.Now(),
    }

    s.mutex.Lock()
    s.cache[sig] = trace
    s.mutex.Unlock()

    return trace
}

func main() {
    scanner := NewThreatScanner()
    http.HandleFunc("/inspect", func(w http.ResponseWriter, r *http.Request) {
        payload := []byte(r.URL.Query().Get("payload"))
        trace := scanner.Analyze("10.0.0.21", "172.16.4.8", payload)
        fmt.Fprintf(w, "signature=%s risk=%.2f", trace.Signature, trace.RiskScore)
    })

    fmt.Println("threat scanner online :8080")
    http.ListenAndServe(":8080", nil)
}
"""

DATA_CODE = """
WITH market_window AS (
    SELECT
        symbol,
        trade_date,
        close_price,
        volume,
        AVG(close_price) OVER (
            PARTITION BY symbol
            ORDER BY trade_date
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS ma20,
        AVG(volume) OVER (
            PARTITION BY symbol
            ORDER BY trade_date
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS volume_ma20
    FROM daily_prices
),
signal_base AS (
    SELECT
        symbol,
        trade_date,
        close_price,
        volume,
        ma20,
        volume_ma20,
        CASE
            WHEN close_price > ma20 AND volume > volume_ma20 * 4 THEN 'BREAKOUT'
            WHEN close_price < ma20 * 0.95 THEN 'PULLBACK'
            ELSE 'WATCH'
        END AS signal
    FROM market_window
)
SELECT
    symbol,
    trade_date,
    close_price,
    ROUND((close_price / ma20 - 1) * 100, 2) AS ma20_gap_pct,
    ROUND(volume / NULLIF(volume_ma20, 0), 2) AS volume_ratio,
    signal
FROM signal_base
WHERE signal <> 'WATCH'
ORDER BY trade_date DESC, volume_ratio DESC;
"""

THEMES = {
    "ai": AI_CODE,
    "cyber": CYBER_CODE,
    "data": DATA_CODE,
}

def enable_windows_ansi() -> None:
    if os.name == "nt":
        os.system("")

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def fake_status_line() -> str:
    items = [
        "[compile] optimizing tensor kernels...",
        "[gpu] allocating shared memory blocks...",
        "[build] resolving dependency graph...",
        "[scan] analyzing source modules...",
        "[deploy] validating runtime profile...",
        "[cache] warming instruction pipeline...",
        "[security] checking signatures...",
        "[network] syncing remote index...",
        "[ai] calibrating attention layers...",
        "[runtime] accelerating notebook workflow...",
    ]
    return random.choice(items)

def color_for_char(ch: str) -> str:
    if ch in "{}[]()<>":
        return YELLOW
    if ch in "=+-*/:;,.|":
        return CYAN
    if ch == "#":
        return GRAY
    return GREEN

def type_text(text: str, speed: float, jitter: float, status_rate: float) -> None:
    for line in text.strip("\n").splitlines():
        if random.random() < status_rate:
            sys.stdout.write(DIM + fake_status_line() + RESET + "\n")
            sys.stdout.flush()
            time.sleep(speed * random.randint(4, 12))

        for ch in line:
            sys.stdout.write(color_for_char(ch) + ch + RESET)
            sys.stdout.flush()
            delay = speed + random.uniform(0, jitter)
            if ch in ",.;:":
                delay *= random.uniform(1.5, 3.0)
            time.sleep(delay)

        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(speed * random.randint(2, 10))

def matrix_noise(lines: int = 8, width: int = 100) -> None:
    chars = "01abcdef{}[]()<>:=+-*/_"
    for _ in range(lines):
        row = "".join(random.choice(chars) for _ in range(width))
        sys.stdout.write(GRAY + row + RESET + "\n")
    sys.stdout.flush()

def load_code(args: argparse.Namespace) -> str:
    if args.file:
        path = Path(args.file)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
        return path.read_text(encoding="utf-8")
    return THEMES.get(args.theme, AI_CODE)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", choices=["ai", "cyber", "data"], default="ai")
    parser.add_argument("--file", help="출력할 코드 파일 경로")
    parser.add_argument("--speed", type=float, default=0.0015)
    parser.add_argument("--jitter", type=float, default=0.004)
    parser.add_argument("--status-rate", type=float, default=0.22)
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--no-clear", action="store_true")
    parser.add_argument("--noise", action="store_true")
    args = parser.parse_args()

    enable_windows_ansi()

    while True:
        if not args.no_clear:
            clear_screen()

        if args.noise:
            matrix_noise()
            time.sleep(0.35)

        code = load_code(args)
        type_text(code, speed=args.speed, jitter=args.jitter, status_rate=args.status_rate)

        if not args.loop:
            break

        time.sleep(1.0)

if __name__ == "__main__":
    main()
