---
title: GeneralAI Agent
emoji: 🧠
colorFrom: indigo
colorTo: indigo
sdk: gradio
sdk_version: 5.25.2
app_file: app.py
pinned: false
hf_oauth: true
# optional, default duration is 8 hours/480 minutes. Max duration is 30 days/43200 minutes.
hf_oauth_expiration_minutes: 480
---

> 📘 _[Configuration Reference – Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-config-reference)_

---

# 🧠 GeneralAI Agent

**GeneralAI Agent** is a reasoning-first AI system designed using the **SmolAgents** framework.
It handles multi-step GAIA benchmark questions by planning tool use, executing intermediate steps, and presenting final answers—with full traceability.

---

## ⚙️ Architecture & Capabilities

-   🤖 Built with **SmolAgents**: lightweight agent framework using the ReAct pattern for step-by-step reasoning.
-   🛠️ **Tool use planning**: dynamically selects and invokes tools like calculators, web search, or retrievers.
-   🧠 **Stateful execution loop**: tracks intermediate thoughts and actions across multiple reasoning hops.
-   🎛️ **Modular configuration**: powered by **Hydra** for clean overrides of prompts, tools, and logic.
-   📊 **Observability with LangFuse**: all thoughts, tool invocations, and outcomes are tracked and inspectable.
-   🧰 **Frontend with Gradio**: enables interactive access for local or deployed use.

---

## 📌 Notes

This project was developed as part of the Hugging Face Agents course and serves as a practical implementation of intelligent agent workflows using modern open-source tooling.
It emphasizes modularity, transparency, and real-world tool integration in reasoning pipelines.
