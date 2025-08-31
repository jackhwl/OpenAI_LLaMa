# Model Context Protocol (MCP) Architecture

This overview of the Model Context Protocol (MCP) discusses its scope and core concepts, and provides examples demonstrating each core concept.

## Scope

The Model Context Protocol includes the following projects:

* MCP Specification: A specification of MCP that outlines the implementation requirements for clients and servers.
* MCP SDKs: SDKs for different programming languages that implement MCP.
* MCP Development Tools: Tools for developing MCP servers and clients, including the MCP Inspector
* MCP Reference Server Implementations: Reference implementations of MCP servers.

## Concepts of MCP

### Participants

MCP follows a client-server architecture where an MCP host — an AI application like Claude Code or Claude Desktop — establishes connections to one or more MCP servers. The MCP host accomplishes this by creating one MCP client for each MCP server. Each MCP client maintains a dedicated one-to-one connection with its corresponding MCP server.

The key participants in the MCP architecture are:

* **MCP Host**: The AI application that coordinates and manages one or multiple MCP clients
* **MCP Client**: A component that maintains a connection to an MCP server and obtains context from an MCP server for the MCP host to use
* **MCP Server**: A program that provides context to MCP clients

**Example**: Visual Studio Code acts as an MCP host. When Visual Studio Code establishes a connection to an MCP server, such as the Sentry MCP server, the Visual Studio Code runtime instantiates an MCP client object that maintains the connection to the Sentry MCP server.

MCP servers can execute locally or remotely:
* "Local" MCP servers run on the same machine (using STDIO transport)
* "Remote" MCP servers run on external platforms (using Streamable HTTP transport)

### Layers

MCP consists of two layers:

* **Data layer**: Defines the JSON-RPC based protocol for client-server communication, including lifecycle management, and core primitives, such as tools, resources, prompts and notifications.
* **Transport layer**: Defines the communication mechanisms and channels that enable data exchange between clients and servers, including transport-specific connection establishment, message framing, and authorization.

#### Data Layer
The data layer implements a JSON-RPC 2.0 based exchange protocol that defines the message structure and semantics.
This layer includes:

* **Lifecycle management**: Handles connection initialization, capability negotiation, and connection termination
* **Server features**: Enables servers to provide core functionality including tools, resources, and prompts
* **Client features**: Enables servers to sample from the host LLM, elicit input from users, and log messages
* **Utility features**: Supports capabilities like notifications for real-time updates and progress tracking

#### Transport Layer
The transport layer manages communication channels and authentication between clients and servers:

* **Stdio transport**: Uses standard input/output streams for direct process communication between local processes
* **Streamable HTTP transport**: Uses HTTP POST for client-to-server messages with optional Server-Sent Events for streaming capabilities

### Data Layer Protocol

MCP uses JSON-RPC 2.0 as its underlying RPC protocol. The data layer defines primitives that specify what clients and servers can offer each other.

#### Primitives

MCP defines three core primitives that **servers** can expose:

* **Tools**: Executable functions that AI applications can invoke to perform actions
* **Resources**: Data sources that provide contextual information to AI applications
* **Prompts**: Reusable templates that help structure interactions with language models

Each primitive type has associated methods for discovery (`*/list`), retrieval (`*/get`), and in some cases, execution (`tools/call`).

MCP also defines primitives that **clients** can expose:

* **Sampling**: Allows servers to request language model completions from the client's AI application
* **Elicitation**: Allows servers to request additional information from users
* **Logging**: Enables servers to send log messages to clients for debugging and monitoring purposes

#### Notifications

The protocol supports real-time notifications to enable dynamic updates between servers and clients. Notifications are sent as JSON-RPC 2.0 notification messages (without expecting a response) and enable MCP servers to provide real-time updates to connected clients.