// Enterprise Docker Analyzer - Frontend JavaScript

class DockerAnalyzer {
    constructor() {
        this.currentAnalysis = null;
        this.learningProgress = {
            completedSteps: new Set(),
            currentLevel: 1
        };
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Tab navigation
        this.initializeTabNavigation();
        
        // Image analysis
        document.getElementById('analyzeBtn').addEventListener('click', () => this.analyzeImage());
        
        // Compare images
        document.getElementById('compareBtn').addEventListener('click', () => this.compareImages());
        
        // Real-time updates
        this.initializeWebSocket();
        
        // Add educational tips
        this.showEducationalTips();
    }

    showEducationalTips() {
        // Show helpful tips for first-time users
        const tips = [
            "💡 Try analyzing 'nginx:alpine' to see a secure image",
            "💡 Try analyzing 'python:3.9-slim' to see vulnerabilities",
            "💡 Upload a Dockerfile to learn about best practices"
        ];
        
        // Show tips one by one with delays
        tips.forEach((tip, index) => {
            setTimeout(() => {
                this.showNotification(tip, 'info');
            }, (index + 1) * 3000);
        });
    }

    initializeTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Remove active class from all buttons and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked button and corresponding content
                button.classList.add('active');
                document.getElementById(`${targetTab}-tab`).classList.add('active');
                
                // Show contextual help
                this.showContextualHelp(targetTab);

                // Clear dashboard and analysis sections when switching tabs
                if (targetTab === 'compare') {
                    this.clearAnalysisSections();
                }
            });
        });
    }

    showContextualHelp(tab) {
        const helpMessages = {
            'image': '🔍 Enter any Docker image name to analyze its security vulnerabilities and best practices.',
            'compare': '⚖️ Compare two Docker images side-by-side to understand security differences.'
        };
        
        if (helpMessages[tab]) {
            this.showNotification(helpMessages[tab], 'info');
        }
    }

    async analyzeImage() {
        const imageName = document.getElementById('imageName').value.trim();
        
        if (!imageName) {
            this.showNotification('❌ Please enter an image name', 'error');
            return;
        }

        // Validate image name format
        if (!imageName.includes(':')) {
            this.showNotification('❌ Please use format: image:tag (e.g., nginx:alpine)', 'error');
            return;
        }

        try {
            this.showProgress();
            this.updateStatus('🔍 Analyzing Docker image with real Trivy vulnerability scanning...');
            
            const response = await fetch('/api/v1/analyze/image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image_name: imageName,
                    analysis_type: 'comprehensive'
                })
            });

            const result = await response.json();
            
            if (response.ok && !result.error) {
                this.displayEducationalResults(result);
                this.showNotification('✅ Analysis completed! Check the results below.', 'success');
                this.markStepCompleted('image_analysis');
            } else {
                this.displayError(result.error || 'Analysis failed');
                this.showNotification(result.error || 'Analysis failed', 'error');
            }
        } catch (error) {
            this.displayError('Analysis failed: ' + error.message);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            this.hideProgress();
        }
    }

    displayEducationalResults(result) {
        this.currentAnalysis = result;
        
        // Update main dashboard
        this.updateDashboard(result);
        
        // Update detailed analysis cards
        this.updateAnalysisCards(result);
        
        // Show educational insights
        this.displayLearningInsights(result);
        
        // Show best practices
        this.displayBestPractices(result);
        
        // Show industry comparison
        this.displayIndustryComparison(result);
        
        // Show detailed vulnerabilities
        this.displayVulnerabilities(result);
        
        // Update progress and status
        this.updateStatus('✅ Analysis completed successfully!');
        this.hideProgress();
        
        // Show learning progress
        this.updateLearningProgress();
    }

    updateLearningProgress() {
        const progress = (this.learningProgress.completedSteps.size / 6) * 100;
        
        if (progress >= 50 && this.learningProgress.currentLevel === 1) {
            this.learningProgress.currentLevel = 2;
            this.showNotification('🎓 Level Up! You\'re now at Intermediate level. Try creating your own Dockerfile!', 'success');
        }
        
        if (progress >= 80 && this.learningProgress.currentLevel === 2) {
            this.learningProgress.currentLevel = 3;
            this.showNotification('🏆 Advanced Level! You\'re mastering Docker security!', 'success');
        }
    }

    markStepCompleted(step) {
        this.learningProgress.completedSteps.add(step);
        this.updateLearningProgress();
    }

    updateDashboard(result) {
        const dashboard = document.getElementById('dashboard');
        
        const securityScore = result.security_analysis?.security_score || 0;
        const totalVulns = result.security_analysis?.total_vulnerabilities || 0;
        const criticalVulns = result.security_analysis?.critical_count || 0;
        const highVulns = result.security_analysis?.high_count || 0;
        
        dashboard.innerHTML = `
            <div class="dashboard-header">
                <h2>🐳 Docker Image Analysis: ${result.image_name}</h2>
                <div class="analysis-timestamp">📅 ${new Date(result.timestamp).toLocaleString()}</div>
            </div>
            
            <div class="dashboard-metrics">
                <div class="metric-card ${this.getSecurityScoreClass(securityScore)}">
                    <div class="metric-icon">🛡️</div>
                    <div class="metric-value">${securityScore.toFixed(1)}</div>
                    <div class="metric-label">Security Score</div>
                </div>
                
                <div class="metric-card ${criticalVulns > 0 ? 'critical' : 'success'}">
                    <div class="metric-icon">🚨</div>
                    <div class="metric-value">${criticalVulns}</div>
                    <div class="metric-label">Critical Vulnerabilities</div>
                </div>
                
                <div class="metric-card ${highVulns > 0 ? 'warning' : 'success'}">
                    <div class="metric-icon">⚠️</div>
                    <div class="metric-value">${highVulns}</div>
                    <div class="metric-label">High Vulnerabilities</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-value">${totalVulns}</div>
                    <div class="metric-label">Total Vulnerabilities</div>
                </div>
            </div>
            
            ${this.getEducationalSummary(result)}
        `;
    }

    getEducationalSummary(result) {
        const securityScore = result.security_analysis?.security_score || 0;
        const totalVulns = result.security_analysis?.total_vulnerabilities || 0;
        
        if (securityScore >= 90) {
            return `
                <div class="educational-summary success">
                    <h3>🎉 Excellent Security!</h3>
                    <p>This image follows security best practices. Great job!</p>
                </div>
            `;
        } else if (securityScore >= 70) {
            return `
                <div class="educational-summary warning">
                    <h3>⚠️ Good, but can be improved</h3>
                    <p>This image has some security issues. Check the recommendations below.</p>
                </div>
            `;
        } else {
            return `
                <div class="educational-summary critical">
                    <h3>🚨 Security Issues Found</h3>
                    <p>This image has significant security vulnerabilities. Review the details below.</p>
                </div>
            `;
        }
    }

    displayLearningInsights(result) {
        const insightsContainer = document.getElementById('learningInsights');
        const insights = result.learning_insights || [];
        
        if (insights.length === 0) {
            insightsContainer.innerHTML = `
                <div class="insights-section">
                    <h3>🎉 No significant issues found!</h3>
                    <p>Your image follows good security practices. This is excellent!</p>
                </div>
            `;
            return;
        }
        
        insightsContainer.innerHTML = `
            <div class="insights-section">
                <h3>💡 Learning Insights</h3>
                <div class="insights-list">
                    ${insights.map(insight => `
                        <div class="insight-item">
                            <div class="insight-icon">${this.getInsightIcon(insight)}</div>
                            <div class="insight-text">${insight}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    displayBestPractices(result) {
        const practicesContainer = document.getElementById('bestPractices');
        const practices = result.best_practices || [];
        
        if (practices.length === 0) {
            practicesContainer.innerHTML = `
                <div class="practices-section">
                    <h3>✅ Best Practices Followed</h3>
                    <p>Your image follows Docker security best practices!</p>
                </div>
            `;
            return;
        }
        
        practicesContainer.innerHTML = `
            <div class="practices-section">
                <h3>📚 Best Practices & Recommendations</h3>
                <div class="practices-list">
                    ${practices.map(practice => `
                        <div class="practice-item ${practice.priority.toLowerCase()}">
                            <div class="practice-header">
                                <h4>${practice.title}</h4>
                                <span class="practice-category">${practice.category}</span>
                                <span class="practice-priority ${practice.priority.toLowerCase()}">${practice.priority}</span>
                            </div>
                            <div class="practice-description">${practice.description}</div>
                            <div class="practice-impact"><strong>Impact:</strong> ${practice.impact}</div>
                            <div class="practice-recommendation"><strong>Recommendation:</strong> ${practice.recommendation}</div>
                            ${practice.example ? `<div class="practice-example"><strong>Example:</strong><pre>${practice.example}</pre></div>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    displayIndustryComparison(result) {
        const comparisonContainer = document.getElementById('industryComparison');
        const comparison = result.industry_benchmark || {};
        
        if (!comparison || Object.keys(comparison).length === 0) {
            comparisonContainer.innerHTML = `
                <div class="comparison-section">
                    <h3>📊 Industry Comparison</h3>
                    <p>Industry comparison data not available for this image.</p>
                </div>
            `;
            return;
        }
        
        comparisonContainer.innerHTML = `
            <div class="comparison-section">
                <h3>📊 Industry Comparison</h3>
                <div class="comparison-metrics">
                    ${comparison.percentile ? `<div class="comparison-item"><strong>Percentile:</strong> ${comparison.percentile}</div>` : ''}
                    ${comparison.recommendation ? `<div class="comparison-item"><strong>Recommendation:</strong> ${comparison.recommendation}</div>` : ''}
                </div>
            </div>
        `;
    }

    displayVulnerabilities(result) {
        const vulnContainer = document.getElementById('vulnerabilities');
        const vulnerabilities = result.security_analysis?.vulnerabilities || [];
        
        if (vulnerabilities.length === 0) {
            vulnContainer.innerHTML = `
                <div class="vulnerabilities-section">
                    <h3>✅ No Vulnerabilities Found</h3>
                    <p>Excellent! No security vulnerabilities were detected in this image.</p>
                </div>
            `;
            return;
        }
        
        // Group vulnerabilities by severity
        const grouped = {
            CRITICAL: vulnerabilities.filter(v => v.severity === 'CRITICAL'),
            HIGH: vulnerabilities.filter(v => v.severity === 'HIGH'),
            MEDIUM: vulnerabilities.filter(v => v.severity === 'MEDIUM'),
            LOW: vulnerabilities.filter(v => v.severity === 'LOW')
        };
        
        vulnContainer.innerHTML = `
            <div class="vulnerabilities-section">
                <h3>🔍 Vulnerability Details</h3>
                ${Object.entries(grouped).map(([severity, vulns]) => 
                    vulns.length > 0 ? `
                        <div class="vuln-section ${severity.toLowerCase()}">
                            <h4>${severity} (${vulns.length})</h4>
                            <div class="vulnerability-list">
                                ${vulns.map(vuln => `
                                    <div class="vulnerability-item">
                                        <div class="vuln-header">
                                            <span class="vuln-cve">${vuln.cve_id}</span>
                                            <span class="vuln-severity ${vuln.severity.toLowerCase()}">${vuln.severity}</span>
                                        </div>
                                        <div class="vuln-package"><strong>Package:</strong> ${vuln.package_name}</div>
                                        <div class="vuln-version"><strong>Version:</strong> ${vuln.installed_version}</div>
                                        ${vuln.fixed_version ? `<div class="vuln-fixed"><strong>Fixed in:</strong> ${vuln.fixed_version}</div>` : ''}
                                        <div class="vuln-description">${vuln.description}</div>
                                        ${vuln.cvss_score > 0 ? `<div class="vuln-cvss"><strong>CVSS Score:</strong> ${vuln.cvss_score}</div>` : ''}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''
                ).join('')}
            </div>
        `;
    }

    renderVulnerabilityList(vulnerabilities) {
        return vulnerabilities.map(vuln => `
            <div class="vulnerability-item">
                <div class="vuln-header">
                    <span class="vuln-cve">${vuln.cve_id}</span>
                    <span class="vuln-severity ${vuln.severity.toLowerCase()}">${vuln.severity}</span>
                </div>
                <div class="vuln-package"><strong>Package:</strong> ${vuln.package_name}</div>
                <div class="vuln-version"><strong>Version:</strong> ${vuln.installed_version}</div>
                ${vuln.fixed_version ? `<div class="vuln-fixed"><strong>Fixed in:</strong> ${vuln.fixed_version}</div>` : ''}
                <div class="vuln-description">${vuln.description}</div>
                ${vuln.cvss_score > 0 ? `<div class="vuln-cvss"><strong>CVSS Score:</strong> ${vuln.cvss_score}</div>` : ''}
            </div>
        `).join('');
    }

    updateAnalysisCards(result) {
        // Update Docker analysis
        if (result.docker_analysis) {
            this.updateDockerAnalysis(result.docker_analysis);
        }
        
        // Update Security analysis
        if (result.security_analysis) {
            this.updateSecurityAnalysis(result.security_analysis);
        }
        
        // Update Performance analysis
        if (result.performance_analysis) {
            this.updatePerformanceAnalysis(result.performance_analysis);
        }
    }

    updateDockerAnalysis(analysis) {
        const container = document.getElementById('dockerAnalysis');
        if (analysis.error) {
            container.innerHTML = `<p class="error">${analysis.error}</p>`;
            return;
        }
        
        const sizeMB = (analysis.total_size / (1024 * 1024)).toFixed(2);
        container.innerHTML = `
            <div class="metric"><strong>Image Size:</strong> ${sizeMB} MB</div>
            <div class="metric"><strong>Layers:</strong> ${analysis.layer_count}</div>
            <div class="metric"><strong>Base Image:</strong> ${analysis.base_image}</div>
            <div class="metric"><strong>User:</strong> ${analysis.user_configuration}</div>
            ${analysis.exposed_ports.length > 0 ? `<div class="metric"><strong>Exposed Ports:</strong> ${analysis.exposed_ports.join(', ')}</div>` : ''}
        `;
    }

    updateSecurityAnalysis(analysis) {
        const container = document.getElementById('securityAnalysis');
        container.innerHTML = `
            <div class="metric"><strong>Security Score:</strong> ${analysis.security_score.toFixed(1)}/100</div>
            <div class="metric"><strong>Total Vulnerabilities:</strong> ${analysis.total_vulnerabilities}</div>
            <div class="metric"><strong>Critical:</strong> ${analysis.critical_count}</div>
            <div class="metric"><strong>High:</strong> ${analysis.high_count}</div>
            <div class="metric"><strong>Medium:</strong> ${analysis.medium_count}</div>
            <div class="metric"><strong>Low:</strong> ${analysis.low_count}</div>
        `;
    }

    updatePerformanceAnalysis(analysis) {
        const container = document.getElementById('performanceAnalysis');
        if (analysis.error) {
            container.innerHTML = `<p class="error">${analysis.error}</p>`;
            return;
        }
        
        container.innerHTML = `
            <div class="metric"><strong>Image Size:</strong> ${analysis.image_size_mb} MB</div>
            <div class="metric"><strong>Performance Score:</strong> ${analysis.performance_score}/100</div>
            <div class="metric"><strong>Recommendations:</strong></div>
            <ul>
                ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        `;
    }

    getSecurityScoreClass(score) {
        if (score >= 90) return 'success';
        if (score >= 70) return 'warning';
        return 'critical';
    }

    getInsightIcon(insight) {
        if (insight.includes('vulnerability')) return '🚨';
        if (insight.includes('security')) return '🛡️';
        if (insight.includes('best practice')) return '📚';
        if (insight.includes('performance')) return '⚡';
        if (insight.includes('size')) return '📦';
        return '💡';
    }

    async compareImages() {
        const image1 = document.getElementById('compareImage1').value.trim();
        const image2 = document.getElementById('compareImage2').value.trim();
        
        if (!image1 || !image2) {
            this.showNotification('❌ Please enter both image names', 'error');
            return;
        }

        // Clear previous analysis results before showing comparison
        this.clearAnalysisSections();

        try {
            this.showProgress();
            this.updateStatus('⚖️ Comparing images...');
            
            const response = await fetch(`/api/v1/compare?image1=${encodeURIComponent(image1)}&image2=${encodeURIComponent(image2)}`);
            const result = await response.json();
            
            if (response.ok && !result.error) {
                this.displayComparison(result);
                this.showNotification('✅ Comparison completed!', 'success');
                this.markStepCompleted('image_comparison');
            } else {
                this.displayError(result.error || 'Comparison failed');
                this.showNotification(result.error || 'Comparison failed', 'error');
            }
        } catch (error) {
            this.displayError('Comparison failed: ' + error.message);
            this.showNotification('Comparison failed: ' + error.message, 'error');
        } finally {
            this.hideProgress();
        }
    }

    displayComparison(result) {
        // Hide unrelated sections for a focused comparison view
        document.getElementById('dashboard').style.display = 'none';
        document.getElementById('learningInsights').style.display = 'none';
        document.getElementById('bestPractices').style.display = 'none';
        document.getElementById('industryComparison').style.display = 'none';
        document.querySelector('.analysis-cards').style.display = 'none';
        document.getElementById('vulnerabilities').style.display = 'none';

        const container = document.getElementById('comparisonResults');
        const image1 = result.image1;
        const image2 = result.image2;
        const comparison = result.comparison;

        // Determine winner
        let winner = null;
        if (image1.vulnerabilities < image2.vulnerabilities) winner = 1;
        else if (image2.vulnerabilities < image1.vulnerabilities) winner = 2;

        // Fun fact or security tip
        const funFacts = [
            "🔒 Did you know? Alpine-based images often have 80% fewer vulnerabilities than full OS images!",
            "🚀 Tip: Regularly update your base images to reduce known CVEs.",
            "🐳 Use multi-stage builds to keep your images lean and secure.",
            "🛡️ The fewer packages, the smaller the attack surface!"
        ];
        const randomFact = funFacts[Math.floor(Math.random() * funFacts.length)];

        // Mini bar chart HTML
        function miniBarChart(val1, val2, label) {
            const max = Math.max(val1, val2, 1);
            const w1 = Math.round((val1 / max) * 100);
            const w2 = Math.round((val2 / max) * 100);
            return `<div class='mini-bar-chart'><span>${label}:</span>
                <div class='bar bar1' style='width:${w1}px' title='${val1}'></div>
                <div class='bar bar2' style='width:${w2}px' title='${val2}'></div>
                <span class='bar-label'>${val1} vs ${val2}</span>
            </div>`;
        }

        container.innerHTML = `
            <div class="comparison-results-card animated-fade-in">
                <h3>⚖️ Image Comparison Results</h3>
                <div class="comparison-grid-insightful">
                    <div class="comparison-item-highlight ${winner === 1 ? 'winner' : ''}">
                        <h4>${image1.name} ${winner === 1 ? '🏆' : ''}</h4>
                        <div class="metric">Vulnerabilities: <span class="badge ${winner === 1 ? 'badge-success' : 'badge-danger'}">${image1.vulnerabilities}</span></div>
                        <div class="metric">Security Score: <span class="badge">${image1.security_score.toFixed(1)}</span></div>
                        ${miniBarChart(image1.vulnerabilities, image2.vulnerabilities, 'Vulnerabilities')}
                        ${miniBarChart(image1.security_score, image2.security_score, 'Score')}
                    </div>
                    <div class="comparison-item-highlight ${winner === 2 ? 'winner' : ''}">
                        <h4>${image2.name} ${winner === 2 ? '🏆' : ''}</h4>
                        <div class="metric">Vulnerabilities: <span class="badge ${winner === 2 ? 'badge-success' : 'badge-danger'}">${image2.vulnerabilities}</span></div>
                        <div class="metric">Security Score: <span class="badge">${image2.security_score.toFixed(1)}</span></div>
                        ${miniBarChart(image2.vulnerabilities, image1.vulnerabilities, 'Vulnerabilities')}
                        ${miniBarChart(image2.security_score, image1.security_score, 'Score')}
                    </div>
                </div>
                <div class="comparison-recommendation">
                    <h4>💡 Recommendation</h4>
                    <p>${comparison.recommendation}</p>
                    <p><strong>Vulnerability Difference:</strong> ${comparison.vulnerability_difference}</p>
                    <p><strong>Score Difference:</strong> ${comparison.score_difference.toFixed(1)}</p>
                </div>
                <div class="comparison-actions">
                    <button class="btn btn-secondary" onclick="window.dockerAnalyzer.swapComparisonImages()">🔄 Swap Images</button>
                    <button class="btn btn-primary" onclick="window.dockerAnalyzer.resetComparisonView()">🔬 New Comparison</button>
                    <button class="btn btn-success" onclick="window.dockerAnalyzer.downloadComparisonReport()">⬇️ Download Comparison Report</button>
                </div>
                <div class="comparison-funfact">
                    <span>${randomFact}</span>
                </div>
            </div>
        `;
        container.style.display = 'block';
    }

    downloadComparisonReport() {
        const container = document.getElementById('comparisonResults');
        const html = container.innerHTML;
        const blob = new Blob([`<html><body>${html}</body></html>`], {type: 'text/html'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'docker-image-comparison.html';
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    }

    swapComparisonImages() {
        const img1 = document.getElementById('compareImage1');
        const img2 = document.getElementById('compareImage2');
        const temp = img1.value;
        img1.value = img2.value;
        img2.value = temp;
        this.compareImages();
    }

    resetComparisonView() {
        // Show all sections again
        document.getElementById('dashboard').style.display = '';
        document.getElementById('learningInsights').style.display = '';
        document.getElementById('bestPractices').style.display = '';
        document.getElementById('industryComparison').style.display = '';
        document.querySelector('.analysis-cards').style.display = '';
        document.getElementById('vulnerabilities').style.display = '';
        document.getElementById('comparisonResults').innerHTML = '';
    }

    showProgress() {
        document.getElementById('progress').style.display = 'block';
        document.querySelector('.progress-fill').style.width = '0%';
        this.animateProgress();
    }

    hideProgress() {
        document.getElementById('progress').style.display = 'none';
    }

    animateProgress() {
        const progressFill = document.querySelector('.progress-fill');
        let width = 0;
        const interval = setInterval(() => {
            if (width >= 90) {
                clearInterval(interval);
            } else {
                width += Math.random() * 10;
                progressFill.style.width = width + '%';
            }
        }, 200);
    }

    updateStatus(message) {
        document.getElementById('status').textContent = message;
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 8 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 8000);
    }

    initializeWebSocket() {
        // WebSocket for real-time updates (if needed)
        // Currently using polling for simplicity
    }

    displayError(message) {
        const dashboard = document.getElementById('dashboard');
        dashboard.innerHTML = `
            <div class="error-state">
                <h3>❌ Analysis Failed</h3>
                <div class="error-message">${message}</div>
                <div class="error-suggestions">
                    <h4>💡 Try these solutions:</h4>
                    <ul>
                        <li>Check your internet connection</li>
                        <li>Try a different image name</li>
                        <li>Ensure Docker is running</li>
                        <li>Verify Trivy is installed</li>
                    </ul>
                </div>
            </div>
        `;
    }

    clearAnalysisSections() {
        // Clear all main analysis sections
        document.getElementById('dashboard').innerHTML = '';
        document.getElementById('learningInsights').innerHTML = '';
        document.getElementById('bestPractices').innerHTML = '';
        document.getElementById('industryComparison').innerHTML = '';
        document.getElementById('dockerAnalysis').innerHTML = '<p>Analyze an image to see Docker configuration details</p>';
        document.getElementById('securityAnalysis').innerHTML = '<p>Real Trivy vulnerability scanning results</p>';
        document.getElementById('performanceAnalysis').innerHTML = '<p>Image size and performance metrics</p>';
        document.getElementById('vulnerabilities').innerHTML = '';
    }
}

// Initialize the analyzer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dockerAnalyzer = new DockerAnalyzer();
}); 