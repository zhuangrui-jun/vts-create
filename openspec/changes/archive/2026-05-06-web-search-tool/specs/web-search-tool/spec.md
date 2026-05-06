## ADDED Requirements

### Requirement: LLM tool calling for web search

The system SHALL provide a `web_search` tool via OpenAI function calling, allowing the LLM to autonomously decide when to invoke web search.

#### Scenario: LLM calls web search for current events

- **WHEN** the user asks "今天有什么新闻" and the LLM determines it needs real-time information
- **THEN** the LLM emits a `web_search` tool call with an appropriate query, the system executes the Bocha API search, and search results are fed back as context for the response

#### Scenario: LLM responds without search

- **WHEN** the user asks "你好" or another greeting that doesn't require real-time data
- **THEN** the LLM streams its response immediately without invoking any tool

### Requirement: Bocha AI search integration

The system SHALL call the Bocha AI search API at `https://api.bocha.cn/v1/ai-search` with Bearer authentication when the LLM invokes the web_search tool.

#### Scenario: Successful search

- **WHEN** the web_search tool is called with query "北京天气"
- **THEN** search results (title, URL, snippet) are returned and formatted as context for the LLM

#### Scenario: Search API failure

- **WHEN** the Bocha API returns an error or is unreachable
- **THEN** the system SHALL return a fallback message to the LLM: "搜索暂时不可用"

### Requirement: Streaming priority

When the LLM does NOT need search, the text SHALL stream immediately without any additional latency from tool checking.

#### Scenario: No tool call needed

- **WHEN** the LLM receives a message that doesn't require search
- **THEN** content tokens stream to the frontend without any delay from tool-related processing
