#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// List of directories to process
const DIRECTORIES = ['./templates/img/', './campaign/characters/non-player/img/', './campaign/characters/player/img/'];

const README_FILENAME = 'README.md';
const NB_IMAGES_PER_LINE = 4;

// Loop through each directory
DIRECTORIES.forEach((ROOT_DIR) => {
  let nbImages = 0;
  let mdContent = '<table><tr>';

  fs.readdirSync(ROOT_DIR).forEach((image) => {
    if (image !== README_FILENAME) {
      if (!(nbImages % NB_IMAGES_PER_LINE)) {
        if (nbImages > 0) {
          mdContent += `
</tr>`;
        }
        mdContent += `
<tr>`;
      }
      nbImages++;
      mdContent += `
<td valign="bottom">
<img src="./${image}" width="200"><br>
${image}
</td>
`;
    }
  });
  mdContent += `
</tr></table>`;

  fs.writeFileSync(path.join(ROOT_DIR, README_FILENAME), mdContent);
});
