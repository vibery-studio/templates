#!/usr/bin/env node
/**
 * Generate release assets for vibery templates
 * Creates individual .tar.gz for each template and registry.json
 */

const fs = require('fs-extra');
const path = require('path');
const tar = require('tar');

const ROOT_DIR = path.join(__dirname, '..');
const DIST_DIR = path.join(ROOT_DIR, 'dist');

// Template types and their directories
const TEMPLATE_TYPES = ['agents', 'skills', 'commands', 'mcps', 'hooks', 'settings'];

/**
 * Extract description from markdown file (first line after # heading or first paragraph)
 */
function extractDescription(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      // Skip empty lines and headings
      if (!line || line.startsWith('#')) continue;
      // Return first non-empty, non-heading line (truncated)
      return line.slice(0, 150).replace(/[*_`]/g, '');
    }
  } catch (e) {
    return '';
  }
  return '';
}

/**
 * Get template name from path (remove extension)
 */
function getTemplateName(filePath) {
  const basename = path.basename(filePath);
  return basename.replace(/\.(md|json)$/, '');
}

/**
 * Calculate directory size recursively
 */
function getDirSize(dirPath) {
  let size = 0;
  const files = fs.readdirSync(dirPath);
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      size += getDirSize(filePath);
    } else {
      size += stat.size;
    }
  }
  return size;
}

/**
 * Count files in directory recursively
 */
function countFiles(dirPath) {
  let count = 0;
  const files = fs.readdirSync(dirPath);
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      count += countFiles(filePath);
    } else {
      count++;
    }
  }
  return count;
}

/**
 * Process single-file templates (agents, commands, etc.)
 */
async function processSingleFileTemplates(type) {
  const typeDir = path.join(ROOT_DIR, type);
  if (!fs.existsSync(typeDir)) return [];

  const templates = [];
  const files = fs.readdirSync(typeDir).filter(f =>
    f.endsWith('.md') || f.endsWith('.json')
  );

  for (const file of files) {
    const filePath = path.join(typeDir, file);
    const stat = fs.statSync(filePath);

    if (!stat.isFile()) continue;

    const name = getTemplateName(file);
    const archiveName = `${type.slice(0, -1)}--${name}.tar.gz`;
    const archivePath = path.join(DIST_DIR, archiveName);

    // Create tar.gz with single file
    await tar.create(
      {
        gzip: true,
        file: archivePath,
        cwd: typeDir,
      },
      [file]
    );

    templates.push({
      name,
      type: type.slice(0, -1), // Remove trailing 's'
      description: extractDescription(filePath),
      size: stat.size,
      archive: archiveName,
    });

    console.log(`  Created: ${archiveName}`);
  }

  return templates;
}

/**
 * Process directory templates (skills)
 */
async function processDirectoryTemplates(type) {
  const typeDir = path.join(ROOT_DIR, type);
  if (!fs.existsSync(typeDir)) return [];

  const templates = [];
  const dirs = fs.readdirSync(typeDir).filter(d => {
    const dirPath = path.join(typeDir, d);
    return fs.statSync(dirPath).isDirectory();
  });

  for (const dir of dirs) {
    const dirPath = path.join(typeDir, dir);
    const name = dir;
    const archiveName = `${type.slice(0, -1)}--${name}.tar.gz`;
    const archivePath = path.join(DIST_DIR, archiveName);

    // Create tar.gz with directory contents
    await tar.create(
      {
        gzip: true,
        file: archivePath,
        cwd: typeDir,
      },
      [dir]
    );

    // Try to get description from SKILL.md or first .md file
    let description = '';
    const skillMd = path.join(dirPath, 'SKILL.md');
    if (fs.existsSync(skillMd)) {
      description = extractDescription(skillMd);
    } else {
      const mdFiles = fs.readdirSync(dirPath).filter(f => f.endsWith('.md'));
      if (mdFiles.length > 0) {
        description = extractDescription(path.join(dirPath, mdFiles[0]));
      }
    }

    templates.push({
      name,
      type: type.slice(0, -1),
      description,
      size: getDirSize(dirPath),
      files: countFiles(dirPath),
      archive: archiveName,
    });

    console.log(`  Created: ${archiveName}`);
  }

  return templates;
}

/**
 * Main function
 */
async function main() {
  console.log('Generating release assets...\n');

  // Clean and create dist directory
  await fs.emptyDir(DIST_DIR);

  const allTemplates = [];

  for (const type of TEMPLATE_TYPES) {
    console.log(`Processing ${type}...`);

    let templates;
    if (type === 'skills') {
      // Skills are directories
      templates = await processDirectoryTemplates(type);
    } else {
      // Others are single files
      templates = await processSingleFileTemplates(type);
    }

    allTemplates.push(...templates);
  }

  // Read version from package.json
  const pkg = require('../package.json');

  // Generate registry.json
  const registry = {
    version: pkg.version,
    updated: new Date().toISOString(),
    base_url: 'https://github.com/vibery-studio/templates/releases/latest/download',
    templates: allTemplates,
  };

  const registryPath = path.join(DIST_DIR, 'registry.json');
  await fs.writeJson(registryPath, registry, { spaces: 2 });

  console.log(`\nGenerated registry.json with ${allTemplates.length} templates`);
  console.log(`Output directory: ${DIST_DIR}`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
