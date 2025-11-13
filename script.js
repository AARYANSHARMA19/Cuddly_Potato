// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content-section');

    // Handle navigation clicks
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Show corresponding section
            const sectionId = this.getAttribute('data-section');
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });

    // Initialize with dashboard visible
    const dashboardLink = document.querySelector('[data-section="dashboard"]');
    const dashboardSection = document.getElementById('dashboard');
    if (dashboardLink && dashboardSection) {
        dashboardLink.classList.add('active');
        dashboardSection.classList.add('active');
    }
});

// EC2 Instance Functions
function createInstance() {
    alert('Launch EC2 Instance\n\n' +
          'In a real AWS console, this would open a wizard to:\n' +
          '1. Choose an AMI (Amazon Machine Image)\n' +
          '2. Select instance type (t2.micro, t3.medium, etc.)\n' +
          '3. Configure instance details\n' +
          '4. Add storage\n' +
          '5. Configure security groups\n' +
          '6. Review and launch');
}

// VPC Functions
function createVPC() {
    alert('Create VPC\n\n' +
          'In a real AWS console, this would allow you to:\n' +
          '1. Specify IPv4 CIDR block (e.g., 10.0.0.0/16)\n' +
          '2. Choose IPv6 CIDR block (optional)\n' +
          '3. Set tenancy (default or dedicated)\n' +
          '4. Name your VPC\n' +
          '5. Configure DNS hostnames and resolution');
}

// RDS Functions
function createDatabase() {
    alert('Create Database\n\n' +
          'In a real AWS console, this would allow you to:\n' +
          '1. Choose database engine (MySQL, PostgreSQL, etc.)\n' +
          '2. Select version\n' +
          '3. Choose DB instance class\n' +
          '4. Configure storage\n' +
          '5. Set up Multi-AZ deployment\n' +
          '6. Configure backup retention\n' +
          '7. Set up security groups\n' +
          '8. Create database');
}

// Load Balancer Functions
function createLoadBalancer() {
    alert('Create Load Balancer\n\n' +
          'In a real AWS console, this would allow you to:\n' +
          '1. Choose load balancer type (ALB, NLB, or Classic)\n' +
          '2. Configure load balancer settings\n' +
          '3. Select VPC and availability zones\n' +
          '4. Configure security groups\n' +
          '5. Configure routing (target groups)\n' +
          '6. Register targets (EC2 instances)\n' +
          '7. Review and create');
}

// Route 53 Functions
function createHostedZone() {
    alert('Create Hosted Zone\n\n' +
          'In a real AWS console, this would allow you to:\n' +
          '1. Enter domain name\n' +
          '2. Choose type (Public or Private)\n' +
          '3. Add comment/description\n' +
          '4. Configure VPC (for private zones)\n' +
          '5. Create hosted zone with NS and SOA records');
}

// Multi-Tier Architecture Functions
function deployArchitecture() {
    const confirmation = confirm(
        'Deploy Multi-Tier Architecture\n\n' +
        'This will create:\n' +
        '• VPC with public and private subnets across 3 AZs\n' +
        '• Internet Gateway and NAT Gateways\n' +
        '• Security Groups for each tier\n' +
        '• Application Load Balancers for web and app tiers\n' +
        '• EC2 instances for web and application tiers\n' +
        '• RDS database with Multi-AZ\n' +
        '• Route 53 DNS configuration\n\n' +
        'Estimated time: 15-20 minutes\n' +
        'Estimated cost: ~$200-300/month\n\n' +
        'Do you want to proceed?'
    );
    
    if (confirmation) {
        showDeploymentProgress();
    }
}

function showDeploymentProgress() {
    alert('Deployment Started!\n\n' +
          'In a real AWS console, you would see:\n' +
          '✓ Creating VPC...\n' +
          '✓ Creating subnets...\n' +
          '✓ Creating Internet Gateway...\n' +
          '✓ Creating NAT Gateways...\n' +
          '✓ Creating security groups...\n' +
          '✓ Launching EC2 instances...\n' +
          '✓ Creating load balancers...\n' +
          '✓ Creating RDS database...\n' +
          '✓ Configuring Route 53...\n\n' +
          'Deployment would complete in 15-20 minutes.\n' +
          'You would receive notifications at each step.');
}

function exportArchitecture() {
    const architectureConfig = {
        vpc: {
            cidr: '10.0.0.0/16',
            name: 'production-vpc',
            region: 'us-east-1'
        },
        subnets: [
            { name: 'public-subnet-1a', cidr: '10.0.1.0/24', az: 'us-east-1a', type: 'public' },
            { name: 'private-subnet-1b', cidr: '10.0.2.0/24', az: 'us-east-1b', type: 'private' },
            { name: 'private-subnet-1c', cidr: '10.0.3.0/24', az: 'us-east-1c', type: 'private' }
        ],
        securityGroups: [
            {
                name: 'web-tier-sg',
                inbound: [
                    { port: 80, protocol: 'tcp', source: '0.0.0.0/0' },
                    { port: 443, protocol: 'tcp', source: '0.0.0.0/0' }
                ]
            },
            {
                name: 'app-tier-sg',
                inbound: [
                    { port: 8080, protocol: 'tcp', source: 'web-tier-sg' }
                ]
            },
            {
                name: 'db-tier-sg',
                inbound: [
                    { port: 3306, protocol: 'tcp', source: 'app-tier-sg' }
                ]
            }
        ],
        loadBalancers: [
            { name: 'web-tier-alb', type: 'application', scheme: 'internet-facing' },
            { name: 'app-tier-alb', type: 'application', scheme: 'internal' }
        ],
        ec2Instances: [
            { name: 'web-server-01', type: 't3.medium', tier: 'web' },
            { name: 'web-server-02', type: 't3.medium', tier: 'web' },
            { name: 'app-server-01', type: 't3.large', tier: 'app' },
            { name: 'app-server-02', type: 't3.large', tier: 'app' },
            { name: 'app-server-03', type: 't3.large', tier: 'app' }
        ],
        rds: {
            identifier: 'prod-db-01',
            engine: 'mysql',
            version: '8.0.32',
            instanceClass: 'db.r5.large',
            multiAZ: true,
            storage: 100
        },
        route53: {
            domain: 'example.com',
            records: [
                { name: 'www', type: 'CNAME', value: 'web-tier-alb' },
                { name: 'api', type: 'CNAME', value: 'app-tier-alb' }
            ]
        }
    };

    const jsonStr = JSON.stringify(architectureConfig, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'aws-architecture-config.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    alert('Architecture configuration exported!\n\n' +
          'The JSON file contains:\n' +
          '• VPC and subnet configurations\n' +
          '• Security group rules\n' +
          '• Load balancer settings\n' +
          '• EC2 instance specifications\n' +
          '• RDS database configuration\n' +
          '• Route 53 DNS records\n\n' +
          'This can be used with Infrastructure as Code tools like:\n' +
          '• AWS CloudFormation\n' +
          '• Terraform\n' +
          '• AWS CDK');
}

// Add interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f0f8ff';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Add click handlers to action buttons
    const actionButtons = document.querySelectorAll('.btn-action');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const title = this.getAttribute('title');
            console.log(`Action clicked: ${title}`);
        });
    });
});

// Utility function to simulate API calls
function simulateAPICall(action, duration = 1000) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ success: true, action: action });
        }, duration);
    });
}

// Console logs for debugging
console.log('AWS Management Console loaded successfully');
console.log('Available services: EC2, VPC, RDS, ELB, Route 53');
console.log('Multi-tier architecture support enabled');
