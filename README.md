# Smartcab-Trainer
This is a Udacity machine learning nanodegree project deliverable, please use in accordance to Udacity honor code.

## Project Goals
1. Apply reinforcement learning to build a simulated vehicle navigation agent.
2. Model a complex control problem in terms of limited available inputs, and design a scheme to automatically learn an optimal driving strategy based on rewards and penalties.

## Software and Libraries
The following SW was used in the first part of the project:
* Python 2.7
* pygame

## Problem Setup
Smartcab operates in an idealized grid-like city, with roads going North-South and East-West. Other vehicles may be present on the roads, but no pedestrians. There is a traffic light at each intersection that can be in one of two states: North-South open or
East-West open.

US right-of-way rules apply: On a green light, you can turn left only if there is no oncoming traffic at the intersection coming straight. On a red light, you can turn right if there is no oncoming traffic turning left or traffic from the left going straight.

## Inputs
* **Route**: Waypoints at each intersection, where next waypoint is always either one block straight ahead, one block left, one block right, one block back or exactly there (reached the destination).
* **Traffic lights**: To check if green for the direction of movement (heading).
* **Cars at the intersection**: Includes direction they want to go.
* **Trip timer**: counts down every time step. If the timer is at 0 and the destination has not been reached, the trip is over, and a new one may start.

## Outputs
* **Action**: At any instant, decide whether smartcab should stay put at the current intersection, move one block forward, one block left, or one block right (no backward movement).
* **Rewards**:
  * *Large reward*: successfully completed trip - passenger is dropped off at the desired destination (some intersection) within a pre-specified time bound (computed with a route plan).
  * *Small reward*: correct move executed at an intersection.
  * *Small penalty*: incorrect move.
  * *Large penalty*: violating traffic rules and/or causing an accident.

## Final Report and Source Code
Final report and source code are included in this repository. Startup Python file is agent.py.
