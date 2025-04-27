from crewai import Crew, Agent, Task, Process, LLM


gemini_llm = LLM(
    model="gemini/gemini-1.5-pro",
    api_key="AIzaSyC09vgOIf0feqQ2omtUaraUbzYZu9vUtHI",  # Ensure this is securely stored in production
    provider="google",
    max_tokens=300
)

# Define agents
manager = Agent(
    role="Manager",
    goal="Understand user's query and coordinate appropriate responses by deciding whether it's general talk, a financial idea, or a request for idea + alpha.",
    backstory="You are responsible for interpreting the user's message and managing the appropriate agents to respond effectively.",
    allow_delegation=True,
    llm=gemini_llm
)

idea_creator = Agent(
    role="Idea Creator",
    goal="Generate creative financial ideas for alpha generation. Answer in three lines maximum.",
    backstory="You specialize in inventing new trading strategies based on financial insights. Answer in three lines maximum.",
    llm=gemini_llm
)

alpha_creator = Agent(
    role="Alpha Creator",
    goal="Transform financial ideas into detailed financial alphas (trading signals). Answer in five lines maximum.",
    backstory="You are skilled at designing quantifiable and profitable alphas from ideas. Answer in five lines maximum.",
    llm=gemini_llm
)

# Main Crew Class
class FinancialAlphaCrew:
    def __init__(self):
        self.manager = manager
        self.idea_creator = idea_creator
        self.alpha_creator = alpha_creator

    def handle_query(self, query_content):
        # Step 1: First, Manager decides the query type
        classification_task = Task(
            agent=self.manager,
            description=f"""Analyze this user query and determine its type. 
Respond ONLY with one of these options exactly:
- general_talk
- financial_idea
- request_idea_and_alpha

User query: {query_content}""",
            expected_output="Exactly one of: general_talk, financial_idea, request_idea_and_alpha"
        )

        classification_crew = Crew(
            agents=[self.manager],
            tasks=[classification_task],
            process=Process.sequential,
        )
        query_type = classification_crew.kickoff()
        query_type = str(query_type).strip().lower()

        # Step 2: Based on the query type, decide next action
        if query_type == "general_talk":
            response_task = Task(
                agent=self.manager,
                description=f"Respond politely and informatively to the user's general query: {query_content}. Answer in three lines maximum.",
                expected_output="A polite and informative reply. Answer in three lines maximum."
            )
            response_crew = Crew(
                agents=[self.manager],
                tasks=[response_task],
                process=Process.sequential,
            )
            return response_crew.kickoff()

        elif query_type == "financial_idea":
            alpha_task = Task(
                agent=self.alpha_creator,
                description=f"Create a financial alpha based on this user-provided idea: {query_content} \n Answer in five lines maximum.",
                expected_output="A structured financial alpha based on the idea. Answer in five lines maximum."
            )
            alpha_crew = Crew(
                agents=[self.alpha_creator],
                tasks=[alpha_task],
                process=Process.sequential,
            )
            return alpha_crew.kickoff()

        elif query_type == "request_idea_and_alpha":
            # First create idea
            idea_task = Task(
                agent=self.idea_creator,
                description="Generate a new financial idea that can be used for alpha generation. Answer in three lines maximum.",
                expected_output="A creative financial idea. Answer in three lines maximum."
            )
            idea_crew = Crew(
                agents=[self.idea_creator],
                tasks=[idea_task],
                process=Process.sequential,
            )
            generated_idea = idea_crew.kickoff()

            # Then create alpha based on generated idea
            alpha_task = Task(
                agent=self.alpha_creator,
                description=f"Create a financial alpha based on this newly generated idea: {generated_idea} \n Answer in five lines maximum.",
                expected_output="A structured financial alpha based on the idea. Answer in five lines maximum"
            )
            alpha_crew = Crew(
                agents=[self.alpha_creator],
                tasks=[alpha_task],
                process=Process.sequential,
            )
            generated_alpha = alpha_crew.kickoff()
            
            return generated_alpha

            # return {
            #     "generated_idea": generated_idea,
            #     "generated_alpha": generated_alpha
            # }

        else:
            return "Sorry, I could not understand your query."

# Example Usage:

financial_alpha_crew = FinancialAlphaCrew()

# Example queries:
# response = financial_alpha_crew.handle_query("Hi, how are you doing today?")
# response = financial_alpha_crew.handle_query("Use moving average crossovers for a trading strategy.")
response = financial_alpha_crew.handle_query("Can you suggest a financial idea and build an alpha as well?")