import docker
import json

client = docker.from_env()

tag = "ci-cd-chaos-app:v5"   # or whichever version you built

try:
    image = client.images.get(tag)
except docker.errors.ImageNotFound:
    print(f"Image {tag} not found!")
    exit(1)

print("RootFS Layers:")
print(json.dumps(image.attrs.get("RootFS", {}).get("Layers", []), indent=2))

print("\nDocker History:")
history = client.api.history(image.id)
for i, layer in enumerate(reversed(history), start=1):
    print(f"{i}: ID={layer.get('Id')}, Size={layer.get('Size')}, Cmd={layer.get('CreatedBy')}")
