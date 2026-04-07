# Is Context Engineering the New RAG?

Source: https://www.youtube.com/watch?v=wGpJdn8frYE&list=PLLasX02E8BPBCP7KdYsjKKFFQUmNEUmE9&index=2

An interview from "The Shift: Agentic Edition" with Allison, Pamela, and Matt from the Microsoft Foundry team. Edited from the podcast transcript. Speaker attributions are based on context clues since the transcript does not label speakers.

## Allison

Today we are going to dive into what makes an agent knowledgeable. When I first think of knowledge for agents, I immediately think of RAG. However, we are in this era of agents everywhere, and I keep hearing that RAG is dead. So can you tell me what RAG is? Is RAG dead?

## Pamela

RAG is retrieval-augmented generation, and it is definitely not dead, even though everybody likes to say that.

The idea is that we want LLMs to be able to accurately answer questions. So we look at a question, retrieve some information to answer it, and let the LLM synthesize all that information using its ability to produce really fluent natural language. That way we get the best of both worlds: great conversational fluency and information synthesis on one side, and accurate domain-specific information on the other.

## Allison

What is an agent?

## Pamela

An agent is an LLM that uses tool calling in a loop to achieve a goal. It has access to tools, it looks at the question, and it says, "I am going to call this tool and this tool and pass these arguments, and that way I can get the answer."

So is RAG relevant in the age of agents? Definitely, because you give the agent a tool that fetches information from your database, a tool that fetches from the web, a tool that searches your issue tracker — that is all retrieval. We are still doing RAG about 90% of the time.

## Allison

So in the era of agents, RAG is not dead, it is just more sophisticated.

## Matt

Yeah, I really like what you said about tool calling. We are graduating beyond chats and actually having our LLMs take action in the world. That is really what agents are all about.

The key connection to RAG is that these agents are very smart — LLMs are trained on the internet and know a lot — but they do not know about your specific task. What makes them remarkable is the context window. When you prompt an LLM, you are putting that message inside the context window, which is basically all the inputs the LLM can take. Context is any of the information the agent needs to do its job.

The hard part about building an agent is making sure you have exactly the right context. Early on, models could only look at a couple thousand tokens at a time and were not super useful. Now there are models with millions of tokens in the context window. But even with that massive window, there are still limitations in the model's ability to understand everything in it. So finding high-quality context is really important. Once you have the right mix of knowledge in the context window, that is when you unlock the magic of agents and they can start being more of a colleague or a tool for you to do your job.

## Pamela

The context can also include the conversation history and, if it is an agent, whatever tool calls it has done in the past. And then there is the newer notion of memory. As the agent has conversations, it can make better recommendations and answer questions better based on facts it has learned about the user. We are giving it the conversation history, the tool call results, and any relevant memories that will help the LLM best answer the question.

## Allison

Connecting RAG to context, it seems like context is just a new retrieval problem.

## Pamela

I think "context" is just a newer term. You are going to hear the term "context engineering" a lot more.

## Matt

It is interesting how things have evolved. A lot of the techniques and foundations of prompt engineering have really been the foundation for context engineering. But at the end of the day, it is really about the information you are putting in the prompt. Am I sending a clear example for the LLM? Does it understand what it is supposed to do? What it is not supposed to do? Context engineering is really enabling you to build a more effective agent that can actually go and do things, not just a chatbot responding in a funny way.

## Allison

When I think of retrieval, the first thing I think about is vector databases. How should I think about vector databases in this era of context? Can I just buy a vector database and that will help me get the right context to my LLM?

## Pamela

Vector databases are really cool because they allow us to do semantic search. If I am searching for a purple shirt, I can also get back a mauve shirt or a heliotrope shirt — things that are semantically similar but not the same words. Users are able to describe what they want with much greater flexibility. I also love that vector search supports users coming from other languages, because many embedding models are trained with multilingual data. Suddenly people can type queries in Spanish and actually get answers.

But vector search is not enough. I have written blog posts with that title. I give talks about this every month, because developers keep saying all you need is a vector database, and that is just not true. I am begging people to add more to their search stack.

## Matt

When Foundry IQ was first created, it actually began as a text search engine — a search bar with some checkboxes on the side for what type you are searching for. That foundation is still relevant today. If you have gone to a hardware store looking for a specific screw with a specific length, and you tried to semantically search for that screw, you would find a lot of interesting things, but you really just want a specific screw. That is one of the weaknesses of semantic search: it is not exact.

## Pamela

Right, we do that example all the time with our sample data, which is a hardware shop. If I search for a 25-foot hose, vector search returns a 50-foot hose and a 75-foot hose first, and then way down there is the 25-foot hose. That is what happens if you only use vector search.

## Allison

So you are telling me that vector search is not enough, text search is not enough. I need both.

## Matt

That is exactly right. In Foundry IQ we put them together using a technique called Reciprocal Rank Fusion. Really all it is is merging two sets of search results together. Text search and vector search fix the weaknesses of each other, and you end up with a really good match for the query.

But we are not done yet. Now that we have a candidate set of documents that are relevant to the query, the order of the list could be adjusted. In Foundry IQ we have trained a much smaller model — fun fact, this was around way before LLMs — called a re-ranker. The core idea is that it reorders the results based on the actual query being searched. This provides a really significant boost in quality. When you have re-ranked hybrid search results, you are making sure that the best fit for the agent's query ends up in the context window, which is critical because the agent is thinking about so many other things.

## Pamela

There is one more benefit of re-rankers. The re-ranker assigns a score of zero to four, based on how humans trained it — humans looked at search results and queries and said, "I think this is a four, this is the best result for this query." That is useful because both vector search and keyword search can return completely irrelevant results.

With vector search, you are in this multidimensional space — I always picture an ice cream cone — and you have the target vector and you are finding the vectors close to it. You get the 10 closest vectors, but the 10th closest could actually be way out there. You got it only because it was the 10th closest and there were not many similar things to your question. That is a noisy result.

Keyword search can also give noisy results. For the hardware example, if I search for "25-foot hose," I then get back a 25-inch drain snake. How am I going to use a drain snake to water my garden? It is irrelevant, but it matched because of the "25." With the re-ranker, if we set a threshold, we can just drop results that are not high enough.

## Allison

So with context engineering, the main goal is to provide the LLM with only the most relevant content for a particular query. Hybrid search is one way to reach that goal, and re-ranking gives you even better results on top of that.

## Matt

As we evolved Foundry IQ for the age of agents and context engineering, we thought about what you need to build a context engineering pipeline. If you have a query, how do you get relevant results? How do you even know what to query? The system selects the different knowledge sources you need, fetches from them using state-of-the-art retrieval, merges the results, figures out if it needs another round of queries, and checks whether the documents it found are relevant or off-base and need to be removed. Managing that context window is critical.

It is a multifaceted, complex problem. The benefit of encapsulating it in a single knowledge base is that as you build other agents, you get to reuse it. You avoid reinventing the wheel every time you build a new agent.

## Pamela

And you use an LLM for that stitching step, right? The stage where you are trying to decide whether you need to go and do another search — how do you decide that?

## Matt

An LLM definitely plays a role, and this is a tradeoff that agent developers make. LLMs that are really smart are not particularly fast. So what we did was use a process called distillation, where you take a really large model performing a task, gather a bunch of data about how it did that task, and then fine-tune a much smaller model — we call them SLMs, small language models — to perform almost on par with the larger model. It is a remarkable technique that lets you get a lot of extra mileage out of smaller models.

Because we are building a context engineering pipeline, we have a very small model that looks at the documents and the query and says, "Is this actually enough to answer the query?" If it decides it needs another pass, it triggers another query planning process that takes into account the documents already found.

## Allison

Even with the full retrieval stack — hybrid search, re-ranking — you still only have one shot to get the most relevant information. But now with knowledge bases and agentic retrieval, you can try again and make sure you are getting the right information in more than one pass.

## Matt

Yeah, at the end of the day we realized that retrieval as it was is very human-driven. You think you know what you are searching for, you search, you find some information, you look at it, and then you ask whether you need to keep searching or change your query based on what you found. We really tried to recreate that experience as the agentic retrieval product.

## Allison

The main thing I hear from customers is: "Wait, agentic retrieval — I am still getting used to RAG, I am still getting used to connecting my data to my agent. What do I need to do?" And I also hear: "I do not even know if my agent is performing well. How do I know that my agent is actually giving me the right answers?" So how should we be evaluating agents?

## Pamela

I am glad they are asking those questions. I would be more concerned if nobody ever asked. A lot of times when developers are first building agents, they have their favorite questions that they send to the agent. But LLMs can be convincingly wrong. You have to have a human expert who knows the data and can say, "Yes, that is a correct answer," or "That is wrong in some way."

## Allison

To know your agent is performing as it should, you need to be measuring it for groundedness and for relevance. And regardless of what tweaks you make to the agent, you want to keep those same metrics steady and consistent so you can see if a change actually affected the scores.

## Pamela

Yeah, that is a great start. Groundedness and relevance are the two most popular metrics for RAG applications. You definitely want to start with those. What a lot of people do is get started with those metrics and then start analyzing production use cases — have a human with domain expertise go through the results and annotate whether they actually thought the answer was correct, and in what way it failed. That is how you might determine your own custom metric.

And humans tend to score things highly if they sound good, even if they are inaccurate. You will see that helpfulness rankings go up, but hallucinations go up at the same time. LLMs have been trained to please us, and humans like to hear what we want to hear. We have to counter that sometimes, because we want to give people accurate information. I actually love that GPT-5 specifically sacrificed helpfulness in favor of accuracy during training. I am hoping more models do that, because accuracy is increasingly important.

## Matt

A really common thing you will see in LLM-based applications is interactive, clickable links in the generated answers. That gives people the confidence that this is not made up — that if they really wanted to, they could go read the page and find where the answer comes from.

## Pamela

Providing citations is a best practice. But we should also assume that 99% of users are not going to click through those citations. We are all too lazy. That is why we really need to do evaluations to determine whether we are giving back good results.

For the RAG application prompt, what I recommend is: if the sources are not sufficient to answer the question, indicate that. Say, "I do not have full information from these sources." You can also indicate whether you have partial sources available. If you tell the model exactly how to handle the situation of not having complete sources, then it knows what to do.

## Allison

It seems like there could be a major security risk with that. How do you make sure that every user is able to use the agent based on the information they are allowed access to?

## Matt

If you are an organization using Foundry and Microsoft products, chances are you have already set up your security through Entra — who is a member of your organization, what role do they have, are they in certain security groups, do they have access to specific things. The great thing about Foundry IQ is that all that same access flows through. Documents can be marked with the specific user or group that can access them.

We chose to make this more of a retrieval problem and less of an LLM problem, because the best way to make security a natural part of agents is to put it at the retrieval layer, not at the prompt layer.

## Pamela

That shocks me that anybody even thinks you could do it at the prompt layer. We have seen that you can find out what data an LLM was trained with just by probing it enough. How could anyone imagine you could hide anything in the prompt? That is crazy to me.

## Allison

Speaking of grass, MCP. What is MCP?

## Pamela

Unclear connection there, but great transition.

MCP is so big right now. I actually went to MCP Night very close to here a month ago. It was the fanciest tech event I had ever been to — cocktail attire. I have never been to a tech event with cocktail attire. I had to buy boots, I had a lookbook — I think it was an AI-generated lookbook. MCP is so big that it is warranting fancy events for 2,000 people, and they said they are going to move to Oracle Stadium next because of the demand.

MCP stands for Model Context Protocol, and it is a standard protocol for giving more context to agentic applications. It came out of Anthropic's Claude Code — they wanted a way for people to bring in more functionality to make Claude Code more powerful. And once you have an MCP server, since it is a standard, it works everywhere. If that MCP server works in GitHub Copilot, you can also bring it into anything that understands MCP — LangChain, Foundry agents, all the agent frameworks.

It becomes a common way of exposing an API surface so that any agentic application can use the same tools. As a developer, you might start thinking: does my application have to be a user-facing application, or could I just build an MCP server? In the future, maybe you will write your MCP servers before you write your front end.

## Matt

Going back to the original question of what an agent is — it is being able to use tools, take action in the world. To me, MCP is really about where those tools are located. Are they running right alongside the LLM, or are they somewhere else? Just like I go to bing.com or microsoft.com to access a resource over the web, agents can now do the same thing and have their capabilities enhanced.

The exciting thing about MCP for context engineering is that you can add that capability to any agent. We are also working on adding other MCPs as knowledge sources to Foundry IQ. So it goes both ways. You can reach out to things we never thought of when we built Foundry IQ — maybe you want to integrate with Jira, or go to Wikipedia. You can plug in new integrations, and because an LLM is mediating all these interactions, it can just figure it out.

## Allison

So it is just MCP all the way down now.

## Pamela

Yeah, the great thing about MCP is that it is like the USB-C of AI. It is one plug that you can put anywhere and it just kind of gets extended.

## Matt

I saw this really interesting talk from a frontend engineer who is trying to figure out what frontend engineering looks like in the future. He thinks frontend engineering might go away the way we traditionally think of it. Right now, if we want to provide a service, we build a website with a navigation menu. But in the future, we might build MCP servers first. You go to your favorite agent, say "I want to book a ticket," and it uses the ticketing MCP server. You never have to visit a website. You can still have visuals — a map, product images, cool purple shirts for this podcast — but you are interacting entirely over chat with a shopping server over MCP. That is a potential future version of the web.

## Allison

So maybe RAG is not dead — the web interface might be dead.

## Matt

The web is dead!

## Allison

You are going to have to throw some cold water here. Human verification is never going to go out of style. When you build an agentic application, yes, think about what to build first. But having an interface where humans can at least check and correct agent work is really important.

## Pamela

I agree, because Copilot and similar products are all user-facing interfaces, and they do keep a human in the loop. It is just a different interface for the human being in the loop.

How do we present results to users? Andrej Karpathy gave a great talk where he said every interface needs a way of showing a diff. When we are doing code and the agentic coding tool makes a change, we can see the diff. Imagine that for everything. If you are using an agent to create a PowerPoint presentation and you ask it to make a bunch of changes, what is the diff? How do you visualize what changed so you can have confidence that you liked what the agent did?

## Matt

It is up to all the builders out there to make these tough decisions. We are really excited about the ability to give agents better context so they can do the work, but there are a lot of open problems still to be solved.

## Pamela

If we can find really good ways of keeping humans in the loop and empowering them with enough information to figure out whether they liked what happened — that is the challenge. People are working in so many different domains. They come to us with the most fascinating documents: semi-structured Excel files, diagrams, weird tables. "How do we ingest this?" is a really good question.

The high level is: you are going to do some context engineering, you want to put rigor into it, you want to figure out what works for your domain, and you want to evaluate it. We have great retrieval techniques and great data ingestion techniques for complicated data. You are going to experiment and see what gives you the best results. It is a really fun space to work in, because you start to understand both how powerful these models are and that they have really interesting limitations. You always talk about the jagged edge.

## Matt

When we talk about model intelligence, we talk about a model that can get a 1600 on the SAT, the smartest person around.

## Pamela

I also got a 1600 on the SAT. I feel the need to mention that.

## Matt

Are you serious? You could be an LLM. That is amazing.

## Pamela

I am very good at pattern recognition.

## Matt

So when you talk about model intelligence, you talk about a model that scores really well on any standardized test, but also does not necessarily know how many letters are in the word "strawberry." The builders who are figuring out how to really get the most out of these models are the ones who are asking, "Where are the strategies that work? And how can context engineering help me overcome the model's limitations and let me get useful work done?"