#!/usr/bin/env python3
"""
Docker Utilities
Utility functions for Docker operations
"""

import docker
import asyncio
import os
from typing import Optional

class DockerUtils:
    """Docker utility functions"""
    
    def __init__(self):
        self.docker_client = docker.from_env()
    
    async def build_image(self, dockerfile_path: str, image_name: str, build_context: str = None):
        """Build Docker image from Dockerfile. Returns (success, error_message)."""
        try:
            if build_context is None:
                build_context = os.path.dirname(dockerfile_path)
                dockerfile_name = os.path.basename(dockerfile_path)
            else:
                # When using a dedicated build context, Docker expects the file to be named "Dockerfile"
                dockerfile_name = "Dockerfile"
            
            print(f"DEBUG DOCKER_UTILS: build_context={build_context}")
            print(f"DEBUG DOCKER_UTILS: dockerfile_name={dockerfile_name}")
            print(f"DEBUG DOCKER_UTILS: image_name={image_name}")
            print(f"DEBUG DOCKER_UTILS: Files in build_context: {os.listdir(build_context)}")
            
            image, logs = self.docker_client.images.build(
                path=build_context,
                dockerfile=dockerfile_name,
                tag=image_name,
                rm=True
            )
            return True, None
        except Exception as e:
            error_message = str(e)
            print(f"DEBUG DOCKER_UTILS: Exception caught: {error_message}")
            if hasattr(e, 'build_log'):
                try:
                    error_message = '\n'.join([str(line) for line in e.build_log])
                    print(f"DEBUG DOCKER_UTILS: Build log: {error_message}")
                except Exception:
                    pass
            return False, error_message
    
    async def pull_image(self, image_name: str) -> bool:
        """Pull Docker image from registry"""
        try:
            self.docker_client.images.pull(image_name)
            return True
        except Exception as e:
            print(f"Pull failed: {e}")
            return False
    
    async def image_exists(self, image_name: str) -> bool:
        """Check if image exists locally"""
        try:
            self.docker_client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            return False
    
    async def get_image_size(self, image_name: str) -> Optional[int]:
        """Get image size in bytes"""
        try:
            image = self.docker_client.images.get(image_name)
            return image.attrs['Size']
        except Exception:
            return None
    
    async def get_image_info(self, image_name: str) -> Optional[dict]:
        """Get detailed image information"""
        try:
            image = self.docker_client.images.get(image_name)
            return {
                'id': image.id,
                'tags': image.tags,
                'size': image.attrs['Size'],
                'created': image.attrs['Created'],
                'architecture': image.attrs['Architecture'],
                'os': image.attrs['Os']
            }
        except Exception:
            return None
    
    async def list_images(self) -> list:
        """List all local images"""
        try:
            images = self.docker_client.images.list()
            return [
                {
                    'id': img.id,
                    'tags': img.tags,
                    'size': img.attrs['Size'],
                    'created': img.attrs['Created']
                }
                for img in images
            ]
        except Exception:
            return []
    
    async def remove_image(self, image_name: str) -> bool:
        """Remove Docker image"""
        try:
            self.docker_client.images.remove(image_name, force=True)
            return True
        except Exception as e:
            print(f"Remove failed: {e}")
            return False
    
    async def run_container(self, image_name: str, command: str = None) -> Optional[str]:
        """Run container and return output"""
        try:
            container = self.docker_client.containers.run(
                image_name,
                command=command,
                detach=False,
                remove=True
            )
            return container.decode('utf-8') if isinstance(container, bytes) else str(container)
        except Exception as e:
            print(f"Container run failed: {e}")
            return None
    
    async def get_container_stats(self, image_name: str) -> Optional[dict]:
        """Get container statistics"""
        try:
            container = self.docker_client.containers.run(
                image_name,
                command="sleep 5",
                detach=True,
                remove=True
            )
            
            # Wait a moment for stats to be available
            await asyncio.sleep(1)
            
            stats = container.stats(stream=False)
            container.stop()
            
            return stats
            
        except Exception as e:
            print(f"Stats collection failed: {e}")
            return None 