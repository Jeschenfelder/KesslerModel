# Sorted Circle rules model
Based on Kessler (add citation)

## Set-up:
- Two layers initially: Stones; Fines+Water
- Cooling faster in Stones
- Stones, Ice, Void inhabit full cell
- Water, Fines inhabit half cell

## Cooling cycle: Steps
- Run Temperature diffusion for one timestep
- If Fine+Water cell & T drops below zero:
	- Convert excess T change into Heat
	- Calculate amount of water 'frozen' by heat
	- if all water is frozen, add in ice cell and move according to rules
- Once all is frozen, cooling is done (or after nt time steps?)

## Thawing cycle: Steps

