def transition_set(state_set, alphabet):

    tr_set = set()
    for state in state_set:
        for edge in adj_dict[state]:
            if edge[0] == alphabet:
                tr_set.add(edge[1])
                res = contain_lambda(edge[1])
                while(res != None):
                    tr_set.add(res)
                    res = contain_lambda(res)
    return list(tr_set)


def contain_lambda(state):
    for edge in adj_dict[state]:
        if edge[0] == "$":
            return edge[1]
    return None


def initial(state_set: list):
    for state in state_set:
        for edge in adj_dict[state]:
            if edge[0] == '$':
                if not state_set.__contains__(edge[1]):
                    state_set.append(edge[1])
    return state_set


if __name__ == '__main__':
    global states
    global sigma
    global final_states
    global Accepted
    Accepted = 0
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

    dfa_set = list()
    dfa_set.append([states[0]])
    for state_set in dfa_set:
        state_set.sort()
        if state_set != []:
            change = False
            l = len(dfa_set)
            state_set = initial(state_set)
            for alphabet in sigma:
                added_set = transition_set(state_set, alphabet)
                added_set.sort()
                if (not dfa_set.__contains__(added_set) and not added_set == state_set):
                    dfa_set.append(added_set)
                    change = True
    # print(dfa_set)
    print(len(dfa_set))
