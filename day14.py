def parse_instructions(txt):
    '''Converts input in "x A, y B => z C" format to dictionary'''
    from re import findall
    inputs, outputs = txt.split("=>")
    
    inputs = {key:-1*int(digit) for digit, key in zip(findall(r"\d+", inputs), findall(r"[A-Za-z]+", inputs))}
    outputs = {key:int(digit) for digit, key in zip(findall(r"\d+", outputs), findall(r"[A-Za-z]+", outputs))}
    
    return {**inputs, **outputs}
    
def build_LP(instructions):
    '''Uses linear program approach to minimize amount of ORE required, while producing
    1 FUEL, using the exchange rates given in input instructions'''
    
    import pulp
    pulp.LpSolverDefault.msg = 0 # turn off noise
        
    # create problem
    problem = pulp.LpProblem('required_ORE', pulp.LpMinimize)

    # add variables (# of times each reaction runs and amount left over for each type)
    variables = {**{'Reaction_{}'.format(i):pulp.LpVariable('Reaction_{}'.format(i), cat='Integer') for i in range(len(instructions))}, **{col:pulp.LpVariable(col, cat='Integer') for col in instructions.columns}}

    # set goal (minimize ORE used)
    problem += variables['ORE']

    # no reaction can be run backwards
    for variable in variables.values():
        problem += (0<=variable)
        

    for col in instructions.columns.drop('ORE'):
        # how much is made
        problem += (variables[col]==pulp.lpDot(instructions[col].apply(lambda x:x if x>0 else 0), variables.values()))
        
    for col in instructions.columns:
        # how much is left over
        problem += (variables[col]+pulp.lpDot(instructions[col].apply(lambda x:x if x<0 else 0), variables.values())>=0)
        
    # must make 1 fuel
    problem += (variables['FUEL']>=1)
    
    # solve problem
    status = problem.solve()
    
    # make sure program converged
    assert pulp.LpStatus[status]=='Optimal'
    return round(variables['ORE'].value())
    
def main():
    with open('day14.txt', 'r') as f:
        data = f.read().strip().split("\n")
    f.close()
    
    import pandas as pd
    instructions = pd.DataFrame([parse_instructions(datum) for datum in data], dtype=int).fillna(0).astype(int)
    
    # day 1
    print(build_LP(instructions))
    
if __name__=='__main__':
    main()