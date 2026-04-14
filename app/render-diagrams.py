#!/usr/bin/env python3
"""Mermaid diagram renderer for Claude Code Workshop app."""

import subprocess
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Diagram:
    name: str
    source: str


DIAGRAMS = [
    Diagram(
        name="spec-driven-flow",
        source="""
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fafaf8', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff4e6'}}}%%
flowchart LR
    D[Discovery 🔍] -->|writes| R[Research 🔬]
    R -->|writes| Ref[Refinement ⚒️]
    Ref -->|writes| P[Planning 📝]
    P -->|writes| I[Implement 🔨]
    I -->|writes| Rev[Review ✅]

    style D fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
    style R fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style Ref fill:#fef9c3,stroke:#ca8a04,stroke-width:2px
    style P fill:#fce7f3,stroke:#db2777,stroke-width:2px
    style I fill:#f3e8ff,stroke:#9333ea,stroke-width:2px
    style Rev fill:#ffedd5,stroke:#d97757,stroke-width:2px
""",
    ),
    Diagram(
        name="context-windows",
        source="""
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fafaf8', 'edgeLabelBackground':'#ffffff'}}}%%
flowchart TB
    subgraph S1["Session 1"]
        A1[Clean Context] --> D1[Read Spec] --> W1[Focused Work] --> O1[Write Artifact]
    end

    subgraph S2["Session 2"]
        A2[Clean Context] --> D2[Read Prior Artifact] --> W2[Focused Work] --> O2[Write Artifact]
    end

    subgraph S3["Session 3"]
        A3[Clean Context] --> D3[Read Prior Artifact] --> W3[Focused Work] --> O3[Write Artifact]
    end

    O1 -.->|artifact chain| D2
    O2 -.->|artifact chain| D3

    style S1 fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
    style S2 fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style S3 fill:#fef9c3,stroke:#ca8a04,stroke-width:2px
""",
    ),
    Diagram(
        name="parallel-contexts",
        source="""
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fafaf8', 'edgeLabelBackground':'#ffffff'}}}%%
flowchart TB
    subgraph FeatureA["Feature A: Auth System"]
        A1[Discovery] --> A2[Research] --> A3[Plan]
    end

    subgraph FeatureB["Feature B: Payment Flow"]
        B1[Discovery] --> B2[Research] --> B3[Plan]
    end

    subgraph FeatureC["Feature C: Notifications"]
        C1[Discovery] --> C2[Research] --> C3[Plan]
    end

    style FeatureA fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
    style FeatureB fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style FeatureC fill:#fce7f3,stroke:#db2777,stroke-width:2px
""",
    ),
    Diagram(
        name="externalization-analogy",
        source="""
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fafaf8', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff4e6'}}}%%
flowchart LR
    subgraph Human["Externalization of Human"]
        direction LR
        T[Thought<br/>🧠] -->|ideas in symbols| L[Language<br/>🗣️]
        L -->|memory extension| W[Writing<br/>✍️]
        W -->|mass dissemination| P[Printing<br/>📰]
        P -->|automated manipulation| C[Computing<br/>💻]
    end

    subgraph LLM["Externalization of LLM Agent"]
        direction LR
        Weights[Weights<br/>🕸️] -->|externalized state| M[Memory 🧠]
        Weights -->|externalized expertise| S[Skill 🛠️]
        Weights -->|externalized interaction| Pro[Protocol 📡]
        M --> Harness
        S --> Harness
        Pro --> Harness
        Harness[Externalized Agency] --> H[Harness 🎛️]
    end

    style Human fill:#fff4e6,stroke:#d4a373,stroke-width:2px
    style LLM fill:#e6f4ff,stroke:#3787d4,stroke-width:2px
    style T fill:#ffcccc
    style L fill:#ccffcc
    style W fill:#ccccff
    style P fill:#ffffcc
    style C fill:#ffccff
    style Weights fill:#ffcccc
    style M fill:#ccffcc
    style S fill:#ccccff
    style Pro fill:#ffffcc
    style Harness fill:#ffccff
    style H fill:#ff9966,stroke:#333,stroke-width:2px
""",
    ),
    Diagram(
        name="memory-lifecycle",
        source="""
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fafaf8', 'edgeLabelBackground':'#ffffff'}}}%%
flowchart LR
    D[Discovery<br/>🌱] -->|new facts| A[Accumulation<br/>📚]
    A -->|stale knowledge| Dec[Decay<br/>🍂]
    Dec -->|extract learnings| C[Consolidation<br/>💎]
    C -->|inform| D

    style D fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style A fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
    style Dec fill:#fef9c3,stroke:#ca8a04,stroke-width:2px
    style C fill:#f3e8ff,stroke:#9333ea,stroke-width:2px
""",
    ),
    Diagram(
        name="mcp-protocols",
        source="""
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fafaf8', 'edgeLabelBackground':'#ffffff'}}}%%
flowchart TB
    subgraph MCP["MCP Server as Protocol"]
        R[Resources<br/>📂] --> S
        T[Tools<br/>🛠️] --> S
        P[Prompts<br/>📝] --> S
        S[Structured Protocol] --> A1
        S --> A2
        S --> A3
    end

    A1[Discover Agent] -->|queries state| S
    A2[Research Agent] -->|registers findings| S
    A3[Plan Agent] -->|reads constraints| S

    style MCP fill:#e6f4ff,stroke:#3787d4,stroke-width:2px
    style S fill:#ff9966,stroke:#333,stroke-width:2px
    style A1 fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style A2 fill:#fef9c3,stroke:#ca8a04,stroke-width:2px
    style A3 fill:#fce7f3,stroke:#db2777,stroke-width:2px
""",
    ),
    Diagram(
        name="module-interactions",
        source="""
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fafaf8', 'edgeLabelBackground':'#ffffff'}}}%%
flowchart TB
    subgraph Dynamics["Cross-Cutting Dynamics"]
        direction LR
        M[Memory<br/>State] -->|experience distillation| S[Skills<br/>Expertise]
        S -->|execution recording| M
        S -->|capability invocation| P[Protocols<br/>Interaction]
        P -->|capability generation| S
        M -->|strategy selection| P
        P -->|result assimilation| M
    end

    style M fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
    style S fill:#fff4e6,stroke:#d4a373,stroke-width:2px
    style P fill:#dcfce7,stroke:#16a34a,stroke-width:2px
""",
    ),
]


def render_diagram(diagram: Diagram, output_dir: Path, format: str = "png") -> Path:
    mmd_path = output_dir / f"{diagram.name}.mmd"
    out_path = output_dir / f"{diagram.name}.{format}"
    mmd_path.write_text(diagram.source.strip(), encoding="utf-8")

    cmd = [
        "npx",
        "-y",
        "@mermaid-js/mermaid-cli",
        "-i",
        str(mmd_path),
        "-o",
        str(out_path),
        "-b",
        "white",
    ]

    print(f"Rendering {diagram.name} ...")
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(f"  -> {out_path}")
    return out_path


def main():
    output_dir = Path(__file__).parent / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    for diagram in DIAGRAMS:
        render_diagram(diagram, output_dir, format="png")
        render_diagram(diagram, output_dir, format="svg")

    print("\nAll diagrams rendered successfully.")


if __name__ == "__main__":
    main()
