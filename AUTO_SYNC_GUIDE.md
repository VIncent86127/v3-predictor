# V3预测系统 - 自动同步指南

## 自动同步机制

本项目已配置自动同步到GitHub，确保每次修改都会自动上传。

---

## 方式1：Git Hook自动推送（推荐）

每次commit后会自动推送到GitHub：

```bash
cd /home/ubuntu/.openclaw/workspace/v3-predictor

# 修改文件后
git add .
git commit -m "Update: 描述修改内容"
# 自动触发push，无需手动执行git push
```

---

## 方式2：自动同步脚本

### 单次同步

```bash
./auto-sync.sh "描述修改内容"
```

### 持续监控同步

```bash
# 启动后台监控进程
nohup python3 auto-sync-daemon.py > sync.log 2>&1 &

# 或前台运行（可看到实时日志）
python3 auto-sync-daemon.py
```

监控模式会每60秒检查一次文件变化，自动提交并推送。

---

## 方式3：手动同步

```bash
git add .
git commit -m "Update: 描述修改内容"
git push origin main
```

---

## 验证同步状态

访问GitHub仓库：https://github.com/VIncent86127/v3-predictor

查看最新提交记录确认同步成功。

---

## GitHub配置

- **仓库**：https://github.com/VIncent86127/v3-predictor
- **用户名**：VIncent86127
- **认证方式**：gh auth login（已配置）
- **推送方式**：HTTPS + GitHub CLI认证

---

## 故障排除

### 问题1：推送失败

```bash
# 检查认证状态
gh auth status

# 重新认证（如需要）
gh auth login
```

### 问题2：Hook未生效

```bash
# 确保hook有执行权限
chmod +x .git/hooks/post-commit

# 检查hook文件
cat .git/hooks/post-commit
```

### 问题3：查看同步日志

```bash
# 查看同步日志
cat .sync.log

# 查看git log
git log --oneline -10
```

---

## 最佳实践

1. **重要修改**：使用有意义的commit message
2. **批量修改**：一次性提交多个相关文件
3. **测试后提交**：确保代码测试通过后再commit
4. **定期检查**：访问GitHub确认同步成功

---

**最后更新**：2026-06-22