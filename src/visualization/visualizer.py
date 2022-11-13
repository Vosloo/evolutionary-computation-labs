import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt

from src.algorithms.methods import Method
from src.model import Grade, Node

plt.rcParams["figure.figsize"] = (16, 12)
sns.set_theme(style="darkgrid")


class Visualizer:
    def _hex_to_RGB(self, hex: str) -> list[int]:
        return [int(hex[i : i + 2], 16) for i in range(1, 6, 2)]

    def _RGB_to_hex(self, RGB: list[int]) -> str:
        RGB = [int(x) for x in RGB]
        return "#" + "".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB])

    def _create_linear_gradient(
        self, start_hex: str = "#FF0000", end_hex: str = "#00FF00", n: int = 10
    ) -> list[str]:
        s = self._hex_to_RGB(start_hex)
        f = self._hex_to_RGB(end_hex)
        gradient = [start_hex]
        for t in range(1, n):
            curr_vector = [int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) for j in range(3)]
            gradient.append(self._RGB_to_hex(curr_vector))

        return gradient

    def _map_linear_gradient(self, nodes: list[Node]) -> list[str]:
        min_cost = min(nodes, key=lambda x: x.cost).cost
        gradient = self._create_linear_gradient(
            start_hex="#C6EA8D",
            end_hex="#FE90AF",
            n=max(nodes, key=lambda x: x.cost).cost - min_cost + 1,
        )

        return [gradient[node.cost - min_cost] for node in nodes]

    def visualise_solution(self, grade: Grade, instance_name: str, method_name: Method) -> None:
        G = nx.Graph()

        nodes = grade.best_run.nodes

        for node in nodes:
            G.add_node(node, pos=(node.x, node.y), size=node.cost)

        for i in range(len(nodes) - 1):
            G.add_edge(nodes[i], nodes[i + 1])

        G.add_edge(nodes[-1], nodes[0])

        pos = nx.get_node_attributes(G, "pos")

        # Add node colors from gradient adding legend
        node_colors = self._map_linear_gradient(nodes)

        # Normalize node sizes from 200 to 1000
        node_sizes = [node.cost for node in nodes]
        node_sizes = [
            200 + (1000 - 200) * ((node_size - min(node_sizes)) / (max(node_sizes) - min(node_sizes)))
            for node_size in node_sizes
        ]

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

        meth_name = method_name.name.replace("_", " ").title()
        plt.title(f"{instance_name} - {meth_name} method")
        plt.show()

    def plot_grades(self, grades: dict[str, Grade]) -> None:
        _, (ax1, ax2, ax3) = plt.subplots(3, 1)

        for method_name, grade in grades.items():
            ax1.plot(
                [run.id for run in grade.runs], [run.cost for run in grade.runs], label=method_name
            )
            ax2.plot(
                [run.id for run in grade.runs], [run.distance for run in grade.runs], label=method_name
            )
            ax3.plot(
                [run.id for run in grade.runs],
                [run.cost + run.distance for run in grade.runs],
                label=method_name,
            )

            ax1.scatter(
                grade.best_run.id,
                grade.best_run.cost,
                color=ax1.lines[-1].get_color(),
                label=f"{method_name} best run",
            )
            ax2.scatter(
                grade.best_run.id,
                grade.best_run.distance,
                color=ax2.lines[-1].get_color(),
                label=f"{method_name} best run",
            )
            ax3.scatter(
                grade.best_run.id,
                grade.best_run.cost + grade.best_run.distance,
                color=ax3.lines[-1].get_color(),
                label=f"{method_name} best run",
            )

        ax1.set_title("Cost")
        ax2.set_title("Distance")
        ax3.set_title("Score")

        ax1.legend()
        ax2.legend()
        ax3.legend()

        plt.show()
