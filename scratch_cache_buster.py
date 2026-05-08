import os

directory = 'c:/Users/sibyn/nova_events_project/frontend'
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the script tag
        content = content.replace('src="js/main.js?v=2"', 'src="js/main.js?v=3"')
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

print("Cache busting updated to v=3.")
