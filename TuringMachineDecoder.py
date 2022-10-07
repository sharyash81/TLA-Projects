class Transition:
    def __init__(self, cs, cr, ns, nw, m):
        self.current_state = cs
        self.current_read = cr
        self.next_state = ns
        self.next_write = nw
        self.move = m


def turing_accpet(str_symbol, final, current, index):
    global transitions
    if current == final:
        return True
    current_char = int(str_symbol[index])
    for transition in transitions:
        if transition.current_state == current and transition.current_read == current_char:
            str_symbol[index] = transition.next_write
            if transition.move == 1:
                if turing_accpet(str_symbol, final, transition.next_state, index-1):
                    return True
            else:
                if turing_accpet(str_symbol, final, transition.next_state, index+1):
                    return True
    return False


if __name__ == '__main__':
    global transitions
    turing_machine = input()
    input_trs = turing_machine.split('00')
    transitions = list()
    final = 0
    for transition in input_trs:
        tr_list = transition.split('0')
        if len(tr_list[2]) > int(final):
            final = len(tr_list[2])
        transitions.append(Transition(len(tr_list[0]), len(
            tr_list[1]), len(tr_list[2]), len(tr_list[3]), len(tr_list[4])))
    n = int(input())
    strings = list()
    for i in range(n):
        strs = input().split('0')
        maps = list()
        for item in strs:
            maps.append(len(item))
        if len(strs) == 1 and strs[0] == '':
            maps = list()
        for j in range(10):
            maps.append(1)
            maps.insert(0, 1)
        strings.append(maps)
    for i in range(n):
        if turing_accpet(strings[i], final, 1, 10):
            print("Accepted")
        else:
            print("Rejected")
