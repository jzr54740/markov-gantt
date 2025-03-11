import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

###############################################
###### Show the entire Markov Chain ###########
states = ['Beginner', 'Intermediate', 'Advanced 1', 'Advanced 2', 'Advanced 3', 'Advanced 4', 'Injury', 'Dropout', 'Completion']
transitionMatrix = np.array([
[0, .8614, 0, 0, 0,0,.0919,.0467,0],
[0,0,.8636,0,0,0,.035,0,.1014],
[0,0,0,.8320,0,0,.0304,0,.1377],
[0,0,0,0,.3333,0,.0998,0,.5669],
[0,0,0,0,0,.2409,.1095,0,.6496],
[0,0,0,0,0,0,.0606,0,.9394],
[0,0,0,0,0,0,0,.1616,.8384],
[0,0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,1]
])

def visualizeMarkovChain(states, transitionMatrix):
  G = nx.DiGraph()
  for i, fromState in enumerate(states):
    for j, toState in enumerate(states):
      if i == j: #self-loop
        continue
      else:
        prob = transitionMatrix[i][j]
        if prob > =:
          G.add_edge(fromState, toState, weight=prob, label=format(prob*100, '.2f') + '%')
  pos = nx.circular_layout(G)
  plt.figure(figsize=(16,8))
  nx.draw(G, pos, with_labels=True, node_size=7000, color='lightblue', font_size=10, font_weight='bold')
  labels = nx.get_edge_attributes(G, 'label')
  nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12)

  plt.show()

visualizeMarkovChain(states, transitionMatrix)

################################################
####### Gantt Chart with all stages ############
states = ['Beginner', 'Intermediate', 'Advanced Stage 1', 'Advanced Stage 2', 'Advanced Stage 3', 'Advanced Stage 4', 'Injury', 'Dropout', 'Completion']
states.reverse()
simulated_training = [
    ("Beginner", 0, 4),  # State, Start Week, Duration
    ("Intermediate", 4, 7),
    ("Advanced Stage 1", 11, 2),
    ("Advanced Stage 2", 13, 2),
    ("Advanced Stage 3", 15, 2),
    ("Advanced Stage 4", 17, 1),
    ("Tapering", 18, 2),
    ("Completion", 20, 1)
]

simulated_training.reverse()
df = pd.DataFrame(simulated_training, columns=["State", "Start Week", "Duration"])
state_colors = {
    "Beginner": "lightblue",
    "Intermediate": "blue",
    "Advanced Stage 1": "green",
    "Advanced Stage 2": "limegreen",
    "Advanced Stage 3": "yellow",
    "Advanced Stage 4": "orange",
    "Injury": "red",
    "Dropout": "black",
    "Completion": "purple"
}
fig, ax = plt.subplots(figsize=(10, 5))
for i, row in df.iterrows():
    ax.broken_barh([(row["Start Week"], row["Duration"])], (i - 0.4, 0.8), 
                   facecolors=state_colors[row["State"]])

ax.set_xlabel("Training Weeks")
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["State"])
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

###################################################################
####### Gantt chart that adapts to Markov Chain, no injury ########

def simulateTraining(transitionMatrix, states):
  np.random.seed(38)
  currentState = "Beginner"
  trainingPath = []
  while currenntState not in ["Completion", "Dropout"]:
    trainingPath.append(currentState)
    nextState = np.random.choice(states, p=list(transitionMatrix[states.index(currentState)]))
    currentState = nextState
  trainingPath.append(currentState)
  return trainingPath

states = ['Beginner', 'Intermediate', 'Advanced Stage 1', 'Advanced Stage 2', 'Advanced Stage 3', 'Advanced Stage 4', 'Injury', 'Dropout', 'Completion']
transitionMatrix = np.array([
[0, .8614, 0, 0, 0,0,.0919,.0467,0],
[0,0,.8636,0,0,0,.035,0,.1014],
[0,0,0,.8320,0,0,.0304,0,.1377],
[0,0,0,0,.3333,0,.0998,0,.5669],
[0,0,0,0,0,.2409,.1095,0,.6496],
[0,0,0,0,0,0,.0606,0,.9394],
[0,0,0,0,0,0,0,.1616,.8384],
[0,0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,1]
])

oneTrainingInstance = simulateTraining(transitionMatrix, states)
trainingWeeks = 20

simulated_training = {
  "Beginner": .20,
  "Intermediate": .35,
  "Advanced Stage 1": .10,
  "Advanced Stage 2": .10,
  "Advanced Stage 3": .10,
  "Advanced Stage 4": .05,
  "Tapering": .1,
  "Injury": .1
}

filteredTraining = {key: value for key, value in simulated_training.items() if key in oneTrainingInstance}
sumValues = sum(filteredTraining.values())
normalizedTraining = {key: value / sumValues for key, value in filteredTraining.items()}

states.reverse()

ganttTraining = []
currentWeek = 0
for key, value in normalizedTraining.items():
  ganttTraining.append((key, currentWeek, value * trainingWeeks))
  currentWeek += value * trainingWeeks
ganttTraining.append(('Completion', 20, 1))
ganttTraining.reverse()

df = pd.DataFrame(ganttTraining, columns=["State", "Start Week", "Duration"])
state_colors = {
    "Beginner": "lightblue",
    "Intermediate": "blue",
    "Advanced Stage 1": "green",
    "Advanced Stage 2": "limegreen",
    "Advanced Stage 3": "yellow",
    "Advanced Stage 4": "orange",
    "Injury": "red",
    "Dropout": "black",
    "Completion": "purple"
}
fig, ax = plt.subplots(figsize=(10, 5))
for i, row in df.iterrows():
    ax.broken_barh([(row["Start Week"], row["Duration"])], (i - 0.4, 0.8), 
                   facecolors=state_colors[row["State"]])

ax.set_xlabel("Training Week")
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["State"])
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

########################################################################
##### Gantt chart that adapts to Markov chain and handles injuries #####

def simulateTraining(transitionMatrix, states):
  np.random.seed(44)
  currentState = "Beginner"
  trainingPath = []
  while currenntState not in ["Completion", "Dropout"]:
    trainingPath.append(currentState)
    nextState = np.random.choice(states, p=list(transitionMatrix[states.index(currentState)]))
    currentState = nextState
  trainingPath.append(currentState)
  return trainingPath

states = ['Beginner', 'Intermediate', 'Advanced Stage 1', 'Advanced Stage 2', 'Advanced Stage 3', 'Advanced Stage 4', 'Injury', 'Dropout', 'Completion']
transitionMatrix = np.array([
[0, .8614, 0, 0, 0,0,.0919,.0467,0],
[0,0,.8636,0,0,0,.035,0,.1014],
[0,0,0,.8320,0,0,.0304,0,.1377],
[0,0,0,0,.3333,0,.0998,0,.5669],
[0,0,0,0,0,.2409,.1095,0,.6496],
[0,0,0,0,0,0,.0606,0,.9394],
[0,0,0,0,0,0,0,.1616,.8384],
[0,0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,1]
])

oneTrainingInstance = simulateTraining(transitionMatrix, states)
trainingWeeks = 20

simulated_training = {
  "Beginner": .20,
  "Intermediate": .35,
  "Advanced Stage 1": .10,
  "Advanced Stage 2": .10,
  "Advanced Stage 3": .10,
  "Advanced Stage 4": .05,
  "Tapering": .1,
  "Injury": .1
}

if 'Injury' in oneTrainingInstance:
  injuryIndex = oneTrainingInstance.index('Injury')
  oneTrainingInstance.insert(injuryIndex + 1, oneTrainingInstance[injuryIndex-2])

filteredTraining = {key: value for key, value in simulated_training.items() if key in oneTrainingInstance}
sumValues = sum(filteredTraining.values())
normalizedTraining = {key: value / sumValues for key, value in filteredTraining.items()}

ganttTraining = []
currentWeek = 0
for key in oneTrainingInstance:
  if key in normalizedTraining:
    ganttTraining.append((key currentWeek, normalizedTraining[key] * numWeeks / oneTrainingInstance.count(key)))
    currentWeek += normalizedTraining[key] * numWeeks / oneTrainingInstance.count(key)
ganttTraining.append(('Completion', 20, 1))
ganttTraining.reverse()

df = pd.DataFrame(ganttTraining, columns=["State", "Start Week", "Duration"])
state_colors = {
    "Beginner": "lightblue",
    "Intermediate": "blue",
    "Advanced Stage 1": "green",
    "Advanced Stage 2": "limegreen",
    "Advanced Stage 3": "yellow",
    "Advanced Stage 4": "orange",
    "Injury": "red",
    "Dropout": "black",
    "Completion": "purple"
}
fig, ax = plt.subplots(figsize=(10, 5))
for i, row in df.iterrows():
    ax.broken_barh([(row["Start Week"], row["Duration"])], (i - 0.4, 0.8), 
                   facecolors=state_colors[row["State"]])

ax.set_xlabel("Training Week")
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["State"])
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()
