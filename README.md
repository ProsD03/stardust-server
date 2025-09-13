# ✨ Stardust Server
Stardust Server is an OpenAI-like LLM Server. It acts as a middleman between any OpenAI Compatible frontend (like OpenWebUI, SillyTavern...) and a number of LLM providers (OpenAI, XAI, Mistral...), while also adding an advanced memory architecture that lowers token usage while providing better answers and retaining informations from early messages. It also provides a simple web interface to manage saved chats and check the status of the services.

The server is fully customizable: add your favorite providers, configure models with different prompts and LLM models, deploy locally or on a cloud provider.

## Features
- OpenAI /v1 endpoint: the server provides the necessary endpoints that most frontends need to work. They are implemented is a fully compliant way, with the minimum fields required to be accepted.
  - /chat/completion: both streaming and non streaming variants;
  - /models: lists all configured models
- Many LLMs compatibility: the server is compatible with many of the common LLM providers, like OpenAI, XAI and Mistral.
- Advanced Memory Architecture: the server implements a multi-layered memory architecture which provides better context for requests, while reducing their token cost.
- Management Web UI: the server provides a simple webui to manage the conversations outside of your favourite frontend.

## Note about OpenAI /v1 compatibility
Stardust Server _is_ fully OpenAI compatible: this means that any frontend will be able to use this server as a proxy for other LLM APIs. However, to fully take advantage of the memory function, an additional field is required: chatid. This field acts as an identifier for the specific chat, so that the extracted memories are specific for that chat instead of global. An example Valve for OpenWebUI will be provided, which implements this feature. In the case your favourite frontend cannot implement this feature, don't worry! Memories will be automatically grouped by model for any requests that don't have the "chatid" field. This means that you'll have to specify a model for each concurrent chat, or delete the memory each time you start a new one, but is the only way of making this server work with any frontend.

## Memory Architecture
Stardust Server implements advanced memory capabilities to any model you connect to it, reducing token usage, providing better context and quality of the responses. The server's memory architecture is structured in 3 layers, which all work to provide long term context for each request:
- Short Term Memory (STM): raw messages from the requests. Only the last 10 (configurable) messages are kept in the STM.
- Medium Term Memory (MTM): rolling summary of the chat. The Rolling Summary is a short description of the context of the chat, generated from all the messages that are not in the STM. Each time a message exits the STM, the Rolling Summary is updated so that the oldest detailed are removed or reduced in importance, while the newest are added. The Rolling Summary is generated through an LLM choosen by the user (mini models work best).
- Long Term Memory (LTM): a vector database containing all the messages, split in shorter chunks. Each time a message exits STM it is also added to the vector database, labled with who wrote it for better context awareness. Only the 5 (configurable) most inherent chunks are used for each response.
The STM, MTM and LTM are combined via a custom system prompt that explains what each part means to the LLM, so that it may use it as best as possible when generating the responses. The original system prompt, if present, is not considered part of the chat: it is instead passed raw to the LLM. This avoids issues with dilution of the prompt, which would change the LLM's behaviour over time. Custom memories can be manually injected in the LTM, to add context outside what is written in the chat itself.

Idealy, this architecture reduces the number of tokens used: even if each user request generates many requests to LLM serivces (one to generate the response, one to update the MTM, one to extract chunks from the LTM, and a number of requests to create LTM chunks), the overal token usage is reduced since each request is reduced to 10 messages + 5 short chunks, a short description, the user provided system prompt and the custom system prompt. Initially, the cost per request will be higher, but when the chat becomes 50 or more messages long, it should become cheaper. Even if the cost is greater, the quality of the responses is a lot better then without the memory: LLMs just cannot handle long chats without losing details, so this architecture helps them greatly.




