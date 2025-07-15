#!/usr/bin/env python3
"""
Security Scanner Component
Real vulnerability scanning using Trivy and other security tools
"""

import subprocess
import json
import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Vulnerability:
    """Vulnerability information"""
    cve_id: str
    severity: str
    package_name: str
    installed_version: str
    fixed_version: str
    description: str
    score: float

@dataclass
class SecurityAnalysis:
    """Security analysis result"""
    vulnerabilities: List[Vulnerability]
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    security_score: float
    recommendations: List[str]

class SecurityScanner:
    """Enterprise security scanner using real vulnerability data"""
    
    def __init__(self):
        self.trivy_available = self._check_trivy_availability()
    
    def _check_trivy_availability(self) -> bool:
        """Check if Trivy is available via Docker"""
        import subprocess
        try:
            # Check Docker is available
            docker_check = subprocess.run(['docker', 'info'], capture_output=True, text=True)
            if docker_check.returncode != 0:
                return False
            # Check Trivy image is available (pull if not)
            trivy_check = subprocess.run([
                'docker', 'run', '--rm',
                '-v', '/var/run/docker.sock:/var/run/docker.sock',
                'aquasec/trivy:latest', '--version'
            ], capture_output=True, text=True)
            return trivy_check.returncode == 0
        except Exception:
            return False
    
    async def scan_image_security(self, image_name: str) -> SecurityAnalysis:
        """
        Comprehensive security analysis using real vulnerability data
        """
        try:
            if self.trivy_available:
                return await self._scan_with_trivy(image_name)
            else:
                return await self._scan_with_basic_checks(image_name)
        except Exception as e:
            return await self._create_error_analysis(str(e))
    
    async def _scan_with_trivy(self, image_name: str) -> SecurityAnalysis:
        """Scan using Trivy for real vulnerability data via Dockerized Trivy"""
        import asyncio
        try:
            cmd = [
                'docker', 'run', '--rm',
                '-v', '/var/run/docker.sock:/var/run/docker.sock',
                'aquasec/trivy:latest', 'image',
                '--format', 'json',
                '--severity', 'CRITICAL,HIGH,MEDIUM,LOW',
                image_name
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                return await self._create_error_analysis(f"Trivy scan failed: {stderr.decode()}")
            scan_results = json.loads(stdout.decode())
            vulnerabilities = self._parse_trivy_results(scan_results)
            return await self._create_security_analysis(vulnerabilities)
        except Exception as e:
            return await self._create_error_analysis(f"Trivy scan error: {str(e)}")
    
    def _parse_trivy_results(self, scan_results: Dict[str, Any]) -> List[Vulnerability]:
        """Parse Trivy JSON results into vulnerability objects"""
        vulnerabilities = []
        
        for result in scan_results.get('Results', []):
            target = result.get('Target', '')
            
            for vuln in result.get('Vulnerabilities', []):
                vulnerability = Vulnerability(
                    cve_id=vuln.get('VulnerabilityID', ''),
                    severity=vuln.get('Severity', 'UNKNOWN'),
                    package_name=vuln.get('PkgName', ''),
                    installed_version=vuln.get('InstalledVersion', ''),
                    fixed_version=vuln.get('FixedVersion', ''),
                    description=vuln.get('Description', ''),
                    score=float(vuln.get('CVSS', {}).get('nvd', {}).get('V3Score', 0))
                )
                vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    async def _scan_with_basic_checks(self, image_name: str) -> SecurityAnalysis:
        """Basic security checks when Trivy is not available"""
        vulnerabilities = []
        
        # Basic security checks
        basic_checks = [
            self._check_root_user(image_name),
            self._check_exposed_ports(image_name),
            self._check_environment_variables(image_name)
        ]
        
        for check in basic_checks:
            if check:
                vulnerabilities.append(check)
        
        return await self._create_security_analysis(vulnerabilities)
    
    async def _check_root_user(self, image_name: str) -> Vulnerability:
        """Check if container runs as root"""
        try:
            import docker
            client = docker.from_env()
            image = client.images.get(image_name)
            
            config = image.attrs.get('Config', {})
            user = config.get('User', 'root')
            
            if user == 'root':
                return Vulnerability(
                    cve_id='SEC-001',
                    severity='HIGH',
                    package_name='user_configuration',
                    installed_version='root',
                    fixed_version='non-root',
                    description='Container runs as root user, which is a security risk',
                    score=8.0
                )
        except Exception:
            pass
        
        return None
    
    async def _check_exposed_ports(self, image_name: str) -> Vulnerability:
        """Check for unnecessary exposed ports"""
        try:
            import docker
            client = docker.from_env()
            image = client.images.get(image_name)
            
            config = image.attrs.get('Config', {})
            exposed_ports = config.get('ExposedPorts', {})
            
            if len(exposed_ports) > 5:
                return Vulnerability(
                    cve_id='SEC-002',
                    severity='MEDIUM',
                    package_name='port_configuration',
                    installed_version=f'{len(exposed_ports)} ports',
                    fixed_version='minimal ports',
                    description='Too many exposed ports increase attack surface',
                    score=5.0
                )
        except Exception:
            pass
        
        return None
    
    async def _check_environment_variables(self, image_name: str) -> Vulnerability:
        """Check for sensitive environment variables"""
        try:
            import docker
            client = docker.from_env()
            image = client.images.get(image_name)
            
            config = image.attrs.get('Config', {})
            env_vars = config.get('Env', [])
            
            sensitive_patterns = ['password', 'secret', 'key', 'token', 'credential']
            
            for env_var in env_vars:
                for pattern in sensitive_patterns:
                    if pattern in env_var.lower():
                        return Vulnerability(
                            cve_id='SEC-003',
                            severity='HIGH',
                            package_name='environment_variables',
                            installed_version='sensitive_data',
                            fixed_version='use_secrets',
                            description='Sensitive data found in environment variables',
                            score=7.0
                        )
        except Exception:
            pass
        
        return None
    
    async def _create_security_analysis(self, vulnerabilities: List[Vulnerability]) -> SecurityAnalysis:
        """Create comprehensive security analysis"""
        # Count vulnerabilities by severity
        critical_count = len([v for v in vulnerabilities if v.severity == 'CRITICAL'])
        high_count = len([v for v in vulnerabilities if v.severity == 'HIGH'])
        medium_count = len([v for v in vulnerabilities if v.severity == 'MEDIUM'])
        low_count = len([v for v in vulnerabilities if v.severity == 'LOW'])
        
        # Calculate security score
        security_score = 100.0
        security_score -= critical_count * 20
        security_score -= high_count * 15
        security_score -= medium_count * 10
        security_score -= low_count * 5
        
        # Generate recommendations
        recommendations = []
        
        if critical_count > 0:
            recommendations.append("Immediately patch critical vulnerabilities")
        
        if high_count > 0:
            recommendations.append("Prioritize patching high severity vulnerabilities")
        
        if any(v.severity == 'HIGH' and 'root' in v.description.lower() for v in vulnerabilities):
            recommendations.append("Create a non-root user for better security")
        
        if any('port' in v.description.lower() for v in vulnerabilities):
            recommendations.append("Minimize exposed ports to reduce attack surface")
        
        if any('environment' in v.description.lower() for v in vulnerabilities):
            recommendations.append("Use Docker secrets instead of environment variables for sensitive data")
        
        return SecurityAnalysis(
            vulnerabilities=vulnerabilities,
            total_vulnerabilities=len(vulnerabilities),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            security_score=max(0.0, security_score),
            recommendations=recommendations
        )
    
    async def _create_error_analysis(self, error_message: str) -> SecurityAnalysis:
        """Create error analysis when scanning fails"""
        return SecurityAnalysis(
            vulnerabilities=[],
            total_vulnerabilities=0,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0,
            security_score=0.0,
            recommendations=[f"Security scan failed: {error_message}"]
        ) 