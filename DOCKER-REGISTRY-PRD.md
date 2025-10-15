# 🎯 Docker Registry Solution - Product Requirements Document (PRD)

## Executive Summary

**Problem**: 700 workshop attendees need 20 Docker images (~8GB) but venue network can't handle mass downloads.

**Solution**: Local Docker Registry at venue. Attendees pull images from local registry (LAN speed) instead of Docker Hub.

**Impact**:
- Download time: 60 min → 10 min per attendee
- Network load: 1.4TB → Zero (all local)
- Success rate: 50% → 99%

---

## 1. Product Overview

### 1.1 What We're Building

A **private Docker Registry** that:
1. Runs on local network at workshop venue
2. Contains all 20 workshop images pre-loaded
3. Attendees configure Docker to pull from this registry
4. Works 100% offline (no internet needed)

### 1.2 User Personas

**Primary User: Workshop Facilitator (You)**
- Needs: Simple setup, reliable, troubleshoot-able
- Technical level: Intermediate
- Time available: 1-2 hours setup before workshop

**Secondary User: Workshop Attendee (700 people)**
- Needs: Simple configuration, fast downloads
- Technical level: Beginner to Intermediate
- Time available: 5-10 minutes setup

---

## 2. Technical Architecture

### 2.1 System Components

```
┌─────────────────────────────────────────────────────────┐
│                    WORKSHOP VENUE                       │
│                                                         │
│  ┌──────────────────┐                                  │
│  │ Registry Server  │  (Your laptop)                   │
│  │ - Docker Registry│                                  │
│  │ - 20 images      │                                  │
│  │ - Web UI         │                                  │
│  └────────┬─────────┘                                  │
│           │                                             │
│           │ Local Network (Fast!)                      │
│           │                                             │
│  ┌────────┴─────────────────────────────────────────┐  │
│  │                                                   │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │  │Attendee1│  │Attendee2│  │  ...700 │         │  │
│  │  │pulls    │  │pulls    │  │pulls    │         │  │
│  │  │images   │  │images   │  │images   │         │  │
│  │  └─────────┘  └─────────┘  └─────────┘         │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

**Registry Server:**
- Docker Registry v2 (official)
- Docker Registry UI (optional, for monitoring)
- Nginx (optional, for caching/load balancing)

**Attendee Side:**
- Docker daemon configuration
- Simple script to configure registry

---

## 3. Functional Requirements

### 3.1 Registry Setup (Facilitator)

**FR-1: One-Command Setup**
```bash
python3 registry-setup.py --prepare
```
Must:
- Pull all 20 images from Docker Hub
- Start local registry
- Push all images to local registry
- Verify all images available
- Display registry URL

**Time limit:** 60 minutes with good internet

---

**FR-2: Registry Server**

Must provide:
- HTTP endpoint: `http://REGISTRY-IP:5000`
- Image listing endpoint
- Health check endpoint
- Support concurrent pulls (100+ simultaneous)

---

**FR-3: Monitoring Dashboard**

Must show:
- Number of images available (should be 20)
- Number of active downloads
- Registry status (healthy/unhealthy)
- Network address to share

---

### 3.2 Attendee Configuration (700 people)

**FR-4: Simple Configuration Script**
```bash
python3 configure-registry.py --registry 192.168.1.100:5000
```

Must:
- Detect OS (macOS/Windows/Linux)
- Update Docker daemon config
- Restart Docker (if needed)
- Verify connection to registry
- Show success/failure clearly

**Time limit:** 2 minutes per attendee

---

**FR-5: Pull Images Script**
```bash
python3 pull-workshop-images.py
```

Must:
- Pull all 20 images from local registry
- Show progress bar
- Handle failures gracefully
- Verify all images downloaded
- Work offline

**Time limit:** 10 minutes per attendee

---

**FR-6: Fallback to Docker Hub**

If local registry fails:
- Automatically fall back to Docker Hub
- Notify user of fallback
- Continue working (slower)

---

## 4. Non-Functional Requirements

### 4.1 Performance

**NFR-1: Registry Server**
- Support 100 concurrent pulls
- Serve images at LAN speed (>100 MB/s)
- Handle 700 total attendees in 30 minutes

**NFR-2: Download Speed**
- Per attendee: 8GB in <10 minutes
- = 800 MB/min = 13 MB/s minimum
- Easily achievable on LAN (1 Gbps = 125 MB/s)

### 4.2 Reliability

**NFR-3: Uptime**
- Registry must stay up for 4 hours (workshop duration)
- Automatic restart if crashes
- Health checks every 30 seconds

**NFR-4: Error Handling**
- Clear error messages
- Automatic retries (3 attempts)
- Fallback to Docker Hub if registry fails

### 4.3 Usability

**NFR-5: Simplicity**
- Facilitator: 2 commands max
- Attendee: 1-2 commands max
- No manual configuration files
- Scripts explain what they're doing

### 4.4 Security

**NFR-6: Registry Access**
- No authentication (trusted local network)
- Insecure registry flag required (attendees' Docker)
- Only accessible on local network

---

## 5. User Workflows

### 5.1 Facilitator Workflow (Before Workshop)

```
Day Before Conference:
┌──────────────────────────────────────────┐
│ 1. Pull all images from Docker Hub      │  60 min (with internet)
│    $ python3 registry-setup.py --pull   │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 2. Start local registry                 │  1 min
│    $ python3 registry-setup.py --start  │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 3. Push images to local registry        │  10 min
│    $ python3 registry-setup.py --push   │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 4. Verify all images present            │  1 min
│    $ python3 registry-setup.py --verify │
└──────────────────────────────────────────┘

Total: ~75 minutes (one time)
```

---

### 5.2 Facilitator Workflow (At Conference)

```
30 Minutes Before Workshop:
┌──────────────────────────────────────────┐
│ 1. Connect to venue network              │  2 min
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 2. Start registry server                 │  1 min
│    $ python3 registry-setup.py --serve   │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 3. Note your IP address                  │  1 min
│    Registry URL: http://192.168.1.100:5000
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 4. Display on screen for attendees       │
│    See slide template in Section 6       │
└──────────────────────────────────────────┘

Total: 5 minutes
```

---

### 5.3 Attendee Workflow

```
┌──────────────────────────────────────────┐
│ 1. Configure Docker for local registry  │  2 min
│    $ python3 configure-registry.py \     │
│      --registry 192.168.1.100:5000       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 2. Pull workshop images                  │  10 min
│    $ python3 pull-workshop-images.py     │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 3. Verify images downloaded              │  1 min
│    $ docker images | grep workshop       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│ 4. Start workshop                        │
│    $ python3 START-WORKSHOP.py           │
└──────────────────────────────────────────┘

Total: ~15 minutes
```

---

## 6. Success Metrics

### 6.1 Setup Phase
- ✅ Registry setup completes in <75 minutes
- ✅ All 20 images pushed successfully
- ✅ Registry accessible from test machine
- ✅ Health check returns 200 OK

### 6.2 Workshop Phase
- ✅ 95%+ attendees successfully configure Docker
- ✅ Average download time <10 minutes per attendee
- ✅ Registry serves 700 attendees in 30 minutes
- ✅ <5% need fallback to Docker Hub

### 6.3 User Satisfaction
- ✅ Facilitator: "Setup was straightforward"
- ✅ Attendees: "Configuration was simple"
- ✅ Network: "No congestion or slowdowns"

---

## 7. Implementation Components

### 7.1 Scripts to Build

**1. registry-setup.py** (For facilitator)
- Pull images from Docker Hub
- Start Docker registry container
- Push images to local registry
- Verify images
- Display registry info

**2. configure-registry.py** (For attendees)
- Detect OS
- Update Docker daemon config
- Add insecure registry
- Restart Docker daemon
- Test connection

**3. pull-workshop-images.py** (For attendees)
- Pull all 20 images from local registry
- Show progress
- Verify completion
- Handle errors

**4. registry-monitor.py** (For facilitator)
- Dashboard showing live stats
- Number of connected clients
- Images being pulled
- Registry health

---

### 7.2 Configuration Files

**Image manifest** (images.json):
```json
{
  "images": [
    {
      "source": "postgres:15-alpine",
      "target": "workshop/postgres:15-alpine"
    },
    {
      "source": "redis:7-alpine",
      "target": "workshop/redis:7-alpine"
    }
    // ... 18 more
  ]
}
```

**Docker daemon config** (daemon.json):
```json
{
  "insecure-registries": ["192.168.1.100:5000"]
}
```

---

## 8. Failure Modes & Mitigation

### 8.1 Registry Server Fails

**Symptoms**: Can't connect to registry
**Mitigation**:
- Auto-restart container
- Fallback: Start backup registry on second laptop
- Last resort: Use Docker Hub (slow but works)

### 8.2 Network Issues

**Symptoms**: Slow downloads from registry
**Mitigation**:
- Use nginx caching proxy
- Start multiple registry instances (load balance)
- Reduce concurrent downloads

### 8.3 Docker Config Fails

**Symptoms**: Attendee can't configure insecure registry
**Mitigation**:
- Script provides manual instructions
- Screen share for troubleshooting
- Pair with neighbor who succeeded

### 8.4 Disk Space

**Symptoms**: Registry server runs out of space
**Mitigation**:
- Require 20GB free space (check in script)
- Clean old images before setup
- Monitor disk usage

---

## 9. Rollout Plan

### Phase 1: Development (Now)
- Build all scripts
- Test on local network
- Document everything

### Phase 2: Testing (1 week before)
- Test with 5-10 people
- Measure download speeds
- Fix issues

### Phase 3: Workshop Day (Conference)
- Set up 30 min before
- Monitor during workshop
- Troubleshoot as needed

---

## 10. Comparison vs Alternatives

| Metric | Docker Registry | HTTP Servers | USB Drives |
|--------|----------------|--------------|------------|
| **Setup Time** | 75 min | 30 min | Days |
| **Attendee Time** | 15 min | 20 min | 5 min |
| **Technical** | Medium | Easy | Easy |
| **Scale** | Excellent | Good | Poor |
| **Cost** | $0 | $0 | $2,500 |
| **Professional** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Elegance** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ |

**Why Registry Wins:**
- Most professional approach
- Standard Docker workflow
- Scales to any number
- Cleanest attendee experience

---

## 11. Documentation Needed

### For Facilitator:
1. **Setup Guide** - Step-by-step registry setup
2. **Troubleshooting Guide** - Common issues
3. **Monitoring Guide** - How to watch registry

### For Attendees:
1. **Quick Start** - 1-page instructions
2. **Windows Guide** - OS-specific steps
3. **macOS Guide** - OS-specific steps
4. **Linux Guide** - OS-specific steps

### Presentation Slides:
1. **Instructions Slide** - What attendees should do
2. **Registry URL Slide** - Big, visible URL
3. **Troubleshooting Slide** - If issues arise

---

## 12. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Registry crashes | Low | High | Auto-restart, backup registry |
| Network slow | Medium | Medium | Use LAN, not WiFi |
| Config fails | Medium | Medium | Clear error messages, manual steps |
| Out of disk space | Low | High | Check space before setup |
| Docker Hub needed | Low | Low | Fallback works automatically |

---

## 13. Success Criteria

**Must Have:**
- ✅ Registry serves all 20 images
- ✅ 700 attendees can pull in 30 minutes
- ✅ One-command setup for facilitator
- ✅ One-command config for attendees

**Nice to Have:**
- ✅ Web UI showing stats
- ✅ Progress bars
- ✅ Automatic retries
- ✅ Pretty terminal output

**Out of Scope:**
- ❌ Authentication (not needed on local network)
- ❌ HTTPS (not needed, adds complexity)
- ❌ Persistent storage (images already pushed)

---

## 14. Timeline

**Day 0 (Now)**: PRD approval ✅ (You're reading this)
**Day 1**: Build registry-setup.py
**Day 2**: Build configure-registry.py
**Day 3**: Build pull-workshop-images.py
**Day 4**: Testing with 5 people
**Day 5**: Documentation
**Day 6**: Final testing
**Conference Day**: Deploy!

---

## 15. Questions Before Implementation

Before I start coding, confirm:

1. ✅ **Registry approach approved?** (Yes, you chose this)
2. ❓ **Your laptop OS?** (macOS/Windows/Linux - for testing)
3. ❓ **Internet speed?** (for initial image pull)
4. ❓ **Test environment available?** (to test before conference)
5. ❓ **Conference date?** (how much time we have)

---

## 16. Next Steps

After PRD approval, I will:

1. **Clean up old files** (remove USB/bundle approach)
2. **Create docker-registry/ directory** (new clean structure)
3. **Implement registry-setup.py** (facilitator tool)
4. **Implement configure-registry.py** (attendee tool)
5. **Implement pull-workshop-images.py** (attendee tool)
6. **Create documentation** (guides for all)
7. **Test workflow** (end-to-end)

---

## 🎯 Ready to Proceed?

**This PRD defines:**
- ✅ What we're building (Docker Registry)
- ✅ How it works (Architecture)
- ✅ Who uses it (Facilitator + 700 attendees)
- ✅ Success metrics (15 min per attendee)
- ✅ Risk mitigation (Fallbacks)

**Approve this PRD and I'll start implementation immediately!**

Type **"APPROVED"** and I'll:
1. Delete old offline files
2. Create clean docker-registry structure
3. Build all scripts
4. Test everything
5. Document it all

Ready? 🚀
