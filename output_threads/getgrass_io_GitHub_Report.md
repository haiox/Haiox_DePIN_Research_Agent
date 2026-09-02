# 🕵️‍♂️ DePIN Research Report: https://getgrass.io/

## 📊 Tokenomics
```json
{
  "tokenName": "Grass",
  "totalSupply": "Not disclosed",
  "utility": "Native token of the Grass Network; used to reward users for contributing idle bandwidth. Also serves as a medium for incentivizing network participation.",
  "distribution": "Not disclosed (no supply schedule, vesting, or allocation details provided on the page)",
  "rewardMechanism": "Users earn Grass Tokens or USDC based on Network Points (active bandwidth contribution) and Uptime Points (device availability). Referral bonuses provide additional Uptime Points. Allocation also factors in bandwidth usage and geographic location.",
  "additionalNotes": "No tokenomics details (e.g., total supply, emission rate, token burns) are disclosed on the page. Rewards are calculated from points and geographic factors. The project is associated with Solana blockchain, but this is not mentioned in the provided text."
}
```

## ⚠️ Risk Analysis
```json
{
  "technical_risks": [
    "No disclosure of bandwidth caps, speed limits, or data caps, leading to potential unexpected resource consumption.",
    "No hardware requirements specified, which may lead to performance issues on low-end devices.",
    "Lack of transparency about the underlying blockchain (known to be Solana but omitted), creating uncertainty about technical architecture.",
    "No details on how the client software handles network security, encryption, or data routing, raising potential for misuse."
  ],
  "economic_risks": [
    "No tokenomics disclosed: supply, distribution, vesting, or price information absent, making valuation and sustainability unclear.",
    "Payout rates, minimum thresholds, and payout frequency are not specified, creating uncertainty for users.",
    "Reward calculation includes geographic location and bandwidth usage, which may lead to inequitable or opaque reward distribution.",
    "Referral and Android 3x bonus mechanics suggest a growth-focused model that may prioritize user acquisition over long-term economic stability."
  ],
  "centralization_risks": [
    "The project is controlled by a central entity that selects 'verified institutions' without naming them, indicating centralized governance over bandwidth allocation.",
    "Eligibility restrictions based on jurisdiction and 'significant regulatory risk' are determined by the project, allowing centralized exclusion.",
    "The points system (Network Points and Uptime Points) is managed centrally, with no on-chain transparency mentioned.",
    "The project claims privacy but does not provide verifiable technical details, suggesting potential central oversight of user data."
  ],
  "red_flags": [
    "Vague description of bandwidth buyers ('verified institutions') and end use cases (e.g., web scraping, AI training) without concrete examples.",
    "Unsubstantiated security claims: 'regularly audited' and 'recognized by leading antivirus providers' with no named auditors or reports.",
    "Heavy emphasis on referrals and pyramid-style incentive loops, which can indicate unsustainable growth mechanics.",
    "No clear blockchain integration details despite being associated with Solana, raising questions about decentralization.",
    "The project monetizes user bandwidth without clear disclosure of data handling practices, potentially conflicting with privacy promises."
  ]
}
```

## ⚖️ Verification Results
```json
{
  "verification_summary": "The evidence supports the token's native role and reward utility, the points/allocation reward mechanism, and confirms the absence of bandwidth/hardware disclosures.",
  "claim_evaluations": [
    {
      "claim": "Grass is the native token of the Grass Network, used to reward users for contributing idle bandwidth.",
      "status": "supported",
      "confidence_score": 0.96,
      "source_quote": "Grass Tokens are described as the native token of the Grass Network."
    },
    {
      "claim": "Rewards are distributed in Grass Tokens or USDC based on points and allocation factors including bandwidth usage and geographic location.",
      "status": "supported",
      "confidence_score": 0.93,
      "source_quote": "Token allocation is calculated from Grass Points plus factors like how your bandwidth is used and your geographic location."
    },
    {
      "claim": "No bandwidth caps, speed limits, data caps, or hardware requirements are disclosed on the page.",
      "status": "supported",
      "confidence_score": 0.98,
      "source_quote": "No specific bandwidth caps, speed limits, data caps, or hardware requirements are disclosed on this page."
    }
  ]
}
```
