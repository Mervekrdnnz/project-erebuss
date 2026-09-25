# 🪐 Project Erebus — Cloud Attack Path & Privilege Escalation Analysis Engine

[![CI Pipeline](https://github.com/Mervekrdnnz/project-erebuss/actions/workflows/ci.yml/badge.svg)](https://github.com/Mervekrdnnz/project-erebuss/actions)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0%2B-green.svg)](https://neo4j.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Project Erebus** is a cloud security analysis engine designed to model cloud infrastructure as a graph and identify complex **attack paths, privilege escalation chains, IAM role relationships, and public data exposure risks**.

The project combines **Python**, **Neo4j Graph Database**, **Cypher**, automated testing, and security-focused reporting to analyze relationships between cloud identities, permissions, roles, and storage resources.

---

## 🎯 Project Goals

Project Erebus focuses on identifying security risks that may not be obvious when cloud resources are analyzed individually.

The main goals are:

* 🔐 Detect privilege escalation paths
* 🔗 Analyze IAM role chaining
* ☁️ Model cloud infrastructure as a graph
* 🕸️ Identify multi-hop attack paths
* 📦 Detect public or sensitive storage exposure
* 🔎 Analyze relationships between identities and resources
* 📊 Generate security reports in JSON and HTML formats
* 🧪 Validate attack-path detection with automated tests

---

## 🧠 Core Security Concepts

Erebus focuses on several important cloud security concepts:

### IAM Role Chaining

An identity may be able to assume another IAM role, potentially creating a chain that eventually leads to a highly privileged role.

```text
[IAM User / Service]
        |
        | CAN_ASSUME_ROLE
        v
[Intermediate IAM Role]
        |
        | CAN_ASSUME_ROLE
        v
[High-Privileged IAM Role]
```

### Public Data Exposure

The engine can model relationships between identities and cloud storage resources to identify potentially dangerous access paths.

```text
[IAM User / Service]
        |
        | HAS_ACCESS / READ
        v
[Public / Sensitive S3 Bucket]
```

### Multi-Hop Attack Paths

Instead of analyzing permissions independently, Erebus models relationships as a graph.

```text
User
 |
 | CAN_ASSUME_ROLE
 v
Role A
 |
 | CAN_ASSUME_ROLE
 v
Role B
 |
 | HAS_ACCESS
 v
Sensitive Resource
```

This allows the engine to investigate attack paths that require multiple steps.

---

## 📐 Architecture

Project Erebus uses a graph-based security analysis architecture.

```text
                    ┌─────────────────────┐
                    │   Cloud Resources   │
                    │ IAM / S3 / Services │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AWS Ingestion     │
                    │   Mocked Data       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Graph Builder     │
                    │ Nodes & Relations   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Neo4j         │
                    │   Graph Database    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Attack Engine     │
                    │  Cypher Queries     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Reporter        │
                    │ JSON / HTML Reports │
                    └─────────────────────┘
```

---

## 🕸️ Attack Graph Model

Cloud entities are represented as nodes while permissions and relationships are represented as directed edges.

Example:

```text
[IAM User]
     |
     | CAN_ASSUME_ROLE
     v
[IAM Role]
     |
     | HAS_ACCESS
     v
[S3 Bucket]
     |
     | CONTAINS
     v
[Sensitive Data]
```

This graph-based approach makes it possible to search for relationships across multiple hops.

---

## 🛠️ Technology Stack

| Technology         | Purpose                              |
| ------------------ | ------------------------------------ |
| **Python 3.13**    | Core application and analysis engine |
| **Neo4j**          | Graph database                       |
| **Cypher**         | Attack-path queries                  |
| **Pytest**         | Automated testing                    |
| **Docker**         | Containerized Neo4j environment      |
| **GitHub Actions** | CI pipeline                          |
| **JSON**           | Machine-readable security reports    |
| **HTML**           | Human-readable security reports      |

---

## 📁 Project Structure

```text
project-erebus/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   ├── graph/
│   │   ├── connection.py
│   │   └── builder.py
│   │
│   ├── ingestion/
│   │   └── aws.py
│   │
│   └── scanner/
│       ├── engine.py
│       └── reporter.py
│
├── tests/
│   └── test_engine.py
│
├── main.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Component Overview

**`src/graph/connection.py`**

Handles the Neo4j database connection and driver configuration.

**`src/graph/builder.py`**

Creates graph nodes and relationships representing cloud infrastructure.

**`src/ingestion/aws.py`**

Provides mocked AWS infrastructure data for security analysis.

**`src/scanner/engine.py`**

Contains the Cypher-based attack-path discovery and security analysis logic.

**`src/scanner/reporter.py`**

Generates security analysis results in JSON and HTML formats.

**`tests/test_engine.py`**

Contains automated tests for the analysis engine and graph queries.

**`main.py`**

Provides the main CLI entry point and executes the analysis pipeline.

---

## 🚀 Quick Start

### Prerequisites

Before running Project Erebus, make sure the following are installed:

* Python 3.10+
* Docker
* Docker Compose
* Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/Mervekrdnnz/project-erebuss.git
cd project-erebuss
```

---

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Start Neo4j

Start the Neo4j container using Docker Compose:

```bash
docker-compose up -d
```

Verify that the container is running:

```bash
docker ps
```

---

### 5. Run the Analysis

Execute the complete pipeline:

```bash
python main.py
```

---

## ⚙️ Command-Line Options

### Run with Default Configuration

```bash
python main.py
```

### Clean Existing Graph and Re-ingest Data

```bash
python main.py --clean
```

### Generate JSON and HTML Reports

```bash
python main.py --format both
```

---

## 📊 Reporting

Erebus supports multiple report formats.

### JSON

Designed for machine-readable security results and potential integration with other security tools.

Example:

```json
{
  "finding": "Privilege Escalation Path",
  "severity": "HIGH",
  "source": "IAM User",
  "target": "High-Privileged IAM Role"
}
```

### HTML

Designed to provide a more readable security report for analysts and security teams.

The report can contain information such as:

* Finding type
* Severity
* Source identity
* Target resource
* Attack path
* Relationship chain
* Security description

---

## 🧪 Testing

Project Erebus uses **Pytest** for automated testing.

Run the complete test suite:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

---

## 🔄 CI Pipeline

The project includes a GitHub Actions CI pipeline.

The pipeline is designed to automatically validate the project when changes are pushed to the repository.

```text
Git Push
   │
   ▼
GitHub Actions
   │
   ├── Install Dependencies
   │
   ├── Run Tests
   │
   └── Validate Project
```

CI status:

[![CI Pipeline](https://github.com/Mervekrdnnz/project-erebuss/actions/workflows/ci.yml/badge.svg)](https://github.com/Mervekrdnnz/project-erebuss/actions)

---

## 🔍 Example Attack Path

A simplified attack scenario can be represented as:

```text
┌───────────────┐
│ IAM User      │
└───────┬───────┘
        │
        │ CAN_ASSUME_ROLE
        ▼
┌───────────────┐
│ IAM Role A    │
└───────┬───────┘
        │
        │ CAN_ASSUME_ROLE
        ▼
┌───────────────┐
│ IAM Role B    │
│ High Privilege│
└───────┬───────┘
        │
        │ HAS_ACCESS
        ▼
┌───────────────┐
│ S3 Bucket     │
│ Sensitive Data│
└───────────────┘
```

The graph engine can search for relationships connecting the initial identity to privileged resources.

---

## 🛡️ Security Use Cases

Project Erebus can be used as a learning and research project for:

* Cloud Security
* IAM Security
* Attack Path Analysis
* Privilege Escalation Analysis
* Graph-Based Security Analysis
* Cloud Security Posture Management concepts
* Security Automation
* Identity and Access Management
* Threat Modeling

---

## 📌 Project Scope

This project currently uses **mocked AWS infrastructure data** for development and testing.

It is designed as a security analysis and research project rather than a production cloud security scanner.

The architecture can be extended in the future to support real cloud environments and additional resource types.

---

## 🔮 Future Improvements

Potential future improvements include:

* [ ] Real AWS API integration
* [ ] AWS IAM policy parsing
* [ ] Additional cloud resource types
* [ ] Risk scoring
* [ ] Attack-path visualization
* [ ] Interactive Neo4j graph visualization
* [ ] Additional privilege escalation techniques
* [ ] Multi-cloud support
* [ ] AWS / Azure / GCP ingestion
* [ ] REST API
* [ ] Web-based security dashboard
* [ ] Automated security recommendations
* [ ] Expanded test coverage

---

## 📚 Security Concepts Demonstrated

Through Project Erebus, the following concepts are demonstrated:

**Cloud Security**

* IAM relationships
* Cloud resource permissions
* Public storage exposure
* Identity-based access

**Graph Security**

* Nodes and relationships
* Multi-hop path discovery
* Graph traversal
* Cypher queries

**Security Engineering**

* Automated scanning
* Security reporting
* Unit testing
* CI/CD validation
* Containerized infrastructure

---

## 📜 License

This project is licensed under the **MIT License**.

See the [MIT License](https://opensource.org/licenses/MIT) for more information.

---

## 👩‍💻 Author

**Merve Karadeniz**

GitHub:
https://github.com/Mervekrdnnz

---

⭐ If you find this project interesting, feel free to explore the repository and its security analysis components.
