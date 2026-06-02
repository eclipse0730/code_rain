from __future__ import annotations

import argparse
import os
import random
import sys
import time

RESET = "\033[0m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
WHITE = "\033[97m"

SOURCE_LINES = [
    "import asyncio",
    "from pathlib import Path",
    "from notebook_runtime.gpu import TensorSession",
    "from notebook_runtime.builder import NativePackager",
    "",
    "MODEL_PATH = Path('models/realtime-vision-edge.bin')",
    "CACHE_PATH = Path('.cache/kernel-map.json')",
    "",
    "class RealtimeNotebookApp:",
    "    def __init__(self):",
    "        self.session = TensorSession(device='metal', precision='fp16')",
    "        self.packager = NativePackager(target='release')",
    "",
    "    async def warmup(self):",
    "        await self.session.load(MODEL_PATH)",
    "        await self.session.compile_graph(batch_size=8)",
    "        await self.session.bind_camera_stream(index=0)",
    "",
    "    async def build(self):",
    "        bundle = await self.packager.collect_sources('src')",
    "        bundle.attach_runtime(self.session.export_runtime())",
    "        bundle.enable_acceleration('neural-engine')",
    "        return await bundle.write('dist/NotebookVision.app')",
    "",
    "async def main():",
    "    app = RealtimeNotebookApp()",
    "    await app.warmup()",
    "    artifact = await app.build()",
    "    print(f'build complete: {artifact}')",
    "",
    "if __name__ == '__main__':",
    "    asyncio.run(main())",
]

BUILD_STEPS = [
    ("bootstrap", "checking notebook runtime profile", "ok"),
    ("env", "resolving Python 3.12 virtual environment", "ok"),
    ("deps", "locking 184 transitive packages", "ok"),
    ("gpu", "probing Metal Performance Shaders backend", "ok"),
    ("cache", "loading kernel-map.json", "warn"),
    ("compile", "optimizing tensor graph partitions", "ok"),
    ("native", "linking acceleration shim", "warn"),
    ("bundle", "collecting release assets", "ok"),
    ("codesign", "requesting signing identity", "warn"),
    ("package", "writing final notebook demo bundle", "fail"),
]

ERROR_BLOCK = [
    "Traceback (most recent call last):",
    '  File "builder/release.py", line 218, in build_release',
    "    artifact = packager.write(target_dir)",
    '  File "builder/native_packager.py", line 94, in write',
    "    self.link_native_runtime()",
    '  File "builder/native_packager.py", line 141, in link_native_runtime',
    "    raise RuntimeError('missing acceleration symbol: _mpsGraphCompile')",
    "RuntimeError: missing acceleration symbol: _mpsGraphCompile",
    "",
    "[panic] build aborted after 47.82s",
    "[panic] cache index corrupt: .cache/kernel-map.json",
    "[panic] retry budget exhausted",
    "[panic] developer intervention required",
]

GLITCH_LINES = [
    "0x00007ff queue_overflow detected while flushing frame buffer",
    "kernel[vision.edge.003] returned non-zero exit status 3221225477",
    "watcher: file changed during bundle finalization",
    "runtime: dropped 17 pending compile tasks",
    "fatal: cannot recover partial native artifact",
]


def enable_windows_ansi() -> None:
    if os.name == "nt":
        os.system("")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def write(text: str, color: str = RESET, end: str = "\n") -> None:
    sys.stdout.write(color + text + RESET + end)
    sys.stdout.flush()


def type_line(text: str, color: str, speed: float, jitter: float) -> None:
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        delay = speed + random.uniform(0, jitter)
        if char in ",.;:()[]{}":
            delay *= random.uniform(1.4, 2.4)
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def print_source(speed: float, jitter: float) -> None:
    write("$ code --workspace notebook-vision", CYAN)
    time.sleep(0.25)
    write("$ python build_release.py --target laptop-ad --gpu --release", CYAN)
    time.sleep(0.5)

    for line_no, line in enumerate(SOURCE_LINES, start=1):
        prefix = f"{line_no:03d} | "
        sys.stdout.write(GRAY + prefix + RESET)
        sys.stdout.flush()
        type_line(line, color_for_source(line), speed, jitter)
        if random.random() < 0.14:
            write(random.choice(GLITCH_LINES), DIM + YELLOW)
            time.sleep(speed * random.randint(15, 30))


def color_for_source(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith(("class ", "async def", "def ")):
        return CYAN
    if stripped.startswith(("import ", "from ")):
        return YELLOW
    if "raise " in stripped or "RuntimeError" in stripped:
        return RED
    return GREEN


def print_progress(speed: float) -> None:
    write("", RESET)
    write("[build] release pipeline started", WHITE)
    for index, (label, message, status) in enumerate(BUILD_STEPS, start=1):
        time.sleep(speed * random.randint(35, 70))
        bar = progress_bar(index, len(BUILD_STEPS))
        if status == "ok":
            write(f"{bar} [{label}] {message} ... ok", GREEN)
        elif status == "warn":
            write(f"{bar} [{label}] {message} ... warning", YELLOW)
            write(f"       warning: {random.choice(GLITCH_LINES)}", DIM + YELLOW)
        else:
            write(f"{bar} [{label}] {message} ... failed", RED)
            burst_errors(speed)


def progress_bar(current: int, total: int) -> str:
    width = 24
    filled = int(width * current / total)
    return "[" + "#" * filled + "." * (width - filled) + "]"


def burst_errors(speed: float) -> None:
    for _ in range(7):
        line = random.choice(GLITCH_LINES)
        write(f"error: {line}", RED)
        time.sleep(speed * random.randint(10, 22))


def print_error_block(speed: float, jitter: float) -> None:
    write("", RESET)
    write("=" * 72, RED)
    write("BUILD FAILED", RED)
    write("=" * 72, RED)
    for line in ERROR_BLOCK:
        color = RED if line.startswith(("[panic]", "RuntimeError")) else YELLOW
        type_line(line, color, speed * 0.7, jitter)
    write("", RESET)
    write(">>> cut to developer: grabs head, stares at terminal", DIM + WHITE)
    write(">>> laptop fan rises, terminal keeps blinking", DIM + WHITE)


def run_scene(args: argparse.Namespace) -> None:
    if not args.no_clear:
        clear_screen()
    print_source(args.speed, args.jitter)
    print_progress(args.speed)
    print_error_block(args.speed, args.jitter)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cinematic fake build error scene for ads.")
    parser.add_argument("--speed", type=float, default=0.003)
    parser.add_argument("--jitter", type=float, default=0.004)
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--no-clear", action="store_true")
    args = parser.parse_args()

    enable_windows_ansi()

    while True:
        run_scene(args)
        if not args.loop:
            break
        time.sleep(2.0)


if __name__ == "__main__":
    main()
