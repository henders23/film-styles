# Assemble index.html = shared frame header (frame_head.html: styles/filters/animation helpers) + this episode's main.js
# When added to Lemo-Opuscar: this used to cut the part of ../cat-case/index.html before its "// cat (fat orange)" comment;
# that cut-out part (title already changed to this film's) is now frozen as frame_head.html, so nothing depends on projects outside the repo.
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
head = open('frame_head.html', encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(head + '\n' + open('main.js', encoding='utf-8').read() + '\n</script>\n</body>\n</html>\n')
print('ok', head.count('\n'))
