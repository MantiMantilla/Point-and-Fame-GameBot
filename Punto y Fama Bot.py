# Import packages
import pulp as lp
import random as gn

# Ask for game conditions
n_players = int(input("Ingrese la cantidad de jugadores: "))

# Choose own number
my_num = gn.sample(range(1, 10), 4)

# Sets

## Set of players
P = [str(i) for i in range(1,n_players + 1)]

## Set of digit positions
N = [str(i) for i in range(1, 5)]

## Set of possible digits assigned to any position
J = [j for j in range(0, 10)]

# Set partitions

## Set of turns taken for each person p in P
II = {p : [] for p in P}

# Parameters

## whether digit j in J was guessed for the person p in P for trial i in II_p on position n in N
dig = {(p, i, n, j) : 0 for p in P for i in II[p] for n in N for j in J}

## Points earned on person p in P for attempt i in II_p
pun = {(p, i) : 0 for p in P for i in II[p]}

## Fames earned on person p in P for attempt i in II_p
fam = {(p, i) : 0 for p in P for i in II[p]}

# Declare the problem
prob = lp.LpProblem("Point_and_Fame", lp.const.LpMinimize)

# Variables

## The number chosen by person p in P has the digit j in J on position n in N
x = lp.LpVariable.dicts("pers_has_dig_in_pos_",
                        [(p, n, j) for p in P for n in N for j in J],
                        cat = lp.const.LpBinary)

# Constraints

## A digit j in J can be at most in a single position por person p in P
for p in P:
    for j in J:
        prob += lp.lpSum(x[(p, n, j)] for n in N) <= 1
        
## Every person p in P has in every position n in N just one digit
for p in P:
    for n in N:
        prob += lp.lpSum(x[(p, n, j)] for j in J) == 1
        
## Independant of their position, the digits guessed for person p in p in
## round i in II_p must match their chosen number by as many positions as the
## guess has points and fames
for p in P:
    for i in II[p]:
        print(f"retricc. 1: {i}")
        prob += lp.lpSum(lp.lpSum(x[(p, n, j)] for n in N) * lp.lpSum(dig[(p, i, n, j)] for n in N) for j in J) == pun[(p, i)] + fam[(p, i)]
        
## The digits chosen by person p in P match the digits guessed on trial p in P
for p in P:
    for i in II[p]:
        print(f"retricc. 2: {i}")
        prob += lp.lpSum(dig[(p, i, n, j)] * x[(p, n, j)] for n in N for j in J) == fam[(p, i)]
        
# Objective Function

## Minimize the guessed number

prob += lp.lpSum(j * x[p, n, j] for p in P for n in N for j in J)

loop_condition = True

while loop_condition:
    # Optimize
    prob.solve()
    
    # Print results
    print(lp.LpStatus[prob.status])

    for p in P:
        print(f"Player {p}:")
        print(f"Is your number {''.join([str(int(round(sum(j * x[p, n, j].value() for j in J)))) for n in N])}?")
        
    for p in P:
        print("Let's guess a number!")
        person = input("To whom does this number belong? (1 - 4): ")
        new_guess = input("What's the guess? (4 digit number): ")
        new_points = int(input("How many points did this guess earn? (1 - 4): "))
        new_fames = int(input("How many fames did this guess earn? (1 - 4): "))
        i = str(len(II[person]) + 1)
        II[person].append(i)
        pun[(person,i)] = new_points
        fam[(person,i)] = new_fames
        for n in N:
            for j in J:
                if int(new_guess[int(n)-1]) == j:
                    dig[(person, i, n, j)] = 1
                else:
                    dig[(person, i, n, j)] = 0
        ## Independant of their position, the digits guessed for person p in p in
        ## round i in II_p must match their chosen number by as many positions as the
        ## guess has points and fames
        prob += lp.lpSum(lp.lpSum(x[(person, n, j)] for n in N) * lp.lpSum(dig[(person, i, n, j)] for n in N) for j in J) == pun[(person, i)] + fam[(person, i)]
                
        ## The digits chosen by person p in P match the digits guessed on trial p in P
        prob += lp.lpSum(dig[(person, i, n, j)] * x[(person, n, j)] for n in N for j in J) == fam[(person, i)]
        
        
        


