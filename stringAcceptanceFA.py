def Accept(string, first):
    global Accepted
    if len(string) == 0:
        if final_states.__contains__(first):
            Accepted = True
        return
    for neighbor in adj_dict[first]:
        if neighbor[0] == string[0]:
            Accept(string[1:], neighbor[1])
        elif neighbor[0] == '$':
            Accept(string, neighbor[1])
    return


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
    string = input().replace('$', '')
    Accept(string, states[0])
    if Accepted == 1:
        print("Accepted")
    else:
        print("Rejected")
