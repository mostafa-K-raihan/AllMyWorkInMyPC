#!/usr/bin/env node

import process from 'node:process'
import { emitKeypressEvents } from 'readline'


function setupTerminal() {

  emitKeypressEvents(process.stdin)
  process.stdin.setRawMode(true)

  // go to the alrernate screen
  process.stdout.write('\x1b[?1049h')
  process.stdout.write('\x1b[2J');     // Clear the alternate screen
  process.stdout.write('\x1b[?25l'); // Hide the cursor
}


function gameover() {
  process.stdout.write('\x1b[?1049l'); // Restore normal screen
  process.stdout.write('\x1b[?25h'); // Restore cursor
  process.exit()
	return
}

const state = {
	x: 0,
	y: 0,
	targetX: 9,
	targetY: 19,
	interval: setInterval(function () {
	  moveTarget();
        }, 100)
}

setupTerminal()

process.stdin.on('keypress', function (_, key) {
  if (key.name === 'q') { gameover() }
  if (key.name === 'left') { state.x -- }
  if (key.name === 'right') { state.x ++ }
  if (key.name === 'up') { state.y -- }
  if (key.name === 'down') { state.y ++ }

  update()
})


function moveTarget() {
	const x = Math.random()
	if (x > .5) { state.targetX ++ }
	else { state.targetX -- }

	const y = Math.random()
	if (y > .5) { state.targetY ++ }
	else state.targetY --


	update()

}

function update() {
	if (state.x === state.targetX && state.y === state.targetY) { gameover() }
	render()
}
function render() {
  console.clear()
  process.stdout.cursorTo(state.x, state.y)
  process.stdout.write('X')
  process.stdout.cursorTo(state.targetX, state.targetY)
  process.stdout.write('0')
}
