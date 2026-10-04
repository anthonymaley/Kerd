// overtone's one hooks module: the engine takes one per plugin, so this file
// composes the figures 0.2 gathered (register.tsx: context, model, workers),
// the usage band that draws them (usage.tsx) and the guard (guard.tsx).

import type { Register } from 'claude-code'

import { register as guard } from './guard'
import { register as band } from './register'
import { register as usage } from './usage'

export const register: Register = (on, options) => {
  band(on, options)
  usage(on, options)
  guard(on, options)
}
