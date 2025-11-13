# AWS Management Console

A comprehensive web-based interface for managing AWS cloud services. This console provides an intuitive UI for managing compute, networking, databases, load balancers, DNS, and multi-tier architectures.

## 🌟 Features

### Services Supported

1. **EC2 (Elastic Compute Cloud)** - Compute Management
   - Launch and manage EC2 instances
   - View instance status, types, and availability zones
   - Monitor public IPs and instance health
   - Stop and terminate instances

2. **VPC (Virtual Private Cloud)** - Networking
   - Create and manage VPCs with custom CIDR blocks
   - Configure subnets (public and private)
   - Manage security groups with inbound/outbound rules
   - Monitor network resources across availability zones

3. **RDS (Relational Database Service)** - Database Management
   - Create and manage database instances
   - Support for MySQL, PostgreSQL, and other engines
   - Configure instance classes and storage
   - View database endpoints and status

4. **Load Balancers (ELB/ALB)** - Traffic Distribution
   - Create Application Load Balancers (ALB)
   - Manage Classic Load Balancers (ELB)
   - Configure target groups and health checks
   - View DNS names and distribution settings

5. **Route 53** - DNS Management
   - Create and manage hosted zones
   - Configure DNS records (A, CNAME, etc.)
   - Set routing policies (Simple, Weighted, etc.)
   - Manage TTL and record values

6. **Multi-Tier Architecture** - Architecture Visualization
   - Visualize three-tier architecture (Web → App → DB)
   - View security group configurations
   - See load balancer distributions
   - Export architecture configurations
   - Deploy complete architectures

## 🏗️ Multi-Tier Architecture

The console includes a comprehensive multi-tier architecture implementation:

### **Web Tier**
- Internet-facing Application Load Balancer
- EC2 instances in public subnets
- Security group allowing HTTP (80) and HTTPS (443)
- Serves static content and forwards requests to app tier

### **Application Tier**
- Internal Application Load Balancer
- EC2 instances in private subnets
- Security group allowing traffic only from web tier
- Processes business logic and communicates with database

### **Database Tier**
- RDS instances in private subnets
- Security group allowing traffic only from app tier
- Multi-AZ deployment for high availability
- Read replicas for scalability

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, or Edge)
- No additional dependencies required

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AARYANSHARMA19/Aws_Mangement_Console.git
cd Aws_Mangement_Console
```

2. Open `index.html` in your web browser:
```bash
# On Linux/Mac
open index.html

# On Windows
start index.html

# Or simply double-click the index.html file
```

### Usage

1. **Dashboard**: View overview of all AWS resources
2. **Navigate Services**: Use the sidebar to access different AWS services
3. **Create Resources**: Click the "➕ Create" buttons to simulate resource creation
4. **View Details**: Browse tables to see resource configurations
5. **Export Configuration**: Use the architecture export feature to download configurations

## 📁 Project Structure

```
Aws_Mangement_Console/
├── index.html          # Main HTML structure and content
├── styles.css          # Complete styling and responsive design
├── script.js           # Interactive functionality and navigation
└── README.md          # Project documentation
```

## 🎨 Design Features

- **Modern UI**: Clean, professional interface inspired by AWS design
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Elements**: Hover effects, animations, and transitions
- **Color Coding**: Visual indicators for different resource states
- **Easy Navigation**: Sidebar navigation with active state indicators

## 🔧 Technical Details

### Technologies Used
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with flexbox and grid layouts
- **JavaScript (ES6+)**: Interactive functionality and DOM manipulation

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📊 Architecture Example

The console demonstrates a production-ready three-tier architecture:

```
Internet
    ↓
[Route 53 DNS]
    ↓
[Internet Gateway]
    ↓
[Web Tier ALB] → [Web Servers (t3.medium)] → Public Subnet (10.0.1.0/24)
    ↓
[App Tier ALB] → [App Servers (t3.large)] → Private Subnet (10.0.2.0/24)
    ↓
[RDS MySQL] → Database Tier → Private Subnet (10.0.3.0/24)
```

### Security Configuration
- **Web Tier**: Open to internet (ports 80, 443)
- **App Tier**: Accessible only from web tier (port 8080)
- **DB Tier**: Accessible only from app tier (port 3306)

## 🌍 Regions & Availability Zones

Default configuration uses:
- **Region**: us-east-1 (N. Virginia)
- **Availability Zones**: us-east-1a, us-east-1b, us-east-1c

## 📝 Features in Detail

### Dashboard
- Real-time metrics for all services
- Resource counts and health status
- Quick access to service sections

### Resource Management
- Create, view, edit, and delete resources
- Search and filter capabilities
- Batch operations support

### Architecture Export
Export complete infrastructure configuration as JSON for use with:
- AWS CloudFormation
- Terraform
- AWS CDK
- Manual deployment reference

## 🔐 Security Best Practices

The console demonstrates:
- Security group isolation between tiers
- Private subnets for app and database tiers
- Network ACLs for subnet-level protection
- Multi-AZ deployment for high availability
- Read replicas for database scalability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

AARYANSHARMA19

## 🙏 Acknowledgments

- Inspired by AWS Management Console design
- Built for educational and demonstration purposes
- Showcases modern web development practices

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Note**: This is a demonstration/educational interface. It does not connect to actual AWS services or manage real infrastructure. For production AWS management, use the official AWS Management Console at https://console.aws.amazon.com/