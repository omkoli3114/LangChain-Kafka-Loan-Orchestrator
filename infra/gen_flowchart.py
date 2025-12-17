from graphviz import Digraph

dot = Digraph(comment='CapitalConnect Logic Flow', format='png')
dot.attr(rankdir='TB') # Top to bottom layout
dot.attr(ratio='fill') # Attempt to fill a square-ish aspect ratio if size is set, or just pack tightly
# Alternatively, 'compress' or just default TB usually helps vs LR.

dot.attr('node', shape='box', style='filled', fillcolor='lightblue')

# Nodes
dot.node('Start', 'Start: User Lands on Chatbot', shape='oval', fillcolor='lightgrey')
dot.node('Input', 'Input: Name, Income, PAN')
dot.node('Process1', 'Process 1: Master Agent Receives Data')

dot.node('Decision1', 'Decision 1: Credit Score > 700?', shape='diamond', fillcolor='orange')
dot.node('EndReject', 'End: Rejection Message', shape='oval', fillcolor='lightgrey')

dot.node('Decision2', 'Decision 2: EMI < 50% Salary?', shape='diamond', fillcolor='orange')
dot.node('Process2', 'Process 2: Loan Approved')

dot.node('Output', 'Output: Generate Sanction Letter (PDF)')
dot.node('EndSuccess', 'End: Display Download Link', shape='oval', fillcolor='lightgrey')

# Edges
dot.edge('Start', 'Input')
dot.edge('Input', 'Process1')
dot.edge('Process1', 'Decision1')

dot.edge('Decision1', 'EndReject', label='No')
dot.edge('Decision1', 'Decision2', label='Yes')

dot.edge('Decision2', 'EndReject', label='No')  # Assuming failure here also leads to rejection logic, strictly following prompt implies checking valid path
dot.edge('Decision2', 'Process2', label='Yes')

dot.edge('Process2', 'Output')
dot.edge('Output', 'EndSuccess')

# Save and Render
dot.render('capital_connect_flowchart', view=False)  # This creates 'capital_connect_flowchart.png'
