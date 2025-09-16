# demo_tabouret.py
from tabouret_agent import ConversationAgent

def run_demo():
    agent = ConversationAgent()
    response = agent.process_turn()
    print(f"Agent ({response['stage']}): {response['message']}")

    while response["stage"] != "END":
        user_input = input("You: ")
        response = agent.process_turn(user_input)
        print(f"Agent ({response['stage']}): {response['message']}")

if __name__ == "__main__":
    run_demo()
