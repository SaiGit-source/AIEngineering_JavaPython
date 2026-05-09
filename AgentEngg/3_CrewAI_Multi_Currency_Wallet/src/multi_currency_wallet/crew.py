from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from multi_currency_wallet.tools.ExchangeRateTool import ExchangeRateTool
import os

def transaction_report_callback(task_output):
    # 1. Define the folder path
    folder_path = "output/callback"
    file_path = os.path.join(folder_path, "report.txt")

    # 2. Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 3. Save the report
    print(f"Saving report to {file_path}...")
    with open(file_path, "w") as f:
        f.write(task_output.raw)
    
    print("✅ Report successfully saved.")


@CrewBase
class MultiCurrencyWalletCrew():
    """MultiCurrencyWallet crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="unsafe",  # I dont have docker set up on my machine, so I will allow unsafe code execution but with a time limit and retry limit to mitigate risks
            max_execution_time=500, 
            max_retry_limit=3,
            tools=[ExchangeRateTool()],
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
        )
    
    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
            callback=transaction_report_callback ## After coding is done by AI, it writes the Python code to a file and then calls the callback function to save the report of the coding task output to a text file. This is just to demonstrate how callbacks can be used to trigger actions after a task is completed.
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the engineering crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )