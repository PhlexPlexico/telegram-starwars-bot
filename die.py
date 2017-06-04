#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randrange

def rollBoost():
	intrand = randrange(1,6)
	if intrand == 1 or intrand == 2:
		return "Boost: ⬜"
	elif intrand == 3:
		return "Boost: 💥"
	elif intrand == 4:
		return "Boost: 💥♉️"
	elif intrand == 5:
		return "Boost: ♉️ ♉️"
	elif intrand == 6:
		return "Boost: ♉️"
def rollSetBack():
	intrand = randrange(1,6)
	if intrand == 1 or intrand == 2:
		return "Setback: ⬜"
	if intrand == 3 or intrand == 4:
		return "Setback: 🔽"
	if intrand == 5 or intrand == 6:
		return "Setback: ☸️"
def rollAbility():
	intrand = randrange(1,8)
	if intrand == 1:
		return "Ability: ⬜"
	if intrand == 2 or intrand == 3:
		return "Ability: 💥"
	if intrand == 4:
		return "Ability: 💥💥"
	if intrand == 5 or intrand == 6:
		return "Ability: ♉️"
	if intrand == 7:
		return "Ability: 💥♉️"
	if intrand == 8:
		return "Ability: ♉️ ♉️"
def rollDifficulty():
	intrand = randrange(1,8)
	if intrand == 1:
		return "Difficulty: ⬜"
	if intrand == 2:
		return "Difficulty: 🔽"
	if intrand == 3:
		return "Difficulty: 🔽🔽"
	if intrand == 4 or intrand == 5 or intrand == 6:
		return "Difficulty: ☸️"
	if intrand == 7:
		return "Difficulty: ☸️ ☸️"
	if intrand == 8:
		return "Difficulty: 🔽☸️"
def rollProficiency():
	intrand = randrange(1,12)
	if intrand == 1:
		return "Proficiency: ⬜"
	if intrand == 2 or intrand == 3:
		return "Proficiency: 💥"
	if intrand == 4 or intrand == 5:
		return "Proficiency: 💥💥"
	if intrand == 6:
		return "Proficiency: ♉️"
	if intrand == 7 or intrand == 8 or intrand == 9:
		return "Proficiency: 💥♉️"
	if intrand == 10 or intrand == 11:
		return "Proficiency: ♉️ ♉️"
	if intrand == 12:
		return "Proficiency: ⚔️"
def rollChallenge():
	intrand = randrange(1,12)
	if intrand == 1:
		return "Challenge: ⬜"
	if intrand == 2 or intrand == 3:
		return "Challenge: 🔽"
	if intrand == 4 or intrand == 5:
		return "Challenge: 🔽"
	if intrand == 7 or intrand == 8:
		return "Challenge: ☸️"
	if intrand == 8 or intrand == 9:
		return "Challenge: 🔽☸️"
	if intrand == 10 or intrand == 11:
		return "Challenge: ☸️ ☸️"
	if intrand == 12:
		return "Challenge: ⎊"
def rollForce():
	intrand = randrange(1,12)
	if intrand == 1 or intrand == 2 or intrand == 3 or intrand == 4 or intrand == 5 or intrand == 6:
		return "Force: ⚫"
	if intrand == 7:
		return "Force: ⚫⚫"
	if intrand == 8 or intrand == 9:
		return "Force: ⚪"
	if intrand == 10 or intrand == 11 or intrand == 12:
		return "Force: ⚪⚪"

def rollAll():
	strBoost = rollBoost()
	strSetBack = rollSetBack()
	strAbility = rollAbility()
	strDifficulty = rollDifficulty()
	strProficiency = rollProficiency()
	strChallenge = rollChallenge()
	strForce = rollForce()
	return str(strBoost + "\n" + strSetBack + "\n" + strAbility + "\n" + strDifficulty + "\n" + strProficiency + " \n" + strChallenge + "\n" + strForce)
