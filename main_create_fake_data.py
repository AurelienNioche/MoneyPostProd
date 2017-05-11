import numpy as np
import itertools as it
import json
from os import path

from agents.frequentist_agent import FrequentistAgent
from agents.rl_agent import RLOnAcceptanceAgent


class Economy(object):

    roles = [(0, 1), (1, 2), (2, 0)]
    n_goods = 3

    def __init__(self, repartition_of_roles, t_max, agent_model,
                 cognitive_parameters=None):

        self.t_max = t_max
        self.cognitive_parameters = cognitive_parameters
        self.agent_model = agent_model
        self.repartition_of_roles = np.asarray(repartition_of_roles)

        self.n_agent = sum(self.repartition_of_roles)

        self.markets = self.construct_markets(self.n_goods)
        self.exchanges_types = list(it.combinations(range(self.n_goods), r=2))

        self.choice = [None for i in range(self.n_agent)]  # Just for backup
        self.success = [0 for i in range(self.n_agent)] * self.n_agent  # Just for backup

        self.agents = self.create_agents()

    @staticmethod
    def construct_markets(n_goods):

        markets = {}
        for i in it.permutations(range(n_goods), r=2):
            markets[i] = []
        return markets

    def create_agents(self):

        agents = []

        agent_idx = 0

        for agent_type, n in enumerate(self.repartition_of_roles):

            i, j = self.roles[agent_type]

            for ind in range(n):
                a = self.agent_model(
                    prod=i, cons=j,
                    cognitive_parameters=self.cognitive_parameters,
                    n_goods=self.n_goods,
                    idx=agent_idx)

                agents.append(a)
                agent_idx += 1

        return agents

    def time_step(self):

        # ---------- MANAGE EXCHANGES ----- #
        self.organize_encounters()

        # Each agent consumes at the end of each round and adapt his behavior (or not).
        for agent in self.agents:
            agent.consume()

    def organize_encounters(self):

        for k in self.markets:
            self.markets[k] = []

        for idx in range(self.n_agent):
            agent_choice = self.agents[idx].which_exchange_do_you_want_to_try()
            self.markets[agent_choice].append(idx)
            self.choice[idx] = agent_choice  # Keep a trace

        success_idx = []
        for i, j in self.exchanges_types:

            a1 = self.markets[(i, j)]
            a2 = self.markets[(j, i)]
            min_a = int(min([len(a1), len(a2)]))

            if min_a:

                success_idx += list(np.random.choice(a1, size=min_a))
                success_idx += list(np.random.choice(a2, size=min_a))

        self.success = [0, ] * self.n_agent
        for idx in success_idx:

            self.success[idx] = 1  # Keep a trace
            self.agents[idx].proceed_to_exchange()

    def get_choice(self):

        return self.choice

    def get_agent_type(self):

        return [i.P for i in self.agents]

    def inventory(self):

        return [i.H for i in self.agents]

    def get_success(self):

        return self.success

    def get_consumption(self):

        return [i.consumption for i in self.agents]


class Backup(object):

    def __init__(self, file_path):

        self.file_path = file_path

        self.data = None
        self.n = None

    def init(self, agent_type):

        self.n = len(agent_type)
        self.data = {
            "p": list(agent_type),
            "market_choice": [],
            "hist_success": [],
            "reward_amount": [0 for i in range(self.n)]
        }

    def add_data(self, choice, success, consumption):

        self.data["market_choice"].append(choice.copy())
        self.data["hist_success"].append(success.copy())

        for i in range(self.n):

            self.data["reward_amount"][i] += consumption[i]

    def end(self):

        with open(self.file_path, "w") as f:
            json.dump(self.data, f)


def main():

    file_path = path.expanduser("~/Desktop/AndroidXP/fake.json")

    t_max = 100

    repartition_of_roles = 33, 33, 33

    cognitive_parameters = {
        "alpha": 0.1,
        "temp": 0.01
    }

    parameters = {
        "repartition_of_roles": repartition_of_roles,
        "agent_model": RLOnAcceptanceAgent,
        "cognitive_parameters": cognitive_parameters,
        "t_max": t_max
    }

    e = Economy(**parameters)

    b = Backup(file_path=file_path)
    b.init(agent_type=e.get_agent_type())

    for t in range(t_max):
        e.time_step()
        b.add_data(choice=e.get_choice(), success=e.get_success(), consumption=e.get_consumption())

    b.end()


if __name__ == "__main__":

    main()
