# 🕵️‍♂️ DePIN Research Report: https://teneo.pro/

## 📊 Tokenomics
```json
{
  "token_name": "Fragments",
  "token_symbol": null,
  "total_supply": null,
  "utility": "Rewards for running Beacon app; likely used within Teneo ecosystem",
  "distribution": null,
  "additional_rewards": "Teneo Points (via Community Node, quests, leaderboard); USDC as payment currency for agent requests",
  "blockchain": null,
  "token_standard": null,
  "notes": "No token ticker, supply, or blockchain details disclosed; rewards appear points-based, likely pre-token"
}
```

## ⚠️ Risk Analysis
```json
{
  "project": "Teneo Protocol",
  "risk_assessment": {
    "technical_risks": [
      "No disclosed bandwidth, CPU, or hardware requirements for running nodes, making resource impact on user devices unpredictable.",
      "No technical documentation on how public social media data is collected, processed, or validated.",
      "Running a Chrome extension and cross-platform app that contributes data creates potential privacy, security, and malware attack surface risks.",
      "The x402 payment protocol and USDC micropayment integration lack technical details on reliability, latency, and scalability.",
      "Metrics are presented with obfuscated/animated counters, making claimed job counts and node counts unverifiable.",
      "Rewards are points-based with no token contract, chain, or technical reward mechanism disclosed."
    ],
    "economic_risks": [
      "Fragments and Teneo Points have no disclosed tokenomics, supply schedule, vesting, or conversion value.",
      "Supply-side contributors earn points while demand-side pays in USDC, creating unclear and potentially unsustainable value capture for node operators.",
      "No token ticker or blockchain details are provided, indicating a pre-token points-farming model with uncertain future economic incentives.",
      "Claimed 'millions of community nodes' are unverifiable and may include inactive or sybil nodes.",
      "Agent marketplace usage is highly concentrated in a few agents, while others show very low demand (e.g., Nansen at 31 jobs), indicating fragile marketplace economics.",
      "Reward incentives may attract speculative users rather than genuine infrastructure contributors, leading to poor data quality and network reliability."
    ],
    "centralization_risks": [
      "Teneo centrally controls reward distribution, leaderboards, quests, and point calculations.",
      "The Beacon app and Community Node extension appear to be proprietary and closed-source, giving Teneo full control over node software.",
      "The Agent Console marketplace is curated and operated by Teneo, creating a centralized gateway for demand-side access.",
      "The x402 payment rail may be decentralized, but job routing, agent listings, and data validation remain under Teneo's control.",
      "Community metrics such as '300K+ builders and node runners' are unverifiable and could be gamed or inflated."
    ],
    "red_flags": [
      "Animated/obfuscated metric counters imply scale without providing verifiable data.",
      "No technical documentation, token contract, or hardware requirements are disclosed despite heavy reward incentives.",
      "Privacy claims such as 'Your device. Your data. Your control.' are not backed by auditable code or data-handling policies.",
      "Points-based rewards with no token details are typical of pre-token DePIN projects that may never deliver economic value.",
      "The project claims millions of nodes and jobs but provides no on-chain or cryptographic proof.",
      "Use of personal devices for data harvesting raises regulatory and ethical concerns around data provenance and consent."
    ]
  },
  "overall_risk_level": "High"
}
```

## ⚖️ Verification Results
```json
{
  "verification_summary": "The tokenomics summary aligns with the raw evidence, confirming Fragments as Beacon rewards and Teneo Points/USDC as additional incentives, while noting the lack of disclosed token details.",
  "claim_evaluations": [
    {
      "claim": "Fragments are earned by running the Beacon app",
      "status": "supported",
      "confidence_score": 1.0,
      "source_quote": "Fragments \u2014 earned by running the Beacon app."
    },
    {
      "claim": "Teneo Points are earned via Community Node, quests, and leaderboard",
      "status": "supported",
      "confidence_score": 1.0,
      "source_quote": "Teneo Points \u2014 earned via the Community Node extension, quests, and leaderboard."
    },
    {
      "claim": "No token ticker, supply, or blockchain details are disclosed",
      "status": "supported",
      "confidence_score": 1.0,
      "source_quote": "No token ticker, tokenomics, supply, or blockchain details are mentioned \u2014 rewards appear to be points-based (likely pre-token)."
    }
  ]
}
```
