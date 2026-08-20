import { existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { execFileSync, spawnSync } from 'node:child_process'

const expectedAccountId = '6881527e6e0b9bc4a0c009473428d1bc'
const localWrangler = fileURLToPath(new URL('../node_modules/wrangler/bin/wrangler.js', import.meta.url))

function runWrangler(args) {
  const env = { ...process.env }
  delete env.WRANGLER_LOG
  delete env.WRANGLER_LOG_SANITIZE
  if (existsSync(localWrangler)) {
    return execFileSync(process.execPath, [localWrangler, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], env })
  }
  const command = process.platform === 'win32' ? 'npx.cmd' : 'npx'
  const result = spawnSync(command, ['wrangler', ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], env, shell: process.platform === 'win32' })
  if (result.error) throw result.error
  if (result.status !== 0) {
    const error = new Error(`Wrangler exited with status ${result.status}`)
    error.stdout = result.stdout
    error.stderr = result.stderr
    throw error
  }
  return result.stdout
}

function verifyJson(output) {
  const parsed = JSON.parse(output)
  return JSON.stringify(parsed).includes(expectedAccountId)
}

function verifyText(output) {
  return output.includes(expectedAccountId)
}

let verified = false
let lastError = ''
try {
  const output = runWrangler(['whoami', '--json'])
  verified = verifyJson(output)
} catch (error) {
  lastError = error?.stderr ? String(error.stderr) : String(error?.message || error)
}
if (!verified) {
  try {
    const output = runWrangler(['whoami'])
    verified = verifyText(output)
  } catch (error) {
    lastError = error?.stderr ? String(error.stderr) : String(error?.message || error)
  }
}
if (!verified) {
  if (lastError.trim()) process.stderr.write(lastError.trimEnd() + '\n')
  process.stderr.write(`Unable to verify the active Cloudflare account as the pinned OpenGLESScope account ${expectedAccountId}. Deployment is blocked.\n`)
  process.exit(1)
}
process.stdout.write(`Verified OpenGLESScope Cloudflare account ${expectedAccountId}.\n`)
