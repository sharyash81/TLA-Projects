import copy


def dfs(state):
    global reachable_vertex
    reachable_vertex.append(state)
    for vertex in adj_dict[state]:
        if not reachable_vertex.__contains__(vertex[1]):
            dfs(vertex[1])


if __name__ == '__main__':
    global reachable_vertex
    global adj_dict
    reachable_vertex = list()
    states = input()[1:-1].split(',')
    sigma = input()[1:-1].split(',')
    final_states = input()[1:-1].split(',')
    NUMBER_OF_RULES = int(input())
    adj_dict = dict()
    for i in range(len(states)):
        adj_dict[states[i]] = list()
    for i in range(NUMBER_OF_RULES):
        s = input().split(',')
        adj_dict[s[0]].append((s[1], s[2]))
    dfs(states[0])
    for state in states:
        if not reachable_vertex.__contains__(state):
            adj_dict.pop(state)
    for state in reachable_vertex:
        adj_dict[state].sort()
        adj_dict[state] = dict(adj_dict[state])
    group_dict = dict()
    for state in reachable_vertex:
        if (final_states.__contains__(state)):
            group_dict[state] = 0
        else:
            group_dict[state] = 1
    orig_dict = copy.deepcopy(adj_dict)
    count = 2
    while(True):
        for state in reachable_vertex:
            for alphabet in sigma:
                adj_dict[state][alphabet] = group_dict[orig_dict[state][alphabet]]
        new_list = list()
        new_list_with_state = list()
        for state in reachable_vertex:
            f = list()
            for kv in adj_dict[state]:
                f.append(adj_dict[state][kv])
            t = (tuple(f), group_dict[state])
            if not new_list.__contains__(t):
                new_list.append(t)
                new_list_with_state.append((state, t))
                group_dict[state] = len(new_list)
            else:
                for item in new_list_with_state:
                    if (item[1] == t):
                        group_dict[state] = group_dict[item[0]]
                        break
        if (len(new_list) == count):
            break
        else:
            count = len(new_list)
    print(count)
