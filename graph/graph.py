from pylab import plt, np
from os import path
import json


class Parameters(object):

    figsize = (25, 12)
    legend_font_size = 30
    label_font_size = 40
    label_value_size = 27
    title_size = 50
    line_width = 5


class MarketAttendancePlot(Parameters):

    def __init__(self, save_path, choice):

        self.X, self.Ys = self.format_data(choice)
        self.fig_name = save_path + "/market_attendance.pdf"

    @staticmethod
    def format_data(choice):

        t_max = len(choice)

        x = np.arange(t_max)

        y0 = []
        y1 = []
        y2 = []
        for t in range(t_max):
            y0.append(choice[t].count([0, 1]) + choice[t].count([1, 0]))
            y1.append(choice[t].count([1, 2]) + choice[t].count([2, 1]))
            y2.append(choice[t].count([2, 0]) + choice[t].count([0, 2]))

        ys = y0, y1, y2

        return x, ys

    def plot(self):

        fig = plt.figure(figsize=self.figsize)
        fig.patch.set_facecolor('white')
        # fig.patch.set_alpha(0)

        ax = plt.gca()
        ax.set_title("Markets attendance \n", fontsize=self.title_size)

        labels = [
            "Market 0 -> 1 / 1 -> 0",
            "Market 1 -> 2 / 2 -> 1",
            "Market 2 -> 0 / 0 -> 2",
        ]
        line_styles = [
            "-",
            "--",
            ":"
        ]

        for i, y in enumerate(self.Ys):
            ax.plot(self.X, y, label=labels[i],
                    linewidth=self.line_width, color="black", linestyle=line_styles[i])

        ax.legend(bbox_to_anchor=(0.8, 1.19), loc=2, fontsize=self.legend_font_size, frameon=False)
        ax.tick_params(axis='both', which='major', labelsize=self.label_value_size)

        ax.set_xlabel("t", fontsize=self.label_font_size)
        ax.set_ylabel("n", fontsize=self.label_font_size)

        ax.spines['right'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)
        plt.close()


class ChoicePlot(Parameters):

    def __init__(self, save_path, choice):

        self.X, self.Ys = self.format_data(choice)
        self.fig_name = save_path + "/choice.pdf"

    @staticmethod
    def format_data(choice):

        t_max = len(choice)

        x = np.arange(t_max)

        y0, y1, y2, y3, y4, y5 = [], [], [], [], [], []

        for t in range(t_max):
            y0.append(choice[t].count([0, 1]))
            y1.append(choice[t].count([1, 0]))
            y2.append(choice[t].count([1, 2]))
            y3.append(choice[t].count([2, 1]))
            y4.append(choice[t].count([2, 0]))
            y5.append(choice[t].count([0, 2]))

        ys = y0, y1, y2, y3, y4, y5

        return x, ys

    def plot(self):

        fig = plt.figure(figsize=self.figsize)
        fig.patch.set_facecolor('white')
        fig.patch.set_alpha(0)

        ax = plt.gca()
        ax.set_title("Choices \n", fontsize=self.title_size)

        labels = [
            "Choice 0 -> 1",
            "Choice 1 -> 0",
            "Choice 1 -> 2",
            "Choice 2 -> 1",
            "Choice 2 -> 0",
            "Choice 0 -> 2",
        ]
        line_styles = [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-"
        ]
        markers = [
            4,
            5,
            4,
            5,
            4,
            5
        ]

        colors = [
            "red",
            "red",
            "blue",
            "blue",
            "green",
            "green"
        ]

        for i, y in enumerate(self.Ys):
            ax.plot(
                self.X, y, label=labels[i],
                linewidth=self.line_width, color=colors[i], linestyle=line_styles[i],
                marker=markers[i])

        ax.legend(bbox_to_anchor=(0.95, 1.19), loc=2, fontsize=self.legend_font_size, frameon=False)
        ax.tick_params(axis='both', which='major', labelsize=self.label_value_size)

        ax.set_xlabel("t", fontsize=self.label_font_size)
        ax.set_ylabel("n", fontsize=self.label_font_size)

        ax.spines['right'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)
        plt.close()


class ConsumptionPlot(Parameters):

    def __init__(self, save_path, choice, success, agent_type):

        self.X, self.Y = self.format_data(choice=choice, success=success, agent_type=agent_type)
        self.fig_name = save_path + "/consumption.pdf"

    @staticmethod
    def format_data(choice, success, agent_type):

        t_max = len(choice)

        x = np.arange(t_max)
        y = []

        for t in range(t_max):

            consumption = 0
            for c, s, at, in zip(choice[t], success[t], agent_type):
                if c[1] == (at + 1) % 3 and s:
                    consumption += 1

            y.append(consumption)

        return x, y

    def plot(self):

        fig = plt.figure(figsize=self.figsize)
        fig.patch.set_facecolor('white')
        fig.patch.set_alpha(0)

        ax = plt.gca()
        ax.set_title("Consumption\n", fontsize=self.title_size)

        ax.plot(self.X, self.Y, linewidth=self.line_width, color="black")
        ax.tick_params(axis='both', which='major', labelsize=self.label_value_size)

        ax.set_xlabel("t", fontsize=self.label_font_size)
        ax.set_ylabel("n", fontsize=self.label_font_size)

        ax.spines['right'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)
        plt.close()


class MediumOfExchangePlot(Parameters):

    def __init__(self, save_path, choice, agent_type):

        self.fig_name = save_path + "/medium_of_exchange.pdf"
        self.X, self.Ys = self.format_data(choice, agent_type)

    @staticmethod
    def format_data(choice, agent_type):

        t_max = len(choice)

        x = np.arange(t_max)

        ys = [], [], []

        for t in range(t_max):

            # Will register the number of times each good has been used as a medium of exchange
            y = [0, 0, 0]

            for i, ch, at in zip(range(len(agent_type)), choice[t], agent_type):

                p = at
                c = (at + 1) % 3
                m = (at + 2) % 3
                if (ch[0] == p and ch[1] == m) or (ch[0] == m and ch[1] == c):
                    y[m] += 1

            for i in range(3):
                ys[i].append(y[i])

        return x, ys

    def plot(self):

        fig = plt.figure(figsize=self.figsize)
        fig.patch.set_facecolor('white')
        # fig.patch.set_alpha(0)

        ax = plt.gca()
        ax.set_title("Medium of exchange \n", fontsize=self.title_size)

        labels = [
            "Good 0",
            "Good 1",
            "Good 2",
        ]
        line_styles = [
            ":",
            "--",
            "-"
        ]

        for i, y in enumerate(self.Ys):
            ax.plot(self.X, y, label=labels[i], linewidth=self.line_width, color="black", linestyle=line_styles[i])

        ax.legend(bbox_to_anchor=(0.95, 1.19), loc=2, fontsize=self.legend_font_size, frameon=False)
        ax.tick_params(axis='both', which='major', labelsize=self.label_value_size)

        ax.set_xlabel("t", fontsize=self.label_font_size)
        ax.set_ylabel("n", fontsize=self.label_font_size)

        ax.spines['right'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)
        plt.close()


class RewardsDistribution(Parameters):

    bar_width = 2

    def __init__(self, save_path, reward_amount):

        self.X, self.Y = self.format_data(reward_amount)
        self.fig_name = save_path + "/rewards_distribution.pdf"

    @staticmethod
    def format_data(reward_amount):

        x = np.arange(min(reward_amount), max(reward_amount), 2)
        y = []
        for i in x:
            y.append(reward_amount.count(i) + reward_amount.count(i+1))

        return x, y

    def plot(self):

        fig = plt.figure(figsize=self.figsize)
        fig.patch.set_facecolor('white')
        # fig.patch.set_alpha(0)

        ax = plt.gca()
        ax.set_title("Rewards distribution\n", fontsize=self.title_size)

        ax.bar(self.X, self.Y, self.bar_width, tick_label=self.X, color="grey")
        ax.tick_params(axis='both', which='major', labelsize=self.label_value_size)

        plt.savefig(self.fig_name)
        plt.close()


def plot(data, save_path):

    mark_plot = MarketAttendancePlot(save_path, data["market_choice"])
    mark_plot.plot()

    cons_plot = ConsumptionPlot(
        save_path,
        success=data["hist_success"],
        agent_type=data["p"],
        choice=data["market_choice"],
    )
    cons_plot.plot()

    mof_plot = MediumOfExchangePlot(
            save_path,
            agent_type=data["p"],
            choice=data["market_choice"]
            )

    mof_plot.plot()

    ch_plot = ChoicePlot(save_path, choice=data["market_choice"])
    ch_plot.plot()

    rd_plot = RewardsDistribution(save_path, reward_amount=data["reward_amount"])
    rd_plot.plot()


def main():

    save_path = path.expanduser("~/Desktop/AndroidXP")
    file_path = path.expanduser("~/Desktop/AndroidXP/data.json")
    with open(file_path) as f:
        data = json.load(f)

    plot(data=data, save_path=save_path)


if __name__ == "__main__":

    main()
