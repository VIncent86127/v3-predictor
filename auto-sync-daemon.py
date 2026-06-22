#!/usr/bin/env python3
"""
V3预测系统 - 自动同步工具
监控文件变化并自动提交到GitHub
"""

import os
import sys
import time
import subprocess
from pathlib import Path

PROJECT_DIR = Path("/home/ubuntu/.openclaw/workspace/v3-predictor")

def run_command(cmd, cwd=PROJECT_DIR):
    """运行命令"""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def has_changes():
    """检查是否有改动"""
    returncode, stdout, stderr = run_command("git diff-index --quiet HEAD --")
    return returncode != 0

def commit_and_push(message="Auto update"):
    """提交并推送"""
    # 添加所有改动
    run_command("git add .")
    
    # 提交
    returncode, stdout, stderr = run_command(f'git commit -m "{message}"')
    if returncode != 0:
        print(f"Commit failed: {stderr}")
        return False
    
    # 推送
    returncode, stdout, stderr = run_command("git push origin main")
    if returncode != 0:
        print(f"Push failed: {stderr}")
        return False
    
    print(f"✅ Changes pushed to GitHub: {message}")
    return True

def watch_and_sync(interval=60):
    """监控文件变化并自动同步"""
    print(f"🔍 Watching for changes in {PROJECT_DIR}")
    print(f"⏱️  Check interval: {interval} seconds")
    print(f"🌐 GitHub: https://github.com/VIncent86127/v3-predictor")
    print(f"Press Ctrl+C to stop\n")
    
    while True:
        try:
            if has_changes():
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Changes detected, syncing...")
                commit_and_push(f"Auto update at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Stopped watching")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 单次提交模式
        message = " ".join(sys.argv[1:])
        commit_and_push(message)
    else:
        # 持续监控模式
        watch_and_sync()