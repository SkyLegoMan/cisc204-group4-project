# CISC/CMPE 204 Modelling Project

Welcome to Group 4's project for CISC/CMPE 204, which focuses on modelling the card game Briscola!

## Locations of Draft Elements
The current draft of the `run.py` script is located in the main repoitory folder `cisc204-group4-project`. The current draft of the Modelling Report is a `.pdf` file located in the `drafts` subfolder, under the `documents` folder, under the `cisc204-group4-project` repository folder.

## Topic Summary
The game Briscola has players play a card from their hand each round. Based on the suit of the card and the value of each card (Ace, King, etc.), a player wins a round if the card they played had the highest value and was the same suit as the first card played. In addition, at the start of the game a suit is chosen to be the “Briscola”, which ignores the requirement of the highest card needing to be the same suit as the first card played in order to win the round, but still follows the rules regarding value. The game continues until all cards have been played, with each player drawing one card at the end of each round. In a regular game of Briscola, the player with the most points at the end of all the rounds wins – based on the card values. For this project, the player who wins the most rounds wins the game instead. </br> </br>
We will model if it is possible for Player-1 to win 4 of the 10 possible rounds in a game of four players. The model will be using the game configuration seen below, which shows the players’ starting hands and the Briscola suit (swords). The rest of the deck is not predetermined. 
<p align="center">
<img src="https://github.com/user-attachments/assets/21326167-2735-4483-a797-7b54744fb571" />
</p>

## Structure

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `run.py`: General wrapper script that you can choose to use or not. Only requirement is that you implement the one function inside of there for the auto-checks.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.

## Required Libraries

* `bauhaus`: Python package used for creating logical encodings. Installed by running `pip install bauhaus`.
* `nnf`: Python package used for writting logic into negation normal form, and creating logical theories alongside `bauhaus`. Installed by running `pip install nnf`.

## How To Run
To run the model, run the run.py script within the project by running python3 `run.py` in a terminal. If you wish to experiment with changing some parameters inside the model, open the python script `example.py` to change the preset Briscola suit and preset starting hands of each player.
