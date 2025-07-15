#!/bin/bash

echo "🧹 Cleaning up Chaos Engineering Workshop"
echo "======================================="

# Find and stop all Jenkins containers
echo "🛑 Stopping all Jenkins containers..."
JENKINS_CONTAINERS=$(docker ps -aq --filter 'name=jenkins' 2>/dev/null)
if [ -n "$JENKINS_CONTAINERS" ]; then
    echo "Found Jenkins containers: $JENKINS_CONTAINERS"
    docker stop $JENKINS_CONTAINERS 2>/dev/null
    docker rm $JENKINS_CONTAINERS 2>/dev/null
    echo "✅ Jenkins containers stopped and removed"
else
    echo "ℹ️ No Jenkins containers found"
fi

# Remove chaos containers
echo "🗑️ Removing chaos containers..."
CHAOS_CONTAINERS=$(docker ps -aq --filter 'name=chaos-*' 2>/dev/null)
if [ -n "$CHAOS_CONTAINERS" ]; then
    echo "Found chaos containers: $CHAOS_CONTAINERS"
    docker rm -f $CHAOS_CONTAINERS 2>/dev/null
    echo "✅ Chaos containers removed"
else
    echo "ℹ️ No chaos containers found"
fi

# Clean up docker-compose services
echo "🗑️ Cleaning up docker-compose services..."
if [ -f "docker-compose-step5.yml" ]; then
    docker-compose -f docker-compose-step5.yml down 2>/dev/null || true
    echo "✅ Docker-compose services stopped"
else
    echo "ℹ️ No docker-compose file found"
fi

# Remove stable containers
echo "🗑️ Removing stable containers..."
STABLE_CONTAINERS=$(docker ps -aq --filter 'name=stable-*' 2>/dev/null)
if [ -n "$STABLE_CONTAINERS" ]; then
    echo "Found stable containers: $STABLE_CONTAINERS"
    docker rm -f $STABLE_CONTAINERS 2>/dev/null
    echo "✅ Stable containers removed"
else
    echo "ℹ️ No stable containers found"
fi

# Remove chaos networks
echo "🌐 Removing chaos networks..."
CHAOS_NETWORKS=$(docker network ls --filter 'name=chaos-*' --format '{{.Name}}' 2>/dev/null)
if [ -n "$CHAOS_NETWORKS" ]; then
    echo "Found chaos networks: $CHAOS_NETWORKS"
    echo "$CHAOS_NETWORKS" | xargs -I {} docker network rm {} 2>/dev/null
    echo "✅ Chaos networks removed"
else
    echo "ℹ️ No chaos networks found"
fi

# Remove Jenkins image
echo "🗑️ Removing Jenkins image..."
if docker images | grep -q jenkins-docker; then
    docker rmi jenkins-docker 2>/dev/null
    echo "✅ Jenkins image removed"
else
    echo "ℹ️ Jenkins image not found"
fi

# Clean up any dangling containers
echo "🧹 Cleaning up dangling containers..."
DANGLING_CONTAINERS=$(docker ps -aq --filter 'status=exited' 2>/dev/null)
if [ -n "$DANGLING_CONTAINERS" ]; then
    echo "Found dangling containers: $DANGLING_CONTAINERS"
    docker rm $DANGLING_CONTAINERS 2>/dev/null
    echo "✅ Dangling containers removed"
else
    echo "ℹ️ No dangling containers found"
fi

echo "✅ Cleanup complete!"
echo ""
echo "🎉 All chaos has been contained!"
echo ""
echo "💡 Pro Tip: You can now run ./setup.sh again to start fresh!" 