# AI-Native Hackathon Project — Full Spec-Driven System

This repository contains the complete implementation of the AI-Native Hackathon Project, following a spec-driven architecture with 5 phases: Constitution → Specification → Modeling → Implementation → Reflection & Evaluation.

## Project Structure

The project is organized into five main phases:

1. **Constitution Phase** - Governing principles and constraints
2. **Specification Phase** - Feature requirements and user scenarios
3. **Modeling Phase** - Architecture decisions and system design
4. **Implementation Phase** - Code development and testing
5. **Reflection & Evaluation Phase** - Analysis and validation

## Repository Structure

```
project-root/
├── .specify/                # SpecKit Plus configuration and templates
│   ├── memory/              # Project constitution and principles
│   └── templates/           # Specification, plan, and task templates
├── specs/                   # Feature specifications
├── research/                # Collected documentation and papers
├── diagrams/                # Draw.io compatible diagrams
├── examples/                # Runnable code examples
├── src/                     # Supporting scripts and utilities
├── tests/                   # Validation and testing scripts
├── docusaurus/              # Docusaurus site configuration
└── history/                 # Prompt History Records and ADRs
    ├── prompts/             # Prompt History Records organized by stage
    │   ├── constitution/    # Constitution stage PHRs
    │   └── <feature-name>/  # Feature-specific PHRs
    └── adrs/                # Architecture Decision Records
```

## Getting Started

### Prerequisites

- Node.js 18+ (for Docusaurus)
- Git
- Claude Code (for Spec-Kit Plus workflow)
- Context7 MCP Server (for specification integration)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project-01-book-with-AI
   ```

2. Install Node.js dependencies for Docusaurus:
   ```bash
   cd docusaurus/
   npm install
   ```

3. Initialize Spec-Kit Plus workflow:
   ```bash
   # Run initial setup for spec-driven development
   # This will create the basic structure based on the constitution
   ```

### Running Examples

Each feature includes runnable examples in the `examples/` directory:

```bash
# Navigate to examples
cd examples/

# Run examples for a specific feature
# Examples will be organized by feature
```

## Docusaurus Site

The project documentation is built using Docusaurus. To run the site locally:

```bash
cd docusaurus/
npm install
npm run start
```

## Contributing

This project follows the Spec-Kit Plus spec-driven workflow with 5 phases:
1. Constitution: Establish governing principles
2. Specification: Define feature requirements
3. Modeling: Create architectural plans
4. Implementation: Develop and test features
5. Reflection & Evaluation: Analyze and validate outcomes

All changes must comply with the project constitution and follow the established workflow.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.