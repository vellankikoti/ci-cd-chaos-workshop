
# Scenario 1: Docker Build Chaos - Robust Demo Guide

## 🚀 How to Use This Scenario for Demos

### 1. Run the Jenkins Pipeline
- Go to the `scenario_01_docker_build` pipeline in Jenkins.
- Set the `APP_VERSION` parameter (1-5) to choose which app version to build and run.
- By default, the app container will be left running after the pipeline for manual inspection and demo purposes.
- If you want the container to be removed automatically, set the `CLEANUP_AFTER` parameter to `true`.

### 2. What Happens in the Pipeline
- **Verify Local Workspace:** Shows workspace contents and checks for required files (Dockerfile).
- **Validate Version:** Ensures you selected a valid version (1-5).
- **🧹 Pre-Cleanup:** Removes any old containers using port 3000 or with the same name.
- **🔧 Build Docker Image:** Builds the app image for the selected version using standardized environment variables.
- **🚀 Run App Container:** Starts the app on port 3000.
- **📋 Check App Logs:** Shows logs from the running container.
- **🌐 Test HTTP Response:** Checks if the app responds on http://localhost:3000.
- **🎉 Demo Instructions:** Prints clear instructions for manual testing and next steps.
- **Cleanup (optional):** If `CLEANUP_AFTER` is true, removes the container at the end.

### 3. Pipeline Improvements
- **Standardized Environment Variables:** Uses consistent `SCENARIO_PATH`, `IMAGE_NAME`, `BUILD_TAG` variables.
- **Robust Workspace Verification:** Checks for required files and shows workspace contents.
- **Enhanced Error Handling:** Proper success/failure post actions with clear messaging.
- **Consistent Stage Naming:** All stages use emojis and follow the same pattern as other scenarios.

### 4. Manual Testing
- After the pipeline, the app will be running in a container named `chaos-app-vX` (where X is the version).
- Access the app at: [http://localhost:3000](http://localhost:3000)
- View logs:
  ```bash
  docker logs chaos-app-v1  # or v2, v3, v4, v5
  ```
- Stop/remove the container:
  ```bash
  docker rm -f chaos-app-v1
  ```
- Switch versions by re-running the pipeline with a different `APP_VERSION`.

### 5. Cleanup All Demo Containers
- Use the provided script to remove all demo containers:
  ```bash
  ./cleanup_chaos_apps.sh
  ```

### 6. Demo Tips
- You can run multiple versions (on different ports) by editing the Jenkinsfile to use different ports per version.
- The pipeline is robust and will show all steps, errors, and demo instructions.
- Use the `CLEANUP_AFTER` parameter for automated cleanup, or leave containers running for live demos.
- The pipeline now follows the same reliable pattern as all other scenarios.

---

**Happy Chaos Demoing!**