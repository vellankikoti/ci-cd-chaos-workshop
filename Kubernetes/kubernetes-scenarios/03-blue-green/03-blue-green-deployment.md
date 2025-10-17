# 🚀 Scenario 03: Blue-Green Deployment - Zero-Downtime Magic

**"From Scary Downtime to Seamless Deployments"**

---

## 🎯 What You'll Learn

- Master blue-green deployment strategy
- Achieve true zero-downtime deployments
- Implement instant rollback capability
- Understand deployment strategy trade-offs
- Use Kubernetes service selectors dynamically

**Time**: 15-20 minutes | **Difficulty**: ⭐⭐☆☆☆

---

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Kubernetes cluster running
kubectl cluster-info

# 2. Install Python dependencies (Flask only!)
cd hero-solution
pip3 install -r requirements.txt
```

### Deploy Blue-Green App

```bash
# ONE command - automatically uses enhanced version if available!
python3 deploy.py
kubectl port-forward -n blue-green-demo svc/demo-app 31006:80
# Open: http://localhost:31006
```

### 🌟 Smart Auto-Detection!

The `deploy.py` script **automatically detects** if enhanced files exist and deploys the best version:

- ✅ **Enhanced version found?** → Deploys **stunning traffic visualization** with interactive controls!
- ✅ **Enhanced version not found?** → Deploys standard version (still great!)

**No need to choose** - it picks the best version automatically!

**Enhanced Features** (when available):
- 🌊 **Animated Traffic Particles** - Watch traffic flow from load balancer to pods!
- 🎛️ **Interactive Traffic Slider** - Gradual 0-100% traffic control (canary)
- 📊 **Live Pod Health** - 6 pods with heartbeat animations
- 🚀 **One-Click Switch** - Smooth animated transition to green
- ↩️ **One-Click Rollback** - Instant rollback to blue
- 📈 **Real-Time Metrics** - Requests, response time, uptime
- 📜 **Request History** - See which pods handle requests

**The script will output ready-to-copy commands!** Look for:

```
🔄 SWITCH BETWEEN VERSIONS:

   # Switch to GREEN (v2.0)
   python3 switch.py green

   # Switch to BLUE (v1.0)
   python3 switch.py blue

   # Check current version
   python3 switch.py status
```

**Copy and paste the commands from the output!** They include:
- ✅ Port-forward command for the app
- ✅ Version switching commands
- ✅ Status check commands
- ✅ Verification commands

**Result**: Both blue (v1.0) and green (v2.0) versions running, with instant switching capability!

> **💡 Pro Tip:** The deployment script outputs everything you need. No need to memorize commands - just copy and paste!

---

## 🎮 The Blue-Green Experience

### What is Blue-Green Deployment?

Blue-green deployment is a strategy where you run **two identical production environments**:

- **BLUE** = Current version (v1.0)
- **GREEN** = New version (v2.0)

At any time, only ONE is live (receiving traffic). You can switch between them **instantly** with **zero downtime**.

### How It Works

```
1. Initial State:
   BLUE (v1.0) ← ACTIVE (all traffic)
   GREEN (v2.0) ← STANDBY (no traffic, but running)

2. Deploy new code to GREEN
   BLUE (v1.0) ← ACTIVE
   GREEN (v2.0-NEW) ← STANDBY (test it!)

3. Switch traffic to GREEN
   BLUE (v1.0) ← STANDBY (instant rollback available!)
   GREEN (v2.0-NEW) ← ACTIVE (all traffic)

4. If GREEN has issues:
   → Instant rollback to BLUE (one command!)
```

### Interactive Demo

```bash
# 1. Deploy both versions
python3 deploy.py

# 2. Open app in browser
http://localhost:31006

# 3. Check current status
python3 switch.py status
# Shows: BLUE is ACTIVE

# 4. Switch to GREEN (zero downtime!)
python3 switch.py green
# Refresh browser - now shows GREEN gradient!

# 5. Switch back to BLUE (instant rollback!)
python3 switch.py blue
# Refresh browser - back to BLUE gradient!
```

**Watch the magic:** Keep refreshing the browser while switching - **zero errors, zero downtime!**

---

## 🔍 Understanding the Strategy

### The Key Components

#### 1. **Two Identical Deployments**
```yaml
# Blue Deployment (v1.0)
metadata:
  name: blue-deployment
  labels:
    version: blue

# Green Deployment (v2.0)
metadata:
  name: green-deployment
  labels:
    version: green
```

Both deployments are **always running** - this is the secret to zero downtime!

#### 2. **Service with Dynamic Selector**
```yaml
# Service controls which version gets traffic
apiVersion: v1
kind: Service
metadata:
  name: demo-app
spec:
  selector:
    app: demo-app
    version: blue  # ← Change this to 'green' to switch!
```

**The magic:** Change `version: blue` to `version: green` and traffic **instantly** routes to green pods!

#### 3. **Instant Switching**
```bash
# This command changes the service selector
kubectl patch service demo-app -p '{"spec":{"selector":{"version":"green"}}}'

# Result: All traffic now goes to green pods
# Blue pods still running (ready for rollback!)
```

### The Workflow

```
Deploy → Test → Switch → Verify → Rollback if needed

1. Deploy GREEN (new version)
   ✓ Pods start up
   ✓ Health checks pass
   ✓ NO TRAFFIC yet

2. Test GREEN
   ✓ Port-forward to green pods
   ✓ Run tests
   ✓ Verify everything works

3. Switch to GREEN
   ✓ Change service selector
   ✓ Traffic instantly routes to green
   ✓ Zero downtime!

4. Verify GREEN
   ✓ Monitor logs
   ✓ Check metrics
   ✓ Watch for errors

5. Rollback if needed
   ✓ One command: python3 switch.py blue
   ✓ Instant rollback!
   ✓ Green stays running for debugging
```

---

## 📊 Verify Blue-Green Deployment

### Check Both Versions Running
```bash
# See all pods with version labels
kubectl get pods -n blue-green-demo -L version

# Output:
# NAME                     READY   STATUS    VERSION
# blue-deployment-xxx      1/1     Running   blue
# blue-deployment-yyy      1/1     Running   blue
# blue-deployment-zzz      1/1     Running   blue
# green-deployment-aaa     1/1     Running   green
# green-deployment-bbb     1/1     Running   green
# green-deployment-ccc     1/1     Running   green
```

### Check Which Version Is Active
```bash
# Check service selector
kubectl get service demo-app -n blue-green-demo -o yaml | grep version

# Or use our helper
python3 switch.py status
```

### Test Each Version Directly
```bash
# Test BLUE directly (bypass service)
kubectl port-forward -n blue-green-demo deploy/blue-deployment 8081:8080
curl http://localhost:8081/health

# Test GREEN directly
kubectl port-forward -n blue-green-demo deploy/green-deployment 8082:8080
curl http://localhost:8082/health
```

---

## 🎯 Hands-On Exercises

### Exercise 1: Zero-Downtime Switch

**Goal:** Experience true zero-downtime deployment

```bash
# Terminal 1: Run continuous requests
while true; do
  curl -s http://localhost:31006/health | jq .version
  sleep 0.5
done

# Terminal 2: Switch versions
python3 switch.py green

# Observe: NO FAILED REQUESTS during switch!
```

### Exercise 2: Instant Rollback

**Goal:** Practice instant rollback

```bash
# 1. Switch to green
python3 switch.py green

# 2. "Oh no, there's a bug!" - Rollback!
python3 switch.py blue

# Observe: Instant rollback, zero downtime
```

### Exercise 3: Canary-Style Testing

**Goal:** Use blue-green for canary testing

```bash
# 1. Scale green to 1 pod (10% of traffic if you switch)
kubectl scale deployment green-deployment -n blue-green-demo --replicas=1

# 2. Switch to green (now only 1 pod serves traffic)
python3 switch.py green

# 3. Monitor for issues
kubectl logs -n blue-green-demo -l version=green -f

# 4. If good, scale up green
kubectl scale deployment green-deployment -n blue-green-demo --replicas=3

# 5. If bad, instant rollback
python3 switch.py blue
```

---

## 🎓 Blue-Green vs Other Strategies

### Comparison Table

| Feature | Blue-Green | Rolling Update | Canary |
|---------|-----------|----------------|--------|
| **Downtime** | Zero | Zero | Zero |
| **Speed** | Instant | Gradual | Gradual |
| **Rollback** | Instant | Manual | Manual |
| **Resource Usage** | 2x (both running) | 1.5x (overlap) | 1.1x (small overlap) |
| **Risk** | Low (instant rollback) | Medium | Low (gradual) |
| **Complexity** | Simple | Simple | Medium |
| **Database** | Must be compatible | Must be compatible | Must be compatible |

### When to Use Blue-Green

**✅ Use Blue-Green When:**
- Zero downtime is critical
- Instant rollback capability needed
- You can afford 2x resources
- Database schema is backward compatible
- Application is stateless

**❌ Don't Use Blue-Green When:**
- Resources are very limited
- Database migrations are complex
- Application has lots of state
- Testing in production not allowed

---

## 🔐 Security & Best Practices

### Implemented in Demo

✅ **Non-root containers** (UID 1000)
✅ **Read-only root filesystem**
✅ **Dropped all capabilities**
✅ **Resource limits** enforced
✅ **Health checks** (liveness & readiness)
✅ **Security contexts** configured

### Production Best Practices

1. **Pre-Deployment Testing**
   ```bash
   # Test green before switching
   kubectl port-forward deploy/green-deployment 8080:8080
   # Run full test suite against localhost:8080
   ```

2. **Database Migrations**
   ```bash
   # Use backward-compatible migrations
   # Example: Add column, deploy code, remove old column
   ```

3. **Monitoring During Switch**
   ```bash
   # Watch error rates, latency, throughput
   # Auto-rollback if metrics degrade
   ```

4. **Gradual Traffic Shift**
   ```bash
   # Use service mesh for weighted routing
   # 10% → 25% → 50% → 100% to green
   ```

---

## 🧹 Cleanup

```bash
# Delete everything
kubectl delete namespace blue-green-demo

# Remove generated file
rm k8s-deployed.yaml
```

---

## 🎉 What You Accomplished

✅ Deployed two identical production environments
✅ Achieved zero-downtime deployments
✅ Implemented instant rollback capability
✅ Understood service selector switching
✅ Practiced blue-green workflow

---

## 📚 Next Steps

1. **Try the chaos scenario** (if available)
   - See what happens with downtime
   - Compare with blue-green solution

2. **Integrate with CI/CD**
   - Auto-deploy to green
   - Run tests
   - Auto-switch if tests pass

3. **Add monitoring**
   - Track deployment metrics
   - Auto-rollback on errors
   - Alert on anomalies

4. **Explore service mesh**
   - Istio or Linkerd
   - Gradual traffic shifting
   - A/B testing capabilities

---

## 🤝 Resources

- [Blue-Green Deployment (Martin Fowler)](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Zero-Downtime Deployments](https://kubernetes.io/blog/2018/04/30/zero-downtime-deployment-kubernetes-jenkins/)
- [Service Mesh Patterns](https://istio.io/latest/docs/concepts/traffic-management/)

---

**🎉 Congratulations! You've mastered blue-green deployments!**
