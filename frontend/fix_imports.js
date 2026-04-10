const fs = require('fs');
const path = require('path');

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(function(file) {
    file = path.join(dir, file);
    const stat = fs.statSync(file);
    if (stat && stat.isDirectory()) { 
        results = results.concat(walk(file));
    } else { 
        if (file.endsWith('.vue')) results.push(file);
    }
  });
  return results;
}

const files = walk('src/views');

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  
  const scriptSetupMatch = content.match(/<script setup>([\s\S]*?)<\/script>/);
  if (!scriptSetupMatch) return;
  
  let scriptContent = scriptSetupMatch[1];
  
  // Find all import statements
  const importRegex = /^import\s+[\s\S]*?from\s+['"][^'"]+['"]\s*;?|^import\s+['"][^'"]+['"]\s*;?/gm;
  
  const imports = [];
  let match;
  while ((match = importRegex.exec(scriptContent)) !== null) {
      imports.push(match[0].trim());
  }
  
  if (imports.length > 0) {
      // Remove all imports from the script body
      let cleanScript = scriptContent.replace(importRegex, '');
      
      // Clean up multiple blank lines
      cleanScript = cleanScript.replace(/\n\s*\n\s*\n/g, '\n\n');
      
      // Group imports and put them at the top
      const newScriptContent = '\n' + imports.join('\n') + '\n' + cleanScript;
      
      content = content.replace(scriptSetupMatch[0], `<script setup>${newScriptContent}</script>`);
      fs.writeFileSync(file, content);
      console.log(`Fixed imports in ${file}`);
  }
});
