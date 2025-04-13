# GenAI Marketing Platform

A comprehensive marketing platform powered by Generative AI, designed to streamline marketing operations and enhance content creation.

## 🚀 Features

- **AI-Powered Content Generation**: Create high-quality marketing content using advanced language models
- **Multi-Channel Support**: Generate content optimized for various marketing channels
- **Data-Driven Insights**: Leverage analytics to improve marketing strategies
- **Collaborative Workspace**: Team-based content creation and management
- **Customizable Templates**: Pre-built templates for different marketing needs

## 🏗️ Project Structure

```
.
├── backend/           # FastAPI-based backend service
│   ├── app/          # Application core
│   ├── database/     # Database models and migrations
│   ├── services/     # Business logic and services
│   └── tests/        # Backend test suite
├── frontend/         # Web-based frontend application
│   ├── images/       # Static images and assets
│   ├── script.js     # Frontend JavaScript
│   ├── style.css     # Frontend styles
│   └── index.html    # Main application page
├── datascripts/      # Data processing and ETL scripts
├── infrastructure/   # Infrastructure as Code (IaC)
└── docker-compose.yml # Docker Compose configuration
```

## 🏢 System Architecture

![System Architecture](assets/architecture.png)

The above diagram illustrates the high-level architecture of the GenAI Marketing Platform, showing the interaction between different components and services.

## ☁️ Cloud Infrastructure

The platform is deployed on AWS using CloudFormation for infrastructure as code. The infrastructure includes:

- **VPC with Public and Private Subnets**: Segregated network architecture for security
- **EC2 Instances**: 
  - Flask Main Service (t3.micro)
  - ChromaDB Service (t3.small)
- **Database Layer**:
  - RDS PostgreSQL for structured data
  - DynamoDB for unstructured campaign data
- **Storage**:
  - S3 Bucket for media storage
- **Security**:
  - Security Groups for EC2 and RDS
  - Private subnets for database layer

```mermaid
graph TB
    subgraph VPC[VPC 10.0.0.0/16]
        subgraph PublicSubnets[Public Subnets]
            direction TB
            WebSubnet1[Web Subnet 1<br/>10.0.48.0/20]
            WebSubnet2[Web Subnet 2<br/>10.0.64.0/20]
            WebSubnet3[Web Subnet 3<br/>10.0.80.0/20]
            AppSubnet1[App Subnet 1<br/>10.0.0.0/20]
            AppSubnet2[App Subnet 2<br/>10.0.16.0/20]
            AppSubnet3[App Subnet 3<br/>10.0.32.0/20]
        end

        subgraph PrivateSubnets[Private Subnets]
            direction TB
            DBSubnet1[DB Subnet 1<br/>10.0.96.0/20]
            DBSubnet2[DB Subnet 2<br/>10.0.112.0/20]
            DBSubnet3[DB Subnet 3<br/>10.0.128.0/20]
        end

        subgraph Services[Services]
            direction TB
            Flask[Flask EC2<br/>t3.micro]
            ChromaDB[ChromaDB EC2<br/>t3.small]
            RDS[RDS PostgreSQL]
            DynamoDB[DynamoDB]
            S3[S3 Bucket]
        end
    end

    Internet[Internet] --> IGW[Internet Gateway]
    IGW --> VPC

    WebSubnet1 & WebSubnet2 & WebSubnet3 --> Flask
    AppSubnet1 & AppSubnet2 & AppSubnet3 --> ChromaDB
    DBSubnet1 & DBSubnet2 & DBSubnet3 --> RDS

    Flask --> RDS
    Flask --> DynamoDB
    Flask --> S3
    Flask --> ChromaDB
```

### Infrastructure Components

1. **Networking**:
   - VPC with CIDR block 10.0.0.0/16
   - Public subnets for web and application layers
   - Private subnets for database layer
   - Internet Gateway for public access
   - Route tables for network traffic management

2. **Compute**:
   - Flask EC2 Instance (t3.micro) for main application
   - ChromaDB EC2 Instance (t3.small) for vector database
   - Security groups for controlled access

3. **Storage**:
   - RDS PostgreSQL (db.t3.micro) for structured data
   - DynamoDB for campaign drafts and unstructured data
   - S3 bucket for media storage with public access

4. **Security**:
   - Security groups for EC2 and RDS
   - Private subnets for sensitive data
   - Controlled public access to S3 bucket

## 📊 Data Engineering Pipeline

![Data Engineering Pipeline](assets/data-engineering.png)

This diagram showcases our data engineering pipeline, detailing how we processed 12000 products from Amazon listings and 5000 Instagram posts for our RAG.

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **AI/ML**: LangChain, OpenAI, ChromaDB
- **Authentication**: JWT
- **API Documentation**: OpenAPI/Swagger

### Frontend
- **Core**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS
- **Build Tools**: Docker

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Node.js (for frontend development)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/genai-marketing-platform.git
cd genai-marketing-platform
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the application using Docker Compose:
```bash
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for their language models
- FastAPI team for the excellent web framework
- All contributors who have helped shape this project
