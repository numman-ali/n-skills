#!/usr/bin/env node

/**
 * sync-external.mjs
 *
 * Syncs external skills from upstream repositories into n-skills.
 * Reads sources.yaml, clones/fetches repos, and copies skill folders.
 *
 * Usage:
 *   node scripts/sync-external.mjs [--force] [--skill=name]
 */

import { execSync, execFileSync } from "child_process";
import { createHash } from "crypto";
import { existsSync, mkdirSync, rmSync, cpSync, readFileSync, writeFileSync, readdirSync, statSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { parse as parseYaml, stringify as stringifyYaml } from "yaml";

/**
 * Compute a content hash of an entire directory (recursive).
 * This is used to detect if actual file contents changed, not just commits.
 */
function hashDirectory(dirPath, excludes = []) {
  const hash = createHash("sha256");

  function processDir(currentPath, relativePath = "") {
    const entries = readdirSync(currentPath).sort();
    for (const entry of entries) {
      const fullPath = join(currentPath, entry);
      const relPath = relativePath ? `${relativePath}/${entry}` : entry;

      // Check excludes
      const shouldExclude = excludes.some((pattern) => {
        if (pattern.endsWith("/")) {
          return relPath.includes(pattern.slice(0, -1));
        }
        if (pattern.startsWith("*.")) {
          return relPath.endsWith(pattern.slice(1));
        }
        return relPath.includes(pattern);
      });
      if (shouldExclude) continue;

      const stat = statSync(fullPath);
      if (stat.isDirectory()) {
        processDir(fullPath, relPath);
      } else {
        // Include file path and content in hash
        hash.update(relPath);
        hash.update(readFileSync(fullPath));
      }
    }
  }

  processDir(dirPath);
  return hash.digest("hex");
}

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const SOURCES_FILE = join(ROOT, "sources.yaml");
const SYNC_STATE_FILE = join(ROOT, ".sync-state.json");
const TEMP_DIR = join(ROOT, ".sync-temp");

// Parse CLI arguments
const args = process.argv.slice(2);
const force = args.includes("--force");
const skillArg = args.find((a) => a.startsWith("--skill="));
const targetSkill = skillArg ? skillArg.split("=")[1] : null;

console.log("🔄 n-skills External Sync");
console.log("=".repeat(50));

// Read sources.yaml
if (!existsSync(SOURCES_FILE)) {
  console.error("❌ sources.yaml not found");
  process.exit(1);
}

const sourcesContent = readFileSync(SOURCES_FILE, "utf-8");
const sources = parseYaml(sourcesContent);

// Load previous sync state
let syncState = {};
if (existsSync(SYNC_STATE_FILE)) {
  try {
    syncState = JSON.parse(readFileSync(SYNC_STATE_FILE, "utf-8"));
  } catch (e) {
    console.warn("⚠️  Could not read sync state, starting fresh");
  }
}

// Create temp directory
if (existsSync(TEMP_DIR)) {
  rmSync(TEMP_DIR, { recursive: true });
}
mkdirSync(TEMP_DIR, { recursive: true });

let hasChanges = false;
const errors = [];

// Process each skill
for (const skill of sources.skills || []) {
  // Skip native skills (maintained directly in repo)
  if (skill.native) {
    console.log(`\n⏭️  ${skill.name} (native, skipping sync)`);
    continue;
  }

  // Skip if targeting specific skill
  if (targetSkill && skill.name !== targetSkill) {
    continue;
  }

  console.log(`\n📦 Processing: ${skill.name}`);
  console.log(`   Source: ${skill.source.repo}/${skill.source.path}`);
  console.log(`   Target: ${skill.target.path}`);

  try {
    const repoUrl = `https://github.com/${skill.source.repo}.git`;
    const ref = skill.source.ref || "main";
    const repoDir = join(TEMP_DIR, skill.source.repo.replace("/", "-"));

    // Clone or fetch
    if (!existsSync(repoDir)) {
      console.log(`   Cloning ${skill.source.repo}...`);
      execFileSync("git", ["clone", "--depth", "1", "--branch", ref, repoUrl, repoDir], {
        stdio: "pipe",
      });
    }

    // Get current commit hash
    const commitHash = execFileSync("git", ["-C", repoDir, "rev-parse", "HEAD"], {
      encoding: "utf-8",
    }).trim();

    console.log(`   Commit: ${commitHash.slice(0, 8)}`);

    // Source and target paths
    const sourcePath = join(repoDir, skill.source.path);
    const targetPath = join(ROOT, skill.target.path);

    if (!existsSync(sourcePath)) {
      throw new Error(`Source path not found: ${skill.source.path}`);
    }

    // Compute content hash of upstream skill folder
    const syncConfig = skill.sync || {};
    const excludes = syncConfig.exclude || ["node_modules/", "*.lock", "bun.lock", "tmp/"];
    const contentHash = hashDirectory(sourcePath, excludes);
    console.log(`   Content hash: ${contentHash.slice(0, 12)}`);

    // Check if content has actually changed
    const existingSourceJson = join(targetPath, ".source.json");
    if (!force && existsSync(existingSourceJson)) {
      try {
        const existing = JSON.parse(readFileSync(existingSourceJson, "utf-8"));
        if (existing.content_hash === contentHash) {
          console.log(`   ✅ Content unchanged, skipping`);
          continue;
        }
      } catch (e) {
        // If we can't read it, proceed with sync
      }
    }

    // Validate SKILL.md exists
    const skillMdPath = join(sourcePath, "SKILL.md");
    if (!existsSync(skillMdPath)) {
      throw new Error(`SKILL.md not found in ${skill.source.path}`);
    }

    // New structure: skill content goes into skills/<skill-name>/ subfolder
    // This matches official Claude Code plugin format
    const skillSubfolder = join(targetPath, "skills", skill.name);

    // Clean target skills subfolder (preserve .claude-plugin/ at plugin root)
    if (existsSync(skillSubfolder)) {
      rmSync(skillSubfolder, { recursive: true });
    }
    mkdirSync(skillSubfolder, { recursive: true });

    // Copy files into the skills/<skill-name>/ subfolder
    const includes = syncConfig.include || null;

    if (includes) {
      // Copy specific files/folders
      for (const item of includes) {
        const src = join(sourcePath, item);
        const dest = join(skillSubfolder, item);
        if (existsSync(src)) {
          cpSync(src, dest, { recursive: true });
        }
      }
    } else {
      // Copy everything except excludes
      cpSync(sourcePath, skillSubfolder, {
        recursive: true,
        filter: (src) => {
          const relativePath = src.replace(sourcePath, "");
          return !excludes.some((pattern) => {
            if (pattern.endsWith("/")) {
              return relativePath.includes(pattern.slice(0, -1));
            }
            if (pattern.startsWith("*.")) {
              return relativePath.endsWith(pattern.slice(1));
            }
            return relativePath.includes(pattern);
          });
        },
      });
    }

    // Write attribution file at plugin root (not in skill subfolder)
    const attributionPath = join(targetPath, ".source.json");
    writeFileSync(
      attributionPath,
      JSON.stringify(
        {
          synced_from: skill.source.repo,
          source_path: skill.source.path,
          commit: commitHash,
          content_hash: contentHash,
          synced_at: new Date().toISOString(),
          homepage: skill.homepage,
          author: skill.author,
          license: skill.license,
        },
        null,
        2
      )
    );

    // Update sync state
    syncState[skill.name] = {
      commit: commitHash,
      synced_at: new Date().toISOString(),
      source: skill.source.repo,
    };

    hasChanges = true;
    console.log(`   ✅ Synced successfully`);
  } catch (error) {
    console.error(`   ❌ Error: ${error.message}`);
    errors.push({ skill: skill.name, error: error.message });
  }
}

// Save sync state
writeFileSync(SYNC_STATE_FILE, JSON.stringify(syncState, null, 2));

// Cleanup
rmSync(TEMP_DIR, { recursive: true });

// Bump versions if there were changes
if (hasChanges) {
  // Bump package.json version
  const PACKAGE_FILE = join(ROOT, "package.json");
  let newVersion = null;
  if (existsSync(PACKAGE_FILE)) {
    try {
      const pkg = JSON.parse(readFileSync(PACKAGE_FILE, "utf-8"));
      if (pkg.version) {
        const parts = pkg.version.split(".");
        parts[2] = String(parseInt(parts[2] || "0", 10) + 1);
        newVersion = parts.join(".");
        pkg.version = newVersion;
        writeFileSync(PACKAGE_FILE, JSON.stringify(pkg, null, 2) + "\n");
        console.log(`\n📦 Bumped package.json version to ${newVersion}`);
      }
    } catch (e) {
      console.warn("⚠️  Could not bump package.json version:", e.message);
    }
  }

  // Update package-lock.json via npm install
  if (newVersion) {
    try {
      execSync("npm install --package-lock-only", { cwd: ROOT, stdio: "pipe" });
      console.log(`📦 Updated package-lock.json via npm install`);
    } catch (e) {
      console.warn("⚠️  Could not update package-lock.json:", e.message);
    }
  }

  // Bump marketplace.json version (use same version as package.json)
  const MARKETPLACE_FILE = join(ROOT, ".claude-plugin", "marketplace.json");
  if (newVersion && existsSync(MARKETPLACE_FILE)) {
    try {
      const marketplace = JSON.parse(readFileSync(MARKETPLACE_FILE, "utf-8"));
      if (marketplace.metadata) {
        marketplace.metadata.version = newVersion;
        marketplace.metadata.generated_at = new Date().toISOString();
        writeFileSync(MARKETPLACE_FILE, JSON.stringify(marketplace, null, 2) + "\n");
        console.log(`📦 Bumped marketplace.json version to ${newVersion}`);
      }
    } catch (e) {
      console.warn("⚠️  Could not bump marketplace.json version:", e.message);
    }
  }
}

// Summary
console.log("\n" + "=".repeat(50));
console.log("📊 Sync Summary");

if (hasChanges) {
  console.log("   Status: Changes detected");
  // Output for GitHub Actions
  if (process.env.GITHUB_OUTPUT) {
    writeFileSync(process.env.GITHUB_OUTPUT, "changes=true\n", { flag: "a" });
  }
} else {
  console.log("   Status: No changes");
  if (process.env.GITHUB_OUTPUT) {
    writeFileSync(process.env.GITHUB_OUTPUT, "changes=false\n", { flag: "a" });
  }
}

if (errors.length > 0) {
  console.log(`   Errors: ${errors.length}`);
  for (const e of errors) {
    console.log(`     - ${e.skill}: ${e.error}`);
  }
  process.exit(1);
}

console.log("\n✨ Done!\n");
