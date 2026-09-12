# Coinbase Payments MCP composition path

On-demand reference for the MCP-composition path to paid You.com endpoints: the host runs the You.com MCP server and the Coinbase Payments MCP server together, and the agent reasons between them. No You.com API key and no manual wallet signing in the agent.

## How it works

- Connect two MCP servers in the host:
  - **You.com MCP** at `https://api.you.com/mcp` for search, contents, research, and finance tools.
  - **Coinbase Payments MCP** (https://github.com/coinbase/payments-mcp) for wallet sign-in and on-chain USDC payment on Base.
- Fund the wallet through the Payments MCP sign-in flow. No `YDC_API_KEY` is required; payment is keyless x402 settled from the wallet.
- The agent reasons across both servers: it calls You.com tools, and when a tool returns `402 payment-required`, it uses the Payments MCP to pay and the host retries with payment headers. The free allotment draws down first; once exhausted, `402` triggers a pay-from-wallet retry and the result flows back through the You.com tool.

## When to choose this over the direct client

Choose the MCP-composition path when:

- You want no key management and no manual EIP-3009 / SIWX signing in your code.
- The host already runs MCP servers and can orchestrate both.
- You prefer the host to handle payment settlement end to end.

Trade-off: this requires a host that runs both MCP servers and tolerates long finance/research resolution times (reports are async and can take minutes).

## Pointers

- You.com MCP docs: https://you.com/docs/build-with-agents/mcp-server
- Coinbase Payments MCP repository: https://github.com/coinbase/payments-mcp
