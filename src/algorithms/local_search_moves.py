from enum import Enum
from itertools import combinations, product

from src.model import Delta, DeltaInterNodes, DeltaIntraEdges, DistanceMatrix, Node, Run
from src.utils import get_edges


class MoveAction(Enum):
    REMOVE = 0
    KEEP = 1
    USE = 2


def local_search_moves(
    initial_solution: list[Node],
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    **kwargs,
) -> list[Node]:
    if initial_solution is None:
        raise ValueError("Initial solution is None!")

    current_run = Run(0, initial_solution, distance_matrix)
    current_sequence = set(current_run.nodes)
    nodes_set = set(nodes)

    move_list = _get_move_list(current_run.nodes, nodes_set, distance_matrix)
    while True:
        if current_run.score < 0:
            raise ValueError("Current solution is not valid!")

        to_remove = set()
        for move in move_list:
            res = validate_move(move, current_sequence)
            if res == MoveAction.KEEP:
                continue

            elif res == MoveAction.REMOVE:
                to_remove.add(move)
                continue

            # Current run needs to be updated before updating move list
            current_run = Run.from_delta(current_run, move)
            current_sequence = set(current_run.nodes)

            # Add new moves to move_list
            move_list += _get_updated_move_list(move, current_sequence, nodes_set, distance_matrix)

            # Remove used move
            to_remove.add(move)

            break
        else:
            # Move list is empty or no valid move was found
            break

        move_list = _filter_sort_move_list(move_list, to_remove)

    return current_run.nodes


def _filter_sort_move_list(move_list: list[Delta], to_remove: set | None = None) -> list[Delta]:
    if to_remove is None:
        to_remove = set()

    move_list = [move for move in move_list if move < 0 and move not in to_remove]
    move_list.sort()
    return move_list


def _get_move_list(
    original_sequence: list[Node], nodes: set[Node], distance_matrix: DistanceMatrix
) -> list[Delta]:
    inter_moves = _inter(original_sequence, nodes, distance_matrix)
    intra_moves = _intra(original_sequence, distance_matrix)

    move_list: list[Delta] = inter_moves + intra_moves
    move_list = _filter_sort_move_list(move_list)

    return move_list


def _inter(
    original_sequence: list[Node], nodes: set[Node], distance_matrix: DistanceMatrix
) -> list[DeltaInterNodes]:
    og_seq = set(original_sequence)
    changes = product(og_seq, nodes - og_seq)

    neighbourhood: list[DeltaInterNodes] = []
    for change in changes:
        inter_node, outer_node = change
        neighbourhood.append(DeltaInterNodes(inter_node, outer_node, distance_matrix))

    return neighbourhood


def _intra(original_sequence: list[Node], distance_matrix: DistanceMatrix) -> list[DeltaIntraEdges]:
    all_edges = get_edges(original_sequence)
    edge_swaps = combinations(all_edges, 2)

    neighbourhood = []

    # remove non valid edge swaps
    for swap in edge_swaps:
        left, right = swap
        if left[1] == right[0] or left[0] == right[1]:
            continue

        outerA, outerB = left[0], right[1]

        neighbourhood.append(DeltaIntraEdges(outerA, outerB, distance_matrix))

    # Size: n*(n - 3)/2
    return neighbourhood


def validate_move(move: Delta, current_sequence: set[Node]) -> MoveAction:
    if isinstance(move, DeltaIntraEdges):
        return _is_intra_edges_move_valid(move, current_sequence)
    elif isinstance(move, DeltaInterNodes):
        return _is_inter_nodes_move_valid(move, current_sequence)
    else:
        raise ValueError("Invalid move!")


def _is_inter_nodes_move_valid(move: DeltaInterNodes, current_sequence: set[Node]) -> MoveAction:
    # Check if nodeA is still in the sequence and still has same neighbours
    # and
    # Check if nodeB is still not in the sequence
    nodeA_prev, nodeA, nodeA_next, nodeB = move.applied_to_nodes

    is_valid = (
        nodeA in current_sequence
        and nodeB not in current_sequence
        and nodeA.prev_connection == nodeA_prev
        and nodeA.next_connection == nodeA_next
    )
    if is_valid:
        return MoveAction.USE
    else:
        return MoveAction.REMOVE


def _is_intra_edges_move_valid(move: DeltaIntraEdges, current_sequence: set[Node]) -> MoveAction:
    # Check if nodeA is still in the sequence and connected to innerA same as before
    # and
    # Check if nodeB is still in the sequence and connected to innerB same as before

    outerA, innerA, innerB, outerB = move.applied_to_nodes

    if outerA not in current_sequence or outerB not in current_sequence:
        return MoveAction.REMOVE

    if outerA.next_connection == innerA:
        if outerB.prev_connection == innerB:
            return MoveAction.USE
        elif outerB.next_connection == innerB:
            return MoveAction.KEEP
    elif outerA.prev_connection == innerA:
        if outerB.prev_connection == innerB:
            return MoveAction.KEEP
        # Deleted USE when both are reversed

    return MoveAction.REMOVE


def _get_updated_move_list(
    current_move: Delta,
    current_sequence: set[Node],
    nodes: set[Node],
    distance_matrix: DistanceMatrix,
) -> list[Delta]:
    # Create all combinations for newly added node with all nodes not in the sequence
    # and
    # Create all combinations for removed node with all nodes in the sequence
    inter_delta = []
    intra_delta = []

    if isinstance(current_move, DeltaInterNodes):
        outside_sequence = nodes - current_sequence

        # old_intra_node - new_outer_node (no connections)
        # old_outer_node - new_intra_node (has connections)
        # AFTER APPLY!
        old_intra_node, old_outer_node = current_move.nodes
        # old_intra_node.connections = None, None
        # old_outer_node.connections = 2, 4
        #
        # current_sequence contains old_outer_node
        # outside_sequence contains old_intra_node
        inter_delta.extend(
            [
                DeltaInterNodes(intra_node, outer_node, distance_matrix)
                for intra_node, outer_node in product(current_sequence, [old_intra_node])
            ]
        )
        inter_delta.extend(
            [
                DeltaInterNodes(inter_node, outer_node, distance_matrix)
                for inter_node, outer_node in product([old_outer_node], outside_sequence)
            ]
        )

        outerA_1, outerA_2 = old_outer_node.prev_connection, old_outer_node
        for node in current_sequence:
            # Case for outerA_1:
            if node not in (
                outerA_1,
                outerA_1.next_connection,
                outerA_1.next_connection.next_connection,
            ):
                intra_delta.append(DeltaIntraEdges(outerA_1, node, distance_matrix))

            # Case for outerA_2:
            if node not in (
                outerA_2,
                outerA_2.next_connection,
                outerA_2.next_connection.next_connection,
            ):
                intra_delta.append(DeltaIntraEdges(outerA_2, node, distance_matrix))

    # New delta edges are created by BOTH DeltaInterNodes and DeltaIntraEdges

    # Create all combinations for newly added edge with all edges in the sequence
    # and
    # Create all combinations for removed edge with all edges in the sequence
    elif isinstance(current_move, DeltaIntraEdges):
        outerA, outerB = current_move.nodes

        for node in current_sequence:
            if node in (outerA, outerB):
                continue

            if node != outerB.prev_connection and node.next_connection != outerB.prev_connection:
                intra_delta.append(DeltaIntraEdges(node, outerB, distance_matrix))

            if node != outerA.next_connection and node.prev_connection != outerA.next_connection:
                intra_delta.append(DeltaIntraEdges(outerA, node, distance_matrix))

    return inter_delta + intra_delta
