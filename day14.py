def parse_instructions(txt):
    '''Converts input in "x A, y B => z C" format to dictionary'''
    from re import findall
    inputs, outputs = txt.split("=>")
    
    inputs = {key:-1*int(digit) for digit, key in zip(findall(r"\d+", inputs), findall(r"[A-Za-z]+", inputs))}
    outputs = {key:int(digit) for digit, key in zip(findall(r"\d+", outputs), findall(r"[A-Za-z]+", outputs))}
    
    return {**inputs, **outputs}
    
def build_LP(instructions, day_1=True):
    '''For day 1, uses linear program approach to minimize amount of ORE required, while producing
    1 FUEL, using the exchange rates given in input instructions
    For day 2, uses linear program approach to maximize amount of FUEL produced, while using
    1 trillion ORE'''
    
    import pulp
    pulp.LpSolverDefault.msg = 0 # turn off noise
        
    # create problem
    if day_1:
        # for day 1, minimize ORE
        problem = pulp.LpProblem('required_ORE', pulp.LpMinimize)
    else:
        # for day 2, maximize FUEL
        problem = pulp.LpProblem('produced_FUEL', pulp.LpMaximize)

    # add variables (# of times each reaction runs and amount left over for each type)
    variables = {**{'Reaction_{}'.format(i):pulp.LpVariable('Reaction_{}'.format(i), cat='Integer') for i in range(len(instructions))}, **{col:pulp.LpVariable(col, cat='Integer') for col in instructions.columns}}

    # set goal
    if day_1:
        # minimize ORE used
        problem += variables['ORE']
    else:
        # maximize FUEL produced
        problem += variables['FUEL']

    # no reaction can be run backwards
    for variable in variables.values():
        problem += (0<=variable)
        

    for col in instructions.columns.drop('ORE'):
        # how much is made
        problem += (variables[col]==pulp.lpDot(instructions[col].apply(lambda x:x if x>0 else 0), variables.values()))
        
    for col in instructions.columns:
        # how much is left over
        problem += (variables[col]+pulp.lpDot(instructions[col].apply(lambda x:x if x<0 else 0), variables.values())>=0)
        
    if day_1:
        # must make 1 fuel
        problem += (variables['FUEL']>=1)
    else:
        # start with 1 trillion ORE
        problem += (variables['ORE']==1000000000000)
    
    # solve problem
    status = problem.solve()
    
    # make sure program converged
    assert pulp.LpStatus[status]=='Optimal'
    if day_1:
        return round(variables['ORE'].value())
    else:
        return round(variables['FUEL'].value())
    
def main():
    with open('day14.txt', 'r') as f:
        data = f.read().strip().split("\n")
    f.close()
    
    import pandas as pd
    instructions = pd.DataFrame([parse_instructions(datum) for datum in data], dtype=int).fillna(0).astype(int)
    
    # day 1
    print(build_LP(instructions, day_1=True))
    
    # day 2
    print(build_LP(instructions, day_1=False))
    
if __name__=='__main__':
    main()