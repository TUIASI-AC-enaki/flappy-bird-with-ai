# flappy-bird-with-ai

This application consists of a copy of the game Flappy Bird built using PyGame in which the user has the opportunity to compete with an AI.

The player controls a bird that must avoid all obstacles in order not to die, 
these being: pipes (one of which from the bottom and one from the top), 
the ground and the ceiling. 
The bird is affected by gravity and the only action the user can perform is 
to click to make it jump up in an attempt to stay alive.

The goal of the game we created is to defeat the computer in this game. 

The project started from the existing game created in this [tutorial](https://www.youtube.com/watch?v=UZg49z76cLw).

## Training the AI bird

### Class Diagram for training

![Achitecture](https://github.com/TUIASI-AC-enaki/flappy-bird-with-ai/blob/main/documentation/architecture.png)

### AI Model

For AI we used a neural network with 4 neurons in the input layer (3 inputs and one bias) and a single output neuron that describes whether or not to press on the screen to make the bird jump.

![AI Model](https://github.com/TUIASI-AC-enaki/flappy-bird-with-ai/blob/main/documentation/neuron.png)

* __Bias__ - the bias neuron.
* __H_bird__ - the current height of the bird in play.
* __H_bottom_pipe__ - the height at which the next bottom pipe is located.
* __H_top_pipe__ - the height at which the next top pipe is located.


### Notes

* For training the genetic algorithm was used, with 90% chance of crossing, 
20% chance of mutation, maximum number of generations 200000. 
* As a selection function we took a random segment consisting of 50% of individuals 
after which we crossed them up we reach at most the size of the children' population equal 
to the initial one. We make mutations and keep only the best individuals. 
* As a fitness function we used the distance that a bird travels until it hits an obstacle.
* When evolution is stopped, or all ai birds are dead, their weights and other information (generations alive, ancestor generations, average score per all generations alive) are put in the training.json file

## GUI

### Training

There are 2 buttons: 
* Start Evolution - start training using the data from training.json
* Stop Evolution - stop training and update the training.json

In order to start the training run `training.py` file.

![Training](https://github.com/TUIASI-AC-enaki/flappy-bird-with-ai/blob/main/documentation/ss/training.png)

### Game

In order to start the game run `game.py` file.

![Game](https://github.com/TUIASI-AC-enaki/flappy-bird-with-ai/blob/main/documentation/ss/game.png)

